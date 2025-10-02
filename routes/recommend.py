from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from datetime import datetime

from models.schemas import (
    ChannelRecommendationRequest, ChannelRecommendationResponse, ChannelRecommendation
)
from services.database import db
from services.channel_service import channel_service
from services.ai_service import ai_service
from services.carbon_tracker import carbon_tracker

router = APIRouter()

@router.post("/channel", response_model=ChannelRecommendationResponse)
async def recommend_channel(request: ChannelRecommendationRequest):
    """Recommend best ad channels based on brand, product, and audience"""
    
    try:
        # Track energy for this operation
        energy_data = carbon_tracker.track_generation("gpt-4o-mini", cache_hit=False)
        
        # Get brand data
        brand = await db.get_brand(request.brand_id)
        if not brand:
            raise HTTPException(status_code=404, detail="Brand not found")
        
        # Get product data
        products = await db.get_products_by_brand(request.brand_id)
        product = next((p for p in products if p['id'] == request.product_id), None)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Get audience data for the segment
        audience_data = await db.get_audience_by_brand(request.brand_id)
        segment_audience = [a for a in audience_data if a['segment'] == request.audience_segment]
        
        if not segment_audience:
            raise HTTPException(status_code=404, detail=f"No audience data found for segment: {request.audience_segment}")
        
        # Analyze audience segment
        audience_analysis = await ai_service.analyze_audience_segment(segment_audience)
        
        # Get channel recommendations
        recommendations = channel_service.recommend_channels(
            brand_data=brand,
            product_data=product,
            audience_analysis=audience_analysis,
            campaign_goal=request.campaign_goal,
            budget=request.budget
        )
        
        # Get best channel (highest confidence)
        best_channel = recommendations[0].channel if recommendations else None
        total_confidence = sum(rec.confidence_score for rec in recommendations) / len(recommendations) if recommendations else 0.0
        
        # Create response
        response_data = {
            "recommendations": [rec.dict() for rec in recommendations],
            "best_channel": best_channel,
            "total_confidence": total_confidence,
            "brand_id": request.brand_id,
            "product_id": request.product_id,
            "audience_segment": request.audience_segment,
            "campaign_goal": request.campaign_goal
        }
        
        # Store recommendation in database
        await db.create_channel_recommendation(response_data)
        
        return ChannelRecommendationResponse(**response_data)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error recommending channels: {str(e)}")

@router.get("/channel/brand/{brand_id}", response_model=List[ChannelRecommendationResponse])
async def get_channel_recommendations_by_brand(brand_id: str):
    """Get all channel recommendations for a brand"""
    
    try:
        recommendations = await db.get_channel_recommendations_by_brand(brand_id)
        return [ChannelRecommendationResponse(**rec) for rec in recommendations]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving channel recommendations: {str(e)}")

@router.post("/channel/optimize", response_model=ChannelRecommendationResponse)
async def optimize_channel_recommendations(
    brand_id: str,
    product_id: str,
    audience_segment: str,
    campaign_goal: str,
    budget: float = None
):
    """Optimize channel recommendations using multi-armed bandit learning"""
    
    try:
        # Get historical performance data
        # This would typically come from feedback data
        # For now, we'll use the existing recommendation logic
        
        request = ChannelRecommendationRequest(
            brand_id=brand_id,
            product_id=product_id,
            audience_segment=audience_segment,
            campaign_goal=campaign_goal,
            budget=budget
        )
        
        return await recommend_channel(request)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error optimizing channel recommendations: {str(e)}")

@router.get("/channel/performance/{channel}", response_model=Dict[str, Any])
async def get_channel_performance(channel: str):
    """Get performance statistics for a specific channel"""
    
    try:
        # Get channel performance from the service
        if hasattr(channel_service, 'channel_stats') and channel in channel_service.channel_stats:
            stats = channel_service.channel_stats[channel]
            total_attempts = stats.get('successes', 0) + stats.get('failures', 0)
            success_rate = stats.get('successes', 0) / total_attempts if total_attempts > 0 else 0
            
            return {
                "channel": channel,
                "total_attempts": total_attempts,
                "successes": stats.get('successes', 0),
                "failures": stats.get('failures', 0),
                "success_rate": success_rate,
                "confidence": success_rate  # Simplified confidence based on success rate
            }
        else:
            return {
                "channel": channel,
                "total_attempts": 0,
                "successes": 0,
                "failures": 0,
                "success_rate": 0.0,
                "confidence": 0.5  # Default confidence for new channels
            }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving channel performance: {str(e)}")

@router.post("/channel/learn", response_model=Dict[str, str])
async def learn_from_performance(
    channel: str,
    clicks: int,
    impressions: int,
    conversions: int
):
    """Update channel learning based on performance feedback"""
    
    try:
        # Update channel performance in the service
        from models.schemas import ChannelType
        
        try:
            channel_enum = ChannelType(channel)
            channel_service.update_channel_performance(
                channel=channel_enum,
                clicks=clicks,
                impressions=impressions,
                conversions=conversions
            )
            
            return {
                "status": "success",
                "message": f"Updated learning for {channel} channel",
                "ctr": clicks / impressions if impressions > 0 else 0,
                "conversion_rate": conversions / clicks if clicks > 0 else 0
            }
            
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid channel: {channel}")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating channel learning: {str(e)}")

@router.get("/channel/insights", response_model=Dict[str, Any])
async def get_channel_insights():
    """Get insights about channel performance across all campaigns"""
    
    try:
        # Get insights from channel service
        insights = {
            "total_channels": len(channel_service.channel_stats),
            "channel_performance": {},
            "top_performing_channel": None,
            "learning_insights": []
        }
        
        if channel_service.channel_stats:
            # Calculate performance for each channel
            for channel, stats in channel_service.channel_stats.items():
                total_attempts = stats.get('successes', 0) + stats.get('failures', 0)
                success_rate = stats.get('successes', 0) / total_attempts if total_attempts > 0 else 0
                
                insights["channel_performance"][channel] = {
                    "success_rate": success_rate,
                    "total_attempts": total_attempts,
                    "confidence": success_rate
                }
            
            # Find top performing channel
            if insights["channel_performance"]:
                top_channel = max(
                    insights["channel_performance"].items(),
                    key=lambda x: x[1]["success_rate"]
                )
                insights["top_performing_channel"] = {
                    "channel": top_channel[0],
                    "success_rate": top_channel[1]["success_rate"]
                }
        
        # Add learning insights
        insights["learning_insights"] = [
            "Multi-armed bandit learning is active",
            "Channel recommendations improve with more data",
            "Success rates are updated based on real performance"
        ]
        
        return insights
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving channel insights: {str(e)}")
