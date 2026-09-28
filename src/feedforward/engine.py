"""
Feedforward Engine for Substation by K

The core engine that implements feedforward analysis for:
1. Predicting the impact of configuration changes
2. Simulating scenarios before implementation
3. Optimizing network and device configurations
4. Recommending best practices
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging
import copy

logger = logging.getLogger(__name__)


class ChangeType(Enum):
    """Types of changes that can be made to the substation"""
    CONFIGURATION = "configuration"
    NETWORK = "network"
    DEVICE = "device"
    SIGNAL = "signal"
    TOPOLOGY = "topology"


class ImpactLevel(Enum):
    """Levels of impact for a change"""
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RecommendationType(Enum):
    """Types of recommendations"""
    APPROVE = "approve"
    REJECT = "reject"
    MODIFY = "modify"
    TEST = "test"
    MONITOR = "monitor"


@dataclass
class ImpactAnalysis:
    """Analysis of the impact of a proposed change"""
    change_id: str
    change_type: ChangeType
    affected_devices: List[str] = field(default_factory=list)
    affected_signals: List[str] = field(default_factory=list)
    affected_connections: List[Tuple[str, str]] = field(default_factory=list)
    potential_issues: List[Dict[str, Any]] = field(default_factory=list)
    impact_level: ImpactLevel = ImpactLevel.NONE
    confidence: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'change_id': self.change_id,
            'change_type': self.change_type.value,
            'affected_devices': self.affected_devices,
            'affected_signals': self.affected_signals,
            'affected_connections': [
                {'from': c[0], 'to': c[1]} for c in self.affected_connections
            ],
            'potential_issues': self.potential_issues,
            'impact_level': self.impact_level.value,
            'confidence': self.confidence
        }


@dataclass
class SimulationResult:
    """Result of simulating a change"""
    simulation_id: str
    change_id: str
    success: bool
    signal_flow: Dict[str, Any] = field(default_factory=dict)
    communication_failures: List[Dict[str, Any]] = field(default_factory=list)
    protocol_issues: List[Dict[str, Any]] = field(default_factory=list)
    performance_issues: List[Dict[str, Any]] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'simulation_id': self.simulation_id,
            'change_id': self.change_id,
            'success': self.success,
            'signal_flow': self.signal_flow,
            'communication_failures': self.communication_failures,
            'protocol_issues': self.protocol_issues,
            'performance_issues': self.performance_issues,
            'warnings': self.warnings
        }


@dataclass
class Recommendation:
    """Recommendation for a proposed change"""
    recommendation_id: str
    change_id: str
    recommendation_type: RecommendationType
    description: str
    actions: List[str] = field(default_factory=list)
    priority: int = 0
    confidence: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'recommendation_id': self.recommendation_id,
            'change_id': self.change_id,
            'type': self.recommendation_type.value,
            'description': self.description,
            'actions': self.actions,
            'priority': self.priority,
            'confidence': self.confidence
        }


@dataclass
class FeedforwardResult:
    """Complete result of feedforward analysis"""
    change_id: str
    analysis: ImpactAnalysis
    simulation: Optional[SimulationResult] = None
    recommendations: List[Recommendation] = field(default_factory=list)
    should_proceed: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        result = {
            'change_id': self.change_id,
            'analysis': self.analysis.to_dict(),
            'recommendations': [r.to_dict() for r in self.recommendations],
            'should_proceed': self.should_proceed,
            'created_at': self.created_at.isoformat()
        }
        
        if self.simulation:
            result['simulation'] = self.simulation.to_dict()
        
        return result


class FeedforwardEngine:
    """
    Main feedforward engine for predicting and optimizing changes.
    
    This engine:
    1. Analyzes proposed changes for potential impact
    2. Simulates the change in a virtual environment
    3. Predicts potential issues
    4. Generates recommendations
    """
    
    def __init__(
        self, 
        knowledge_graph: Any = None, 
        substation_memory: Any = None,
        digital_twin: Any = None
    ):
        """
        Initialize the feedforward engine.
        
        Args:
            knowledge_graph: Knowledge graph instance for substation topology
            substation_memory: Substation Memory™ instance for historical data
            digital_twin: Digital Twin instance for simulation
        """
        self.knowledge_graph = knowledge_graph
        self.substation_memory = substation_memory
        self.digital_twin = digital_twin
        
        # Initialize sub-components
        self.impact_predictor = ImpactPredictor(knowledge_graph)
        self.simulator = SubstationSimulator(digital_twin, knowledge_graph)
        self.optimizer = ConfigurationOptimizer(knowledge_graph, substation_memory)
        
        logger.info("FeedforwardEngine initialized")
    
    def analyze_change(self, change_proposal: Dict[str, Any]) -> FeedforwardResult:
        """
        Main method to analyze a proposed change using feedforward analysis.
        
        Args:
            change_proposal: Dictionary describing the proposed change
                - change_id: Unique identifier for the change
                - change_type: Type of change (configuration, network, etc.)
                - device: Device ID (if applicable)
                - parameter: Parameter being changed (if applicable)
                - old_value: Current value
                - new_value: Proposed new value
                - description: Description of the change
                
        Returns:
            FeedforwardResult: Complete analysis and recommendations
        """
        logger.info(f"Analyzing change: {change_proposal.get('change_id')}")
        
        change_id = change_proposal.get('change_id', 'unknown')
        
        # Step 1: Predict impact
        impact_analysis = self.impact_predictor.predict_impact(change_proposal)
        logger.debug(f"Impact analysis completed for {change_id}")
        
        # Step 2: Simulate the change
        simulation = None
        if self.digital_twin:
            try:
                simulation = self.simulator.simulate_change(change_proposal)
                logger.debug(f"Simulation completed for {change_id}")
            except Exception as e:
                logger.error(f"Simulation failed for {change_id}: {e}")
        
        # Step 3: Generate recommendations
        recommendations = self._generate_recommendations(
            change_proposal, impact_analysis, simulation
        )
        logger.debug(f"Generated {len(recommendations)} recommendations for {change_id}")
        
        # Step 4: Determine if change should proceed
        should_proceed = self._determine_should_proceed(
            impact_analysis, simulation, recommendations
        )
        
        result = FeedforwardResult(
            change_id=change_id,
            analysis=impact_analysis,
            simulation=simulation,
            recommendations=recommendations,
            should_proceed=should_proceed
        )
        
        logger.info(f"Feedforward analysis completed for {change_id}")
        return result
    
    def _generate_recommendations(
        self, 
        change_proposal: Dict[str, Any],
        impact_analysis: ImpactAnalysis,
        simulation: Optional[SimulationResult]
    ) -> List[Recommendation]:
        """
        Generate recommendations based on impact analysis and simulation.
        
        Args:
            change_proposal: The proposed change
            impact_analysis: Impact analysis results
            simulation: Simulation results (if available)
            
        Returns:
            List of Recommendation objects
        """
        recommendations = []
        change_id = change_proposal.get('change_id', 'unknown')
        
        # If no issues found, recommend approval
        if (not impact_analysis.potential_issues and 
            (not simulation or (simulation.success and not simulation.communication_failures 
                               and not simulation.protocol_issues))):
            recommendations.append(Recommendation(
                recommendation_id=f"rec_approve_{change_id}",
                change_id=change_id,
                recommendation_type=RecommendationType.APPROVE,
                description="Change can be safely applied",
                actions=["Proceed with the change", "Monitor after implementation"],
                priority=0,
                confidence=0.9
            ))
            return recommendations
        
        # If critical issues found, recommend rejection
        if impact_analysis.impact_level == ImpactLevel.CRITICAL:
            recommendations.append(Recommendation(
                recommendation_id=f"rec_reject_{change_id}",
                change_id=change_id,
                recommendation_type=RecommendationType.REJECT,
                description="Change has critical impact and should not be applied",
                actions=[
                    "Do not proceed with the change",
                    "Review impact analysis",
                    "Consider alternative solutions"
                ],
                priority=10,
                confidence=0.85
            ))
        
        # For other cases, generate specific recommendations
        if impact_analysis.potential_issues:
            for i, issue in enumerate(impact_analysis.potential_issues):
                recommendations.append(Recommendation(
                    recommendation_id=f"rec_issue_{change_id}_{i}",
                    change_id=change_id,
                    recommendation_type=RecommendationType.MODIFY,
                    description=f"Address issue: {issue.get('description', 'Unknown issue')}",
                    actions=self._get_actions_for_issue(issue, change_proposal),
                    priority=8,
                    confidence=0.8
                ))
        
        if simulation and not simulation.success:
            recommendations.append(Recommendation(
                recommendation_id=f"rec_sim_{change_id}",
                change_id=change_id,
                recommendation_type=RecommendationType.TEST,
                description="Simulation failed - test thoroughly before applying",
                actions=[
                    "Test change in a controlled environment first",
                    "Verify all affected signals",
                    "Check device compatibility"
                ],
                priority=9,
                confidence=0.85
            ))
        
        if simulation and simulation.communication_failures:
            recommendations.append(Recommendation(
                recommendation_id=f"rec_comm_{change_id}",
                change_id=change_id,
                recommendation_type=RecommendationType.MODIFY,
                description=f"Fix {len(simulation.communication_failures)} communication failures",
                actions=self._get_communication_actions(simulation.communication_failures),
                priority=7,
                confidence=0.8
            ))
        
        if simulation and simulation.protocol_issues:
            recommendations.append(Recommendation(
                recommendation_id=f"rec_proto_{change_id}",
                change_id=change_id,
                recommendation_type=RecommendationType.MODIFY,
                description=f"Resolve {len(simulation.protocol_issues)} protocol issues",
                actions=self._get_protocol_actions(simulation.protocol_issues),
                priority=7,
                confidence=0.8
            ))
        
        # Add monitoring recommendation
        recommendations.append(Recommendation(
            recommendation_id=f"rec_monitor_{change_id}",
            change_id=change_id,
            recommendation_type=RecommendationType.MONITOR,
            description="Monitor system after change implementation",
            actions=[
                "Monitor affected signals for 24 hours",
                "Check for any new errors or warnings",
                "Verify communication with all devices"
            ],
            priority=5,
            confidence=0.7
        ))
        
        # Sort by priority (descending)
        recommendations.sort(key=lambda r: r.priority, reverse=True)
        
        return recommendations
    
    def _get_actions_for_issue(self, issue: Dict[str, Any], change_proposal: Dict[str, Any]) -> List[str]:
        """Get specific actions for an issue"""
        issue_type = issue.get('type', 'unknown')
        
        actions_map = {
            'communication_failure': [
                "Check network connectivity between affected devices",
                "Verify protocol configuration",
                "Inspect network cables and switches"
            ],
            'protocol_incompatibility': [
                "Update firmware on incompatible devices",
                "Use protocol converter if necessary",
                "Consult manufacturer documentation"
            ],
            'configuration_error': [
                "Review configuration of affected devices",
                "Verify signal mappings",
                "Check for syntax errors in configuration"
            ],
            'device_compatibility': [
                "Verify device compatibility",
                "Check manufacturer specifications",
                "Consider using compatible alternatives"
            ]
        }
        
        return actions_map.get(issue_type, ["Investigate issue", "Consult documentation"])
    
    def _get_communication_actions(self, failures: List[Dict[str, Any]]) -> List[str]:
        """Get actions for communication failures"""
        actions = []
        for failure in failures:
            from_device = failure.get('from', 'unknown')
            to_device = failure.get('to', 'unknown')
            actions.append(f"Check connection between {from_device} and {to_device}")
        
        actions.extend([
            "Verify network switch configurations",
            "Test network latency",
            "Check for packet loss"
        ])
        
        return actions
    
    def _get_protocol_actions(self, issues: List[Dict[str, Any]]) -> List[str]:
        """Get actions for protocol issues"""
        actions = []
        for issue in issues:
            devices = issue.get('devices', [])
            if devices:
                actions.append(f"Verify protocol compatibility for {', '.join(devices)}")
        
        actions.extend([
            "Check protocol versions",
            "Update device firmware if needed",
            "Review protocol configuration"
        ])
        
        return actions
    
    def _determine_should_proceed(
        self, 
        impact_analysis: ImpactAnalysis,
        simulation: Optional[SimulationResult],
        recommendations: List[Recommendation]
    ) -> bool:
        """
        Determine if the change should proceed based on analysis.
        
        Args:
            impact_analysis: Impact analysis results
            simulation: Simulation results
            recommendations: Generated recommendations
            
        Returns:
            True if change should proceed, False otherwise
        """
        # If any recommendation is to reject, don't proceed
        if any(r.recommendation_type == RecommendationType.REJECT for r in recommendations):
            return False
        
        # If impact is critical, don't proceed
        if impact_analysis.impact_level == ImpactLevel.CRITICAL:
            return False
        
        # If simulation failed, don't proceed
        if simulation and not simulation.success:
            return False
        
        # If there are communication failures in simulation, don't proceed
        if simulation and simulation.communication_failures:
            return False
        
        # If there are protocol issues in simulation, don't proceed
        if simulation and simulation.protocol_issues:
            return False
        
        # If there are potential issues in impact analysis, be cautious
        if impact_analysis.potential_issues:
            return False
        
        # Otherwise, proceed
        return True
    
    def get_change_summary(self, result: FeedforwardResult) -> Dict[str, Any]:
        """
        Generate a summary of the change analysis for reporting.
        
        Args:
            result: FeedforwardResult object
            
        Returns:
            Dictionary with analysis summary
        """
        summary = {
            'change_id': result.change_id,
            'should_proceed': result.should_proceed,
            'impact_level': result.analysis.impact_level.value,
            'confidence': result.analysis.confidence,
            'affected_devices': len(result.analysis.affected_devices),
            'affected_signals': len(result.analysis.affected_signals),
            'potential_issues': len(result.analysis.potential_issues),
            'recommendations': [
                {
                    'type': r.recommendation_type.value,
                    'description': r.description,
                    'priority': r.priority
                } for r in result.recommendations
            ]
        }
        
        if result.simulation:
            summary['simulation_success'] = result.simulation.success
            summary['communication_failures'] = len(result.simulation.communication_failures)
            summary['protocol_issues'] = len(result.simulation.protocol_issues)
        
        return summary
    
    def suggest_optimizations(self, current_state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Suggest optimizations for the current substation configuration.
        
        Args:
            current_state: Current state of the substation
            
        Returns:
            List of optimization suggestions
        """
        if self.optimizer:
            return self.optimizer.suggest_optimizations(current_state)
        return []
    
    def validate_change(self, change_proposal: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate a change proposal for basic errors.
        
        Args:
            change_proposal: The proposed change
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Check required fields
        required_fields = ['change_id', 'change_type']
        for field in required_fields:
            if field not in change_proposal:
                errors.append(f"Missing required field: {field}")
        
        # Check change type
        change_type = change_proposal.get('change_type')
        if change_type and change_type not in [ct.value for ct in ChangeType]:
            errors.append(f"Invalid change type: {change_type}")
        
        # Check configuration changes
        if change_type == ChangeType.CONFIGURATION.value:
            if 'device' not in change_proposal:
                errors.append("Configuration change requires 'device' field")
            if 'parameter' not in change_proposal:
                errors.append("Configuration change requires 'parameter' field")
            if 'new_value' not in change_proposal:
                errors.append("Configuration change requires 'new_value' field")
        
        return len(errors) == 0, errors
