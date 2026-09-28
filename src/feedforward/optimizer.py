"""
Configuration Optimizer for Substation by K

This module provides optimization suggestions for substation configurations
based on historical data, best practices, and performance metrics.
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


@dataclass
class OptimizationSuggestion:
    """A suggestion for optimizing the substation configuration"""
    suggestion_id: str
    category: str
    description: str
    affected_devices: List[str] = field(default_factory=list)
    affected_signals: List[str] = field(default_factory=list)
    current_value: Any = None
    suggested_value: Any = None
    impact: str = "medium"
    priority: int = 0
    confidence: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        result = {
            'suggestion_id': self.suggestion_id,
            'category': self.category,
            'description': self.description,
            'affected_devices': self.affected_devices,
            'affected_signals': self.affected_signals,
            'impact': self.impact,
            'priority': self.priority,
            'confidence': self.confidence
        }
        if self.current_value is not None:
            result['current_value'] = str(self.current_value)
        if self.suggested_value is not None:
            result['suggested_value'] = str(self.suggested_value)
        return result


class ConfigurationOptimizer:
    """
    Provides optimization suggestions for substation configurations.
    
    This class analyzes the current configuration and suggests improvements
    based on:
    - Historical performance data
    - Best practices
    - Industry standards
    - Device capabilities
    """
    
    # Best practices for different device types
    BEST_PRACTICES = {
        'gateway': {
            'max_connections': 50,
            'recommended_vlan': 100,
            'buffer_size': 1024,
            'timeout': 30
        },
        'switch': {
            'max_devices_per_vlan': 20,
            'recommended_mtu': 1500,
            'storm_control': True,
            'spanning_tree': True
        },
        'ied': {
            'goose_retry': 3,
            'goose_timeout': 1000,
            'mms_timeout': 5000,
            'sampled_values_timeout': 100
        }
    }
    
    # Common optimization categories
    OPTIMIZATION_CATEGORIES = [
        'performance',
        'reliability',
        'security',
        'maintainability',
        'cost'
    ]
    
    def __init__(self, knowledge_graph: Any = None, substation_memory: Any = None):
        """
        Initialize the configuration optimizer.
        
        Args:
            knowledge_graph: Knowledge graph for topology
            substation_memory: Substation Memory™ for historical data
        """
        self.knowledge_graph = knowledge_graph
        self.substation_memory = substation_memory
        logger.info("ConfigurationOptimizer initialized")
    
    def suggest_optimizations(self, current_state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Suggest optimizations for the current substation configuration.
        
        Args:
            current_state: Current state of the substation
            
        Returns:
            List of optimization suggestions
        """
        suggestions = []
        
        # Performance optimizations
        suggestions.extend(self._suggest_performance_optimizations(current_state))
        
        # Reliability optimizations
        suggestions.extend(self._suggest_reliability_optimizations(current_state))
        
        # Security optimizations
        suggestions.extend(self._suggest_security_optimizations(current_state))
        
        # Network optimizations
        suggestions.extend(self._suggest_network_optimizations(current_state))
        
        # Sort by priority
        suggestions.sort(key=lambda s: s['priority'], reverse=True)
        
        return [s.to_dict() for s in suggestions]
    
    def _suggest_performance_optimizations(
        self, 
        current_state: Dict[str, Any]
    ) -> List[OptimizationSuggestion]:
        """Suggest performance optimizations"""
        suggestions = []
        devices = current_state.get('devices', {})
        connections = current_state.get('connections', {})
        
        # Check for high latency connections
        for conn_id, conn in connections.items():
            latency = conn.get('latency', 0)
            if latency > 50:  # 50ms threshold
                from_device = conn.get('from')
                to_device = conn.get('to')
                
                suggestions.append(OptimizationSuggestion(
                    suggestion_id=f"perf_latency_{conn_id}",
                    category='performance',
                    description=f"High latency ({latency}ms) between {from_device} and {to_device}",
                    affected_devices=[from_device, to_device],
                    current_value=latency,
                    suggested_value="<50ms",
                    impact='high',
                    priority=8,
                    confidence=0.9
                ))
        
        # Check for devices with high resource usage
        for device_id, device in devices.items():
            cpu = device.get('cpu_usage', 0)
            memory = device.get('memory_usage', 0)
            
            if cpu > 80:
                suggestions.append(OptimizationSuggestion(
                    suggestion_id=f"perf_cpu_{device_id}",
                    category='performance',
                    description=f"High CPU usage ({cpu}%) on device {device_id}",
                    affected_devices=[device_id],
                    current_value=cpu,
                    suggested_value="<80%",
                    impact='high',
                    priority=7,
                    confidence=0.85
                ))
            
            if memory > 80:
                suggestions.append(OptimizationSuggestion(
                    suggestion_id=f"perf_mem_{device_id}",
                    category='performance',
                    description=f"High memory usage ({memory}%) on device {device_id}",
                    affected_devices=[device_id],
                    current_value=memory,
                    suggested_value="<80%",
                    impact='high',
                    priority=7,
                    confidence=0.85
                ))
        
        return suggestions
    
    def _suggest_reliability_optimizations(
        self, 
        current_state: Dict[str, Any]
    ) -> List[OptimizationSuggestion]:
        """Suggest reliability optimizations"""
        suggestions = []
        devices = current_state.get('devices', {})
        
        # Check for single points of failure
        if self.knowledge_graph:
            critical_devices = self.knowledge_graph.get_critical_devices()
            for device_id in critical_devices:
                device = devices.get(device_id)
                if device:
                    suggestions.append(OptimizationSuggestion(
                        suggestion_id=f"rel_redundancy_{device_id}",
                        category='reliability',
                        description=f"Add redundancy for critical device {device_id}",
                        affected_devices=[device_id],
                        impact='high',
                        priority=9,
                        confidence=0.8
                    ))
        
        # Check for devices without backup
        for device_id, device in devices.items():
            device_type = device.get('type', 'unknown')
            
            # Gateways and SCADA systems should have backups
            if device_type.lower() in ['gateway', 'scada']:
                has_backup = device.get('has_backup', False)
                if not has_backup:
                    suggestions.append(OptimizationSuggestion(
                        suggestion_id=f"rel_backup_{device_id}",
                        category='reliability',
                        description=f"Add backup for {device_type} {device_id}",
                        affected_devices=[device_id],
                        impact='high',
                        priority=8,
                        confidence=0.9
                    ))
        
        # Check GOOSE configuration
        for device_id, device in devices.items():
            if device.get('type', '').lower() == 'ied':
                goose_config = device.get('goose_config', {})
                retry = goose_config.get('retry', 3)
                timeout = goose_config.get('timeout', 1000)
                
                if retry < 3:
                    suggestions.append(OptimizationSuggestion(
                        suggestion_id=f"rel_goose_retry_{device_id}",
                        category='reliability',
                        description=f"Increase GOOSE retry count for {device_id}",
                        affected_devices=[device_id],
                        current_value=retry,
                        suggested_value=3,
                        impact='medium',
                        priority=6,
                        confidence=0.85
                    ))
                
                if timeout > 2000:
                    suggestions.append(OptimizationSuggestion(
                        suggestion_id=f"rel_goose_timeout_{device_id}",
                        category='reliability',
                        description=f"Reduce GOOSE timeout for {device_id}",
                        affected_devices=[device_id],
                        current_value=timeout,
                        suggested_value=1000,
                        impact='medium',
                        priority=6,
                        confidence=0.8
                    ))
        
        return suggestions
    
    def _suggest_security_optimizations(
        self, 
        current_state: Dict[str, Any]
    ) -> List[OptimizationSuggestion]:
        """Suggest security optimizations"""
        suggestions = []
        devices = current_state.get('devices', {})
        network = current_state.get('network', {})
        
        # Check for devices with default credentials
        for device_id, device in devices.items():
            credentials = device.get('credentials', {})
            username = credentials.get('username', '')
            password = credentials.get('password', '')
            
            if username in ['admin', 'default', 'user'] or password in ['password', 'admin', '1234', '']:
                suggestions.append(OptimizationSuggestion(
                    suggestion_id=f"sec_credentials_{device_id}",
                    category='security',
                    description=f"Change default credentials on {device_id}",
                    affected_devices=[device_id],
                    impact='critical',
                    priority=10,
                    confidence=0.95
                ))
        
        # Check for open ports
        for device_id, device in devices.items():
            open_ports = device.get('open_ports', [])
            
            # Common vulnerable ports
            vulnerable_ports = [23, 21, 22, 3389, 5900]
            
            for port in open_ports:
                if port in vulnerable_ports:
                    suggestions.append(OptimizationSuggestion(
                        suggestion_id=f"sec_port_{device_id}_{port}",
                        category='security',
                        description=f"Close or secure port {port} on {device_id}",
                        affected_devices=[device_id],
                        current_value=port,
                        suggested_value="closed",
                        impact='high',
                        priority=9,
                        confidence=0.9
                    ))
        
        # Check for VLAN segmentation
        vlan_devices = defaultdict(list)
        for device_id, device in devices.items():
            vlan = device.get('vlan')
            if vlan:
                vlan_devices[vlan].append(device_id)
        
        # Check for VLANs with too many devices
        for vlan, vlan_device_list in vlan_devices.items():
            if len(vlan_device_list) > 20:
                suggestions.append(OptimizationSuggestion(
                    suggestion_id=f"sec_vlan_{vlan}",
                    category='security',
                    description=f"VLAN {vlan} has too many devices ({len(vlan_device_list)})",
                    affected_devices=vlan_device_list,
                    current_value=len(vlan_device_list),
                    suggested_value="<20",
                    impact='medium',
                    priority=7,
                    confidence=0.8
                ))
        
        return suggestions
    
    def _suggest_network_optimizations(
        self, 
        current_state: Dict[str, Any]
    ) -> List[OptimizationSuggestion]:
        """Suggest network optimizations"""
        suggestions = []
        devices = current_state.get('devices', {})
        connections = current_state.get('connections', {})
        network = current_state.get('network', {})
        
        # Check for unused VLANs
        used_vlans = set()
        for device in devices.values():
            vlan = device.get('vlan')
            if vlan:
                used_vlans.add(vlan)
        
        configured_vlans = network.get('vlans', [])
        for vlan in configured_vlans:
            if vlan not in used_vlans:
                suggestions.append(OptimizationSuggestion(
                    suggestion_id=f"net_vlan_unused_{vlan}",
                    category='network',
                    description=f"Remove unused VLAN {vlan}",
                    current_value=vlan,
                    suggested_value="removed",
                    impact='low',
                    priority=4,
                    confidence=0.85
                ))
        
        # Check for devices without VLAN assignment
        for device_id, device in devices.items():
            if not device.get('vlan') and device.get('type', '').lower() not in ['scada', 'rtu']:
                suggestions.append(OptimizationSuggestion(
                    suggestion_id=f"net_vlan_missing_{device_id}",
                    category='network',
                    description=f"Assign VLAN to device {device_id}",
                    affected_devices=[device_id],
                    impact='medium',
                    priority=6,
                    confidence=0.8
                ))
        
        # Check for redundant connections
        connection_pairs = set()
        redundant_connections = []
        
        for conn_id, conn in connections.items():
            from_device = conn.get('from')
            to_device = conn.get('to')
            
            # Normalize the pair (sort to avoid direction issues)
            pair = tuple(sorted([from_device, to_device]))
            
            if pair in connection_pairs:
                redundant_connections.append(conn_id)
            else:
                connection_pairs.add(pair)
        
        for conn_id in redundant_connections:
            conn = connections[conn_id]
            from_device = conn.get('from')
            to_device = conn.get('to')
            
            suggestions.append(OptimizationSuggestion(
                suggestion_id=f"net_redundant_{conn_id}",
                category='network',
                description=f"Remove redundant connection between {from_device} and {to_device}",
                affected_devices=[from_device, to_device],
                current_value=conn_id,
                suggested_value="removed",
                impact='low',
                priority=4,
                confidence=0.7
            ))
        
        return suggestions
    
    def optimize_signal_paths(self, current_state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Optimize signal paths for better performance and reliability.
        
        Args:
            current_state: Current state of the substation
            
        Returns:
            List of signal path optimization suggestions
        """
        suggestions = []
        signals = current_state.get('signals', {})
        
        for signal_id, signal in signals.items():
            # Check for signals with long paths
            path = signal.get('path', [])
            if len(path) > 5:  # More than 5 hops
                suggestions.append(OptimizationSuggestion(
                    suggestion_id=f"path_short_{signal_id}",
                    category='network',
                    description=f"Signal {signal_id} has a long path ({len(path)} hops)",
                    affected_signals=[signal_id],
                    current_value=len(path),
                    suggested_value="<5 hops",
                    impact='medium',
                    priority=6,
                    confidence=0.75
                ))
            
            # Check for signals with high latency
            latency = signal.get('latency', 0)
            if latency > 100:  # 100ms threshold
                suggestions.append(OptimizationSuggestion(
                    suggestion_id=f"path_latency_{signal_id}",
                    category='performance',
                    description=f"Signal {signal_id} has high latency ({latency}ms)",
                    affected_signals=[signal_id],
                    current_value=latency,
                    suggested_value="<100ms",
                    impact='medium',
                    priority=7,
                    confidence=0.8
                ))
        
        return [s.to_dict() for s in suggestions]
    
    def get_device_optimizations(self, device_id: str) -> List[Dict[str, Any]]:
        """
        Get optimization suggestions for a specific device.
        
        Args:
            device_id: ID of the device to optimize
            
        Returns:
            List of optimization suggestions for the device
        """
        if not self.knowledge_graph:
            return []
        
        device = self.knowledge_graph.get_device(device_id)
        if not device:
            return []
        
        suggestions = []
        device_type = device.get('type', 'unknown').lower()
        configuration = device.get('configuration', {})
        
        # Check against best practices
        best_practices = self.BEST_PRACTICES.get(device_type, {})
        
        for param, recommended_value in best_practices.items():
            current_value = configuration.get(param)
            
            if current_value is not None and current_value != recommended_value:
                suggestions.append(OptimizationSuggestion(
                    suggestion_id=f"dev_{device_id}_{param}",
                    category='configuration',
                    description=f"Update {param} on {device_id} to best practice value",
                    affected_devices=[device_id],
                    current_value=current_value,
                    suggested_value=recommended_value,
                    impact='medium',
                    priority=5,
                    confidence=0.85
                ))
        
        return [s.to_dict() for s in suggestions]
    
    def analyze_historical_patterns(self) -> List[Dict[str, Any]]:
        """
        Analyze historical patterns to suggest optimizations.
        
        Returns:
            List of optimization suggestions based on historical data
        """
        if not self.substation_memory:
            return []
        
        suggestions = []
        
        try:
            # Get frequent failures
            frequent_failures = self.substation_memory.get_frequent_failures(limit=10)
            
            for failure in frequent_failures:
                device_id = failure.get('device_id')
                failure_type = failure.get('failure_type')
                count = failure.get('count', 0)
                
                if count > 3:  # More than 3 failures
                    suggestions.append(OptimizationSuggestion(
                        suggestion_id=f"hist_{device_id}_{failure_type}",
                        category='reliability',
                        description=f"Address frequent {failure_type} failures on {device_id} ({count} occurrences)",
                        affected_devices=[device_id],
                        current_value=count,
                        suggested_value="0",
                        impact='high',
                        priority=9,
                        confidence=0.9
                    ))
            
            # Get devices with frequent configuration changes
            frequent_changes = self.substation_memory.get_frequent_configuration_changes(limit=10)
            
            for change in frequent_changes:
                device_id = change.get('device_id')
                parameter = change.get('parameter')
                count = change.get('count', 0)
                
                if count > 5:  # More than 5 changes
                    suggestions.append(OptimizationSuggestion(
                        suggestion_id=f"hist_config_{device_id}_{parameter}",
                        category='maintainability',
                        description=f"Stabilize configuration for {parameter} on {device_id} ({count} changes)",
                        affected_devices=[device_id],
                        current_value=count,
                        suggested_value="<3",
                        impact='medium',
                        priority=7,
                        confidence=0.8
                    ))
            
        except Exception as e:
            logger.error(f"Error analyzing historical patterns: {e}")
        
        return [s.to_dict() for s in suggestions]
