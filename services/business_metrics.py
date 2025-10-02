from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class BusinessMetricsService:
    def __init__(self):
        self.campaign_metrics = {}
        self.brand_metrics = {}
        self.roi_data = {}
        
    def track_campaign_performance(self, 
                                 campaign_id: str,
                                 ad_id: str,
                                 channel: str,
                                 impressions: int,
                                 clicks: int,
                                 conversions: int,
                                 spend: float,
                                 revenue: float = 0.0):
        """Track campaign performance metrics"""
        
        if campaign_id not in self.campaign_metrics:
            self.campaign_metrics[campaign_id] = {
                "campaign_id": campaign_id,
                "start_date": datetime.now().isoformat(),
                "ads": {},
                "total_impressions": 0,
                "total_clicks": 0,
                "total_conversions": 0,
                "total_spend": 0.0,
                "total_revenue": 0.0
            }
        
        campaign = self.campaign_metrics[campaign_id]
        
        # Update ad-specific metrics
        if ad_id not in campaign["ads"]:
            campaign["ads"][ad_id] = {
                "ad_id": ad_id,
                "channel": channel,
                "impressions": 0,
                "clicks": 0,
                "conversions": 0,
                "spend": 0.0,
                "revenue": 0.0,
                "created_at": datetime.now().isoformat()
            }
        
        ad_metrics = campaign["ads"][ad_id]
        ad_metrics["impressions"] += impressions
        ad_metrics["clicks"] += clicks
        ad_metrics["conversions"] += conversions
        ad_metrics["spend"] += spend
        ad_metrics["revenue"] += revenue
        
        # Update campaign totals
        campaign["total_impressions"] += impressions
        campaign["total_clicks"] += clicks
        campaign["total_conversions"] += conversions
        campaign["total_spend"] += spend
        campaign["total_revenue"] += revenue
        
        logger.info(f"Updated campaign metrics for {campaign_id}")
    
    def calculate_roi_metrics(self, campaign_id: str) -> Dict[str, Any]:
        """Calculate ROI and performance metrics for a campaign"""
        
        if campaign_id not in self.campaign_metrics:
            return None
        
        campaign = self.campaign_metrics[campaign_id]
        
        # Basic metrics
        total_impressions = campaign["total_impressions"]
        total_clicks = campaign["total_clicks"]
        total_conversions = campaign["total_conversions"]
        total_spend = campaign["total_spend"]
        total_revenue = campaign["total_revenue"]
        
        # Calculate rates
        ctr = (total_clicks / total_impressions) if total_impressions > 0 else 0
        conversion_rate = (total_conversions / total_clicks) if total_clicks > 0 else 0
        
        # Calculate costs
        cpc = (total_spend / total_clicks) if total_clicks > 0 else 0
        cpa = (total_spend / total_conversions) if total_conversions > 0 else 0
        
        # Calculate ROI metrics
        roi = ((total_revenue - total_spend) / total_spend * 100) if total_spend > 0 else 0
        roas = (total_revenue / total_spend) if total_spend > 0 else 0
        
        # Calculate customer lifetime value (simplified)
        avg_order_value = (total_revenue / total_conversions) if total_conversions > 0 else 0
        clv = avg_order_value * 2.5  # Simplified CLV calculation
        
        # Calculate efficiency score (0-100)
        efficiency_score = self._calculate_efficiency_score(ctr, conversion_rate, roi)
        
        metrics = {
            "campaign_id": campaign_id,
            "period": {
                "start_date": campaign["start_date"],
                "end_date": datetime.now().isoformat(),
                "duration_days": (datetime.now() - datetime.fromisoformat(campaign["start_date"])).days
            },
            "performance": {
                "impressions": total_impressions,
                "clicks": total_clicks,
                "conversions": total_conversions,
                "ctr": ctr,
                "conversion_rate": conversion_rate
            },
            "financial": {
                "spend": total_spend,
                "revenue": total_revenue,
                "cpc": cpc,
                "cpa": cpa,
                "roi_percent": roi,
                "roas": roas,
                "avg_order_value": avg_order_value,
                "customer_lifetime_value": clv
            },
            "efficiency": {
                "efficiency_score": efficiency_score,
                "cost_efficiency": (1 / cpa) if cpa > 0 else 0,
                "revenue_efficiency": (total_revenue / total_impressions) if total_impressions > 0 else 0
            },
            "ads_performance": []
        }
        
        # Add individual ad performance
        for ad_id, ad_metrics in campaign["ads"].items():
            ad_ctr = (ad_metrics["clicks"] / ad_metrics["impressions"]) if ad_metrics["impressions"] > 0 else 0
            ad_conversion_rate = (ad_metrics["conversions"] / ad_metrics["clicks"]) if ad_metrics["clicks"] > 0 else 0
            ad_roi = ((ad_metrics["revenue"] - ad_metrics["spend"]) / ad_metrics["spend"] * 100) if ad_metrics["spend"] > 0 else 0
            
            metrics["ads_performance"].append({
                "ad_id": ad_id,
                "channel": ad_metrics["channel"],
                "impressions": ad_metrics["impressions"],
                "clicks": ad_metrics["clicks"],
                "conversions": ad_metrics["conversions"],
                "spend": ad_metrics["spend"],
                "revenue": ad_metrics["revenue"],
                "ctr": ad_ctr,
                "conversion_rate": ad_conversion_rate,
                "roi_percent": ad_roi
            })
        
        return metrics
    
    def _calculate_efficiency_score(self, ctr: float, conversion_rate: float, roi: float) -> float:
        """Calculate overall efficiency score (0-100)"""
        
        # Normalize metrics to 0-100 scale
        ctr_score = min(ctr * 1000, 100)  # CTR in percentage
        conversion_score = min(conversion_rate * 100, 100)  # Conversion rate in percentage
        roi_score = min(max(roi, 0), 100)  # ROI capped at 100%
        
        # Weighted average
        efficiency_score = (ctr_score * 0.3) + (conversion_score * 0.4) + (roi_score * 0.3)
        
        return round(efficiency_score, 2)
    
    def get_brand_performance(self, brand_id: str) -> Dict[str, Any]:
        """Get overall performance metrics for a brand"""
        
        brand_campaigns = [c for c in self.campaign_metrics.values() if c.get("brand_id") == brand_id]
        
        if not brand_campaigns:
            return {
                "brand_id": brand_id,
                "message": "No campaign data available",
                "total_campaigns": 0
            }
        
        # Aggregate metrics across all campaigns
        total_impressions = sum(c["total_impressions"] for c in brand_campaigns)
        total_clicks = sum(c["total_clicks"] for c in brand_campaigns)
        total_conversions = sum(c["total_conversions"] for c in brand_campaigns)
        total_spend = sum(c["total_spend"] for c in brand_campaigns)
        total_revenue = sum(c["total_revenue"] for c in brand_campaigns)
        
        # Calculate aggregate rates
        overall_ctr = (total_clicks / total_impressions) if total_impressions > 0 else 0
        overall_conversion_rate = (total_conversions / total_clicks) if total_clicks > 0 else 0
        overall_roi = ((total_revenue - total_spend) / total_spend * 100) if total_spend > 0 else 0
        
        # Find best performing campaign
        best_campaign = max(brand_campaigns, key=lambda x: x["total_revenue"])
        
        return {
            "brand_id": brand_id,
            "total_campaigns": len(brand_campaigns),
            "overall_metrics": {
                "impressions": total_impressions,
                "clicks": total_clicks,
                "conversions": total_conversions,
                "spend": total_spend,
                "revenue": total_revenue,
                "ctr": overall_ctr,
                "conversion_rate": overall_conversion_rate,
                "roi_percent": overall_roi
            },
            "best_campaign": {
                "campaign_id": best_campaign["campaign_id"],
                "revenue": best_campaign["total_revenue"],
                "roi": ((best_campaign["total_revenue"] - best_campaign["total_spend"]) / best_campaign["total_spend"] * 100) if best_campaign["total_spend"] > 0 else 0
            },
            "campaigns": [
                {
                    "campaign_id": c["campaign_id"],
                    "revenue": c["total_revenue"],
                    "roi": ((c["total_revenue"] - c["total_spend"]) / c["total_spend"] * 100) if c["total_spend"] > 0 else 0
                }
                for c in brand_campaigns
            ]
        }
    
    def get_channel_performance(self) -> Dict[str, Any]:
        """Get performance metrics by channel"""
        
        channel_metrics = {}
        
        for campaign in self.campaign_metrics.values():
            for ad_id, ad_metrics in campaign["ads"].items():
                channel = ad_metrics["channel"]
                
                if channel not in channel_metrics:
                    channel_metrics[channel] = {
                        "channel": channel,
                        "total_impressions": 0,
                        "total_clicks": 0,
                        "total_conversions": 0,
                        "total_spend": 0.0,
                        "total_revenue": 0.0,
                        "ads_count": 0
                    }
                
                channel_metrics[channel]["total_impressions"] += ad_metrics["impressions"]
                channel_metrics[channel]["total_clicks"] += ad_metrics["clicks"]
                channel_metrics[channel]["total_conversions"] += ad_metrics["conversions"]
                channel_metrics[channel]["total_spend"] += ad_metrics["spend"]
                channel_metrics[channel]["total_revenue"] += ad_metrics["revenue"]
                channel_metrics[channel]["ads_count"] += 1
        
        # Calculate rates for each channel
        for channel, metrics in channel_metrics.items():
            metrics["ctr"] = (metrics["total_clicks"] / metrics["total_impressions"]) if metrics["total_impressions"] > 0 else 0
            metrics["conversion_rate"] = (metrics["total_conversions"] / metrics["total_clicks"]) if metrics["total_clicks"] > 0 else 0
            metrics["cpc"] = (metrics["total_spend"] / metrics["total_clicks"]) if metrics["total_clicks"] > 0 else 0
            metrics["roi"] = ((metrics["total_revenue"] - metrics["total_spend"]) / metrics["total_spend"] * 100) if metrics["total_spend"] > 0 else 0
        
        # Sort by revenue
        sorted_channels = sorted(channel_metrics.values(), key=lambda x: x["total_revenue"], reverse=True)
        
        return {
            "channels": sorted_channels,
            "best_channel": sorted_channels[0] if sorted_channels else None,
            "total_channels": len(channel_metrics)
        }
    
    def get_roi_insights(self, campaign_id: str) -> Dict[str, Any]:
        """Get ROI insights and recommendations"""
        
        metrics = self.calculate_roi_metrics(campaign_id)
        if not metrics:
            return {"message": "No data available for this campaign"}
        
        insights = []
        recommendations = []
        
        # CTR insights
        if metrics["performance"]["ctr"] > 0.02:
            insights.append("High CTR indicates strong ad relevance and targeting")
        elif metrics["performance"]["ctr"] < 0.005:
            insights.append("Low CTR suggests ad creative or targeting needs improvement")
            recommendations.append("Test different ad creatives and refine audience targeting")
        
        # Conversion rate insights
        if metrics["performance"]["conversion_rate"] > 0.1:
            insights.append("High conversion rate shows effective landing page and offer")
        elif metrics["performance"]["conversion_rate"] < 0.02:
            insights.append("Low conversion rate indicates landing page or offer issues")
            recommendations.append("Optimize landing page and test different offers")
        
        # ROI insights
        if metrics["financial"]["roi_percent"] > 100:
            insights.append("Excellent ROI - campaign is highly profitable")
        elif metrics["financial"]["roi_percent"] > 0:
            insights.append("Positive ROI - campaign is profitable but could be optimized")
        else:
            insights.append("Negative ROI - campaign needs immediate optimization")
            recommendations.append("Pause campaign and analyze performance data")
        
        # Efficiency insights
        if metrics["efficiency"]["efficiency_score"] > 80:
            insights.append("High efficiency score - campaign is well-optimized")
        elif metrics["efficiency"]["efficiency_score"] < 40:
            insights.append("Low efficiency score - significant optimization needed")
            recommendations.append("Review targeting, creative, and bidding strategy")
        
        return {
            "campaign_id": campaign_id,
            "insights": insights,
            "recommendations": recommendations,
            "priority_actions": recommendations[:3] if recommendations else ["Continue monitoring performance"]
        }

# Global business metrics service instance
business_metrics_service = BusinessMetricsService()
