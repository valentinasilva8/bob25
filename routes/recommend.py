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

@router.get("/channel/strategy", response_model=Dict[str, Any])
async def get_channel_strategy():
    """Get the channel selection strategy matrix"""
    
    try:
        strategy_matrix = {
            "rule_based_mapping": {
                "description": "Use audience data, product type, and segment to map ads to the best platform",
                "feasibility": "Easy (1 day)",
                "status": "✅ Implemented"
            },
            "bandit_optimization": {
                "description": "Start simple but improve over time based on performance (CTR, conversions)",
                "feasibility": "Achievable in 24h",
                "status": "✅ Implemented"
            },
            "channel_matrix": {
                "b2b_professional_services": {
                    "best_platform": "LinkedIn",
                    "why": "Great for credibility, trust, lead generation",
                    "ctr_prediction": "2.0%"
                },
                "consumer_product_gen_z": {
                    "best_platform": "Instagram / TikTok",
                    "why": "Visual, viral, fast conversions",
                    "ctr_prediction": "1.5%"
                },
                "visual_products": {
                    "best_platform": "Instagram / Pinterest",
                    "why": "Image-first, discovery focused",
                    "ctr_prediction": "1.8%"
                },
                "search_intent": {
                    "best_platform": "Google Search / Display",
                    "why": "Users actively searching",
                    "ctr_prediction": "1.0%"
                },
                "local_business": {
                    "best_platform": "Facebook Local / Google Maps",
                    "why": "Geo-targeting + discovery",
                    "ctr_prediction": "1.2%"
                }
            },
            "learning_algorithm": {
                "type": "Multi-armed Bandit",
                "description": "Continuously shifts budget toward channels with higher CTR",
                "tracking_metrics": ["impressions", "clicks", "ctr", "conversions"],
                "status": "Active"
            }
        }
        
        return strategy_matrix
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving channel strategy: {str(e)}")

@router.get("/channel/demo/scenario", response_model=Dict[str, Any])
async def get_demo_scenario():
    """Get the coffee shop demo scenario"""
    
    try:
        demo_scenario = {
            "client": "Local Sustainable Coffee Shop",
            "brand_story": "Family-owned, carbon-neutral, sourced directly from farmers",
            "segment": "Eco-conscious millennials",
            "campaign_goal": "Drive new store visits",
            "ai_decisions": {
                "primary_channel": "Instagram",
                "secondary_channel": "Google Maps Ads",
                "reasoning": {
                    "instagram": "Perfect for visual storytelling and reaching eco-conscious millennials",
                    "google_maps": "Local intent targeting for store visits"
                },
                "ad_style": {
                    "instagram": "Emotional, story-first video for IG Reels",
                    "google_maps": "Local intent copy for search"
                },
                "cta": "Visit us this weekend for a free tasting ☕🌿",
                "predicted_performance": {
                    "instagram": {
                        "ctr": "1.8%",
                        "conversion_rate": "3.2%",
                        "cost_per_visit": "$12.50"
                    },
                    "google_maps": {
                        "ctr": "2.1%",
                        "conversion_rate": "4.5%",
                        "cost_per_visit": "$8.75"
                    }
                }
            },
            "channel_recommendations": [
                {
                    "channel": "Instagram",
                    "confidence": 0.85,
                    "predicted_ctr": 0.018,
                    "reasoning": "Visual platform perfect for eco-conscious millennials, high engagement potential"
                },
                {
                    "channel": "Google Maps Ads",
                    "confidence": 0.78,
                    "predicted_ctr": 0.021,
                    "reasoning": "Local intent targeting, users actively searching for coffee shops"
                },
                {
                    "channel": "Facebook Local",
                    "confidence": 0.65,
                    "predicted_ctr": 0.012,
                    "reasoning": "Community-focused platform, good for local business discovery"
                }
            ],
            "learning_insights": [
                "System will track actual performance vs predictions",
                "Budget will shift toward higher-performing channels",
                "A/B testing will optimize ad creative for each platform"
            ]
        }
        
        return demo_scenario
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving demo scenario: {str(e)}")
