"""
Simple test script for the EcoAd AI API
"""

import requests
import json
from sample_data import SAMPLE_BRAND, SAMPLE_PRODUCTS, SAMPLE_AUDIENCE, SAMPLE_CONTEXT_SIGNALS

BASE_URL = "http://localhost:8000"

def test_api():
    """Test the API endpoints"""
    
    print("🧪 Testing EcoAd AI API...")
    
    # Test 1: Health check
    print("\n1. Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✅ Health check: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return
    
    # Test 2: Upload brand
    print("\n2. Testing brand upload...")
    try:
        response = requests.post(f"{BASE_URL}/upload/brand", json=SAMPLE_BRAND)
        if response.status_code == 200:
            brand_data = response.json()
            brand_id = brand_data["id"]
            print(f"✅ Brand uploaded: {brand_id}")
        else:
            print(f"❌ Brand upload failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return
    except Exception as e:
        print(f"❌ Brand upload failed: {e}")
        return
    
    # Test 3: Upload products
    print("\n3. Testing product upload...")
    try:
        for product in SAMPLE_PRODUCTS:
            product["brand_id"] = brand_id
            response = requests.post(
                f"{BASE_URL}/upload/products",
                data={"brand_id": brand_id, "products_json": json.dumps([product])}
            )
            if response.status_code == 200:
                products = response.json()
                product_id = products[0]["id"] if products else None
                print(f"✅ Product uploaded: {product_id}")
                break
            else:
                print(f"❌ Product upload failed: {response.status_code}")
                print(f"   Error: {response.text}")
                return
    except Exception as e:
        print(f"❌ Product upload failed: {e}")
        return
    
    # Test 4: Upload audience
    print("\n4. Testing audience upload...")
    try:
        for audience in SAMPLE_AUDIENCE:
            audience["brand_id"] = brand_id
            response = requests.post(
                f"{BASE_URL}/upload/audience",
                data={"brand_id": brand_id, "audience_json": json.dumps([audience])}
            )
            if response.status_code == 200:
                audience_data = response.json()
                print(f"✅ Audience uploaded: {len(audience_data)} members")
                break
            else:
                print(f"❌ Audience upload failed: {response.status_code}")
                print(f"   Error: {response.text}")
                return
    except Exception as e:
        print(f"❌ Audience upload failed: {e}")
        return
    
    # Test 5: Generate ad
    print("\n5. Testing ad generation...")
    try:
        ad_request = {
            "brand_id": brand_id,
            "product_id": product_id,
            "audience_segment": "eco_conscious_business_owners",
            "context_signals": SAMPLE_CONTEXT_SIGNALS,
            "campaign_goal": "conversion",
            "include_image": True
        }
        
        response = requests.post(f"{BASE_URL}/generate/ad", json=ad_request)
        if response.status_code == 200:
            ad_data = response.json()
            ad_id = ad_data["id"]
            print(f"✅ Ad generated: {ad_id}")
            print(f"   Headline: {ad_data['headline']}")
            print(f"   Body: {ad_data['body']}")
            print(f"   CTA: {ad_data['cta']}")
            print(f"   Energy consumed: {ad_data['energy_consumed']:.6f} kWh")
            print(f"   CO2 emissions: {ad_data['co2_emissions']:.6f} kg")
        else:
            print(f"❌ Ad generation failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return
    except Exception as e:
        print(f"❌ Ad generation failed: {e}")
        return
    
    # Test 6: Channel recommendation
    print("\n6. Testing channel recommendation...")
    try:
        rec_request = {
            "brand_id": brand_id,
            "product_id": product_id,
            "audience_segment": "eco_conscious_business_owners",
            "campaign_goal": "conversion",
            "budget": 1000
        }
        
        response = requests.post(f"{BASE_URL}/recommend/channel", json=rec_request)
        if response.status_code == 200:
            rec_data = response.json()
            print(f"✅ Channel recommendations generated")
            print(f"   Best channel: {rec_data['best_channel']}")
            print(f"   Total confidence: {rec_data['total_confidence']:.2f}")
            for rec in rec_data['recommendations'][:3]:  # Show top 3
                print(f"   - {rec['channel']}: {rec['confidence_score']:.2f} confidence")
        else:
            print(f"❌ Channel recommendation failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Channel recommendation failed: {e}")
    
    # Test 7: Sustainability metrics
    print("\n7. Testing sustainability metrics...")
    try:
        response = requests.get(f"{BASE_URL}/sustainability/metrics")
        if response.status_code == 200:
            metrics = response.json()
            print(f"✅ Sustainability metrics retrieved")
            print(f"   Total energy: {metrics['total_energy_consumed']:.6f} kWh")
            print(f"   Total CO2: {metrics['total_co2_emissions']:.6f} kg")
            print(f"   Cache hits: {metrics['cache_hits']}")
            print(f"   Green scheduled jobs: {metrics['green_scheduled_jobs']}")
        else:
            print(f"❌ Sustainability metrics failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Sustainability metrics failed: {e}")
    
    # Test 8: Submit feedback
    print("\n8. Testing feedback submission...")
    try:
        feedback_data = {
            "ad_id": ad_id,
            "channel": "linkedin",
            "clicks": 45,
            "impressions": 2500,
            "conversions": 8,
            "spend": 150.00,
            "feedback_notes": "Great performance on LinkedIn!"
        }
        
        response = requests.post(f"{BASE_URL}/feedback/", json=feedback_data)
        if response.status_code == 200:
            feedback = response.json()
            print(f"✅ Feedback submitted: {feedback['id']}")
            print(f"   CTR: {feedback['ctr']:.4f}")
            print(f"   Conversion rate: {feedback['conversion_rate']:.4f}")
        else:
            print(f"❌ Feedback submission failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Feedback submission failed: {e}")
    
    print("\n🎉 API testing completed!")

if __name__ == "__main__":
    test_api()
