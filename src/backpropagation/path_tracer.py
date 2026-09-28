"""
Signal Path Tracer for Substation by K

This module implements signal path tracing through the substation network.
It uses the Knowledge Graph to find the complete path of a signal from
its source to its destination.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class PathSegment:
    """Represents a segment between two points in the signal path"""
    from_device: str
    to_device: str
    protocol: str
    connection_type: str
    latency: Optional[float] = None
    status: str = "active"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'from_device': self.from_device,
            'to_device': self.to_device,
            'protocol': self.protocol,
            'connection_type': self.connection_type,
            'latency': self.latency,
            'status': self.status
        }


class SignalPathTracer:
    """
    Traces signal paths through the substation network.
    
    This class uses the Knowledge Graph to find how signals flow from
    their source (typically an IED) to their destination (typically SCADA).
    """
    
    def __init__(self, knowledge_graph: Any = None):
        """
        Initialize the signal path tracer.
        
        Args:
            knowledge_graph: Knowledge graph instance containing substation topology
        """
        self.knowledge_graph = knowledge_graph
        self._cache: Dict[str, List[PathSegment]] = {}
        logger.info("SignalPathTracer initialized")
    
    def trace_path(
        self, 
        source_device: str, 
        signal_name: str, 
        destination: Optional[str] = None
    ) -> Any:
        """
        Trace the complete path of a signal through the network.
        
        Args:
            source_device: ID of the source device (IED)
            signal_name: Name of the signal (e.g., "52a", "87")
            destination: Optional destination device (defaults to SCADA)
            
        Returns:
            SignalPath object containing the complete path
        """
        from .engine import SignalPath, SignalPoint
        
        # Set default destination if not provided
        if destination is None:
            destination = self._get_default_destination()
        
        # Create cache key
        cache_key = f"{source_device}:{signal_name}:{destination}"
        
        # Check cache
        if cache_key in self._cache:
            logger.debug(f"Using cached path for {cache_key}")
            return self._create_signal_path(
                source_device, signal_name, destination, 
                self._cache[cache_key]
            )
        
        # Trace the path
        segments = self._trace_signal(source_device, signal_name, destination)
        
        # Cache the result
        self._cache[cache_key] = segments
        
        return self._create_signal_path(source_device, signal_name, destination, segments)
    
    def _get_default_destination(self) -> str:
        """Get the default destination (typically SCADA)"""
        if self.knowledge_graph:
            scada = self.knowledge_graph.get_scada_device()
            if scada:
                return scada['device_id']
        return "SCADA"
    
    def _trace_signal(
        self, 
        source: str, 
        signal_name: str, 
        destination: str
    ) -> List[PathSegment]:
        """
        Trace the signal path using the Knowledge Graph.
        
        Args:
            source: Source device ID
            signal_name: Signal name
            destination: Destination device ID
            
        Returns:
            List of PathSegment objects representing the path
        """
        segments = []
        
        if not self.knowledge_graph:
            logger.warning("No knowledge graph available, returning empty path")
            return segments
        
        # Get the signal path from knowledge graph
        try:
            path = self.knowledge_graph.get_signal_path(
                source=source,
                signal=signal_name,
                destination=destination
            )
            
            if not path:
                logger.warning(f"No path found from {source} to {destination} for signal {signal_name}")
                return segments
            
            # Convert path to segments
            for i in range(len(path) - 1):
                from_device = path[i]
                to_device = path[i + 1]
                
                # Get connection details
                connection = self.knowledge_graph.get_connection(
                    from_device, to_device
                )
                
                if connection:
                    segments.append(PathSegment(
                        from_device=from_device,
                        to_device=to_device,
                        protocol=connection.get('protocol', 'unknown'),
                        connection_type=connection.get('type', 'network'),
                        latency=connection.get('latency'),
                        status=connection.get('status', 'active')
                    ))
            
        except Exception as e:
            logger.error(f"Error tracing signal path: {e}")
        
        return segments
    
    def _create_signal_path(
        self, 
        source_device: str, 
        signal_name: str, 
        destination: str, 
        segments: List[PathSegment]
    ) -> Any:
        """
        Create a SignalPath object from segments.
        
        Args:
            source_device: Source device ID
            signal_name: Signal name
            destination: Destination device ID
            segments: List of path segments
            
        Returns:
            SignalPath object
        """
        from .engine import SignalPath, SignalPoint
        
        # Get device info from knowledge graph
        def get_device_info(device_id: str) -> SignalPoint:
            if self.knowledge_graph:
                device = self.knowledge_graph.get_device(device_id)
                if device:
                    return SignalPoint(
                        device_id=device_id,
                        device_type=device.get('type', 'unknown'),
                        device_name=device.get('name', device_id),
                        ip_address=device.get('ip'),
                        mac_address=device.get('mac'),
                        vlan=device.get('vlan')
                    )
            return SignalPoint(
                device_id=device_id,
                device_type="unknown",
                device_name=device_id
            )
        
        # Create source and destination points
        source = get_device_info(source_device)
        dest = get_device_info(destination)
        
        # Create intermediate points
        points = []
        for segment in segments:
            points.append(get_device_info(segment.to_device))
        
        # Create signal path
        path_id = f"path_{source_device}_{signal_name}_{destination}_{datetime.utcnow().timestamp()}"
        
        return SignalPath(
            path_id=path_id,
            signal_name=signal_name,
            signal_type=self._get_signal_type(signal_name),
            source=source,
            destination=dest,
            points=points
        )
    
    def _get_signal_type(self, signal_name: str) -> str:
        """
        Determine the type of signal based on its name.
        
        Args:
            signal_name: Name of the signal
            
        Returns:
            Signal type (e.g., "status", "measurement", "control")
        """
        # Common signal types in substations
        status_signals = ['52a', '52b', '86', '87', '94']
        measurement_signals = ['MV', 'MVAR', 'MW', 'MWH', 'A', 'V', 'Hz']
        control_signals = ['CSWI', 'XCBR', 'XSWI']
        
        signal_upper = signal_name.upper()
        
        if any(s in signal_upper for s in status_signals):
            return "status"
        elif any(s in signal_upper for s in measurement_signals):
            return "measurement"
        elif any(s in signal_upper for s in control_signals):
            return "control"
        
        return "unknown"
    
    def get_all_paths_from_device(self, device_id: str) -> List[Any]:
        """
        Get all signal paths originating from a device.
        
        Args:
            device_id: Device ID to get paths from
            
        Returns:
            List of SignalPath objects
        """
        if not self.knowledge_graph:
            return []
        
        paths = []
        
        try:
            # Get all signals published by this device
            signals = self.knowledge_graph.get_device_signals(device_id)
            
            for signal in signals:
                signal_path = self.trace_path(
                    source_device=device_id,
                    signal_name=signal['name'],
                    destination=None  # Use default (SCADA)
                )
                paths.append(signal_path)
                
        except Exception as e:
            logger.error(f"Error getting paths from device {device_id}: {e}")
        
        return paths
    
    def validate_path(self, signal_path: Any) -> Dict[str, Any]:
        """
        Validate a signal path by checking each segment.
        
        Args:
            signal_path: SignalPath object to validate
            
        Returns:
            Dictionary with validation results
        """
        results = {
            'path_id': signal_path.path_id,
            'signal_name': signal_path.signal_name,
            'valid': True,
            'issues': []
        }
        
        # Check source
        if signal_path.source.status != 'present':
            results['valid'] = False
            results['issues'].append({
                'location': 'source',
                'device': signal_path.source.device_id,
                'issue': 'Source signal not present',
                'severity': 'high'
            })
        
        # Check each segment
        for i, point in enumerate(signal_path.points):
            if point.status != 'present':
                results['valid'] = False
                results['issues'].append({
                    'location': f'point_{i}',
                    'device': point.device_id,
                    'issue': f'Signal not present at {point.device_name}',
                    'severity': 'high'
                })
        
        # Check destination
        if signal_path.destination.status != 'present':
            results['valid'] = False
            results['issues'].append({
                'location': 'destination',
                'device': signal_path.destination.device_id,
                'issue': 'Signal not present at destination',
                'severity': 'high'
            })
        
        return results
    
    def find_alternative_paths(
        self, 
        source: str, 
        signal_name: str, 
        destination: str
    ) -> List[Any]:
        """
        Find alternative paths for a signal if the primary path fails.
        
        Args:
            source: Source device ID
            signal_name: Signal name
            destination: Destination device ID
            
        Returns:
            List of alternative SignalPath objects
        """
        if not self.knowledge_graph:
            return []
        
        alternative_paths = []
        
        try:
            # Get all possible paths from source to destination
            all_paths = self.knowledge_graph.get_all_paths(
                source, destination
            )
            
            # For each path, create a SignalPath
            for path in all_paths:
                segments = []
                for i in range(len(path) - 1):
                    from_device = path[i]
                    to_device = path[i + 1]
                    connection = self.knowledge_graph.get_connection(from_device, to_device)
                    
                    if connection:
                        segments.append(PathSegment(
                            from_device=from_device,
                            to_device=to_device,
                            protocol=connection.get('protocol', 'unknown'),
                            connection_type=connection.get('type', 'network')
                        ))
                
                if segments:
                    alt_path = self._create_signal_path(
                        source, signal_name, destination, segments
                    )
                    alternative_paths.append(alt_path)
                    
        except Exception as e:
            logger.error(f"Error finding alternative paths: {e}")
        
        return alternative_paths
