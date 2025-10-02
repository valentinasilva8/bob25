import numpy as np
from typing import Dict, Any, List, Tuple
from models.schemas import ChannelType, CampaignGoal, ChannelRecommendation
import logging

logger = logging.getLogger(__name__)

class ChannelRecommendationService:
    def __init__(self):
        # Initialize multi-armed bandit parameters
        self.alpha = 1.0  # Prior success count
        self.beta = 1.0   # Prior failure count
        self.channel_stats = {}  # Store channel performance statistics
        
        # Channel characteristics mapping
        self.channel_characteristics = {
            ChannelType.LINKEDIN: {
                "audience_types": ["professional", "b2b", "executive", "entrepreneur"],
                "content_types": ["professional", "educational", "thought_leadership"],
                "best_for_goals": [CampaignGoal.AWARENESS, CampaignGoal.ENGAGEMENT],
                "base_ctr": 0.02,
                "base_cpc": 5.50,
                "demographic": "25-65, professional"
            },
            ChannelType.INSTAGRAM: {
                "audience_types": ["millennial", "gen_z", "visual_learners", "lifestyle"],
                "content_types": ["visual", "lifestyle", "inspiring", "authentic"],
                "best_for_goals": [CampaignGoal.ENGAGEMENT, CampaignGoal.AWARENESS],
                "base_ctr": 0.015,
                "base_cpc": 3.20,
                "demographic": "18-45, visual-focused"
            },
            ChannelType.GOOGLE_DISPLAY: {
                "audience_types": ["general", "shoppers", "researchers", "intent_driven"],
                "content_types": ["informational", "product_focused", "comparison"],
                "best_for_goals": [CampaignGoal.CONVERSION, CampaignGoal.TRAFFIC],
                "base_ctr": 0.01,
                "base_cpc": 1.80,
                "demographic": "All ages, intent-driven"
            },
            ChannelType.FACEBOOK: {
                "audience_types": ["general", "community", "social", "local"],
                "content_types": ["social", "community", "local", "personal"],
                "best_for_goals": [CampaignGoal.ENGAGEMENT, CampaignGoal.AWARENESS],
                "base_ctr": 0.012,
                "base_cpc": 2.40,
                "demographic": "25-65, social"
            },
            ChannelType.TWITTER: {
                "audience_types": ["news_consumers", "influencers", "real_time", "conversational"],
                "content_types": ["news", "real_time", "conversational", "trending"],
                "best_for_goals": [CampaignGoal.ENGAGEMENT, CampaignGoal.AWARENESS],
                "base_ctr": 0.008,
                "base_cpc": 1.20,
                "demographic": "18-50, news-focused"
            },
            ChannelType.TIKTOK: {
                "audience_types": ["gen_z", "millennial", "creative", "entertainment"],
                "content_types": ["creative", "entertaining", "trending", "authentic"],
                "best_for_goals": [CampaignGoal.ENGAGEMENT, CampaignGoal.AWARENESS],
                "base_ctr": 0.025,
                "base_cpc": 4.80,
                "demographic": "16-35, creative"
            }
        }
    
    def recommend_channels(
        self, 
        brand_data: Dict[str, Any], 
        product_data: Dict[str, Any], 
        audience_analysis: Dict[str, Any],
        campaign_goal: CampaignGoal,
        budget: float = None
    ) -> List[ChannelRecommendation]:
        """Recommend best channels based on analysis"""
        
        recommendations = []
        audience_segment = audience_analysis.get("segment", "general")
        audience_characteristics = audience_analysis.get("characteristics", {})
        
        for channel, characteristics in self.channel_characteristics.items():
            # Calculate compatibility score
            compatibility_score = self._calculate_compatibility(
                channel, characteristics, brand_data, product_data, 
                audience_analysis, campaign_goal
            )
            
            # Get performance metrics
            ctr, cpc = self._get_channel_metrics(
                channel, audience_characteristics, campaign_goal
            )
            
            # Apply multi-armed bandit learning if we have historical data
            if channel.value in self.channel_stats:
                ctr, cpc = self._apply_bandit_learning(channel, ctr, cpc)
            
            # Calculate confidence score
            confidence = self._calculate_confidence(
                compatibility_score, audience_characteristics, budget
            )
            
            # Generate reasoning
            reasoning = self._generate_reasoning(
                channel, characteristics, brand_data, product_data, 
                audience_analysis, campaign_goal, compatibility_score
            )
            
            recommendations.append(ChannelRecommendation(
                channel=channel,
                confidence_score=confidence,
                estimated_ctr=ctr,
                estimated_cpc=cpc,
                reasoning=reasoning
            ))
        
        # Sort by confidence score
        recommendations.sort(key=lambda x: x.confidence_score, reverse=True)
        
        return recommendations
    
    def _calculate_compatibility(
        self, 
        channel: ChannelType, 
        characteristics: Dict[str, Any],
        brand_data: Dict[str, Any], 
        product_data: Dict[str, Any],
        audience_analysis: Dict[str, Any],
        campaign_goal: CampaignGoal
    ) -> float:
        """Calculate compatibility score between channel and campaign"""
        
        score = 0.0
        max_score = 0.0
        
        # Audience compatibility (40% weight)
        audience_segment = audience_analysis.get("segment", "general")
        if audience_segment in characteristics["audience_types"]:
            score += 0.4
        max_score += 0.4
        
        # Campaign goal compatibility (30% weight)
        if campaign_goal in characteristics["best_for_goals"]:
            score += 0.3
        max_score += 0.3
        
        # Brand tone compatibility (20% weight)
        brand_tone = brand_data.get("tone", "").lower()
        content_types = [ct.lower() for ct in characteristics["content_types"]]
        
        tone_matches = {
            "professional": ["professional", "educational"],
            "casual": ["lifestyle", "social", "authentic"],
            "friendly": ["social", "community", "personal"],
            "luxury": ["sophisticated", "premium"],
            "eco-friendly": ["authentic", "lifestyle", "inspiring"]
        }
        
        if brand_tone in tone_matches:
            for tone_match in tone_matches[brand_tone]:
                if any(tone_match in ct for ct in content_types):
                    score += 0.2
                    break
        max_score += 0.2
        
        # Product category compatibility (10% weight)
        product_category = product_data.get("category", "").lower()
        category_matches = {
            "technology": [ChannelType.LINKEDIN, ChannelType.TWITTER],
            "fashion": [ChannelType.INSTAGRAM, ChannelType.TIKTOK],
            "beauty": [ChannelType.INSTAGRAM, ChannelType.TIKTOK],
            "b2b": [ChannelType.LINKEDIN, ChannelType.GOOGLE_DISPLAY],
            "ecommerce": [ChannelType.GOOGLE_DISPLAY, ChannelType.FACEBOOK],
            "local": [ChannelType.FACEBOOK, ChannelType.GOOGLE_DISPLAY]
        }
        
        for category, preferred_channels in category_matches.items():
            if category in product_category and channel in preferred_channels:
                score += 0.1
                break
        max_score += 0.1
        
        return score / max_score if max_score > 0 else 0.0
    
    def _get_channel_metrics(
        self, 
        channel: ChannelType, 
        audience_characteristics: Dict[str, Any],
        campaign_goal: CampaignGoal
    ) -> Tuple[float, float]:
        """Get estimated CTR and CPC for channel"""
        
        characteristics = self.channel_characteristics[channel]
        base_ctr = characteristics["base_ctr"]
        base_cpc = characteristics["base_cpc"]
        
        # Adjust based on audience engagement
        engagement_level = audience_characteristics.get("engagement_level", "medium")
        engagement_multiplier = {
            "high": 1.3,
            "medium": 1.0,
            "low": 0.7
        }.get(engagement_level, 1.0)
        
        # Adjust based on campaign goal
        goal_multiplier = {
            CampaignGoal.AWARENESS: 1.0,
            CampaignGoal.ENGAGEMENT: 1.2,
            CampaignGoal.CONVERSION: 0.8,
            CampaignGoal.TRAFFIC: 0.9
        }.get(campaign_goal, 1.0)
        
        ctr = base_ctr * engagement_multiplier * goal_multiplier
        cpc = base_cpc / engagement_multiplier  # Higher engagement = lower CPC
        
        return ctr, cpc
    
    def _apply_bandit_learning(
        self, 
        channel: ChannelType, 
        base_ctr: float, 
        base_cpc: float
    ) -> Tuple[float, float]:
        """Apply multi-armed bandit learning to adjust metrics"""
        
        if channel.value not in self.channel_stats:
            return base_ctr, base_cpc
        
        stats = self.channel_stats[channel.value]
        successes = stats.get("successes", 0)
        failures = stats.get("failures", 0)
        
        if successes + failures == 0:
            return base_ctr, base_cpc
        
        # Beta distribution sampling for CTR
        alpha = self.alpha + successes
        beta = self.beta + failures
        
        # Sample from beta distribution
        learned_ctr = np.random.beta(alpha, beta)
        
        # Adjust CPC based on learned performance
        performance_ratio = successes / (successes + failures) if (successes + failures) > 0 else 1.0
        learned_cpc = base_cpc * (2 - performance_ratio)  # Better performance = lower CPC
        
        return learned_ctr, learned_cpc
    
    def _calculate_confidence(
        self, 
        compatibility_score: float, 
        audience_characteristics: Dict[str, Any],
        budget: float
    ) -> float:
        """Calculate confidence score for recommendation"""
        
        confidence = compatibility_score
        
        # Boost confidence for high-engagement audiences
        engagement_level = audience_characteristics.get("engagement_level", "medium")
        if engagement_level == "high":
            confidence *= 1.2
        elif engagement_level == "low":
            confidence *= 0.8
        
        # Boost confidence for larger budgets (more data)
        if budget and budget > 1000:
            confidence *= 1.1
        elif budget and budget < 100:
            confidence *= 0.9
        
        # Ensure confidence is between 0 and 1
        return min(max(confidence, 0.0), 1.0)
    
    def _generate_reasoning(
        self, 
        channel: ChannelType, 
        characteristics: Dict[str, Any],
        brand_data: Dict[str, Any], 
        product_data: Dict[str, Any],
        audience_analysis: Dict[str, Any],
        campaign_goal: CampaignGoal,
        compatibility_score: float
    ) -> str:
        """Generate human-readable reasoning for recommendation"""
        
        audience_segment = audience_analysis.get("segment", "general")
        brand_tone = brand_data.get("tone", "professional")
        product_category = product_data.get("category", "general")
        
        reasoning_parts = []
        
        # Audience match
        if audience_segment in characteristics["audience_types"]:
            reasoning_parts.append(f"Perfect match for {audience_segment} audience")
        
        # Goal alignment
        if campaign_goal in characteristics["best_for_goals"]:
            reasoning_parts.append(f"Optimal for {campaign_goal.value} campaigns")
        
        # Brand tone alignment
        if brand_tone.lower() in ["professional", "casual", "friendly"]:
            reasoning_parts.append(f"Aligns with {brand_tone} brand tone")
        
        # Category relevance
        if product_category.lower() in ["technology", "fashion", "beauty", "b2b"]:
            reasoning_parts.append(f"Strong performance for {product_category} products")
        
        # Performance indicators
        if compatibility_score > 0.8:
            reasoning_parts.append("High compatibility score")
        elif compatibility_score > 0.6:
            reasoning_parts.append("Good compatibility score")
        
        return "; ".join(reasoning_parts) if reasoning_parts else "Standard performance expected"
    
    def update_channel_performance(
        self, 
        channel: ChannelType, 
        clicks: int, 
        impressions: int, 
        conversions: int
    ):
        """Update channel performance statistics for bandit learning"""
        
        if channel.value not in self.channel_stats:
            self.channel_stats[channel.value] = {"successes": 0, "failures": 0}
        
        # Calculate success rate
        ctr = clicks / impressions if impressions > 0 else 0
        conversion_rate = conversions / clicks if clicks > 0 else 0
        
        # Define success threshold (adjustable)
        success_threshold = 0.01  # 1% CTR threshold
        
        if ctr >= success_threshold:
            self.channel_stats[channel.value]["successes"] += 1
        else:
            self.channel_stats[channel.value]["failures"] += 1
        
        logger.info(f"Updated {channel.value} performance: CTR={ctr:.4f}, Successes={self.channel_stats[channel.value]['successes']}, Failures={self.channel_stats[channel.value]['failures']}")

# Global channel service instance
channel_service = ChannelRecommendationService()
