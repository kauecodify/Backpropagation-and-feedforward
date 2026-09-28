"""
Impact Predictor for Substation by K

This module predicts the impact of proposed changes to the substation
configuration, network, or devices.
"""

from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class ImpactScope(Enum):
    """Scope of impact for a change"""
    DEVICE = "device"
    SIGNAL = "signal"
    CONNECTION = "connection"
    SUBSTATION = "substation"


@dataclass
class AffectedEntity:
    """Represents an entity affected by a change"""
    entity_id: str
    entity_type: str
    impact_scope: ImpactScope
    impact_level: str
    description: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'entity_id': self.entity_id,
            'entity_type': self.entity_type,
            'impact_scope': self.impact_scope.value,
            'impact_level': self.impact_level,
            'description': self.description
        }


class ImpactPredictor:
    """
    Predicts the impact of proposed changes to the substation.
    
    This class analyzes how a change will affect:
    - Individual devices
    - Signal paths
    - Network connections
    - Overall substation operation
    """
    
    # Impact weights for different entity types
    IMPACT_WEIGHTS = {
        'scada': 1.0,
        'gateway': 0.9,
        'ied': 0.8,
        'switch': 0.7,
        'rtu': 0.8,
        'signal': 0.6,
        'connection': 0.5
    }
    
    # Impact levels based on number of affected entities
    IMPACT_LEVELS = {
        'none': (0, 0),
        'low': (1, 3),
        'medium': (4, 10),
        'high': (11, 50),
        'critical': (51, float('inf'))
    }
    
    def __init__(self, knowledge_graph: Any = None):
        """
        Initialize the impact predictor.
        
        Args:
            knowledge_graph: Knowledge graph instance for substation topology
        """
        self.knowledge_graph = knowledge_graph
        self._dependency_cache: Dict[str, Dict[str, Any]] = {}
        logger.info("ImpactPredictor initialized")
    
    def predict_impact(self, change_proposal: Dict[str, Any]) -> Any:
        """
        Predict the impact of a proposed change.
        
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
            ImpactAnalysis: Complete impact analysis
        """
        from .engine import ImpactAnalysis, ImpactLevel, ChangeType
        
        change_id = change_proposal.get('change_id', 'unknown')
        change_type = change_proposal.get('change_type', ChangeType.CONFIGURATION.value)
        
        logger.info(f"Predicting impact for change: {change_id}")
        
        # Initialize analysis
        analysis = ImpactAnalysis(
            change_id=change_id,
            change_type=ChangeType(change_type),
            affected_devices=[],
            affected_signals=[],
            affected_connections=[],
            potential_issues=[],
            impact_level=ImpactLevel.NONE,
            confidence=0.0
        )
        
        # Get affected entities based on change type
        affected_entities = self._get_affected_entities(change_proposal)
        
        # Categorize affected entities
        for entity in affected_entities:
            if entity.entity_type == 'device':
                analysis.affected_devices.append(entity.entity_id)
            elif entity.entity_type == 'signal':
                analysis.affected_signals.append(entity.entity_id)
            elif entity.entity_type == 'connection':
                # Extract device pair for connection
                if ':' in entity.entity_id:
                    from_device, to_device = entity.entity_id.split(':')
                    analysis.affected_connections.append((from_device, to_device))
        
        # Generate potential issues
        analysis.potential_issues = self._generate_potential_issues(
            change_proposal, affected_entities
        )
        
        # Calculate impact level
        analysis.impact_level = self._calculate_impact_level(
            len(analysis.affected_devices),
            len(analysis.affected_signals),
            len(analysis.affected_connections)
        )
        
        # Calculate confidence
        analysis.confidence = self._calculate_confidence(change_proposal, affected_entities)
        
        logger.debug(f"Impact prediction completed for {change_id}")
        return analysis
    
    def _get_affected_entities(self, change_proposal: Dict[str, Any]) -> List[AffectedEntity]:
        """
        Get all entities that will be affected by the change.
        
        Args:
            change_proposal: The proposed change
            
        Returns:
            List of AffectedEntity objects
        """
        entities = []
        change_type = change_proposal.get('change_type', 'configuration')
        
        if change_type == 'configuration':
            entities.extend(self._get_affected_by_configuration(change_proposal))
        elif change_type == 'network':
            entities.extend(self._get_affected_by_network(change_proposal))
        elif change_type == 'device':
            entities.extend(self._get_affected_by_device(change_proposal))
        elif change_type == 'signal':
            entities.extend(self._get_affected_by_signal(change_proposal))
        elif change_type == 'topology':
            entities.extend(self._get_affected_by_topology(change_proposal))
        
        # Remove duplicates
        unique_entities = []
        seen_ids = set()
        for entity in entities:
            entity_id = f"{entity.entity_type}:{entity.entity_id}"
            if entity_id not in seen_ids:
                seen_ids.add(entity_id)
                unique_entities.append(entity)
        
        return unique_entities
    
    def _get_affected_by_configuration(self, change_proposal: Dict[str, Any]) -> List[AffectedEntity]:
        """Get entities affected by a configuration change"""
        entities = []
        device_id = change_proposal.get('device')
        parameter = change_proposal.get('parameter')
        
        if not device_id or not self.knowledge_graph:
            return entities
        
        # The device itself is affected
        entities.append(AffectedEntity(
            entity_id=device_id,
            entity_type='device',
            impact_scope=ImpactScope.DEVICE,
            impact_level='high',
            description=f"Configuration change on device {device_id}"
        ))
        
        # Get device info
        device = self.knowledge_graph.get_device(device_id)
        if not device:
            return entities
        
        device_type = device.get('type', 'unknown')
        
        # For gateways, configuration changes often affect signal mappings
        if device_type.lower() == 'gateway':
            # Get all signals that pass through this gateway
            signals = self.knowledge_graph.get_signals_through_device(device_id)
            for signal in signals:
                entities.append(AffectedEntity(
                    entity_id=signal,
                    entity_type='signal',
                    impact_scope=ImpactScope.SIGNAL,
                    impact_level='medium',
                    description=f"Signal {signal} may be affected by gateway configuration"
                ))
            
            # Get all connections to/from this gateway
            connections = self.knowledge_graph.get_device_connections(device_id)
            for conn in connections:
                other_device = conn['to'] if conn['from'] == device_id else conn['from']
                entities.append(AffectedEntity(
                    entity_id=f"{device_id}:{other_device}",
                    entity_type='connection',
                    impact_scope=ImpactScope.CONNECTION,
                    impact_level='medium',
                    description=f"Connection between {device_id} and {other_device} may be affected"
                ))
        
        # For switches, configuration changes often affect network connectivity
        if device_type.lower() == 'switch':
            # Get all devices connected to this switch
            connected_devices = self.knowledge_graph.get_connected_devices(device_id)
            for conn_device in connected_devices:
                entities.append(AffectedEntity(
                    entity_id=conn_device,
                    entity_type='device',
                    impact_scope=ImpactScope.DEVICE,
                    impact_level='medium',
                    description=f"Device {conn_device} may be affected by switch configuration"
                ))
                
                # Get signals from this device
                signals = self.knowledge_graph.get_device_signals(conn_device)
                for signal in signals:
                    entities.append(AffectedEntity(
                        entity_id=signal,
                        entity_type='signal',
                        impact_scope=ImpactScope.SIGNAL,
                        impact_level='medium',
                        description=f"Signal {signal} from {conn_device} may be affected"
                    ))
        
        # For IEDs, configuration changes affect their signals
        if device_type.lower() == 'ied':
            signals = self.knowledge_graph.get_device_signals(device_id)
            for signal in signals:
                entities.append(AffectedEntity(
                    entity_id=signal,
                    entity_type='signal',
                    impact_scope=ImpactScope.SIGNAL,
                    impact_level='high',
                    description=f"Signal {signal} from IED {device_id} may be affected"
                ))
        
        return entities
    
    def _get_affected_by_network(self, change_proposal: Dict[str, Any]) -> List[AffectedEntity]:
        """Get entities affected by a network change"""
        entities = []
        device_id = change_proposal.get('device')
        parameter = change_proposal.get('parameter')
        new_value = change_proposal.get('new_value')
        
        if not device_id or not self.knowledge_graph:
            return entities
        
        # The device itself is affected
        entities.append(AffectedEntity(
            entity_id=device_id,
            entity_type='device',
            impact_scope=ImpactScope.DEVICE,
            impact_level='high',
            description=f"Network change on device {device_id}"
        ))
        
        # For VLAN changes
        if parameter == 'vlan':
            # Get all devices in the same VLAN or that will be affected
            current_vlan = self.knowledge_graph.get_device_vlan(device_id)
            new_vlan = new_value
            
            # Devices in current VLAN may be affected
            devices_in_vlan = self.knowledge_graph.get_devices_in_vlan(current_vlan)
            for vlan_device in devices_in_vlan:
                if vlan_device != device_id:
                    entities.append(AffectedEntity(
                        entity_id=vlan_device,
                        entity_type='device',
                        impact_scope=ImpactScope.DEVICE,
                        impact_level='medium',
                        description=f"Device {vlan_device} in same VLAN may be affected"
                    ))
            
            # Devices in new VLAN may be affected
            if new_vlan:
                devices_in_new_vlan = self.knowledge_graph.get_devices_in_vlan(new_vlan)
                for new_vlan_device in devices_in_new_vlan:
                    entities.append(AffectedEntity(
                        entity_id=new_vlan_device,
                        entity_type='device',
                        impact_scope=ImpactScope.DEVICE,
                        impact_level='medium',
                        description=f"Device {new_vlan_device} in new VLAN may be affected"
                    ))
        
        # For IP address changes
        if parameter == 'ip':
            # Get all devices that communicate with this device
            communicating_devices = self.knowledge_graph.get_communicating_devices(device_id)
            for comm_device in communicating_devices:
                entities.append(AffectedEntity(
                    entity_id=comm_device,
                    entity_type='device',
                    impact_scope=ImpactScope.DEVICE,
                    impact_level='high',
                    description=f"Device {comm_device} communicates with {device_id}"
                ))
                
                # Get connections between devices
                entities.append(AffectedEntity(
                    entity_id=f"{device_id}:{comm_device}",
                    entity_type='connection',
                    impact_scope=ImpactScope.CONNECTION,
                    impact_level='high',
                    description=f"Connection between {device_id} and {comm_device} will be affected"
                ))
        
        return entities
    
    def _get_affected_by_device(self, change_proposal: Dict[str, Any]) -> List[AffectedEntity]:
        """Get entities affected by a device change (e.g., replacement)"""
        entities = []
        device_id = change_proposal.get('device')
        action = change_proposal.get('action', 'replace')
        
        if not device_id or not self.knowledge_graph:
            return entities
        
        # The device itself is affected
        entities.append(AffectedEntity(
            entity_id=device_id,
            entity_type='device',
            impact_scope=ImpactScope.DEVICE,
            impact_level='critical',
            description=f"Device {device_id} is being {action}ed"
        ))
        
        # Get all signals from this device
        signals = self.knowledge_graph.get_device_signals(device_id)
        for signal in signals:
            entities.append(AffectedEntity(
                entity_id=signal,
                entity_type='signal',
                impact_scope=ImpactScope.SIGNAL,
                impact_level='high',
                description=f"Signal {signal} from device {device_id} will be affected"
            ))
        
        # Get all connections to/from this device
        connections = self.knowledge_graph.get_device_connections(device_id)
        for conn in connections:
            other_device = conn['to'] if conn['from'] == device_id else conn['from']
            entities.append(AffectedEntity(
                entity_id=other_device,
                entity_type='device',
                impact_scope=ImpactScope.DEVICE,
                impact_level='high',
                description=f"Device {other_device} connected to {device_id} may be affected"
            ))
            
            entities.append(AffectedEntity(
                entity_id=f"{device_id}:{other_device}",
                entity_type='connection',
                impact_scope=ImpactScope.CONNECTION,
                impact_level='high',
                description=f"Connection between {device_id} and {other_device} will be affected"
            ))
        
        return entities
    
    def _get_affected_by_signal(self, change_proposal: Dict[str, Any]) -> List[AffectedEntity]:
        """Get entities affected by a signal change"""
        entities = []
        signal_name = change_proposal.get('signal')
        device_id = change_proposal.get('device')
        
        if not signal_name or not self.knowledge_graph:
            return entities
        
        # The signal itself is affected
        entities.append(AffectedEntity(
            entity_id=signal_name,
            entity_type='signal',
            impact_scope=ImpactScope.SIGNAL,
            impact_level='high',
            description=f"Signal {signal_name} is being modified"
        ))
        
        # Get the device that publishes this signal
        if device_id:
            entities.append(AffectedEntity(
                entity_id=device_id,
                entity_type='device',
                impact_scope=ImpactScope.DEVICE,
                impact_level='high',
                description=f"Device {device_id} publishes signal {signal_name}"
            ))
        else:
            # Find devices that publish this signal
            publishing_devices = self.knowledge_graph.get_signal_publishers(signal_name)
            for pub_device in publishing_devices:
                entities.append(AffectedEntity(
                    entity_id=pub_device,
                    entity_type='device',
                    impact_scope=ImpactScope.DEVICE,
                    impact_level='high',
                    description=f"Device {pub_device} publishes signal {signal_name}"
                ))
        
        # Get the path of this signal
        signal_path = self.knowledge_graph.get_signal_path(
            signal=signal_name,
            destination='SCADA'
        )
        
        if signal_path:
            for i in range(len(signal_path) - 1):
                from_device = signal_path[i]
                to_device = signal_path[i + 1]
                
                entities.append(AffectedEntity(
                    entity_id=to_device,
                    entity_type='device',
                    impact_scope=ImpactScope.DEVICE,
                    impact_level='medium',
                    description=f"Device {to_device} is in the path of signal {signal_name}"
                ))
                
                entities.append(AffectedEntity(
                    entity_id=f"{from_device}:{to_device}",
                    entity_type='connection',
                    impact_scope=ImpactScope.CONNECTION,
                    impact_level='medium',
                    description=f"Connection between {from_device} and {to_device} carries signal {signal_name}"
                ))
        
        return entities
    
    def _get_affected_by_topology(self, change_proposal: Dict[str, Any]) -> List[AffectedEntity]:
        """Get entities affected by a topology change"""
        entities = []
        action = change_proposal.get('action', 'add')
        device_id = change_proposal.get('device')
        
        if action == 'add':
            # New device being added
            if device_id:
                entities.append(AffectedEntity(
                    entity_id=device_id,
                    entity_type='device',
                    impact_scope=ImpactScope.DEVICE,
                    impact_level='high',
                    description=f"New device {device_id} is being added"
                ))
        
        elif action == 'remove':
            # Device being removed
            if device_id and self.knowledge_graph:
                # All signals from this device
                signals = self.knowledge_graph.get_device_signals(device_id)
                for signal in signals:
                    entities.append(AffectedEntity(
                        entity_id=signal,
                        entity_type='signal',
                        impact_scope=ImpactScope.SIGNAL,
                        impact_level='critical',
                        description=f"Signal {signal} will be lost when device {device_id} is removed"
                    ))
                
                # All connections to/from this device
                connections = self.knowledge_graph.get_device_connections(device_id)
                for conn in connections:
                    other_device = conn['to'] if conn['from'] == device_id else conn['from']
                    entities.append(AffectedEntity(
                        entity_id=other_device,
                        entity_type='device',
                        impact_scope=ImpactScope.DEVICE,
                        impact_level='high',
                        description=f"Device {other_device} will lose connection to {device_id}"
                    ))
        
        return entities
    
    def _generate_potential_issues(
        self, 
        change_proposal: Dict[str, Any], 
        affected_entities: List[AffectedEntity]
    ) -> List[Dict[str, Any]]:
        """Generate potential issues based on affected entities"""
        issues = []
        change_type = change_proposal.get('change_type', 'configuration')
        
        # Count affected entities by type
        device_count = sum(1 for e in affected_entities if e.entity_type == 'device')
        signal_count = sum(1 for e in affected_entities if e.entity_type == 'signal')
        connection_count = sum(1 for e in affected_entities if e.entity_type == 'connection')
        
        # Communication issues
        if connection_count > 0:
            issues.append({
                'type': 'communication_failure',
                'severity': 'high' if connection_count > 2 else 'medium',
                'description': f"Potential communication failure affecting {connection_count} connections",
                'affected_connections': connection_count,
                'recommendation': 'Verify all connections after change'
            })
        
        # Signal loss issues
        if signal_count > 0:
            issues.append({
                'type': 'signal_loss',
                'severity': 'high' if signal_count > 3 else 'medium',
                'description': f"Potential signal loss affecting {signal_count} signals",
                'affected_signals': signal_count,
                'recommendation': 'Verify all signals are properly mapped'
            })
        
        # Device compatibility issues
        if change_type == 'device':
            new_device = change_proposal.get('new_device')
            if new_device:
                issues.append({
                    'type': 'device_compatibility',
                    'severity': 'medium',
                    'description': f"Potential compatibility issues with new device {new_device}",
                    'recommendation': 'Verify compatibility with existing devices'
                })
        
        # Configuration issues
        if change_type == 'configuration':
            device_id = change_proposal.get('device')
            parameter = change_proposal.get('parameter')
            
            if device_id and self.knowledge_graph:
                device = self.knowledge_graph.get_device(device_id)
                if device:
                    device_type = device.get('type', 'unknown')
                    
                    if device_type.lower() == 'gateway':
                        issues.append({
                            'type': 'configuration_error',
                            'severity': 'high',
                            'description': f"Gateway configuration change may affect multiple signals",
                            'recommendation': 'Test all signal paths through this gateway'
                        })
                    
                    if parameter == 'vlan':
                        issues.append({
                            'type': 'network_isolation',
                            'severity': 'medium',
                            'description': 'VLAN change may isolate devices',
                            'recommendation': 'Verify all devices can still communicate'
                        })
        
        # Network issues
        if change_type == 'network':
            parameter = change_proposal.get('parameter')
            
            if parameter == 'ip':
                issues.append({
                    'type': 'ip_conflict',
                    'severity': 'medium',
                    'description': 'IP address change may cause conflicts',
                    'recommendation': 'Verify new IP address is not already in use'
                })
            
            if parameter == 'vlan':
                issues.append({
                    'type': 'vlan_mismatch',
                    'severity': 'medium',
                    'description': 'VLAN change may cause mismatches with connected devices',
                    'recommendation': 'Verify all connected devices are in the correct VLAN'
                })
        
        return issues
    
    def _calculate_impact_level(
        self, 
        device_count: int, 
        signal_count: int, 
        connection_count: int
    ) -> Any:
        """Calculate the overall impact level"""
        from .engine import ImpactLevel
        
        total_affected = device_count + signal_count + connection_count
        
        for level, (min_val, max_val) in self.IMPACT_LEVELS.items():
            if min_val <= total_affected <= max_val:
                return ImpactLevel(level)
        
        return ImpactLevel.NONE
    
    def _calculate_confidence(
        self, 
        change_proposal: Dict[str, Any], 
        affected_entities: List[AffectedEntity]
    ) -> float:
        """Calculate confidence in the impact prediction"""
        # Base confidence
        confidence = 0.7
        
        # Higher confidence for configuration changes
        if change_proposal.get('change_type') == 'configuration':
            confidence += 0.1
        
        # Higher confidence when we have knowledge graph
        if self.knowledge_graph:
            confidence += 0.1
        
        # Higher confidence with more affected entities (we understand the impact better)
        if len(affected_entities) > 5:
            confidence += 0.05
        
        # Cap at 0.95
        return min(confidence, 0.95)
