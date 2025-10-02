from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from datetime import datetime, timedelta

from models.schemas import (
    SustainabilityMetrics, GreenSchedulingRequest, GreenSchedulingResponse
)
from services.carbon_tracker import carbon_tracker

router = APIRouter()

@router.get("/metrics", response_model=SustainabilityMetrics)
async def get_sustainability_metrics():
    """Get current sustainability metrics"""
    
    try:
        metrics = carbon_tracker.get_sustainability_metrics()
        return SustainabilityMetrics(**metrics)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving sustainability metrics: {str(e)}")

@router.get("/metrics/history", response_model=List[Dict[str, Any]])
async def get_sustainability_history(days: int = 7):
    """Get sustainability metrics history"""
    
    try:
        # This would typically query historical data from a database
        # For now, return mock data
        history = []
        
        for i in range(days):
            date = datetime.now() - timedelta(days=i)
            # Mock historical data
            history.append({
                "date": date.isoformat(),
                "energy_consumed": 0.5 + (i * 0.1),
                "co2_emissions": 0.2 + (i * 0.05),
                "cache_hits": 10 + (i * 2),
                "green_scheduled_jobs": 5 + i
            })
        
        return history
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving sustainability history: {str(e)}")

@router.post("/schedule/green", response_model=GreenSchedulingResponse)
async def schedule_green_job(request: GreenSchedulingRequest):
    """Schedule a job for optimal low-carbon time"""
    
    try:
        # Check if green scheduling is enabled
        if not carbon_tracker.green_scheduling_enabled:
            # Schedule immediately if green scheduling is disabled
            scheduled_time = datetime.now()
            estimated_savings = 0.0
            is_green_scheduled = False
        else:
            # Check if current time is green
            if carbon_tracker.is_green_time():
                scheduled_time = datetime.now()
                estimated_savings = carbon_tracker.estimate_carbon_savings(request.estimated_duration)
                is_green_scheduled = True
            else:
                # Schedule for next green time
                scheduled_time = carbon_tracker.get_next_green_time()
                estimated_savings = carbon_tracker.estimate_carbon_savings(request.estimated_duration)
                is_green_scheduled = True
        
        # Generate job ID
        job_id = f"green_job_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Update green scheduled jobs count
        if is_green_scheduled:
            carbon_tracker.green_scheduled_jobs += 1
        
        return GreenSchedulingResponse(
            job_id=job_id,
            scheduled_time=scheduled_time,
            estimated_carbon_savings=estimated_savings,
            is_green_scheduled=is_green_scheduled
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scheduling green job: {str(e)}")

@router.get("/green/time", response_model=Dict[str, Any])
async def get_green_time_info():
    """Get information about green scheduling times"""
    
    try:
        current_hour = datetime.now().hour
        is_green_now = carbon_tracker.is_green_time()
        next_green_time = carbon_tracker.get_next_green_time()
        
        return {
            "current_hour": current_hour,
            "is_green_time_now": is_green_now,
            "next_green_time": next_green_time.isoformat(),
            "green_hours": list(carbon_tracker.low_carbon_hours),
            "green_scheduling_enabled": carbon_tracker.green_scheduling_enabled,
            "carbon_savings_percentage": carbon_tracker.green_scheduling_factor * 100
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving green time info: {str(e)}")

@router.get("/efficiency/tips", response_model=List[Dict[str, str]])
async def get_efficiency_tips():
    """Get tips for improving energy efficiency"""
    
    try:
        tips = [
            {
                "category": "Model Optimization",
                "tip": "Use smaller models like GPT-4o-mini instead of GPT-4 for 40-60% energy reduction",
                "impact": "High"
            },
            {
                "category": "Caching",
                "tip": "Implement intelligent caching to reuse previous generations and reduce inference calls by 30-50%",
                "impact": "High"
            },
            {
                "category": "Green Scheduling",
                "tip": "Schedule non-urgent jobs during low-carbon grid hours for up to 35% CO2 reduction",
                "impact": "Medium"
            },
            {
                "category": "Batch Processing",
                "tip": "Process multiple requests in batches to improve efficiency and reduce overhead",
                "impact": "Medium"
            },
            {
                "category": "Model Distillation",
                "tip": "Use quantized models (8-bit INT8) for additional energy savings without significant quality loss",
                "impact": "High"
            }
        ]
        
        return tips
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving efficiency tips: {str(e)}")

@router.get("/carbon/footprint", response_model=Dict[str, Any])
async def get_carbon_footprint():
    """Get detailed carbon footprint analysis"""
    
    try:
        metrics = carbon_tracker.get_sustainability_metrics()
        
        # Calculate additional metrics
        total_generations = carbon_tracker.generation_count
        cache_hit_rate = (carbon_tracker.cache_hits / total_generations * 100) if total_generations > 0 else 0
        
        # Estimate equivalent activities
        co2_kg = metrics["total_co2_emissions"]
        equivalent_activities = {
            "car_miles": co2_kg * 2.3,  # kg CO2 per mile
            "tree_days": co2_kg * 0.06,  # kg CO2 absorbed per tree per day
            "phone_charges": co2_kg * 1000,  # Rough estimate
            "lightbulb_hours": co2_kg * 50  # Rough estimate
        }
        
        return {
            "total_co2_emissions_kg": co2_kg,
            "total_energy_kwh": metrics["total_energy_consumed"],
            "carbon_intensity_kg_per_kwh": metrics["carbon_intensity"],
            "cache_hit_rate_percentage": cache_hit_rate,
            "green_scheduled_jobs": metrics["green_scheduled_jobs"],
            "equivalent_activities": equivalent_activities,
            "efficiency_score": min(100, max(0, 100 - (co2_kg * 10))),  # Simple efficiency score
            "recommendations": [
                "Enable green scheduling for better carbon efficiency",
                "Increase cache hit rate to reduce energy consumption",
                "Use smaller models for routine tasks"
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating carbon footprint: {str(e)}")

@router.post("/optimize", response_model=Dict[str, Any])
async def optimize_sustainability():
    """Run sustainability optimization recommendations"""
    
    try:
        current_metrics = carbon_tracker.get_sustainability_metrics()
        
        # Generate optimization recommendations
        recommendations = []
        
        if current_metrics["cache_hits"] < current_metrics["inference_reuse_count"] * 0.5:
            recommendations.append({
                "action": "improve_caching",
                "description": "Increase cache hit rate to reduce energy consumption",
                "priority": "high",
                "estimated_savings": "30-50%"
            })
        
        if not carbon_tracker.green_scheduling_enabled:
            recommendations.append({
                "action": "enable_green_scheduling",
                "description": "Enable green scheduling for low-carbon operations",
                "priority": "high",
                "estimated_savings": "35%"
            })
        
        if current_metrics["average_energy_per_generation"] > 0.002:
            recommendations.append({
                "action": "use_smaller_models",
                "description": "Switch to smaller models for routine tasks",
                "priority": "medium",
                "estimated_savings": "40-60%"
            })
        
        return {
            "current_metrics": current_metrics,
            "recommendations": recommendations,
            "optimization_status": "completed",
            "next_review_date": (datetime.now() + timedelta(days=7)).isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error running sustainability optimization: {str(e)}")
