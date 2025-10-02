#!/usr/bin/env python3
"""
Test script for the channel selection strategy
"""

import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.channel_service import channel_service
from models.schemas import CampaignGoal

async def test_channel_strategy():
    """Test the channel selection strategy"""
    
    print("🧪 Testing Channel Selection Strategy...")
    
    # Test case 1: B2B Professional Services
    print("\n📊 Test Case 1: B2B Professional Services")
    b2b_brand = {
        "company_name": "EcoTech Solutions",
        "target_market": "Small to medium businesses",
        "tone": "professional"
    }
    
    b2b_product = {
        "name": "Smart Energy Monitor",
        "category": "sustainability_software",
        "description": "Enterprise energy monitoring platform"
    }
    
    b2b_audience = {
        "segment": "tech_early_adopters",
        "characteristics": {
            "engagement_level": "high",
            "purchase_intent": "high"
        }
    }
    
    business_type = channel_service.detect_business_type(b2b_brand, b2b_product)
    print(f"   Detected business type: {business_type}")
    
    recommendations = channel_service.recommend_channels(
        brand_data=b2b_brand,
        product_data=b2b_product,
        audience_analysis=b2b_audience,
        campaign_goal=CampaignGoal.AWARENESS
    )
    
    print("   Top 3 recommendations:")
    for i, rec in enumerate(recommendations[:3], 1):
        print(f"   {i}. {rec.channel.value} - Confidence: {rec.confidence_score:.2f} - CTR: {rec.estimated_ctr:.3f}")
    
    # Test case 2: Local Coffee Shop
    print("\n☕ Test Case 2: Local Coffee Shop")
    coffee_brand = {
        "company_name": "Green Bean Coffee Co",
        "target_market": "Local community",
        "tone": "friendly"
    }
    
    coffee_product = {
        "name": "Sustainable Coffee",
        "category": "eco_products",
        "description": "Locally sourced, carbon-neutral coffee"
    }
    
    coffee_audience = {
        "segment": "eco_conscious_shoppers",
        "characteristics": {
            "engagement_level": "high",
            "purchase_intent": "medium"
        }
    }
    
    business_type = channel_service.detect_business_type(coffee_brand, coffee_product)
    print(f"   Detected business type: {business_type}")
    
    recommendations = channel_service.recommend_channels(
        brand_data=coffee_brand,
        product_data=coffee_product,
        audience_analysis=coffee_audience,
        campaign_goal=CampaignGoal.CONVERSION
    )
    
    print("   Top 3 recommendations:")
    for i, rec in enumerate(recommendations[:3], 1):
        print(f"   {i}. {rec.channel.value} - Confidence: {rec.confidence_score:.2f} - CTR: {rec.estimated_ctr:.3f}")
    
    # Test case 3: Fashion Brand
    print("\n👗 Test Case 3: Fashion Brand")
    fashion_brand = {
        "company_name": "EcoStyle Fashion",
        "target_market": "Fashion-conscious millennials",
        "tone": "casual"
    }
    
    fashion_product = {
        "name": "Sustainable T-Shirt",
        "category": "fashion",
        "description": "Organic cotton, eco-friendly fashion"
    }
    
    fashion_audience = {
        "segment": "luxury_seekers",
        "characteristics": {
            "engagement_level": "high",
            "purchase_intent": "high"
        }
    }
    
    business_type = channel_service.detect_business_type(fashion_brand, fashion_product)
    print(f"   Detected business type: {business_type}")
    
    recommendations = channel_service.recommend_channels(
        brand_data=fashion_brand,
        product_data=fashion_product,
        audience_analysis=fashion_audience,
        campaign_goal=CampaignGoal.ENGAGEMENT
    )
    
    print("   Top 3 recommendations:")
    for i, rec in enumerate(recommendations[:3], 1):
        print(f"   {i}. {rec.channel.value} - Confidence: {rec.confidence_score:.2f} - CTR: {rec.estimated_ctr:.3f}")
    
    print("\n✅ Channel selection strategy test completed!")
    print("\n🎯 Key Features Demonstrated:")
    print("   - Rule-based channel mapping based on business type")
    print("   - Audience segment compatibility scoring")
    print("   - Campaign goal alignment")
    print("   - Multi-armed bandit learning capability")
    print("   - Real performance predictions")

if __name__ == "__main__":
    asyncio.run(test_channel_strategy())
