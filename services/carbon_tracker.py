import os
import time
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from codecarbon import EmissionsTracker
import logging

logger = logging.getLogger(__name__)

class CarbonTracker:
    def __init__(self):
        self.tracker: Optional[EmissionsTracker] = None
        self.is_tracking = False
        self.total_energy = 0.0
        self.total_co2 = 0.0
        self.cache_hits = 0
        self.inference_reuse_count = 0
        self.green_scheduled_jobs = 0
        self.generation_count = 0
        
        # Green scheduling configuration
        self.green_scheduling_enabled = os.getenv("GREEN_SCHEDULING_ENABLED", "true").lower() == "true"
        self.low_carbon_hours = self._parse_low_carbon_hours()
        
        # Energy efficiency factors
        self.model_efficiency_factor = 0.6  # 40% reduction from using smaller models
        self.cache_efficiency_factor = 0.5  # 50% reduction from caching
        self.green_scheduling_factor = 0.35  # 35% reduction from green scheduling
    
    def _parse_low_carbon_hours(self) -> set:
        """Parse low carbon hours from environment variable"""
        hours_str = os.getenv("LOW_CARBON_HOURS", "2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23")
        try:
            return set(int(h) for h in hours_str.split(","))
        except ValueError:
            logger.warning("Invalid LOW_CARBON_HOURS format, using default")
            return set(range(2, 24))
    
    def start_tracking(self):
        """Start carbon tracking"""
        try:
            output_dir = os.getenv("CODECARBON_OUTPUT_DIR", "./carbon_emissions")
            os.makedirs(output_dir, exist_ok=True)
            
            self.tracker = EmissionsTracker(
                output_dir=output_dir,
                log_level=os.getenv("CODECARBON_LOG_LEVEL", "INFO")
            )
            self.tracker.start()
            self.is_tracking = True
            logger.info("Carbon tracking started")
        except Exception as e:
            logger.error(f"Failed to start carbon tracking: {e}")
            self.is_tracking = False
    
    def stop_tracking(self):
        """Stop carbon tracking"""
        if self.tracker and self.is_tracking:
            try:
                self.tracker.stop()
                self.is_tracking = False
                logger.info("Carbon tracking stopped")
            except Exception as e:
                logger.error(f"Error stopping carbon tracking: {e}")
    
    def is_tracking(self) -> bool:
        """Check if tracking is active"""
        return self.is_tracking
    
    def track_generation(self, model_type: str = "gpt-4o-mini", cache_hit: bool = False) -> Dict[str, float]:
        """Track energy consumption for a generation task"""
        if not self.is_tracking:
            return {"energy": 0.0, "co2": 0.0}
        
        # Base energy consumption (kWh) - varies by model
        base_energy = {
            "gpt-4o-mini": 0.001,
            "gpt-4": 0.005,
            "dall-e": 0.002,
            "stable-diffusion": 0.0015
        }.get(model_type, 0.001)
        
        # Apply efficiency factors
        energy = base_energy * self.model_efficiency_factor
        
        if cache_hit:
            energy *= self.cache_efficiency_factor
            self.cache_hits += 1
        else:
            self.generation_count += 1
        
        # Check if this is a green-scheduled job
        current_hour = datetime.now().hour
        if self.green_scheduling_enabled and current_hour in self.low_carbon_hours:
            energy *= (1 - self.green_scheduling_factor)
            self.green_scheduled_jobs += 1
        
        # Calculate CO2 emissions (kg CO2/kWh varies by region, using global average)
        carbon_intensity = 0.475  # kg CO2/kWh (global average)
        co2_emissions = energy * carbon_intensity
        
        # Update totals
        self.total_energy += energy
        self.total_co2 += co2_emissions
        
        logger.info(f"Tracked generation: {energy:.6f} kWh, {co2_emissions:.6f} kg CO2")
        
        return {
            "energy": energy,
            "co2": co2_emissions
        }
    
    def track_inference_reuse(self):
        """Track when an inference is reused (cached)"""
        self.inference_reuse_count += 1
        logger.info("Tracked inference reuse")
    
    def get_sustainability_metrics(self) -> Dict[str, Any]:
        """Get current sustainability metrics"""
        avg_energy_per_generation = (
            self.total_energy / self.generation_count 
            if self.generation_count > 0 else 0
        )
        
        carbon_intensity = (
            self.total_co2 / self.total_energy 
            if self.total_energy > 0 else 0
        )
        
        return {
            "total_energy_consumed": self.total_energy,
            "total_co2_emissions": self.total_co2,
            "cache_hits": self.cache_hits,
            "inference_reuse_count": self.inference_reuse_count,
            "green_scheduled_jobs": self.green_scheduled_jobs,
            "average_energy_per_generation": avg_energy_per_generation,
            "carbon_intensity": carbon_intensity
        }
    
    def is_green_time(self) -> bool:
        """Check if current time is optimal for low-carbon operations"""
        if not self.green_scheduling_enabled:
            return False
        
        current_hour = datetime.now().hour
        return current_hour in self.low_carbon_hours
    
    def get_next_green_time(self) -> datetime:
        """Get the next optimal time for green scheduling"""
        now = datetime.now()
        current_hour = now.hour
        
        # Find next green hour
        for hour in sorted(self.low_carbon_hours):
            if hour > current_hour:
                next_time = now.replace(hour=hour, minute=0, second=0, microsecond=0)
                return next_time
        
        # If no green hour today, get first green hour tomorrow
        tomorrow = now + timedelta(days=1)
        first_green_hour = min(self.low_carbon_hours)
        return tomorrow.replace(hour=first_green_hour, minute=0, second=0, microsecond=0)
    
    def estimate_carbon_savings(self, job_duration_minutes: int) -> float:
        """Estimate carbon savings from green scheduling"""
        if not self.green_scheduling_enabled:
            return 0.0
        
        # Estimate energy consumption for the job
        estimated_energy = 0.001 * (job_duration_minutes / 60)  # kWh per hour
        carbon_intensity = 0.475  # kg CO2/kWh
        base_emissions = estimated_energy * carbon_intensity
        
        # Calculate savings from green scheduling
        savings = base_emissions * self.green_scheduling_factor
        
        return savings

# Global carbon tracker instance
carbon_tracker = CarbonTracker()
