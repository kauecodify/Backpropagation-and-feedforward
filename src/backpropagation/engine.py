"""
Backpropagation Engine for Substation by K

The core engine that implements backpropagation (reverse signal path tracing)
for failure analysis in digital substations.

This engine:
1. Identifies the signal path from source to destination
2. Collects data from each point in the path
3. Performs backward analysis to find failure points
4. Calculates probabilities for each potential cause
5. Gathers evidence to support each hypothesis
6. Generates a diagnosis with recommendations
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class SignalStatus(Enum):
    """Status of a signal at a particular point in the path"""
    PRESENT = "present"
    MISSING = "missing"
    CORRUPTED = "corrupted"
    DELAYED = "delayed"
    UNKNOWN = "unknown"


class FailureType(Enum):
    """Types of failures that can occur in the signal path"""
    SIGNAL_MISSING = "signal_missing"
    TRANSMISSION_FAILURE = "transmission_failure"
    PROTOCOL_ERROR = "protocol_error"
    CONFIGURATION_ERROR = "configuration_error"
    DEVICE_FAILURE = "device_failure"
    NETWORK_ISSUE = "network_issue"


@dataclass
class SignalPoint:
    """Represents a point in the signal path"""
    device_id: str
    device_type: str
    device_name: str
    protocol: Optional[str] = None
    ip_address: Optional[str] = None
    mac_address: Optional[str] = None
    vlan: Optional[int] = None
    status: SignalStatus = SignalStatus.UNKNOWN
    timestamp: Optional[datetime] = None
    data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SignalPath:
    """Represents the complete path of a signal through the substation"""
    path_id: str
    signal_name: str
    signal_type: str
    source: SignalPoint
    destination: SignalPoint
    points: List[SignalPoint] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class FailurePoint:
    """Represents a point where the signal path fails"""
    location: SignalPoint
    failure_type: FailureType
    from_point: Optional[SignalPoint] = None
    to_point: Optional[SignalPoint] = None
    description: str = ""
    severity: str = "medium"


@dataclass
class Evidence:
    """Evidence supporting a failure hypothesis"""
    evidence_id: str
    evidence_type: str
    description: str
    data: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 1.0
    timestamp: Optional[datetime] = None


@dataclass
class Hypothesis:
    """A hypothesis about the cause of a failure"""
    hypothesis_id: str
    failure_point: FailurePoint
    description: str
    probability: float
    evidence: List[Evidence] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


@dataclass
class Diagnosis:
    """Complete diagnosis of a failure event"""
    diagnosis_id: str
    event_id: str
    event_description: str
    signal_path: SignalPath
    failure_points: List[FailurePoint] = field(default_factory=list)
    hypotheses: List[Hypothesis] = field(default_factory=list)
    primary_hypothesis: Optional[Hypothesis] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert diagnosis to dictionary for serialization"""
        return {
            'diagnosis_id': self.diagnosis_id,
            'event_id': self.event_id,
            'event_description': self.event_description,
            'signal_path': {
                'path_id': self.signal_path.path_id,
                'signal_name': self.signal_path.signal_name,
                'source': self._point_to_dict(self.signal_path.source),
                'destination': self._point_to_dict(self.signal_path.destination),
                'points': [self._point_to_dict(p) for p in self.signal_path.points]
            },
            'failure_points': [self._failure_to_dict(fp) for fp in self.failure_points],
            'hypotheses': [self._hypothesis_to_dict(h) for h in self.hypotheses],
            'primary_hypothesis': self._hypothesis_to_dict(self.primary_hypothesis) if self.primary_hypothesis else None,
            'created_at': self.created_at.isoformat()
        }
    
    def _point_to_dict(self, point: SignalPoint) -> Dict[str, Any]:
        return {
            'device_id': point.device_id,
            'device_type': point.device_type,
            'device_name': point.device_name,
            'protocol': point.protocol,
            'ip_address': point.ip_address,
            'mac_address': point.mac_address,
            'vlan': point.vlan,
            'status': point.status.value,
            'timestamp': point.timestamp.isoformat() if point.timestamp else None
        }
    
    def _failure_to_dict(self, fp: FailurePoint) -> Dict[str, Any]:
        return {
            'location': self._point_to_dict(fp.location),
            'failure_type': fp.failure_type.value,
            'description': fp.description,
            'severity': fp.severity
        }
    
    def _evidence_to_dict(self, evidence: Evidence) -> Dict[str, Any]:
        return {
            'evidence_id': evidence.evidence_id,
            'evidence_type': evidence.evidence_type,
            'description': evidence.description,
            'data': evidence.data,
            'confidence': evidence.confidence
        }
    
    def _hypothesis_to_dict(self, h: Optional[Hypothesis]) -> Optional[Dict[str, Any]]:
        if not h:
            return None
        return {
            'hypothesis_id': h.hypothesis_id,
            'description': h.description,
            'probability': h.probability,
            'failure_point': self._failure_to_dict(h.failure_point),
            'evidence': [self._evidence_to_dict(e) for e in h.evidence],
            'recommendations': h.recommendations
        }


class BackpropagationEngine:
    """
    Main backpropagation engine for failure analysis.
    
    This engine traces signal paths backwards from failure points to identify
    where the signal chain breaks and gather evidence for diagnosis.
    """
    
    def __init__(self, knowledge_graph: Any = None, substation_memory: Any = None):
        """
        Initialize the backpropagation engine.
        
        Args:
            knowledge_graph: Knowledge graph instance for substation topology
            substation_memory: Substation Memory instance for historical data
        """
        self.knowledge_graph = knowledge_graph
        self.substation_memory = substation_memory
        self.path_tracer = SignalPathTracer(knowledge_graph)
        self.failure_analyzer = FailureAnalyzer()
        self.probability_calculator = ProbabilityCalculator(substation_memory)
        
        logger.info("BackpropagationEngine initialized")
    
    def analyze_failure(self, event: Dict[str, Any]) -> Diagnosis:
        """
        Main method to analyze a failure event using backpropagation.
        
        Args:
            event: Dictionary containing event information
                - event_id: Unique identifier for the event
                - description: Description of the failure event
                - source: Source device/point of the signal
                - signal: Signal name/type that failed
                - destination: Destination where signal should arrive
                
        Returns:
            Diagnosis: Complete diagnosis with hypotheses and evidence
        """
        logger.info(f"Analyzing failure event: {event.get('event_id')}")
        
        # Step 1: Identify the signal path
        signal_path = self._identify_signal_path(event)
        logger.debug(f"Signal path identified: {signal_path.path_id}")
        
        # Step 2: Collect data from each point in the path
        path_data = self._collect_path_data(signal_path)
        logger.debug(f"Collected data from {len(path_data)} points")
        
        # Step 3: Perform backward analysis
        failure_points = self.failure_analyzer.backward_analysis(
            signal_path, path_data
        )
        logger.debug(f"Found {len(failure_points)} failure points")
        
        # Step 4: Calculate probabilities
        hypotheses = self.probability_calculator.calculate_hypotheses(
            failure_points, path_data, signal_path
        )
        logger.debug(f"Generated {len(hypotheses)} hypotheses")
        
        # Step 5: Select primary hypothesis
        primary_hypothesis = self._select_primary_hypothesis(hypotheses)
        
        # Step 6: Create diagnosis
        diagnosis = Diagnosis(
            diagnosis_id=f"diag_{event.get('event_id')}_{datetime.utcnow().timestamp()}",
            event_id=event.get('event_id', 'unknown'),
            event_description=event.get('description', 'Unknown failure'),
            signal_path=signal_path,
            failure_points=failure_points,
            hypotheses=hypotheses,
            primary_hypothesis=primary_hypothesis
        )
        
        logger.info(f"Diagnosis completed: {diagnosis.diagnosis_id}")
        return diagnosis
    
    def _identify_signal_path(self, event: Dict[str, Any]) -> SignalPath:
        """
        Identify the complete signal path from source to destination.
        
        Args:
            event: Failure event dictionary
            
        Returns:
            SignalPath: The complete path of the signal
        """
        if self.knowledge_graph:
            return self.path_tracer.trace_path(
                source_device=event.get('source'),
                signal_name=event.get('signal'),
                destination=event.get('destination')
            )
        
        # Fallback: Create a basic path if no knowledge graph
        return self._create_basic_path(event)
    
    def _create_basic_path(self, event: Dict[str, Any]) -> SignalPath:
        """Create a basic signal path when knowledge graph is not available"""
        source = SignalPoint(
            device_id=event.get('source', 'unknown'),
            device_type="unknown",
            device_name=event.get('source', 'Unknown')
        )
        
        destination = SignalPoint(
            device_id=event.get('destination', 'unknown'),
            device_type="unknown",
            device_name=event.get('destination', 'Unknown')
        )
        
        return SignalPath(
            path_id=f"path_{event.get('event_id')}",
            signal_name=event.get('signal', 'unknown'),
            signal_type="status",
            source=source,
            destination=destination
        )
    
    def _collect_path_data(self, signal_path: SignalPath) -> Dict[str, Dict[str, Any]]:
        """
        Collect data from each point in the signal path.
        
        Args:
            signal_path: The signal path to collect data from
            
        Returns:
            Dictionary mapping point indices to their data
        """
        path_data = {}
        
        # Collect data from source
        if self.knowledge_graph:
            source_data = self.knowledge_graph.get_device_data(signal_path.source.device_id)
            path_data[0] = {'point': signal_path.source, 'data': source_data}
        
        # Collect data from each intermediate point
        for i, point in enumerate(signal_path.points):
            if self.knowledge_graph:
                point_data = self.knowledge_graph.get_device_data(point.device_id)
                path_data[i+1] = {'point': point, 'data': point_data}
        
        # Collect data from destination
        if self.knowledge_graph:
            dest_data = self.knowledge_graph.get_device_data(signal_path.destination.device_id)
            path_data[len(path_data)] = {'point': signal_path.destination, 'data': dest_data}
        
        return path_data
    
    def _select_primary_hypothesis(self, hypotheses: List[Hypothesis]) -> Optional[Hypothesis]:
        """
        Select the most probable hypothesis as the primary diagnosis.
        
        Args:
            hypotheses: List of hypotheses
            
        Returns:
            The hypothesis with the highest probability
        """
        if not hypotheses:
            return None
        
        return max(hypotheses, key=lambda h: h.probability)
    
    def get_diagnosis_summary(self, diagnosis: Diagnosis) -> Dict[str, Any]:
        """
        Generate a summary of the diagnosis for reporting.
        
        Args:
            diagnosis: The complete diagnosis
            
        Returns:
            Dictionary with diagnosis summary
        """
        if not diagnosis.primary_hypothesis:
            return {
                'event': diagnosis.event_description,
                'status': 'no_failure_found',
                'message': 'No failure points identified'
            }
        
        primary = diagnosis.primary_hypothesis
        return {
            'event': diagnosis.event_description,
            'diagnosis': primary.description,
            'probability': f"{primary.probability * 100:.1f}%",
            'failure_location': primary.failure_point.location.device_name,
            'failure_type': primary.failure_point.failure_type.value,
            'evidence': [
                {
                    'type': e.evidence_type,
                    'description': e.description
                } for e in primary.evidence
            ],
            'recommendations': primary.recommendations
        }
