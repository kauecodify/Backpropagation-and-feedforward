"""
Probability Calculator for Substation by K

This module calculates probabilities for failure hypotheses based on:
- Historical data from Substation Memory™
- Current signal path data
- Failure patterns
- Device reliability
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import defaultdict
import logging
import math

logger = logging.getLogger(__name__)


@dataclass
class ProbabilityFactor:
    """A factor that affects the probability of a failure hypothesis"""
    name: str
    weight: float
    value: float
    description: str = ""
    
    def calculate_contribution(self) -> float:
        """Calculate the contribution of this factor to the overall probability"""
        return self.weight * self.value


@dataclass
class ProbabilityCalculation:
    """Complete probability calculation for a hypothesis"""
    hypothesis_id: str
    base_probability: float
    factors: List[ProbabilityFactor] = field(default_factory=list)
    historical_weight: float = 0.3
    current_weight: float = 0.5
    pattern_weight: float = 0.2
    final_probability: float = 0.0
    
    def calculate(self) -> float:
        """Calculate the final probability considering all factors"""
        # Calculate weighted sum of factors
        factor_sum = sum(f.calculate_contribution() for f in self.factors)
        
        # Combine with base probability
        self.final_probability = self.base_probability + factor_sum
        
        # Clamp between 0 and 1
        self.final_probability = max(0.01, min(0.99, self.final_probability))
        
        return self.final_probability


class ProbabilityCalculator:
    """
    Calculates probabilities for failure hypotheses.
    
    This class uses historical data, current observations, and failure
    patterns to calculate the probability that each failure hypothesis
    is the actual cause of the problem.
    """
    
    # Base probabilities for different failure types
    BASE_PROBABILITIES = {
        'signal_missing': 0.7,
        'transmission_failure': 0.6,
        'protocol_error': 0.5,
        'configuration_error': 0.8,
        'device_failure': 0.4,
        'network_issue': 0.6
    }
    
    # Weights for different types of evidence
    EVIDENCE_WEIGHTS = {
        'signal_present_at_source': 0.2,
        'signal_missing_at_destination': 0.3,
        'recent_configuration_change': 0.4,
        'protocol_mismatch': 0.35,
        'device_error_log': 0.3,
        'network_error': 0.25,
        'historical_failure': 0.35,
        'similar_event': 0.25
    }
    
    # Historical frequency weights
    HISTORICAL_WEIGHTS = {
        'same_device': 0.4,
        'same_signal': 0.3,
        'same_failure_type': 0.3,
        'recent': 0.5,
        'frequent': 0.4
    }
    
    def __init__(self, substation_memory: Any = None):
        """
        Initialize the probability calculator.
        
        Args:
            substation_memory: Substation Memory™ instance for historical data
        """
        self.substation_memory = substation_memory
        self._calculation_cache: Dict[str, ProbabilityCalculation] = {}
        logger.info("ProbabilityCalculator initialized")
    
    def calculate_hypotheses(
        self, 
        failure_points: List[Any], 
        path_data: Dict[int, Dict[str, Any]],
        signal_path: Any
    ) -> List[Any]:
        """
        Calculate probabilities for all failure hypotheses.
        
        Args:
            failure_points: List of FailurePoint objects
            path_data: Dictionary mapping point indices to their data
            signal_path: SignalPath object
            
        Returns:
            List of Hypothesis objects with calculated probabilities
        """
        from .engine import Hypothesis, Evidence
        
        hypotheses = []
        
        for i, failure_point in enumerate(failure_points):
            # Create hypothesis
            hypothesis = Hypothesis(
                hypothesis_id=f"hyp_{failure_point.location.device_id}_{i}",
                failure_point=failure_point,
                description=self._generate_hypothesis_description(failure_point),
                probability=0.0,  # Will be calculated
                evidence=[],
                recommendations=self._generate_recommendations(failure_point)
            )
            
            # Calculate probability
            probability = self.calculate_probability(
                failure_point, path_data, signal_path
            )
            hypothesis.probability = probability
            
            # Gather evidence
            evidence = self.gather_evidence(failure_point, path_data, signal_path)
            hypothesis.evidence = evidence
            
            hypotheses.append(hypothesis)
        
        return hypotheses
    
    def calculate_probability(
        self, 
        failure_point: Any, 
        path_data: Dict[int, Dict[str, Any]],
        signal_path: Any
    ) -> float:
        """
        Calculate the probability for a single failure hypothesis.
        
        Args:
            failure_point: FailurePoint object
            path_data: Dictionary mapping point indices to their data
            signal_path: SignalPath object
            
        Returns:
            Probability (0.0 to 1.0) that this is the actual failure
        """
        cache_key = f"{failure_point.location.device_id}_{failure_point.failure_type.value}"
        
        # Check cache
        if cache_key in self._calculation_cache:
            return self._calculation_cache[cache_key].final_probability
        
        # Get base probability
        failure_type = failure_point.failure_type.value
        base_prob = self.BASE_PROBABILITIES.get(failure_type, 0.5)
        
        # Create calculation object
        calc = ProbabilityCalculation(
            hypothesis_id=failure_point.hypothesis_id if hasattr(failure_point, 'hypothesis_id') else cache_key,
            base_probability=base_prob
        )
        
        # Add historical factors
        historical_factors = self._get_historical_factors(failure_point, signal_path)
        calc.factors.extend(historical_factors)
        
        # Add current observation factors
        current_factors = self._get_current_factors(failure_point, path_data, signal_path)
        calc.factors.extend(current_factors)
        
        # Add pattern factors
        pattern_factors = self._get_pattern_factors(failure_point, signal_path)
        calc.factors.extend(pattern_factors)
        
        # Calculate final probability
        final_prob = calc.calculate()
        
        # Cache the result
        self._calculation_cache[cache_key] = calc
        
        return final_prob
    
    def _get_historical_factors(
        self, 
        failure_point: Any, 
        signal_path: Any
    ) -> List[ProbabilityFactor]:
        """
        Get historical factors that affect probability.
        
        Args:
            failure_point: FailurePoint object
            signal_path: SignalPath object
            
        Returns:
            List of ProbabilityFactor objects
        """
        factors = []
        
        if not self.substation_memory:
            return factors
        
        try:
            device_id = failure_point.location.device_id
            failure_type = failure_point.failure_type.value
            signal_name = signal_path.signal_name
            
            # Get historical failures for this device
            historical_failures = self.substation_memory.get_historical_failures(
                device_id=device_id,
                failure_type=failure_type
            )
            
            if historical_failures:
                # Frequency factor
                frequency = len(historical_failures)
                frequency_weight = min(frequency * 0.1, 0.5)  # Cap at 0.5
                factors.append(ProbabilityFactor(
                    name="historical_frequency",
                    weight=self.HISTORICAL_WEIGHTS['frequent'],
                    value=frequency_weight,
                    description=f"Device {device_id} has failed {frequency} times before"
                ))
                
                # Recency factor
                last_failure = historical_failures[0]  # Most recent first
                last_failure_time = last_failure.get('timestamp')
                if last_failure_time:
                    time_since = datetime.utcnow() - last_failure_time
                    if time_since < timedelta(days=30):
                        factors.append(ProbabilityFactor(
                            name="recent_failure",
                            weight=self.HISTORICAL_WEIGHTS['recent'],
                            value=0.4,
                            description=f"Device {device_id} failed recently ({time_since.days} days ago)"
                        ))
                
                # Same failure type factor
                same_type_count = sum(
                    1 for f in historical_failures 
                    if f.get('failure_type') == failure_type
                )
                if same_type_count > 0:
                    factors.append(ProbabilityFactor(
                        name="same_failure_type",
                        weight=self.HISTORICAL_WEIGHTS['same_failure_type'],
                        value=min(same_type_count * 0.15, 0.4),
                        description=f"Device {device_id} has had {same_type_count} similar failures"
                    ))
            
            # Get historical failures for this signal
            signal_failures = self.substation_memory.get_historical_failures(
                signal=signal_name
            )
            
            if signal_failures:
                factors.append(ProbabilityFactor(
                    name="signal_history",
                    weight=self.HISTORICAL_WEIGHTS['same_signal'],
                    value=min(len(signal_failures) * 0.1, 0.3),
                    description=f"Signal {signal_name} has failed {len(signal_failures)} times before"
                ))
            
        except Exception as e:
            logger.error(f"Error getting historical factors: {e}")
        
        return factors
    
    def _get_current_factors(
        self, 
        failure_point: Any, 
        path_data: Dict[int, Dict[str, Any]],
        signal_path: Any
    ) -> List[ProbabilityFactor]:
        """
        Get factors based on current observations.
        
        Args:
            failure_point: FailurePoint object
            path_data: Dictionary mapping point indices to their data
            signal_path: SignalPath object
            
        Returns:
            List of ProbabilityFactor objects
        """
        factors = []
        
        # Check if signal is present at source
        source = signal_path.source
        source_data = path_data.get(0, {}).get('data', {})
        
        if self._is_signal_present(source, source_data):
            factors.append(ProbabilityFactor(
                name="signal_present_at_source",
                weight=self.EVIDENCE_WEIGHTS['signal_present_at_source'],
                value=0.8,
                description="Signal is present at the source device"
            ))
        
        # Check if signal is missing at destination
        destination = signal_path.destination
        dest_index = len([signal_path.source] + signal_path.points)
        dest_data = path_data.get(dest_index, {}).get('data', {})
        
        if not self._is_signal_present(destination, dest_data):
            factors.append(ProbabilityFactor(
                name="signal_missing_at_destination",
                weight=self.EVIDENCE_WEIGHTS['signal_missing_at_destination'],
                value=0.9,
                description="Signal is missing at the destination"
            ))
        
        # Check for recent configuration changes
        if self.substation_memory:
            device_id = failure_point.location.device_id
            last_change = self.substation_memory.get_last_configuration_change(device_id)
            
            if last_change:
                change_time = last_change.get('timestamp')
                if change_time:
                    time_since = datetime.utcnow() - change_time
                    if time_since < timedelta(days=7):
                        factors.append(ProbabilityFactor(
                            name="recent_configuration_change",
                            weight=self.EVIDENCE_WEIGHTS['recent_configuration_change'],
                            value=0.7,
                            description=f"Device {device_id} had configuration changed {time_since.days} days ago"
                        ))
        
        # Check for protocol mismatch
        if failure_point.failure_type.value == 'protocol_error':
            factors.append(ProbabilityFactor(
                name="protocol_mismatch",
                weight=self.EVIDENCE_WEIGHTS['protocol_mismatch'],
                value=0.8,
                description="Protocol mismatch detected"
            ))
        
        return factors
    
    def _get_pattern_factors(
        self, 
        failure_point: Any, 
        signal_path: Any
    ) -> List[ProbabilityFactor]:
        """
        Get factors based on failure patterns.
        
        Args:
            failure_point: FailurePoint object
            signal_path: SignalPath object
            
        Returns:
            List of ProbabilityFactor objects
        """
        factors = []
        
        # Device type patterns
        device_type = failure_point.location.device_type if hasattr(failure_point.location, 'device_type') else 'unknown'
        
        # Gateways often have configuration issues
        if device_type.lower() == 'gateway':
            factors.append(ProbabilityFactor(
                name="gateway_pattern",
                weight=0.3,
                value=0.6,
                description="Gateways frequently have configuration issues"
            ))
        
        # Switches often have network issues
        if device_type.lower() == 'switch':
            factors.append(ProbabilityFactor(
                name="switch_pattern",
                weight=0.25,
                value=0.5,
                description="Switches frequently have network connectivity issues"
            ))
        
        # IEDs rarely fail completely
        if device_type.lower() == 'ied':
            factors.append(ProbabilityFactor(
                name="ied_reliability",
                weight=0.2,
                value=-0.3,  # Negative factor (reduces probability)
                description="IEDs are generally reliable devices"
            ))
        
        return factors
    
    def gather_evidence(
        self, 
        failure_point: Any, 
        path_data: Dict[int, Dict[str, Any]],
        signal_path: Any
    ) -> List[Any]:
        """
        Gather evidence to support a failure hypothesis.
        
        Args:
            failure_point: FailurePoint object
            path_data: Dictionary mapping point indices to their data
            signal_path: SignalPath object
            
        Returns:
            List of Evidence objects
        """
        from .engine import Evidence
        
        evidence = []
        
        # Evidence: Signal present at source
        source = signal_path.source
        source_data = path_data.get(0, {}).get('data', {})
        
        if self._is_signal_present(source, source_data):
            evidence.append(Evidence(
                evidence_id=f"evid_source_{source.device_id}",
                evidence_type="signal_present_at_source",
                description=f"Signal {signal_path.signal_name} is present at source {source.device_name}",
                data={'device': source.device_id, 'status': 'present'},
                confidence=0.9
            ))
        
        # Evidence: Signal missing at destination
        destination = signal_path.destination
        dest_index = len([signal_path.source] + signal_path.points)
        dest_data = path_data.get(dest_index, {}).get('data', {})
        
        if not self._is_signal_present(destination, dest_data):
            evidence.append(Evidence(
                evidence_id=f"evid_dest_{destination.device_id}",
                evidence_type="signal_missing_at_destination",
                description=f"Signal {signal_path.signal_name} is missing at destination {destination.device_name}",
                data={'device': destination.device_id, 'status': 'missing'},
                confidence=0.9
            ))
        
        # Evidence: Signal present at failure point's previous device
        if failure_point.from_point:
            from_data = self._get_point_data(failure_point.from_point, path_data, signal_path)
            if self._is_signal_present(failure_point.from_point, from_data):
                evidence.append(Evidence(
                    evidence_id=f"evid_from_{failure_point.from_point.device_id}",
                    evidence_type="signal_present_before_failure",
                    description=f"Signal is present at {failure_point.from_point.device_name} (before failure point)",
                    data={'device': failure_point.from_point.device_id, 'status': 'present'},
                    confidence=0.85
                ))
        
        # Evidence: Signal missing at failure point
        failure_data = self._get_point_data(failure_point.location, path_data, signal_path)
        if not self._is_signal_present(failure_point.location, failure_data):
            evidence.append(Evidence(
                evidence_id=f"evid_failure_{failure_point.location.device_id}",
                evidence_type="signal_missing_at_failure_point",
                description=f"Signal is missing at failure point {failure_point.location.device_name}",
                data={'device': failure_point.location.device_id, 'status': 'missing'},
                confidence=0.9
            ))
        
        # Evidence: Recent configuration change
        if self.substation_memory:
            device_id = failure_point.location.device_id
            last_change = self.substation_memory.get_last_configuration_change(device_id)
            
            if last_change:
                evidence.append(Evidence(
                    evidence_id=f"evid_config_{device_id}",
                    evidence_type="recent_configuration_change",
                    description=f"Device {device_id} had configuration changed on {last_change.get('timestamp')}",
                    data=last_change,
                    confidence=0.8
                ))
        
        # Evidence: Historical failures
        if self.substation_memory:
            device_id = failure_point.location.device_id
            historical_failures = self.substation_memory.get_historical_failures(
                device_id=device_id,
                limit=3
            )
            
            if historical_failures:
                evidence.append(Evidence(
                    evidence_id=f"evid_history_{device_id}",
                    evidence_type="historical_failures",
                    description=f"Device {device_id} has had {len(historical_failures)} similar failures in the past",
                    data={'failures': historical_failures},
                    confidence=0.7
                ))
        
        return evidence
    
    def _is_signal_present(self, point: Any, data: Dict[str, Any]) -> bool:
        """Check if signal is present at a point"""
        from .engine import SignalStatus
        
        if 'status' in data:
            return data['status'] == SignalStatus.PRESENT.value
        if hasattr(point, 'status'):
            return point.status == SignalStatus.PRESENT
        return False
    
    def _get_point_data(
        self, 
        point: Any, 
        path_data: Dict[int, Dict[str, Any]],
        signal_path: Any
    ) -> Dict[str, Any]:
        """Get data for a specific point"""
        # Find the index of the point in the path
        all_points = [signal_path.source] + signal_path.points + [signal_path.destination]
        
        try:
            index = all_points.index(point)
            return path_data.get(index, {}).get('data', {})
        except ValueError:
            return {}
    
    def _generate_hypothesis_description(self, failure_point: Any) -> str:
        """Generate a human-readable description of the hypothesis"""
        failure_type = failure_point.failure_type.value
        location = failure_point.location.device_name
        
        descriptions = {
            'signal_missing': f"Signal is missing at {location}",
            'transmission_failure': f"Signal transmission failed at {location}",
            'protocol_error': f"Protocol error at {location}",
            'configuration_error': f"Configuration error at {location}",
            'device_failure': f"Device failure at {location}",
            'network_issue': f"Network issue affecting {location}"
        }
        
        return descriptions.get(failure_type, f"Failure at {location}")
    
    def _generate_recommendations(self, failure_point: Any) -> List[str]:
        """Generate recommendations for addressing the failure"""
        failure_type = failure_point.failure_type.value
        location = failure_point.location.device_name
        device_type = failure_point.location.device_type if hasattr(failure_point.location, 'device_type') else 'device'
        
        recommendations = []
        
        # General recommendations based on failure type
        failure_recommendations = {
            'signal_missing': [
                f"Verify signal generation at {location}",
                f"Check if {location} is powered on and operational",
                f"Inspect signal wiring/connections at {location}"
            ],
            'transmission_failure': [
                f"Check network connectivity between devices",
                f"Verify protocol configuration at {location}",
                f"Inspect network cables and switches"
            ],
            'protocol_error': [
                f"Verify protocol compatibility between devices",
                f"Check protocol configuration at {location}",
                f"Update firmware if protocol version mismatch"
            ],
            'configuration_error': [
                f"Review configuration of {location}",
                f"Verify signal mappings at {location}",
                f"Check if recent configuration changes were applied correctly"
            ],
            'device_failure': [
                f"Perform diagnostic tests on {location}",
                f"Check device logs for errors",
                f"Consider replacing {location} if tests indicate failure"
            ],
            'network_issue': [
                f"Check network connectivity to {location}",
                f"Verify switch/gateway configurations",
                f"Test network latency and packet loss"
            ]
        }
        
        recommendations.extend(failure_recommendations.get(failure_type, []))
        
        # Device-specific recommendations
        if device_type.lower() == 'gateway':
            recommendations.extend([
                f"Verify IEC-104/DNP3/Modbus mappings in {location}",
                f"Check protocol conversion settings in {location}",
                f"Review gateway logs for communication errors"
            ])
        
        elif device_type.lower() == 'switch':
            recommendations.extend([
                f"Check VLAN configurations on {location}",
                f"Verify port status on {location}",
                f"Inspect switch logs for errors"
            ])
        
        elif device_type.lower() == 'ied':
            recommendations.extend([
                f"Verify GOOSE/MMS publishing in {location}",
                f"Check IED configuration files",
                f"Review IED logs for application errors"
            ])
        
        # Remove duplicates while preserving order
        seen = set()
        unique_recommendations = []
        for rec in recommendations:
            if rec not in seen:
                seen.add(rec)
                unique_recommendations.append(rec)
        
        return unique_recommendations
