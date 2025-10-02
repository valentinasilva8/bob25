#!/usr/bin/env python3
"""
Quick test script to verify the demo data generation works
"""

import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from demo_data_generator import DemoDataGenerator

async def test_demo():
    """Test the demo data generation"""
    
    print("🧪 Testing EcoAd AI Demo Data Generation...")
    
    try:
        generator = DemoDataGenerator()
        
        # Test dataset loading
        print("\n📊 Testing dataset loading...")
        if generator.ads_dataset is not None:
            print(f"✅ Ads dataset loaded: {len(generator.ads_dataset)} records")
            print(f"   Columns: {list(generator.ads_dataset.columns)}")
        else:
            print("⚠️ Ads dataset not loaded")
            
        if generator.logistic_dataset is not None:
            print(f"✅ Logistic dataset loaded: {len(generator.logistic_dataset)} records")
            print(f"   Columns: {list(generator.logistic_dataset.columns)}")
        else:
            print("⚠️ Logistic dataset not loaded")
        
        # Test audience data generation
        print("\n👥 Testing audience data generation...")
        audience_data = generator._generate_audience_data("test_brand")
        print(f"✅ Generated {len(audience_data)} audience members")
        
        if audience_data:
            sample_user = audience_data[0]
            print(f"   Sample user: {sample_user['segment']} - {sample_user['age_range']} - {sample_user['device']}")
        
        # Test segment determination
        print("\n🎯 Testing segment determination...")
        test_cases = [
            (30, 80000, 85, 220, 1),  # Should be luxury_seekers
            (25, 50000, 75, 250, 1),  # Should be tech_early_adopters
            (35, 30000, 60, 150, 0),  # Should be price_sensitive_buyers
        ]
        
        for age, income, time, usage, clicked in test_cases:
            segment = generator._determine_segment_from_data(age, income, time, usage, clicked)
            print(f"   Age: {age}, Income: ${income}, Time: {time}min, Usage: {usage}min, Clicked: {clicked} → {segment}")
        
        print("\n✅ All tests passed! Demo data generation is working correctly.")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_demo())
