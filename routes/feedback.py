from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from datetime import datetime

from models.schemas import (
    FeedbackRequest, FeedbackResponse
)
from services.database import db
from services.channel_service import channel_service
from services.carbon_tracker import carbon_tracker
from services.business_metrics import business_metrics_service
from services.recommendation_engine import recommendation_engine

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

# Business Metrics Endpoints
@router.post("/campaign/{campaign_id}/track")
async def track_campaign_performance(
    campaign_id: str,
    ad_id: str,
    channel: str,
    impressions: int,
    clicks: int,
    conversions: int,
    spend: float,
    revenue: float = 0.0
):
    """Track campaign performance metrics"""
    
    try:
        business_metrics_service.track_campaign_performance(
            campaign_id=campaign_id,
            ad_id=ad_id,
            channel=channel,
            impressions=impressions,
            clicks=clicks,
            conversions=conversions,
            spend=spend,
            revenue=revenue
        )
        
        return {"message": "Campaign performance tracked successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error tracking campaign performance: {str(e)}")

@router.get("/campaign/{campaign_id}/roi")
async def get_campaign_roi(campaign_id: str):
    """Get ROI metrics for a campaign"""
    
    try:
        metrics = business_metrics_service.calculate_roi_metrics(campaign_id)
        if not metrics:
            raise HTTPException(status_code=404, detail="Campaign not found")
        
        return metrics
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting campaign ROI: {str(e)}")

@router.get("/brand/{brand_id}/performance")
async def get_brand_performance(brand_id: str):
    """Get overall performance metrics for a brand"""
    
    try:
        performance = business_metrics_service.get_brand_performance(brand_id)
        return performance
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting brand performance: {str(e)}")

@router.get("/channels/performance")
async def get_channel_performance():
    """Get performance metrics by channel"""
    
    try:
        performance = business_metrics_service.get_channel_performance()
        return performance
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting channel performance: {str(e)}")

@router.get("/campaign/{campaign_id}/insights")
async def get_roi_insights(campaign_id: str):
    """Get ROI insights and recommendations for a campaign"""
    
    try:
        insights = business_metrics_service.get_roi_insights(campaign_id)
        return insights
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting ROI insights: {str(e)}")

# Recommendation Engine Endpoints
@router.post("/ad/{ad_id}/track")
async def track_ad_performance(
    ad_id: str,
    channel: str,
    audience_segment: str,
    impressions: int,
    clicks: int,
    conversions: int,
    revenue: float = 0.0,
    ad_attributes: Dict[str, Any] = None
):
    """Track ad performance for recommendation learning"""
    
    try:
        recommendation_engine.track_ad_performance(
            ad_id=ad_id,
            channel=channel,
            audience_segment=audience_segment,
            impressions=impressions,
            clicks=clicks,
            conversions=conversions,
            revenue=revenue,
            ad_attributes=ad_attributes
        )
        
        return {"message": "Ad performance tracked successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error tracking ad performance: {str(e)}")

@router.get("/recommendations/ads")
async def get_ad_recommendations(
    audience_segment: str,
    channel: str,
    limit: int = 5
):
    """Get ad recommendations for a specific audience segment and channel"""
    
    try:
        recommendations = recommendation_engine.get_recommendations(
            audience_segment=audience_segment,
            channel=channel,
            limit=limit
        )
        
        return {
            "audience_segment": audience_segment,
            "channel": channel,
            "recommendations": recommendations
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting ad recommendations: {str(e)}")

@router.get("/recommendations/channels")
async def get_channel_recommendations(audience_segment: str):
    """Get best channels for a specific audience segment"""
    
    try:
        recommendations = recommendation_engine.get_channel_recommendations(
            audience_segment=audience_segment
        )
        
        return {
            "audience_segment": audience_segment,
            "channel_recommendations": recommendations
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting channel recommendations: {str(e)}")

@router.get("/patterns/{audience_segment}")
async def get_successful_patterns(audience_segment: str):
    """Get successful ad patterns for an audience segment"""
    
    try:
        patterns = recommendation_engine.get_successful_patterns(audience_segment)
        
        return {
            "audience_segment": audience_segment,
            "patterns": patterns
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting successful patterns: {str(e)}")

@router.get("/insights/performance")
async def get_performance_insights():
    """Get overall performance insights"""
    
    try:
        insights = recommendation_engine.get_performance_insights()
        return insights
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting performance insights: {str(e)}")

@router.get("/insights/whats-working")
async def get_whats_working_summary():
    """Get summary of what's working across all campaigns"""
    
    try:
        summary = recommendation_engine.get_whats_working_summary()
        return summary
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting what's working summary: {str(e)}")
