"""
Failure Analyzer for Substation by K

This module implements the backward analysis algorithm that identifies
failure points in signal paths by tracing backwards from the destination.
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class AnalysisMethod(Enum):
    """Methods for analyzing failures"""
    BACKWARD_TRACING = "backward_tracing"
    FORWARD_TRACING = "forward_tracing"
    BIDIRECTIONAL = "bidirectional"


@dataclass
class AnalysisResult:
    """Result of analyzing a signal path for failures"""
    success: bool
    failure_points: List[Any] = field(default_factory=list)
    analysis_method: AnalysisMethod = AnalysisMethod.BACKWARD_TRACING
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'success': self.success,
            'failure_points': [
                self._failure_to_dict(fp) for fp in self.failure_points
            ],
            'analysis_method': self.analysis_method.value,
            'timestamp': self.timestamp.isoformat()
        }
    
    def _failure_to_dict(self, fp: Any) -> Dict[str, Any]:
        return {
            'location': fp.location.device_name if fp.location else 'unknown',
            'failure_type': fp.failure_type.value if hasattr(fp, 'failure_type') else 'unknown',
            'description': fp.description if hasattr(fp, 'description') else '',
            'severity': fp.severity if hasattr(fp, 'severity') else 'medium'
        }


class FailureAnalyzer:
    """
    Analyzes signal paths to identify failure points.
    
    This class implements the backward analysis algorithm that starts
    from the destination (where the signal is missing) and moves
    backwards through the path to find where the signal chain breaks.
    """
    
    def __init__(self):
        """Initialize the failure analyzer"""
        logger.info("FailureAnalyzer initialized")
    
    def backward_analysis(
        self, 
        signal_path: Any, 
        path_data: Dict[int, Dict[str, Any]]
    ) -> List[Any]:
        """
        Perform backward analysis on a signal path.
        
        This method starts from the destination and moves backwards,
        checking at each point whether the signal is present and correctly
        transmitted from the previous point.
        
        Args:
            signal_path: SignalPath object containing the complete path
            path_data: Dictionary mapping point indices to their data
            
        Returns:
            List of FailurePoint objects where the signal chain breaks
        """
        from .engine import FailurePoint, FailureType, SignalStatus
        
        failure_points = []
        
        # Create a list of all points in order (source -> points -> destination)
        all_points = [signal_path.source] + signal_path.points + [signal_path.destination]
        
        # Start from the destination and move backwards
        for i in range(len(all_points) - 1, 0, -1):
            current = all_points[i]
            previous = all_points[i - 1]
            
            # Get data for current and previous points
            current_data = path_data.get(i, {}).get('data', {})
            previous_data = path_data.get(i - 1, {}).get('data', {})
            
            # Check if signal is present at current point
            if not self._is_signal_present(current, current_data):
                failure_point = self._create_failure_point(
                    location=current,
                    from_point=previous,
                    to_point=current,
                    failure_type=FailureType.SIGNAL_MISSING,
                    reason="Signal not present at current point"
                )
                failure_points.append(failure_point)
                break  # Found the failure point, stop analysis
            
            # Check if signal is correctly transmitted from previous to current
            if not self._is_signal_transmitted(previous, current, previous_data, current_data):
                failure_point = self._create_failure_point(
                    location=current,
                    from_point=previous,
                    to_point=current,
                    failure_type=FailureType.TRANSMISSION_FAILURE,
                    reason="Signal not transmitted from previous point"
                )
                failure_points.append(failure_point)
                break  # Found the failure point, stop analysis
            
            # Check for protocol errors
            protocol_error = self._check_protocol_error(previous, current, previous_data, current_data)
            if protocol_error:
                failure_point = self._create_failure_point(
                    location=current,
                    from_point=previous,
                    to_point=current,
                    failure_type=FailureType.PROTOCOL_ERROR,
                    reason=protocol_error
                )
                failure_points.append(failure_point)
                break
            
            # Check for configuration errors
            config_error = self._check_configuration_error(previous, current, previous_data, current_data)
            if config_error:
                failure_point = self._create_failure_point(
                    location=current,
                    from_point=previous,
                    to_point=current,
                    failure_type=FailureType.CONFIGURATION_ERROR,
                    reason=config_error
                )
                failure_points.append(failure_point)
                break
        
        # If no failure found but signal is missing at destination, add a generic failure
        if not failure_points and not self._is_signal_present(signal_path.destination, path_data.get(len(all_points)-1, {}).get('data', {})):
            failure_point = self._create_failure_point(
                location=signal_path.destination,
                from_point=all_points[-2] if len(all_points) > 1 else None,
                to_point=signal_path.destination,
                failure_type=FailureType.SIGNAL_MISSING,
                reason="Signal missing at destination"
            )
            failure_points.append(failure_point)
        
        return failure_points
    
    def _is_signal_present(self, point: Any, data: Dict[str, Any]) -> bool:
        """
        Check if the signal is present at a given point.
        
        Args:
            point: SignalPoint object
            data: Data collected at this point
            
        Returns:
            True if signal is present, False otherwise
        """
        from .engine import SignalStatus
        
        # Check status from data
        if 'status' in data:
            return data['status'] == SignalStatus.PRESENT.value
        
        # Check status from point
        if hasattr(point, 'status'):
            return point.status == SignalStatus.PRESENT
        
        # Check if there's any signal data
        if 'signal' in data:
            return True
        
        # Default to False if we can't determine
        return False
    
    def _is_signal_transmitted(
        self, 
        from_point: Any, 
        to_point: Any, 
        from_data: Dict[str, Any], 
        to_data: Dict[str, Any]
    ) -> bool:
        """
        Check if the signal is correctly transmitted from one point to another.
        
        Args:
            from_point: Source SignalPoint
            to_point: Destination SignalPoint
            from_data: Data from source point
            to_data: Data from destination point
            
        Returns:
            True if signal is transmitted correctly, False otherwise
        """
        # Check if signal is present at both points
        if not self._is_signal_present(from_point, from_data):
            return False
        if not self._is_signal_present(to_point, to_data):
            return False
        
        # Check if the signal data matches (basic check)
        from_signal = from_data.get('signal')
        to_signal = to_data.get('signal')
        
        if from_signal and to_signal:
            # For digital signals, check if values match
            if isinstance(from_signal, (bool, int)) and isinstance(to_signal, (bool, int)):
                return from_signal == to_signal
        
        # If we can't verify the data, assume it's transmitted
        return True
    
    def _check_protocol_error(
        self, 
        from_point: Any, 
        to_point: Any, 
        from_data: Dict[str, Any], 
        to_data: Dict[str, Any]
    ) -> Optional[str]:
        """
        Check for protocol errors between two points.
        
        Args:
            from_point: Source SignalPoint
            to_point: Destination SignalPoint
            from_data: Data from source point
            to_data: Data from destination point
            
        Returns:
            Error description if protocol error found, None otherwise
        """
        # Get protocols from points
        from_protocol = getattr(from_point, 'protocol', None)
        to_protocol = getattr(to_point, 'protocol', None)
        
        if from_protocol and to_protocol and from_protocol != to_protocol:
            return f"Protocol mismatch: {from_protocol} -> {to_protocol}"
        
        # Check for protocol-specific errors in data
        if 'protocol_error' in from_data:
            return from_data['protocol_error']
        if 'protocol_error' in to_data:
            return to_data['protocol_error']
        
        return None
    
    def _check_configuration_error(
        self, 
        from_point: Any, 
        to_point: Any, 
        from_data: Dict[str, Any], 
        to_data: Dict[str, Any]
    ) -> Optional[str]:
        """
        Check for configuration errors between two points.
        
        Args:
            from_point: Source SignalPoint
            to_point: Destination SignalPoint
            from_data: Data from source point
            to_data: Data from destination point
            
        Returns:
            Error description if configuration error found, None otherwise
        """
        # Check for configuration issues in data
        if 'configuration_error' in from_data:
            return from_data['configuration_error']
        if 'configuration_error' in to_data:
            return to_data['configuration_error']
        
        # Check for missing mappings
        if 'mapping_missing' in to_data:
            return f"Missing mapping configuration at {to_point.device_name}"
        
        return None
    
    def _create_failure_point(
        self, 
        location: Any, 
        from_point: Optional[Any] = None,
        to_point: Optional[Any] = None,
        failure_type: Any = FailureType.SIGNAL_MISSING,
        reason: str = ""
    ) -> Any:
        """
        Create a FailurePoint object.
        
        Args:
            location: SignalPoint where the failure occurs
            from_point: Previous SignalPoint (optional)
            to_point: Next SignalPoint (optional)
            failure_type: Type of failure
            reason: Description of the failure
            
        Returns:
            FailurePoint object
        """
        from .engine import FailurePoint
        
        # Determine severity based on failure type
        severity_map = {
            FailureType.SIGNAL_MISSING: "high",
            FailureType.TRANSMISSION_FAILURE: "high",
            FailureType.PROTOCOL_ERROR: "medium",
            FailureType.CONFIGURATION_ERROR: "medium",
            FailureType.DEVICE_FAILURE: "critical",
            FailureType.NETWORK_ISSUE: "high"
        }
        
        return FailurePoint(
            location=location,
            failure_type=failure_type,
            from_point=from_point,
            to_point=to_point,
            description=reason,
            severity=severity_map.get(failure_type, "medium")
        )
    
    def analyze_with_forward_tracing(
        self, 
        signal_path: Any, 
        path_data: Dict[int, Dict[str, Any]]
    ) -> List[Any]:
        """
        Perform forward analysis on a signal path.
        
        This method starts from the source and moves forward,
        checking at each point whether the signal is correctly
        transmitted to the next point.
        
        Args:
            signal_path: SignalPath object containing the complete path
            path_data: Dictionary mapping point indices to their data
            
        Returns:
            List of FailurePoint objects where the signal chain breaks
        """
        from .engine import FailurePoint, FailureType
        
        failure_points = []
        
        # Create a list of all points in order (source -> points -> destination)
        all_points = [signal_path.source] + signal_path.points + [signal_path.destination]
        
        # Start from the source and move forward
        for i in range(len(all_points) - 1):
            current = all_points[i]
            next_point = all_points[i + 1]
            
            # Get data for current and next points
            current_data = path_data.get(i, {}).get('data', {})
            next_data = path_data.get(i + 1, {}).get('data', {})
            
            # Check if signal is present at current point
            if not self._is_signal_present(current, current_data):
                failure_point = self._create_failure_point(
                    location=current,
                    from_point=all_points[i-1] if i > 0 else None,
                    to_point=next_point,
                    failure_type=FailureType.SIGNAL_MISSING,
                    reason="Signal not present at current point"
                )
                failure_points.append(failure_point)
                break
            
            # Check if signal is correctly transmitted to next point
            if not self._is_signal_transmitted(current, next_point, current_data, next_data):
                failure_point = self._create_failure_point(
                    location=next_point,
                    from_point=current,
                    to_point=next_point,
                    failure_type=FailureType.TRANSMISSION_FAILURE,
                    reason="Signal not transmitted to next point"
                )
                failure_points.append(failure_point)
                break
        
        return failure_points
    
    def bidirectional_analysis(
        self, 
        signal_path: Any, 
        path_data: Dict[int, Dict[str, Any]]
    ) -> Tuple[List[Any], List[Any]]:
        """
        Perform bidirectional analysis on a signal path.
        
        This method runs both backward and forward analysis and
        returns the results from both.
        
        Args:
            signal_path: SignalPath object containing the complete path
            path_data: Dictionary mapping point indices to their data
            
        Returns:
            Tuple of (backward_failures, forward_failures)
        """
        backward_failures = self.backward_analysis(signal_path, path_data)
        forward_failures = self.analyze_with_forward_tracing(signal_path, path_data)
        
        return backward_failures, forward_failures
    
    def analyze_multiple_signals(
        self, 
        signal_paths: List[Any], 
        path_data: Dict[str, Dict[int, Dict[str, Any]]]
    ) -> Dict[str, List[Any]]:
        """
        Analyze multiple signal paths for failures.
        
        Args:
            signal_paths: List of SignalPath objects
            path_data: Dictionary mapping path IDs to their path data
            
        Returns:
            Dictionary mapping path IDs to their failure points
        """
        results = {}
        
        for path in signal_paths:
            path_id = path.path_id
            if path_id in path_data:
                failures = self.backward_analysis(path, path_data[path_id])
                results[path_id] = failures
            else:
                logger.warning(f"No data available for path {path_id}")
                results[path_id] = []
        
        return results
