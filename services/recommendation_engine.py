import numpy as np
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)

class AdRecommendationEngine:
    def __init__(self):
        # Performance tracking
        self.ad_performance = {}  # ad_id -> performance metrics
        self.channel_performance = {}  # channel -> performance by segment
        self.segment_performance = {}  # segment -> best performing ads
        self.pattern_database = {}  # successful patterns
        
        # Recommendation weights
        self.performance_weight = 0.4
        self.similarity_weight = 0.3
        self.recency_weight = 0.2
        self.diversity_weight = 0.1
        
    def track_ad_performance(
        self, 
        ad_id: str,
        channel: str,
        audience_segment: str,
        impressions: int,
        clicks: int,
        conversions: int,
        revenue: float = 0.0,
        ad_attributes: Dict[str, Any] = None
    ):
        """Track performance of an ad for recommendation learning"""
        
        # Calculate performance metrics
        ctr = clicks / impressions if impressions > 0 else 0
        conversion_rate = conversions / clicks if clicks > 0 else 0
        revenue_per_impression = revenue / impressions if impressions > 0 else 0
        
        # Store performance data
        performance_data = {
            "ad_id": ad_id,
            "channel": channel,
            "audience_segment": audience_segment,
            "impressions": impressions,
            "clicks": clicks,
            "conversions": conversions,
            "revenue": revenue,
            "ctr": ctr,
            "conversion_rate": conversion_rate,
            "revenue_per_impression": revenue_per_impression,
            "performance_score": self._calculate_performance_score(ctr, conversion_rate, revenue_per_impression),
            "ad_attributes": ad_attributes or {},
            "timestamp": datetime.now().isoformat()
        }
        
        self.ad_performance[ad_id] = performance_data
        
        # Update channel performance by segment
        channel_key = f"{channel}_{audience_segment}"
        if channel_key not in self.channel_performance:
            self.channel_performance[channel_key] = {
                "total_impressions": 0,
                "total_clicks": 0,
                "total_conversions": 0,
                "total_revenue": 0,
                "ad_count": 0,
                "avg_ctr": 0,
                "avg_conversion_rate": 0,
                "avg_revenue_per_impression": 0
            }
        
        channel_data = self.channel_performance[channel_key]
        channel_data["total_impressions"] += impressions
        channel_data["total_clicks"] += clicks
        channel_data["total_conversions"] += conversions
        channel_data["total_revenue"] += revenue
        channel_data["ad_count"] += 1
        
        # Update averages
        channel_data["avg_ctr"] = channel_data["total_clicks"] / channel_data["total_impressions"]
        channel_data["avg_conversion_rate"] = channel_data["total_conversions"] / channel_data["total_clicks"]
        channel_data["avg_revenue_per_impression"] = channel_data["total_revenue"] / channel_data["total_impressions"]
        
        # Update segment performance
        if audience_segment not in self.segment_performance:
            self.segment_performance[audience_segment] = []
        
        self.segment_performance[audience_segment].append({
            "ad_id": ad_id,
            "performance_score": performance_data["performance_score"],
            "ctr": ctr,
            "conversion_rate": conversion_rate,
            "revenue_per_impression": revenue_per_impression
        })
        
        # Keep only top performing ads per segment
        self.segment_performance[audience_segment].sort(
            key=lambda x: x["performance_score"], reverse=True
        )
        self.segment_performance[audience_segment] = self.segment_performance[audience_segment][:10]
        
        logger.info(f"Tracked performance for ad {ad_id}: CTR={ctr:.3f}, ConvRate={conversion_rate:.3f}, Score={performance_data['performance_score']:.3f}")
    
    def _calculate_performance_score(self, ctr: float, conversion_rate: float, revenue_per_impression: float) -> float:
        """Calculate overall performance score for an ad"""
        
        # Normalize metrics to 0-1 scale
        ctr_score = min(ctr * 100, 1.0)  # Cap at 1% CTR = 1.0 score
        conversion_score = min(conversion_rate * 10, 1.0)  # Cap at 10% conversion = 1.0 score
        revenue_score = min(revenue_per_impression / 10, 1.0)  # Cap at $10 per impression = 1.0 score
        
        # Weighted combination
        performance_score = (
            ctr_score * 0.4 +
            conversion_score * 0.4 +
            revenue_score * 0.2
        )
        
        return performance_score
    
    def get_recommendations(
        self, 
        audience_segment: str,
        channel: str,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """Get ad recommendations for a specific audience segment and channel"""
        
        recommendations = []
        
        # Get top performing ads for this segment
        if audience_segment in self.segment_performance:
            segment_ads = self.segment_performance[audience_segment]
            
            for ad_data in segment_ads:
                ad_id = ad_data["ad_id"]
                if ad_id in self.ad_performance:
                    ad_info = self.ad_performance[ad_id]
                    
                    # Check if this ad worked well on this channel
                    if ad_info["channel"] == channel:
                        recommendations.append({
                            "ad_id": ad_id,
                            "performance_score": ad_data["performance_score"],
                            "ctr": ad_data["ctr"],
                            "conversion_rate": ad_data["conversion_rate"],
                            "revenue_per_impression": ad_data["revenue_per_impression"],
                            "reasoning": f"High performing ad for {audience_segment} on {channel}",
                            "ad_attributes": ad_info.get("ad_attributes", {})
                        })
        
        # Sort by performance score
        recommendations.sort(key=lambda x: x["performance_score"], reverse=True)
        
        return recommendations[:limit]
    
    def get_channel_recommendations(self, audience_segment: str) -> List[Dict[str, Any]]:
        """Get best channels for a specific audience segment"""
        
        channel_scores = {}
        
        for channel_key, performance in self.channel_performance.items():
            if channel_key.endswith(f"_{audience_segment}"):
                channel = channel_key.replace(f"_{audience_segment}", "")
                
                # Calculate channel score
                channel_score = (
                    performance["avg_ctr"] * 0.4 +
                    performance["avg_conversion_rate"] * 0.4 +
                    performance["avg_revenue_per_impression"] * 0.2
                )
                
                channel_scores[channel] = {
                    "channel": channel,
                    "score": channel_score,
                    "avg_ctr": performance["avg_ctr"],
                    "avg_conversion_rate": performance["avg_conversion_rate"],
                    "avg_revenue_per_impression": performance["avg_revenue_per_impression"],
                    "ad_count": performance["ad_count"],
                    "total_impressions": performance["total_impressions"]
                }
        
        # Sort by score
        sorted_channels = sorted(channel_scores.values(), key=lambda x: x["score"], reverse=True)
        
        return sorted_channels
    
    def get_successful_patterns(self, audience_segment: str) -> Dict[str, Any]:
        """Identify successful ad patterns for an audience segment"""
        
        if audience_segment not in self.segment_performance:
            return {"patterns": [], "insights": []}
        
        segment_ads = self.segment_performance[audience_segment]
        top_ads = segment_ads[:5]  # Top 5 performing ads
        
        patterns = {
            "headline_patterns": [],
            "cta_patterns": [],
            "channel_preferences": [],
            "performance_insights": []
        }
        
        # Analyze top performing ads
        for ad_data in top_ads:
            ad_id = ad_data["ad_id"]
            if ad_id in self.ad_performance:
                ad_info = self.ad_performance[ad_id]
                ad_attrs = ad_info.get("ad_attributes", {})
                
                # Extract patterns
                if "headline" in ad_attrs:
                    patterns["headline_patterns"].append(ad_attrs["headline"])
                if "cta" in ad_attrs:
                    patterns["cta_patterns"].append(ad_attrs["cta"])
                if "channel" in ad_info:
                    patterns["channel_preferences"].append(ad_info["channel"])
        
        # Generate insights
        insights = []
        
        if patterns["headline_patterns"]:
            # Find common words in successful headlines
            all_words = []
            for headline in patterns["headline_patterns"]:
                all_words.extend(headline.lower().split())
            
            word_freq = {}
            for word in all_words:
                word_freq[word] = word_freq.get(word, 0) + 1
            
            common_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
            insights.append(f"Successful headlines often contain: {', '.join([word for word, freq in common_words])}")
        
        if patterns["cta_patterns"]:
            insights.append(f"Top CTAs: {', '.join(set(patterns['cta_patterns']))}")
        
        if patterns["channel_preferences"]:
            channel_freq = {}
            for channel in patterns["channel_preferences"]:
                channel_freq[channel] = channel_freq.get(channel, 0) + 1
            
            best_channel = max(channel_freq.items(), key=lambda x: x[1])
            insights.append(f"Best performing channel: {best_channel[0]} ({best_channel[1]} successful ads)")
        
        # Performance insights
        avg_ctr = np.mean([ad["ctr"] for ad in top_ads])
        avg_conversion = np.mean([ad["conversion_rate"] for ad in top_ads])
        
        insights.append(f"Average CTR for successful ads: {avg_ctr:.3f}")
        insights.append(f"Average conversion rate: {avg_conversion:.3f}")
        
        return {
            "patterns": patterns,
            "insights": insights,
            "top_ads": top_ads
        }
    
    def get_performance_insights(self) -> Dict[str, Any]:
        """Get overall performance insights across all campaigns"""
        
        if not self.ad_performance:
            return {"message": "No performance data available"}
        
        all_ads = list(self.ad_performance.values())
        
        # Overall metrics
        total_impressions = sum(ad["impressions"] for ad in all_ads)
        total_clicks = sum(ad["clicks"] for ad in all_ads)
        total_conversions = sum(ad["conversions"] for ad in all_ads)
        total_revenue = sum(ad["revenue"] for ad in all_ads)
        
        overall_ctr = total_clicks / total_impressions if total_impressions > 0 else 0
        overall_conversion_rate = total_conversions / total_clicks if total_clicks > 0 else 0
        
        # Best performing ads
        best_ads = sorted(all_ads, key=lambda x: x["performance_score"], reverse=True)[:5]
        
        # Channel performance
        channel_performance = {}
        for ad in all_ads:
            channel = ad["channel"]
            if channel not in channel_performance:
                channel_performance[channel] = {
                    "ads": 0,
                    "total_ctr": 0,
                    "total_conversion_rate": 0,
                    "total_revenue": 0
                }
            
            channel_performance[channel]["ads"] += 1
            channel_performance[channel]["total_ctr"] += ad["ctr"]
            channel_performance[channel]["total_conversion_rate"] += ad["conversion_rate"]
            channel_performance[channel]["total_revenue"] += ad["revenue"]
        
        # Calculate averages
        for channel in channel_performance:
            data = channel_performance[channel]
            data["avg_ctr"] = data["total_ctr"] / data["ads"]
            data["avg_conversion_rate"] = data["total_conversion_rate"] / data["ads"]
            data["avg_revenue"] = data["total_revenue"] / data["ads"]
        
        # Segment performance
        segment_performance = {}
        for ad in all_ads:
            segment = ad["audience_segment"]
            if segment not in segment_performance:
                segment_performance[segment] = {
                    "ads": 0,
                    "total_performance_score": 0
                }
            
            segment_performance[segment]["ads"] += 1
            segment_performance[segment]["total_performance_score"] += ad["performance_score"]
        
        # Calculate averages
        for segment in segment_performance:
            data = segment_performance[segment]
            data["avg_performance_score"] = data["total_performance_score"] / data["ads"]
        
        return {
            "overall_metrics": {
                "total_impressions": total_impressions,
                "total_clicks": total_clicks,
                "total_conversions": total_conversions,
                "total_revenue": total_revenue,
                "overall_ctr": overall_ctr,
                "overall_conversion_rate": overall_conversion_rate
            },
            "best_performing_ads": [
                {
                    "ad_id": ad["ad_id"],
                    "performance_score": ad["performance_score"],
                    "ctr": ad["ctr"],
                    "conversion_rate": ad["conversion_rate"],
                    "channel": ad["channel"],
                    "audience_segment": ad["audience_segment"]
                }
                for ad in best_ads
            ],
            "channel_performance": channel_performance,
            "segment_performance": segment_performance
        }
    
    def get_whats_working_summary(self) -> Dict[str, Any]:
        """Get a summary of what's working across all campaigns"""
        
        insights = self.get_performance_insights()
        
        if "message" in insights:
            return insights
        
        # Find best performing combinations
        best_combinations = []
        
        for ad in insights["best_performing_ads"]:
            combination = f"{ad['audience_segment']} + {ad['channel']}"
            best_combinations.append({
                "combination": combination,
                "performance_score": ad["performance_score"],
                "ctr": ad["ctr"],
                "conversion_rate": ad["conversion_rate"]
            })
        
        # Find best channels overall
        best_channels = sorted(
            insights["channel_performance"].items(),
            key=lambda x: x[1]["avg_ctr"],
            reverse=True
        )[:3]
        
        # Find best segments overall
        best_segments = sorted(
            insights["segment_performance"].items(),
            key=lambda x: x[1]["avg_performance_score"],
            reverse=True
        )[:3]
        
        return {
            "summary": f"Analyzed {len(self.ad_performance)} ads across {len(insights['channel_performance'])} channels",
            "best_combinations": best_combinations,
            "top_channels": [
                {
                    "channel": channel,
                    "avg_ctr": data["avg_ctr"],
                    "avg_conversion_rate": data["avg_conversion_rate"],
                    "ads_count": data["ads"]
                }
                for channel, data in best_channels
            ],
            "top_segments": [
                {
                    "segment": segment,
                    "avg_performance_score": data["avg_performance_score"],
                    "ads_count": data["ads"]
                }
                for segment, data in best_segments
            ],
            "recommendations": [
                f"Focus on {best_combinations[0]['combination']} - highest performing combination",
                f"Use {best_channels[0][0]} for best CTR ({best_channels[0][1]['avg_ctr']:.3f})",
                f"Target {best_segments[0][0]} segment - highest performance score"
            ]
        }

# Global recommendation engine instance
recommendation_engine = AdRecommendationEngine()
