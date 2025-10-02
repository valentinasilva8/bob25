#!/usr/bin/env python3
"""
Simple script to view generated ads from EcoAd AI
"""

import requests
import json
import sys

def get_ad(ad_id):
    """Get a specific ad by ID"""
    try:
        response = requests.get(f"http://localhost:8000/generate/ad/{ad_id}")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error getting ad {ad_id}: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error connecting to server: {e}")
        return None

def display_ad(ad_data, ad_number):
    """Display an ad in a nice format"""
    if not ad_data:
        return
    
    print(f"\n{'='*60}")
    print(f"🎯 AD #{ad_number} - {ad_data['campaign_goal'].upper()} CAMPAIGN")
    print(f"{'='*60}")
    
    # Ad content
    print(f"\n📝 HEADLINE:")
    print(f"   \"{ad_data['headline']}\"")
    
    print(f"\n📄 BODY TEXT:")
    print(f"   \"{ad_data['body']}\"")
    
    print(f"\n🔘 CALL-TO-ACTION:")
    print(f"   \"{ad_data['cta']}\"")
    
    # Targeting info
    print(f"\n🎯 TARGETING:")
    print(f"   Audience: {ad_data['audience_segment']}")
    print(f"   Device: {ad_data['context_signals']['device_type']}")
    print(f"   Time: {ad_data['context_signals']['time_of_day']}")
    print(f"   Page: {ad_data['context_signals'].get('page_category', 'N/A')}")
    
    # Performance metrics
    print(f"\n📊 METRICS:")
    print(f"   Energy: {ad_data['energy_consumed']} kWh")
    print(f"   CO2: {ad_data['co2_emissions']} kg")
    print(f"   Created: {ad_data['created_at']}")
    
    # Visual preview
    print(f"\n🎨 VISUAL PREVIEW:")
    print(f"   ┌{'─'*40}┐")
    print(f"   │ {'🌱 ' + ad_data['headline']:<36} │")
    print(f"   │ {'':<40} │")
    print(f"   │ {ad_data['body']:<38} │")
    print(f"   │ {'':<40} │")
    print(f"   │ [ {ad_data['cta']} ]{'':<30} │")
    print(f"   └{'─'*40}┘")

def main():
    print("🌱 EcoAd AI - Generated Ads Viewer")
    print("="*50)
    
    # Check server connection
    try:
        health = requests.get("http://localhost:8000/health")
        if health.status_code != 200:
            print("❌ Server is not running. Please start it with: python3 main.py")
            return
    except:
        print("❌ Cannot connect to server. Please start it with: python3 main.py")
        return
    
    print("✅ Server is running!")
    
    # Try to get ads
    ad_ids = ["ad_1", "ad_2"]
    found_ads = []
    
    for ad_id in ad_ids:
        ad_data = get_ad(ad_id)
        if ad_data:
            found_ads.append((ad_id, ad_data))
    
    if not found_ads:
        print("\n❌ No ads found. Let me generate some for you...")
        
        # Generate a sample ad
        print("\n🔄 Generating sample ad...")
        try:
            response = requests.post("http://localhost:8000/generate/ad", 
                json={
                    "brand_id": "brand_1",
                    "product_id": "product_1", 
                    "audience_segment": "eco_conscious_business_owners",
                    "context_signals": {
                        "device_type": "desktop",
                        "time_of_day": "morning",
                        "page_category": "sustainability"
                    },
                    "campaign_goal": "conversion",
                    "include_image": False
                })
            
            if response.status_code == 200:
                ad_data = response.json()
                found_ads.append(("new_ad", ad_data))
                print("✅ Sample ad generated!")
            else:
                print(f"❌ Error generating ad: {response.status_code}")
                return
        except Exception as e:
            print(f"❌ Error generating ad: {e}")
            return
    
    # Display all found ads
    for i, (ad_id, ad_data) in enumerate(found_ads, 1):
        display_ad(ad_data, i)
    
    print(f"\n{'='*60}")
    print("🎉 View complete! You can also:")
    print("   • Open dashboard.html in your browser")
    print("   • Visit http://localhost:8000/docs for API docs")
    print("   • Use curl commands to get specific ads")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
