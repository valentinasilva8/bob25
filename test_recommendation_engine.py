#!/usr/bin/env python3
"""
Test script for the recommendation engine
"""

import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.recommendation_engine import recommendation_engine

async def test_recommendation_engine():
    """Test the recommendation engine with sample data"""
    
    print("🧪 Testing Recommendation Engine...")
    
    # Simulate tracking performance for different ads
    print("\n📊 Simulating ad performance tracking...")
    
    # Track performance for eco_conscious_shoppers on Instagram
    recommendation_engine.track_ad_performance(
        ad_id="ad_001",
        channel="instagram",
        audience_segment="eco_conscious_shoppers",
        impressions=1000,
        clicks=25,
        conversions=3,
        revenue=150.0,
        ad_attributes={
            "headline": "Save the Planet with EcoTech",
            "cta": "Join the Green Revolution",
            "tone": "inspirational"
        }
    )
    
    recommendation_engine.track_ad_performance(
        ad_id="ad_002",
        channel="instagram",
        audience_segment="eco_conscious_shoppers",
        impressions=800,
        clicks=30,
        conversions=4,
        revenue=200.0,
        ad_attributes={
            "headline": "Make a Difference Today",
            "cta": "Start Your Journey",
            "tone": "motivational"
        }
    )
    
    # Track performance for tech_early_adopters on LinkedIn
    recommendation_engine.track_ad_performance(
        ad_id="ad_003",
        channel="linkedin",
        audience_segment="tech_early_adopters",
        impressions=500,
        clicks=15,
        conversions=2,
        revenue=300.0,
        ad_attributes={
            "headline": "Revolutionary Energy Technology",
            "cta": "Learn More",
            "tone": "professional"
        }
    )
    
    recommendation_engine.track_ad_performance(
        ad_id="ad_004",
        channel="linkedin",
        audience_segment="tech_early_adopters",
        impressions=600,
        clicks=20,
        conversions=3,
        revenue=450.0,
        ad_attributes={
            "headline": "Next-Gen Energy Solutions",
            "cta": "Schedule Demo",
            "tone": "technical"
        }
    )
    
    # Track performance for price_sensitive_buyers on Google
    recommendation_engine.track_ad_performance(
        ad_id="ad_005",
        channel="google_display",
        audience_segment="price_sensitive_buyers",
        impressions=2000,
        clicks=40,
        conversions=2,
        revenue=100.0,
        ad_attributes={
            "headline": "Save Money with Smart Energy",
            "cta": "Get 20% Off",
            "tone": "value_focused"
        }
    )
    
    print("✅ Performance data tracked")
    
    # Test ad recommendations
    print("\n🎯 Testing ad recommendations...")
    
    # Get recommendations for eco_conscious_shoppers on Instagram
    recommendations = recommendation_engine.get_recommendations(
        audience_segment="eco_conscious_shoppers",
        channel="instagram",
        limit=3
    )
    
    print(f"Top recommendations for eco_conscious_shoppers on Instagram:")
    for i, rec in enumerate(recommendations, 1):
        print(f"  {i}. Ad {rec['ad_id']} - Score: {rec['performance_score']:.3f}, CTR: {rec['ctr']:.3f}")
        print(f"     Reasoning: {rec['reasoning']}")
    
    # Test channel recommendations
    print("\n📊 Testing channel recommendations...")
    
    channel_recs = recommendation_engine.get_channel_recommendations("eco_conscious_shoppers")
    print(f"Best channels for eco_conscious_shoppers:")
    for i, rec in enumerate(channel_recs, 1):
        print(f"  {i}. {rec['channel']} - Score: {rec['score']:.3f}, CTR: {rec['avg_ctr']:.3f}")
    
    # Test successful patterns
    print("\n🔍 Testing successful patterns...")
    
    patterns = recommendation_engine.get_successful_patterns("eco_conscious_shoppers")
    print(f"Successful patterns for eco_conscious_shoppers:")
    print(f"  Insights: {patterns['insights']}")
    
    # Test overall performance insights
    print("\n📈 Testing performance insights...")
    
    insights = recommendation_engine.get_performance_insights()
    print(f"Overall performance:")
    print(f"  Total impressions: {insights['overall_metrics']['total_impressions']}")
    print(f"  Overall CTR: {insights['overall_metrics']['overall_ctr']:.3f}")
    print(f"  Overall conversion rate: {insights['overall_metrics']['overall_conversion_rate']:.3f}")
    
    print(f"Best performing ads:")
    for i, ad in enumerate(insights['best_performing_ads'][:3], 1):
        print(f"  {i}. Ad {ad['ad_id']} - {ad['channel']} - {ad['audience_segment']} - Score: {ad['performance_score']:.3f}")
    
    # Test what's working summary
    print("\n💡 Testing what's working summary...")
    
    summary = recommendation_engine.get_whats_working_summary()
    print(f"What's working:")
    print(f"  Summary: {summary['summary']}")
    print(f"  Top combinations:")
    for combo in summary['best_combinations'][:3]:
        print(f"    - {combo['combination']} - Score: {combo['performance_score']:.3f}")
    
    print(f"  Recommendations:")
    for rec in summary['recommendations']:
        print(f"    - {rec}")
    
    print("\n✅ Recommendation engine test completed!")
    print("\n🎯 Key Features Demonstrated:")
    print("   - Ad performance tracking and scoring")
    print("   - Audience-specific ad recommendations")
    print("   - Channel performance analysis")
    print("   - Successful pattern identification")
    print("   - Overall performance insights")
    print("   - What's working summary")

if __name__ == "__main__":
    asyncio.run(test_recommendation_engine())
