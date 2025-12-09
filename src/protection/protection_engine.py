"""
Phone Protection Engine Module
Scans apps and monitors phone health
"""

from datetime import datetime
from typing import Dict, List, Optional
from src.types import AppInfo, AppScanResult, PhoneHealthReport


class ProtectionEngine:
    """
    Monitors app security, battery usage, phone health, and suggests optimizations.
    Protects the phone from malware and resource-draining apps.
    """
    
    def __init__(self):
        self.installed_apps: Dict[str, AppInfo] = {}
        self.scan_results: Dict[str, AppScanResult] = {}
        self.blocked_apps: List[str] = []
        
        # Risk database
        self.known_malware_signatures = self._init_malware_signatures()
        self.risky_permission_patterns = self._init_risky_patterns()
        
        # Phone health metrics
        self.last_health_check: Optional[datetime] = None
        self.health_history: List[PhoneHealthReport] = []
    
    def _init_malware_signatures(self) -> Dict[str, str]:
        """Initialize known malware signatures"""
        return {
            # This would contain actual malware signatures in production
            "trojan_sample_1": "trojan.banking.variant_a",
            "ransomware_sample_1": "ransomware.locky.variant",
        }
    
    def _init_risky_patterns(self) -> List[List[str]]:
        """Initialize risky permission patterns"""
        return [
            # High-risk patterns
            ["android.permission.READ_CONTACTS", 
             "android.permission.INTERNET",
             "android.permission.SEND_SMS"],
            
            ["android.permission.ACCESS_FINE_LOCATION",
             "android.permission.CAMERA",
             "android.permission.RECORD_AUDIO"],
            
            ["android.permission.READ_SMS",
             "android.permission.READ_CALL_LOG",
             "android.permission.SEND_SMS"],
        ]
    
    def register_app(self, app: AppInfo):
        """Register installed app"""
        self.installed_apps[app.package_name] = app
    
    def scan_app(self, package_name: str) -> AppScanResult:
        """Scan app for security risks"""
        if package_name not in self.installed_apps:
            return None
        
        app = self.installed_apps[package_name]
        
        # Perform security checks
        risk_level = "safe"
        issues = []
        recommendations = []
        
        # Check for risky permission patterns
        for pattern in self.risky_permission_patterns:
            if all(perm in app.permissions_requested for perm in pattern):
                risk_level = "dangerous"
                issues.append(f"Suspicious permission combination: {', '.join(pattern[:2])}")
        
        # Check for high battery usage
        battery_impact = self._estimate_battery_impact(app)
        if battery_impact == "high":
            risk_level = "warning" if risk_level == "safe" else risk_level
            issues.append("High battery consumption detected")
            recommendations.append("Consider limiting background activity")
        
        # Check if system app (usually safe)
        if app.is_system_app:
            risk_level = "safe"
        
        result = AppScanResult(
            app=app,
            risk_level=risk_level,
            issues=issues,
            recommendations=recommendations,
            battery_impact=battery_impact
        )
        
        self.scan_results[package_name] = result
        return result
    
    def _estimate_battery_impact(self, app: AppInfo) -> str:
        """Estimate app's battery impact"""
        # Based on usage time and permissions
        if app.usage_time_minutes > 300:  # >5 hours
            return "high"
        elif app.usage_time_minutes > 60:  # >1 hour
            return "medium"
        else:
            return "low"
    
    def scan_all_apps(self) -> List[AppScanResult]:
        """Scan all installed apps"""
        results = []
        for package_name in self.installed_apps:
            result = self.scan_app(package_name)
            if result:
                results.append(result)
        return results
    
    def get_risky_apps(self) -> List[AppScanResult]:
        """Get list of risky apps"""
        return [r for r in self.scan_results.values() 
                if r.risk_level in ["warning", "dangerous"]]
    
    def get_battery_intensive_apps(self) -> List[AppScanResult]:
        """Get battery-intensive apps"""
        return [r for r in self.scan_results.values()
                if r.battery_impact == "high"]
    
    def check_phone_health(self, metrics: Dict[str, float]) -> PhoneHealthReport:
        """Check overall phone health"""
        health = PhoneHealthReport(
            timestamp=datetime.now(),
            cpu_usage_percent=metrics.get("cpu_usage", 0),
            memory_usage_percent=metrics.get("memory_usage", 0),
            storage_usage_percent=metrics.get("storage_usage", 0),
            battery_percent=metrics.get("battery", 100),
            temperature_celsius=metrics.get("temperature", 35),
            running_processes=metrics.get("running_processes", 0),
            background_apps=metrics.get("background_apps", 0),
            problematic_apps=[],
            optimization_suggestions=[]
        )
        
        # Check for problems
        if health.cpu_usage_percent > 80:
            health.problematic_apps = [
                r.app.display_name for r in self.get_battery_intensive_apps()
            ]
            health.optimization_suggestions.append("CPU usage is high. Close unnecessary apps.")
        
        if health.memory_usage_percent > 85:
            health.optimization_suggestions.append("Low memory. Clear cache or restart phone.")
        
        if health.storage_usage_percent > 90:
            health.optimization_suggestions.append("Storage almost full. Delete unnecessary files.")
        
        if health.temperature_celsius > 40:
            health.optimization_suggestions.append("Phone is overheating. Let it cool down.")
        
        # Check risky apps
        risky = self.get_risky_apps()
        if risky:
            health.problematic_apps.extend([r.app.display_name for r in risky])
            health.optimization_suggestions.append(f"Found {len(risky)} risky apps. Review security.")
        
        self.health_history.append(health)
        self.last_health_check = datetime.now()
        
        return health
    
    def alert_about_app(self, package_name: str) -> Optional[Dict[str, any]]:
        """Get alert information about specific app"""
        if package_name not in self.scan_results:
            return None
        
        result = self.scan_results[package_name]
        
        if result.risk_level == "safe":
            return None
        
        return {
            "app_name": result.app.display_name,
            "risk_level": result.risk_level,
            "issues": result.issues,
            "recommendations": result.recommendations,
            "action_required": result.risk_level == "dangerous"
        }
    
    def block_app(self, package_name: str):
        """Block app from running (simulated)"""
        if package_name not in self.blocked_apps:
            self.blocked_apps.append(package_name)
    
    def unblock_app(self, package_name: str):
        """Unblock app"""
        if package_name in self.blocked_apps:
            self.blocked_apps.remove(package_name)
    
    def get_protection_status(self) -> Dict[str, any]:
        """Get protection engine status"""
        risky = self.get_risky_apps()
        battery_intensive = self.get_battery_intensive_apps()
        
        return {
            "total_apps_scanned": len(self.scan_results),
            "risky_apps_count": len(risky),
            "battery_intensive_apps": len(battery_intensive),
            "blocked_apps": len(self.blocked_apps),
            "risky_apps": [
                {
                    "name": r.app.display_name,
                    "risk": r.risk_level,
                    "issues": r.issues[:2]  # Top 2 issues
                }
                for r in risky[:5]  # Top 5 risky
            ],
            "last_health_check": self.last_health_check.isoformat() if self.last_health_check else None
        }
