#!/usr/bin/env python3
"""
Generate comprehensive competition data for the recommendation engine
"""

import asyncio
import sys
import os
import random
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.recommendation_engine import recommendation_engine
from services.database import db

class CompetitionDataGenerator:
    def __init__(self):
        self.audience_segments = [
            "eco_conscious_shoppers",
            "tech_early_adopters", 
            "price_sensitive_buyers",
            "luxury_seekers",
            "convenience_seekers",
            "health_conscious",
            "business_professionals",
            "young_families",
            "seniors",
            "students"
        ]
        
        self.channels = [
            "instagram", "facebook", "linkedin", "twitter", "tiktok",
            "google_display", "google_search", "youtube", "pinterest",
            "snapchat", "reddit", "email", "sms"
        ]
        
        self.ad_attributes_templates = {
            "headlines": {
                "eco_conscious_shoppers": [
                    "Save the Planet with Every Purchase",
                    "Make a Difference Today",
                    "Join the Green Revolution",
                    "Sustainable Living Made Easy",
                    "Protect Our Future",
                    "Eco-Friendly Solutions",
                    "Carbon Neutral Products",
                    "Earth-Conscious Choices"
                ],
                "tech_early_adopters": [
                    "Revolutionary Energy Technology",
                    "Next-Gen Energy Solutions",
                    "Cutting-Edge Innovation",
                    "Future of Energy is Here",
                    "Advanced Technology",
                    "Smart Energy Systems",
                    "AI-Powered Solutions",
                    "Breakthrough Technology"
                ],
                "price_sensitive_buyers": [
                    "Save Money with Smart Energy",
                    "Affordable Green Solutions",
                    "Budget-Friendly Options",
                    "Great Value, Great Results",
                    "Save 50% on Energy Costs",
                    "Low-Cost, High-Impact",
                    "Maximum Savings",
                    "Best Value Guaranteed"
                ],
                "luxury_seekers": [
                    "Premium Energy Solutions",
                    "Exclusive Technology",
                    "Luxury Living Made Sustainable",
                    "Elite Energy Systems",
                    "Sophisticated Solutions",
                    "High-End Innovation",
                    "Premium Quality",
                    "Luxury Meets Sustainability"
                ]
            },
            "ctas": {
                "eco_conscious_shoppers": [
                    "Join the Green Revolution",
                    "Start Your Journey",
                    "Make a Difference",
                    "Protect Our Planet",
                    "Choose Sustainability"
                ],
                "tech_early_adopters": [
                    "Learn More",
                    "Schedule Demo",
                    "See the Technology",
                    "Get Early Access",
                    "Explore Innovation"
                ],
                "price_sensitive_buyers": [
                    "Get 20% Off",
                    "Save Money Now",
                    "Claim Your Discount",
                    "Limited Time Offer",
                    "Best Price Guaranteed"
                ],
                "luxury_seekers": [
                    "Experience Luxury",
                    "Join the Elite",
                    "Premium Access",
                    "Exclusive Offer",
                    "Luxury Awaits"
                ]
            },
            "tones": [
                "inspirational", "motivational", "professional", "technical",
                "value_focused", "luxury", "urgent", "friendly", "authoritative"
            ]
        }
        
        self.business_types = [
            "b2b", "local_business", "consumer_products", "eco_products",
            "services", "general", "tech_startup", "retail", "healthcare"
        ]
        
        self.product_categories = [
            "renewable_energy", "sustainable_products", "tech_gadgets",
            "home_improvement", "fashion", "food", "health", "education",
            "finance", "travel", "automotive", "beauty"
        ]
    
    def generate_realistic_performance_data(self, audience_segment: str, channel: str) -> Dict[str, Any]:
        """Generate realistic performance data based on audience-channel combinations"""
        
        # Base performance by audience segment
        base_performance = {
            "eco_conscious_shoppers": {"base_ctr": 0.025, "base_conversion": 0.08, "base_revenue": 2.5},
            "tech_early_adopters": {"base_ctr": 0.035, "base_conversion": 0.12, "base_revenue": 4.0},
            "price_sensitive_buyers": {"base_ctr": 0.020, "base_conversion": 0.06, "base_revenue": 1.8},
            "luxury_seekers": {"base_ctr": 0.015, "base_conversion": 0.15, "base_revenue": 8.0},
            "convenience_seekers": {"base_ctr": 0.030, "base_conversion": 0.10, "base_revenue": 3.0},
            "health_conscious": {"base_ctr": 0.028, "base_conversion": 0.09, "base_revenue": 3.5},
            "business_professionals": {"base_ctr": 0.022, "base_conversion": 0.11, "base_revenue": 5.0},
            "young_families": {"base_ctr": 0.018, "base_conversion": 0.07, "base_revenue": 2.2},
            "seniors": {"base_ctr": 0.012, "base_conversion": 0.05, "base_revenue": 1.5},
            "students": {"base_ctr": 0.040, "base_conversion": 0.04, "base_revenue": 1.0}
        }
        
        # Channel multipliers
        channel_multipliers = {
            "instagram": 1.2, "facebook": 1.0, "linkedin": 0.8, "twitter": 0.6,
            "tiktok": 1.1, "google_display": 0.9, "google_search": 1.3,
            "youtube": 1.0, "pinterest": 0.7, "snapchat": 0.5, "reddit": 0.4,
            "email": 1.5, "sms": 1.8
        }
        
        base = base_performance.get(audience_segment, {"base_ctr": 0.025, "base_conversion": 0.08, "base_revenue": 2.5})
        channel_mult = channel_multipliers.get(channel, 1.0)
        
        # Add some randomness but keep it realistic
        ctr = base["base_ctr"] * channel_mult * random.uniform(0.7, 1.3)
        conversion_rate = base["base_conversion"] * random.uniform(0.8, 1.2)
        revenue_per_impression = base["base_revenue"] * random.uniform(0.6, 1.4)
        
        # Generate impressions (higher for popular channels)
        impressions = random.randint(500, 5000) if channel in ["instagram", "facebook", "google_display"] else random.randint(100, 2000)
        
        clicks = int(impressions * ctr)
        conversions = int(clicks * conversion_rate)
        revenue = impressions * revenue_per_impression
        
        return {
            "impressions": impressions,
            "clicks": clicks,
            "conversions": conversions,
            "revenue": revenue,
            "ctr": ctr,
            "conversion_rate": conversion_rate,
            "revenue_per_impression": revenue_per_impression
        }
    
    def generate_ad_attributes(self, audience_segment: str) -> Dict[str, Any]:
        """Generate realistic ad attributes for an audience segment"""
        
        headlines = self.ad_attributes_templates["headlines"].get(audience_segment, 
            self.ad_attributes_templates["headlines"]["eco_conscious_shoppers"])
        ctas = self.ad_attributes_templates["ctas"].get(audience_segment,
            self.ad_attributes_templates["ctas"]["eco_conscious_shoppers"])
        
        return {
            "headline": random.choice(headlines),
            "cta": random.choice(ctas),
            "tone": random.choice(self.ad_attributes_templates["tones"]),
            "business_type": random.choice(self.business_types),
            "product_category": random.choice(self.product_categories),
            "target_market": audience_segment,
            "created_date": (datetime.now() - timedelta(days=random.randint(1, 90))).isoformat()
        }
    
    async def generate_campaign_data(self, num_campaigns: int = 100):
        """Generate comprehensive campaign data"""
        
        print(f"🚀 Generating {num_campaigns} campaigns with performance data...")
        
        campaign_data = []
        
        for i in range(num_campaigns):
            # Generate random audience and channel
            audience_segment = random.choice(self.audience_segments)
            channel = random.choice(self.channels)
            
            # Generate performance data
            performance = self.generate_realistic_performance_data(audience_segment, channel)
            
            # Generate ad attributes
            ad_attributes = self.generate_ad_attributes(audience_segment)
            
            # Create campaign record
            campaign = {
                "campaign_id": f"campaign_{i+1:03d}",
                "ad_id": f"ad_{i+1:03d}",
                "audience_segment": audience_segment,
                "channel": channel,
                "performance": performance,
                "ad_attributes": ad_attributes,
                "created_date": datetime.now().isoformat()
            }
            
            campaign_data.append(campaign)
            
            # Track performance in recommendation engine
            recommendation_engine.track_ad_performance(
                ad_id=campaign["ad_id"],
                channel=channel,
                audience_segment=audience_segment,
                impressions=performance["impressions"],
                clicks=performance["clicks"],
                conversions=performance["conversions"],
                revenue=performance["revenue"],
                ad_attributes=ad_attributes
            )
            
            if (i + 1) % 20 == 0:
                print(f"  Generated {i+1}/{num_campaigns} campaigns...")
        
        # Save to file for reference
        with open("competition_campaign_data.json", "w") as f:
            json.dump(campaign_data, f, indent=2)
        
        print(f"✅ Generated {num_campaigns} campaigns!")
        print(f"📊 Data saved to competition_campaign_data.json")
        
        return campaign_data
    
    async def generate_high_performance_campaigns(self, num_campaigns: int = 20):
        """Generate high-performing campaigns to show the system learning"""
        
        print(f"🌟 Generating {num_campaigns} high-performance campaigns...")
        
        # High-performing combinations based on our data
        high_performance_combinations = [
            ("tech_early_adopters", "linkedin"),
            ("eco_conscious_shoppers", "instagram"),
            ("luxury_seekers", "email"),
            ("business_professionals", "linkedin"),
            ("convenience_seekers", "google_search"),
            ("health_conscious", "facebook"),
            ("price_sensitive_buyers", "google_display"),
            ("young_families", "facebook"),
            ("students", "tiktok"),
            ("seniors", "email")
        ]
        
        for i in range(num_campaigns):
            audience_segment, channel = random.choice(high_performance_combinations)
            
            # Generate high-performance data
            performance = self.generate_realistic_performance_data(audience_segment, channel)
            
            # Boost performance for these combinations
            performance["ctr"] *= 1.5
            performance["conversion_rate"] *= 1.3
            performance["revenue_per_impression"] *= 1.4
            
            # Recalculate derived metrics
            performance["clicks"] = int(performance["impressions"] * performance["ctr"])
            performance["conversions"] = int(performance["clicks"] * performance["conversion_rate"])
            performance["revenue"] = performance["impressions"] * performance["revenue_per_impression"]
            
            # Generate ad attributes
            ad_attributes = self.generate_ad_attributes(audience_segment)
            
            # Track performance
            recommendation_engine.track_ad_performance(
                ad_id=f"high_perf_ad_{i+1:03d}",
                channel=channel,
                audience_segment=audience_segment,
                impressions=performance["impressions"],
                clicks=performance["clicks"],
                conversions=performance["conversions"],
                revenue=performance["revenue"],
                ad_attributes=ad_attributes
            )
        
        print(f"✅ Generated {num_campaigns} high-performance campaigns!")
    
    async def generate_seasonal_campaigns(self):
        """Generate seasonal campaigns to show context awareness"""
        
        print("🎄 Generating seasonal campaigns...")
        
        seasonal_data = [
            ("eco_conscious_shoppers", "instagram", "Spring Cleaning", "Go Green This Spring", "spring"),
            ("luxury_seekers", "email", "Holiday Collection", "Luxury Holiday Gifts", "winter"),
            ("young_families", "facebook", "Back to School", "Prepare for Success", "fall"),
            ("health_conscious", "google_search", "New Year Resolution", "Start Fresh", "winter"),
            ("price_sensitive_buyers", "google_display", "Black Friday", "Huge Savings", "winter")
        ]
        
        for audience_segment, channel, theme, headline, season in seasonal_data:
            performance = self.generate_realistic_performance_data(audience_segment, channel)
            
            ad_attributes = {
                "headline": headline,
                "cta": f"Shop {theme}",
                "tone": "seasonal",
                "theme": theme,
                "season": season,
                "business_type": "seasonal",
                "product_category": "seasonal"
            }
            
            recommendation_engine.track_ad_performance(
                ad_id=f"seasonal_{season}_{audience_segment}",
                channel=channel,
                audience_segment=audience_segment,
                impressions=performance["impressions"],
                clicks=performance["clicks"],
                conversions=performance["conversions"],
                revenue=performance["revenue"],
                ad_attributes=ad_attributes
            )
        
        print("✅ Generated seasonal campaigns!")
    
    async def run_full_data_generation(self):
        """Run complete data generation for competition"""
        
        print("🎯 Generating comprehensive competition data...")
        print("=" * 50)
        
        # Generate base campaigns
        await self.generate_campaign_data(100)
        
        # Generate high-performance campaigns
        await self.generate_high_performance_campaigns(20)
        
        # Generate seasonal campaigns
        await self.generate_seasonal_campaigns()
        
        print("=" * 50)
        print("📊 Data Generation Complete!")
        print("=" * 50)
        
        # Show summary
        insights = recommendation_engine.get_performance_insights()
        
        print(f"📈 Total Campaigns: {len(insights['best_performing_ads'])}")
        print(f"📊 Total Impressions: {insights['overall_metrics']['total_impressions']:,}")
        print(f"💰 Total Revenue: ${insights['overall_metrics']['total_revenue']:,.2f}")
        print(f"🎯 Overall CTR: {insights['overall_metrics']['overall_ctr']:.3f}")
        print(f"🔄 Overall Conversion Rate: {insights['overall_metrics']['overall_conversion_rate']:.3f}")
        
        print("\n🏆 Top Performing Combinations:")
        for i, ad in enumerate(insights['best_performing_ads'][:5], 1):
            print(f"  {i}. {ad['audience_segment']} + {ad['channel']} - Score: {ad['performance_score']:.3f}")
        
        print("\n💡 What's Working Summary:")
        whats_working = recommendation_engine.get_whats_working_summary()
        for rec in whats_working['recommendations']:
            print(f"  - {rec}")
        
        print("\n✅ Competition data ready!")

async def main():
    generator = CompetitionDataGenerator()
    await generator.run_full_data_generation()

if __name__ == "__main__":
    asyncio.run(main())
