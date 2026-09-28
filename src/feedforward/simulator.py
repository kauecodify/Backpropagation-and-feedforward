"""
Substation Simulator for Substation by K

This module simulates the behavior of a substation with proposed changes
to predict their impact before implementation.
"""

from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime
import logging
import copy

logger = logging.getLogger(__name__)


@dataclass
class SignalFlow:
    """Represents the flow of a signal through the network"""
    signal_id: str
    signal_name: str
    path: List[str] = field(default_factory=list)
    success: bool = True
    failure_point: Optional[str] = None
    failure_reason: Optional[str] = None
    latency: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        result = {
            'signal_id': self.signal_id,
            'signal_name': self.signal_name,
            'path': self.path,
            'success': self.success,
            'latency': self.latency
        }
        if self.failure_point:
            result['failure_point'] = self.failure_point
        if self.failure_reason:
            result['failure_reason'] = self.failure_reason
        return result


class SubstationSimulator:
    """
    Simulates the behavior of a substation.
    
    This class creates a virtual environment where changes can be tested
    before being applied to the real substation. It simulates:
    - Signal flow through the network
    - Protocol compatibility
    - Device behavior
    - Network performance
    """
    
    def __init__(self, digital_twin: Any = None, knowledge_graph: Any = None):
        """
        Initialize the substation simulator.
        
        Args:
            digital_twin: Digital Twin instance for current state
            knowledge_graph: Knowledge graph for topology reference
        """
        self.digital_twin = digital_twin
        self.knowledge_graph = knowledge_graph
        self._current_state: Optional[Dict[str, Any]] = None
        logger.info("SubstationSimulator initialized")
    
    def simulate_change(self, change_proposal: Dict[str, Any]) -> Any:
        """
        Simulate the effect of a proposed change.
        
        Args:
            change_proposal: Dictionary describing the proposed change
                - change_id: Unique identifier for the change
                - change_type: Type of change
                - device: Device ID (if applicable)
                - parameter: Parameter being changed (if applicable)
                - old_value: Current value
                - new_value: Proposed new value
                
        Returns:
            SimulationResult: Results of the simulation
        """
        from .engine import SimulationResult
        
        change_id = change_proposal.get('change_id', 'unknown')
        logger.info(f"Simulating change: {change_id}")
        
        # Get current state
        current_state = self._get_current_state()
        
        # Apply the change to create a modified state
        modified_state = self._apply_change(current_state, change_proposal)
        
        # Run simulation on the modified state
        result = self._run_simulation(modified_state, change_id)
        
        logger.debug(f"Simulation completed for {change_id}")
        return result
    
    def _get_current_state(self) -> Dict[str, Any]:
        """Get the current state of the substation"""
        if self.digital_twin:
            return self.digital_twin.get_current_state()
        elif self.knowledge_graph:
            return self._create_state_from_knowledge_graph()
        else:
            return self._create_empty_state()
    
    def _create_state_from_knowledge_graph(self) -> Dict[str, Any]:
        """Create state from knowledge graph"""
        state = {
            'devices': {},
            'connections': {},
            'signals': {},
            'network': {}
        }
        
        if self.knowledge_graph:
            # Load devices
            devices = self.knowledge_graph.get_all_devices()
            for device in devices:
                state['devices'][device['device_id']] = device
            
            # Load connections
            connections = self.knowledge_graph.get_all_connections()
            for conn in connections:
                state['connections'][conn['connection_id']] = conn
            
            # Load signals
            signals = self.knowledge_graph.get_all_signals()
            for signal in signals:
                state['signals'][signal['signal_id']] = signal
            
            # Load network configuration
            network = self.knowledge_graph.get_network_configuration()
            state['network'] = network
        
        return state
    
    def _create_empty_state(self) -> Dict[str, Any]:
        """Create an empty state"""
        return {
            'devices': {},
            'connections': {},
            'signals': {},
            'network': {}
        }
    
    def _apply_change(
        self, 
        state: Dict[str, Any], 
        change_proposal: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Apply a change to the state.
        
        Args:
            state: Current state of the substation
            change_proposal: The proposed change
            
        Returns:
            Modified state with the change applied
        """
        # Create a deep copy of the state
        modified_state = copy.deepcopy(state)
        
        change_type = change_proposal.get('change_type', 'configuration')
        
        if change_type == 'configuration':
            self._apply_configuration_change(modified_state, change_proposal)
        elif change_type == 'network':
            self._apply_network_change(modified_state, change_proposal)
        elif change_type == 'device':
            self._apply_device_change(modified_state, change_proposal)
        elif change_type == 'signal':
            self._apply_signal_change(modified_state, change_proposal)
        
        return modified_state
    
    def _apply_configuration_change(
        self, 
        state: Dict[str, Any], 
        change_proposal: Dict[str, Any]
    ) -> None:
        """Apply a configuration change to the state"""
        device_id = change_proposal.get('device')
        parameter = change_proposal.get('parameter')
        new_value = change_proposal.get('new_value')
        
        if not device_id or not parameter:
            return
        
        if device_id in state['devices']:
            device = state['devices'][device_id]
            
            # Update configuration
            if 'configuration' not in device:
                device['configuration'] = {}
            
            device['configuration'][parameter] = new_value
            
            # Update timestamp
            device['last_config_change'] = datetime.utcnow().isoformat()
    
    def _apply_network_change(
        self, 
        state: Dict[str, Any], 
        change_proposal: Dict[str, Any]
    ) -> None:
        """Apply a network change to the state"""
        device_id = change_proposal.get('device')
        parameter = change_proposal.get('parameter')
        new_value = change_proposal.get('new_value')
        
        if not device_id or not parameter:
            return
        
        if device_id in state['devices']:
            device = state['devices'][device_id]
            
            if parameter == 'ip':
                device['ip_address'] = new_value
            elif parameter == 'vlan':
                device['vlan'] = new_value
            elif parameter == 'mac':
                device['mac_address'] = new_value
            
            # Update network configuration
            if 'network' not in state:
                state['network'] = {}
            
            state['network'][f"{device_id}_{parameter}"] = new_value
    
    def _apply_device_change(
        self, 
        state: Dict[str, Any], 
        change_proposal: Dict[str, Any]
    ) -> None:
        """Apply a device change (add/remove/replace) to the state"""
        action = change_proposal.get('action', 'replace')
        device_id = change_proposal.get('device')
        new_device = change_proposal.get('new_device')
        
        if action == 'remove' and device_id:
            # Remove device
            if device_id in state['devices']:
                del state['devices'][device_id]
            
            # Remove connections involving this device
            connections_to_remove = []
            for conn_id, conn in state['connections'].items():
                if conn.get('from') == device_id or conn.get('to') == device_id:
                    connections_to_remove.append(conn_id)
            
            for conn_id in connections_to_remove:
                del state['connections'][conn_id]
        
        elif action == 'add' and new_device:
            # Add new device
            state['devices'][new_device['device_id']] = new_device
        
        elif action == 'replace' and device_id and new_device:
            # Replace device
            if device_id in state['devices']:
                del state['devices'][device_id]
            state['devices'][new_device['device_id']] = new_device
    
    def _apply_signal_change(
        self, 
        state: Dict[str, Any], 
        change_proposal: Dict[str, Any]
    ) -> None:
        """Apply a signal change to the state"""
        signal_id = change_proposal.get('signal')
        parameter = change_proposal.get('parameter')
        new_value = change_proposal.get('new_value')
        
        if not signal_id or not parameter:
            return
        
        if signal_id in state['signals']:
            signal = state['signals'][signal_id]
            signal[parameter] = new_value
    
    def _run_simulation(
        self, 
        state: Dict[str, Any], 
        change_id: str
    ) -> Any:
        """
        Run the simulation on the modified state.
        
        Args:
            state: Modified state with change applied
            change_id: ID of the change being simulated
            
        Returns:
            SimulationResult: Results of the simulation
        """
        from .engine import SimulationResult
        
        result = SimulationResult(
            simulation_id=f"sim_{change_id}_{datetime.utcnow().timestamp()}",
            change_id=change_id,
            success=True,
            signal_flow={},
            communication_failures=[],
            protocol_issues=[],
            performance_issues=[],
            warnings=[]
        )
        
        # Simulate signal flow
        self._simulate_signal_flow(state, result)
        
        # Check for communication failures
        self._check_communication_failures(state, result)
        
        # Check for protocol issues
        self._check_protocol_issues(state, result)
        
        # Check for performance issues
        self._check_performance_issues(state, result)
        
        # Determine overall success
        result.success = (
            len(result.communication_failures) == 0 and
            len(result.protocol_issues) == 0 and
            len(result.performance_issues) == 0
        )
        
        return result
    
    def _simulate_signal_flow(
        self, 
        state: Dict[str, Any], 
        result: Any
    ) -> None:
        """Simulate the flow of signals through the network"""
        # Get all signals
        signals = state.get('signals', {})
        
        for signal_id, signal in signals.items():
            signal_flow = self._trace_signal(state, signal)
            result.signal_flow[signal_id] = signal_flow.to_dict()
            
            if not signal_flow.success:
                result.communication_failures.append({
                    'signal_id': signal_id,
                    'signal_name': signal.get('name', signal_id),
                    'failure_point': signal_flow.failure_point,
                    'failure_reason': signal_flow.failure_reason,
                    'severity': 'high'
                })
    
    def _trace_signal(
        self, 
        state: Dict[str, Any], 
        signal: Dict[str, Any]
    ) -> SignalFlow:
        """
        Trace the path of a signal through the network.
        
        Args:
            state: Current state of the substation
            signal: Signal to trace
            
        Returns:
            SignalFlow: The flow of the signal through the network
        """
        signal_id = signal.get('signal_id', 'unknown')
        signal_name = signal.get('name', signal_id)
        source_device = signal.get('source_device')
        destination = signal.get('destination', 'SCADA')
        
        # Find the path from source to destination
        path = self._find_signal_path(state, source_device, destination)
        
        if not path:
            return SignalFlow(
                signal_id=signal_id,
                signal_name=signal_name,
                path=[],
                success=False,
                failure_point=source_device,
                failure_reason="No path found from source to destination"
            )
        
        # Check each segment of the path
        failure_point = None
        failure_reason = None
        total_latency = 0.0
        
        for i in range(len(path) - 1):
            from_device = path[i]
            to_device = path[i + 1]
            
            # Check if connection exists
            connection = self._get_connection(state, from_device, to_device)
            if not connection:
                failure_point = to_device
                failure_reason = f"No connection between {from_device} and {to_device}"
                break
            
            # Check if connection is active
            if connection.get('status') != 'active':
                failure_point = to_device
                failure_reason = f"Connection between {from_device} and {to_device} is inactive"
                break
            
            # Check protocol compatibility
            protocol_error = self._check_protocol_compatibility(
                state, from_device, to_device, connection
            )
            if protocol_error:
                failure_point = to_device
                failure_reason = protocol_error
                break
            
            # Check VLAN compatibility
            vlan_error = self._check_vlan_compatibility(state, from_device, to_device)
            if vlan_error:
                failure_point = to_device
                failure_reason = vlan_error
                break
            
            # Add to path and accumulate latency
            path_segment = f"{from_device}->{to_device}"
            if path_segment not in path:
                path.append(path_segment)
            
            latency = connection.get('latency', 0.0)
            total_latency += latency
        
        return SignalFlow(
            signal_id=signal_id,
            signal_name=signal_name,
            path=path,
            success=failure_point is None,
            failure_point=failure_point,
            failure_reason=failure_reason,
            latency=total_latency
        )
    
    def _find_signal_path(
        self, 
        state: Dict[str, Any], 
        source: str, 
        destination: str
    ) -> List[str]:
        """
        Find the path of a signal from source to destination.
        
        Args:
            state: Current state of the substation
            source: Source device ID
            destination: Destination device ID
            
        Returns:
            List of device IDs representing the path
        """
        if self.knowledge_graph:
            # Use knowledge graph to find path
            path = self.knowledge_graph.get_signal_path(
                source=source,
                destination=destination
            )
            return path if path else []
        
        # Fallback: Use state to find path
        return self._find_path_in_state(state, source, destination)
    
    def _find_path_in_state(
        self, 
        state: Dict[str, Any], 
        source: str, 
        destination: str
    ) -> List[str]:
        """Find path in state using breadth-first search"""
        # Build adjacency list
        graph = {}
        for conn_id, conn in state.get('connections', {}).items():
            from_device = conn.get('from')
            to_device = conn.get('to')
            
            if from_device not in graph:
                graph[from_device] = []
            if to_device not in graph[from_device]:
                graph[from_device].append(to_device)
            
            # Add reverse direction for undirected graph
            if to_device not in graph:
                graph[to_device] = []
            if from_device not in graph[to_device]:
                graph[to_device].append(from_device)
        
        # BFS to find path
        visited = set()
        queue = [[source]]
        
        while queue:
            path = queue.pop(0)
            node = path[-1]
            
            if node == destination:
                return path
            
            if node not in visited:
                visited.add(node)
                for neighbor in graph.get(node, []):
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)
        
        return []
    
    def _get_connection(
        self, 
        state: Dict[str, Any], 
        from_device: str, 
        to_device: str
    ) -> Optional[Dict[str, Any]]:
        """Get the connection between two devices"""
        for conn_id, conn in state.get('connections', {}).items():
            if (conn.get('from') == from_device and conn.get('to') == to_device) or \
               (conn.get('from') == to_device and conn.get('to') == from_device):
                return conn
        return None
    
    def _check_protocol_compatibility(
        self, 
        state: Dict[str, Any], 
        from_device: str, 
        to_device: str, 
        connection: Dict[str, Any]
    ) -> Optional[str]:
        """
        Check if the protocols are compatible between two devices.
        
        Args:
            state: Current state of the substation
            from_device: Source device ID
            to_device: Destination device ID
            connection: Connection between the devices
            
        Returns:
            Error message if protocols are incompatible, None otherwise
        """
        from_protocol = state.get('devices', {}).get(from_device, {}).get('protocol')
        to_protocol = state.get('devices', {}).get(to_device, {}).get('protocol')
        connection_protocol = connection.get('protocol')
        
        # If no protocols specified, assume compatible
        if not from_protocol and not to_protocol and not connection_protocol:
            return None
        
        # Check if connection protocol matches device protocols
        if connection_protocol:
            if from_protocol and from_protocol != connection_protocol:
                return f"Device {from_device} uses {from_protocol} but connection uses {connection_protocol}"
            if to_protocol and to_protocol != connection_protocol:
                return f"Device {to_device} uses {to_protocol} but connection uses {connection_protocol}"
        
        # Check if device protocols are compatible
        if from_protocol and to_protocol and from_protocol != to_protocol:
            # Some protocols are compatible (e.g., IEC 61850 can work with IEC 104 via gateway)
            compatible_pairs = [
                ('GOOSE', 'IEC-104'),
                ('MMS', 'IEC-104'),
                ('GOOSE', 'DNP3'),
                ('MMS', 'DNP3')
            ]
            
            if (from_protocol, to_protocol) not in compatible_pairs and \
               (to_protocol, from_protocol) not in compatible_pairs:
                return f"Protocol mismatch: {from_device} uses {from_protocol}, {to_device} uses {to_protocol}"
        
        return None
    
    def _check_vlan_compatibility(
        self, 
        state: Dict[str, Any], 
        from_device: str, 
        to_device: str
    ) -> Optional[str]:
        """
        Check if VLANs are compatible between two devices.
        
        Args:
            state: Current state of the substation
            from_device: Source device ID
            to_device: Destination device ID
            
        Returns:
            Error message if VLANs are incompatible, None otherwise
        """
        from_vlan = state.get('devices', {}).get(from_device, {}).get('vlan')
        to_vlan = state.get('devices', {}).get(to_device, {}).get('vlan')
        
        if from_vlan is not None and to_vlan is not None and from_vlan != to_vlan:
            return f"VLAN mismatch: {from_device} is in VLAN {from_vlan}, {to_device} is in VLAN {to_vlan}"
        
        return None
    
    def _check_communication_failures(
        self, 
        state: Dict[str, Any], 
        result: Any
    ) -> None:
        """Check for communication failures in the simulation"""
        # Already handled in signal flow simulation
        pass
    
    def _check_protocol_issues(
        self, 
        state: Dict[str, Any], 
        result: Any
    ) -> None:
        """Check for protocol issues in the simulation"""
        # Check all connections for protocol compatibility
        for conn_id, conn in state.get('connections', {}).items():
            from_device = conn.get('from')
            to_device = conn.get('to')
            
            if from_device and to_device:
                error = self._check_protocol_compatibility(state, from_device, to_device, conn)
                if error:
                    result.protocol_issues.append({
                        'connection_id': conn_id,
                        'from_device': from_device,
                        'to_device': to_device,
                        'description': error,
                        'severity': 'high'
                    })
    
    def _check_performance_issues(
        self, 
        state: Dict[str, Any], 
        result: Any
    ) -> None:
        """Check for performance issues in the simulation"""
        # Check for high latency connections
        for conn_id, conn in state.get('connections', {}).items():
            latency = conn.get('latency', 0.0)
            if latency > 100:  # 100ms threshold
                result.performance_issues.append({
                    'connection_id': conn_id,
                    'from_device': conn.get('from'),
                    'to_device': conn.get('to'),
                    'metric': 'latency',
                    'value': latency,
                    'threshold': 100,
                    'severity': 'medium'
                })
        
        # Check for devices with high CPU/memory usage
        for device_id, device in state.get('devices', {}).items():
            cpu = device.get('cpu_usage', 0)
            memory = device.get('memory_usage', 0)
            
            if cpu > 90:
                result.performance_issues.append({
                    'device_id': device_id,
                    'metric': 'cpu_usage',
                    'value': cpu,
                    'threshold': 90,
                    'severity': 'high'
                })
            
            if memory > 85:
                result.performance_issues.append({
                    'device_id': device_id,
                    'metric': 'memory_usage',
                    'value': memory,
                    'threshold': 85,
                    'severity': 'medium'
                })
    
    def test_signal_path(self, signal_name: str, source: str = None) -> Any:
        """
        Test the path of a specific signal.
        
        Args:
            signal_name: Name of the signal to test
            source: Optional source device (defaults to publisher)
            
        Returns:
            SignalFlow: The flow of the signal
        """
        state = self._get_current_state()
        
        # Find the signal
        signal = None
        for s_id, s in state.get('signals', {}).items():
            if s.get('name') == signal_name:
                signal = s
                break
        
        if not signal:
            return SignalFlow(
                signal_id='unknown',
                signal_name=signal_name,
                success=False,
                failure_reason=f"Signal {signal_name} not found"
            )
        
        # Use signal's source if not provided
        signal_source = source or signal.get('source_device')
        destination = signal.get('destination', 'SCADA')
        
        return self._trace_signal(state, signal)
