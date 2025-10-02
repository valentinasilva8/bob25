from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from datetime import datetime

from models.schemas import (
    FeedbackRequest, FeedbackResponse
)
from services.database import db
from services.channel_service import channel_service
from services.carbon_tracker import carbon_tracker

router = APIRouter()

@router.post("/", response_model=FeedbackResponse)
async def submit_feedback(feedback_data: FeedbackRequest):
    """Submit performance feedback for an ad campaign"""
    
    try:
        # Verify ad exists
        ad = await db.get_ad(feedback_data.ad_id)
        if not ad:
            raise HTTPException(status_code=404, detail="Ad not found")
        
        # Calculate metrics
        ctr = feedback_data.clicks / feedback_data.impressions if feedback_data.impressions > 0 else 0
        conversion_rate = feedback_data.conversions / feedback_data.clicks if feedback_data.clicks > 0 else 0
        
        # Create feedback record
        feedback_dict = {
            "ad_id": feedback_data.ad_id,
            "channel": feedback_data.channel.value,
            "clicks": feedback_data.clicks,
            "impressions": feedback_data.impressions,
            "conversions": feedback_data.conversions,
            "spend": feedback_data.spend,
            "ctr": ctr,
            "conversion_rate": conversion_rate,
            "feedback_notes": feedback_data.feedback_notes,
            "created_at": datetime.now().isoformat()
        }
        
        # Store feedback in database
        result = await db.create_feedback(feedback_dict)
        if not result:
            raise HTTPException(status_code=500, detail="Failed to create feedback record")
        
        # Update channel learning
        channel_service.update_channel_performance(
            channel=feedback_data.channel,
            clicks=feedback_data.clicks,
            impressions=feedback_data.impressions,
            conversions=feedback_data.conversions
        )
        
        # Track energy for learning update
        energy_data = carbon_tracker.track_generation("gpt-4o-mini", cache_hit=False)
        
        return FeedbackResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error submitting feedback: {str(e)}")

@router.get("/ad/{ad_id}", response_model=List[FeedbackResponse])
async def get_feedback_by_ad(ad_id: str):
    """Get all feedback for a specific ad"""
    
    try:
        # This would require adding a method to get feedback by ad
        # For now, return empty list
        return []
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving feedback: {str(e)}")

@router.get("/channel/{channel}", response_model=List[FeedbackResponse])
async def get_feedback_by_channel(channel: str):
    """Get all feedback for a specific channel"""
    
    try:
        # This would require adding a method to get feedback by channel
        # For now, return empty list
        return []
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving feedback: {str(e)}")

@router.get("/performance/summary", response_model=Dict[str, Any])
async def get_performance_summary():
    """Get overall performance summary across all campaigns"""
    
    try:
        # This would aggregate performance data from all feedback
        # For now, return mock data
        return {
            "total_campaigns": 0,
            "total_clicks": 0,
            "total_impressions": 0,
            "total_conversions": 0,
            "total_spend": 0.0,
            "average_ctr": 0.0,
            "average_conversion_rate": 0.0,
            "top_performing_channel": None,
            "performance_trends": {
                "ctr_trend": "stable",
                "conversion_trend": "stable",
                "cost_trend": "stable"
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving performance summary: {str(e)}")

@router.post("/batch", response_model=List[FeedbackResponse])
async def submit_feedback_batch(feedback_list: list[FeedbackRequest]):
    """Submit multiple feedback records in batch"""
    
    try:
        results = []
        
        for feedback_data in feedback_list:
            try:
                feedback = await submit_feedback(feedback_data)
                results.append(feedback)
            except Exception as e:
                # Log error but continue with other feedback
                print(f"Error submitting feedback for ad {feedback_data.ad_id}: {e}")
                continue
        
        return results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error submitting feedback batch: {str(e)}")

@router.get("/insights", response_model=Dict[str, Any])
async def get_feedback_insights():
    """Get insights from feedback data"""
    
    try:
        # Get channel performance insights
        channel_insights = await get_channel_insights()
        
        # Get performance summary
        performance_summary = await get_performance_summary()
        
        # Combine insights
        insights = {
            "channel_insights": channel_insights,
            "performance_summary": performance_summary,
            "recommendations": [
                "Focus on channels with highest CTR",
                "Optimize ads for better conversion rates",
                "Consider budget reallocation based on performance"
            ],
            "learning_status": {
                "multi_armed_bandit": "active",
                "channel_optimization": "learning",
                "ad_personalization": "improving"
            }
        }
        
        return insights
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving feedback insights: {str(e)}")

async def get_channel_insights() -> Dict[str, Any]:
    """Get channel-specific insights"""
    
    try:
        insights = {
            "channel_performance": {},
            "top_performers": [],
            "improvement_opportunities": []
        }
        
        # Get channel performance from service
        if hasattr(channel_service, 'channel_stats'):
            for channel, stats in channel_service.channel_stats.items():
                total_attempts = stats.get('successes', 0) + stats.get('failures', 0)
                success_rate = stats.get('successes', 0) / total_attempts if total_attempts > 0 else 0
                
                insights["channel_performance"][channel] = {
                    "success_rate": success_rate,
                    "total_attempts": total_attempts,
                    "status": "performing_well" if success_rate > 0.1 else "needs_improvement"
                }
        
        return insights
        
    except Exception as e:
        return {"error": f"Error getting channel insights: {str(e)}"}
