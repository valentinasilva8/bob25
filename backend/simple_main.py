#!/usr/bin/env python3
"""
Simplified FastAPI server without power tracking
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
import json
import sys

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load ad templates dataset
def load_ad_templates():
    with open('customer_dataset/ad_templates.json', 'r') as f:
        return json.load(f)

# Load demo companies dataset
def load_demo_companies():
    with open('backend/demo_companies.json', 'r') as f:
        return json.load(f)

def calculate_environmental_impact(base_impact, creatives_per_week):
    """Calculate environmental impact based on creatives per week"""
    # Parse creatives per week to get a number
    if creatives_per_week == "1-2":
        multiplier = 1.5
    elif creatives_per_week == "3-5":
        multiplier = 3.0
    elif creatives_per_week == "6-10":
        multiplier = 6.0
    elif creatives_per_week == "11-20":
        multiplier = 12.0
    elif creatives_per_week == "20+":
        multiplier = 25.0
    else:
        multiplier = 1.0
    
    # Adjust the environmental metrics
    adjusted_impact = {
        "total_ads_generated": int(base_impact["total_ads_generated"] * multiplier),
        "total_energy_kwh": round(base_impact["total_energy_kwh"] * multiplier, 3),
        "total_co2_kg": round(base_impact["total_co2_kg"] * multiplier, 4),
        "carbon_efficiency": base_impact["carbon_efficiency"],
        "green_score": max(60, base_impact["green_score"] - (multiplier - 1) * 5)  # Slightly lower score for higher volume
    }
    
    return adjusted_impact

# Smart ad generation functions
def determine_segment(age_range: str, interests: list, audience: str) -> str:
    """Determine the best segment based on user inputs"""
    interests_lower = [i.lower() for i in interests]
    audience_lower = audience.lower()
    
    # Check for specific keywords
    if any(word in audience_lower for word in ['pregnant', 'expecting', 'prenatal']):
        return 'prenatal'
    
    if any(word in audience_lower for word in ['busy', 'professional', 'work', 'office']):
        return 'busy_pros'
    
    if any(word in audience_lower for word in ['student', 'teacher', 'academic', 'school']):
        return 'students_teachers'
    
    if any(word in audience_lower for word in ['recovery', 'injury', 'gentle', 'low impact']):
        return 'recovery_low_impact'
    
    if any(word in interests_lower for word in ['beginner', 'new', 'start', 'first time']):
        return 'new_to_yoga'
    
    # Default based on age
    if age_range:
        try:
            age = int(age_range.split('-')[0])
            if age < 25:
                return 'students_teachers'
            elif age > 50:
                return 'recovery_low_impact'
        except:
            pass
    
    # Default to new_to_yoga for wellness businesses
    return 'new_to_yoga'

def get_neighborhood(zipcode: str, templates: dict) -> str:
    """Get neighborhood name from zipcode"""
    return templates['neighborhoods'].get(zipcode, f"Area {zipcode}")

def generate_smart_ads(business_name: str, mission: str, products: str, 
                      audience: str, zipcode: str, age_range: str, 
                      interests: list, preferred_channels: list) -> list:
    """Generate smart personalized ads using dataset templates"""
    
    templates = load_ad_templates()
    segment = determine_segment(age_range, interests, audience)
    neighborhood = get_neighborhood(zipcode, templates)
    
    # Get examples for this segment
    segment_data = templates['segments'][segment]
    examples = segment_data['examples']
    
    # Find examples that match the neighborhood or use any example
    matching_examples = [ex for ex in examples if ex['neighborhood'] == neighborhood]
    if not matching_examples:
        matching_examples = examples
    
    ads = []
    
    # Ad 1: Use the best matching example
    base_ad = matching_examples[0]  # Use first matching example
    ads.append({
        "id": "ad_1",
        "headline": base_ad['headline'].replace(neighborhood, neighborhood),
        "body": base_ad['body'],
        "cta": base_ad['cta'],
        "audience_segment": segment,
        "energy_consumed": 0.001,
        "co2_emissions": 0.0002,
        "personalization_type": "segment_based"
    })
    
    # Ad 2: Mission-focused with segment tone
    if mission:
        mission_words = mission.split()[:8]  # First 8 words
        headline = f"{' '.join(mission_words)} in {neighborhood}"
        body = f"{mission[:100]}... {segment_data['key_messages'][0]}. Join our {neighborhood} community."
        ads.append({
            "id": "ad_2",
            "headline": headline,
            "body": body,
            "cta": "Learn More",
            "audience_segment": f"{segment}_mission",
            "energy_consumed": 0.001,
            "co2_emissions": 0.0002,
            "personalization_type": "mission_based"
        })
    
    # Ad 3: Product-focused with interests
    if products and interests:
        product_words = products.split()[:6]
        interest_text = ', '.join(interests[:2])
        headline = f"{' '.join(product_words)} for {interest_text} Lovers"
        body = f"Perfect for {age_range} year olds who love {interest_text}. {products[:80]}... Join us in {neighborhood}."
        ads.append({
            "id": "ad_3",
            "headline": headline,
            "body": body,
            "cta": "Explore Classes",
            "audience_segment": f"{segment}_product",
            "energy_consumed": 0.001,
            "co2_emissions": 0.0002,
            "personalization_type": "product_based"
        })
    
    return ads

# Simple mock database
mock_data = {
    "brands": {},
    "products": {},
    "audience": {},
    "ads": {}
}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting Awe Agency Backend...")
    yield
    # Shutdown
    print("🛑 Shutting down...")

app = FastAPI(
    title="Awe Agency Backend",
    description="AI-powered adtech platform for personalized, sustainable advertising",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Awe Agency Backend API",
        "version": "1.0.0",
        "status": "active"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "carbon_tracking": True
    }

@app.get("/business/wellness/businesses")
async def get_wellness_businesses():
    """Get list of available demo businesses for registration"""
    try:
        demo_data = load_demo_companies()
        companies = demo_data.get('companies', {})
        
        return {
            "businesses": [
                {
                    "name": company_data['business_name'],
                    "mission": company_data['mission'][:100] + "...",
                    "category": "wellness",
                    "zipcode": company_data['zipcode'],
                    "age_range": company_data['age_range']
                }
                for company_data in companies.values()
            ],
            "total": len(companies),
            "demo_companies": list(companies.keys())
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading demo businesses: {str(e)}")

@app.post("/business/register/wellness")
async def register_wellness_business(request: dict):
    """Register wellness business with demo data lookup"""
    try:
        # Extract business name and creatives per week from frontend
        business_name = request.get('business_name', '')
        creatives_per_week = request.get('creatives_per_week', '1-2')
        
        print(f"DEBUG: Looking up demo data for: {business_name}")
        print(f"DEBUG: Creatives per week: {creatives_per_week}")
        
        # Load demo companies
        demo_data = load_demo_companies()
        companies = demo_data.get('companies', {})
        
        # Check if this is a demo company (case-insensitive)
        business_name_lower = business_name.lower()
        matching_company = None
        for company_name, company_data in companies.items():
            if company_name.lower() == business_name_lower:
                matching_company = company_name
                break
        
        if matching_company:
            print(f"DEBUG: Found demo data for {business_name} (matched: {matching_company})")
            company_data = companies[matching_company]
            
            # Calculate environmental impact based on creatives per week
            adjusted_environmental_impact = calculate_environmental_impact(
                company_data['environmental_impact'], 
                creatives_per_week
            )
            
            return {
                "registration_id": f"reg_{business_name.lower().replace(' ', '_')}_{company_data['zipcode']}",
                "brand": {
                    "id": "brand_1",
                    "company_name": company_data['business_name'],
                    "mission": company_data['mission'],
                    "tone": "warm, welcoming, community-first"
                },
                "products": [{
                    "id": "product_1",
                    "name": "Wellness Services",
                    "description": company_data['products'],
                    "category": "wellness"
                }],
                "audience": [{
                    "id": "audience_1",
                    "user_id": "wellness_user_1",
                    "segment": "wellness_seeker",
                    "clicks_last_30d": 8,
                    "purchases_last_90d": 2
                }],
                "initial_ads": company_data['generated_ads'],
                "channel_recommendations": company_data['channel_recommendations'],
                "environmental_impact": adjusted_environmental_impact,
                # Include frontend inputs in response for display
                "zipcode": company_data['zipcode'],
                "age_range": company_data['age_range'],
                "interests": company_data['interests'],
                "preferred_channels": company_data['preferred_channels'],
                "creatives_per_week": creatives_per_week
            }
        else:
            # For non-demo companies, return a generic response
            print(f"DEBUG: No demo data found for {business_name}, returning generic response")
            return {
                "registration_id": f"reg_{business_name.lower().replace(' ', '_')}_generic",
                "brand": {
                    "id": "brand_1",
                    "company_name": business_name,
                    "mission": request.get('mission', 'Your business mission'),
                    "tone": "warm, welcoming, community-first"
                },
                "products": [{
                    "id": "product_1",
                    "name": "Wellness Services",
                    "description": request.get('products', 'Your products and services'),
                    "category": "wellness"
                }],
                "audience": [{
                    "id": "audience_1",
                    "user_id": "wellness_user_1",
                    "segment": "wellness_seeker",
                    "clicks_last_30d": 8,
                    "purchases_last_90d": 2
                }],
                "initial_ads": [
                    {
                        "id": "ad_1",
                        "headline": f"Welcome to {business_name}",
                        "body": "Discover our wellness services designed just for you. Join our community today!",
                        "cta": "Learn More",
                        "audience_segment": "general_wellness",
                        "energy_consumed": 0.001,
                        "co2_emissions": 0.0002,
                        "personalization_type": "generic"
                    }
                ],
                "channel_recommendations": {
                    "best_channel": "facebook_local",
                    "total_confidence": 0.8,
                    "recommendations": [
                        {
                            "channel": "facebook_local",
                            "confidence": 0.8,
                            "reason": "Great for local business promotion",
                            "priority": "High"
                        }
                    ]
                },
                "environmental_impact": calculate_environmental_impact({
                    "total_ads_generated": 1,
                    "total_energy_kwh": 0.001,
                    "total_co2_kg": 0.0002,
                    "carbon_efficiency": "90% reduction vs traditional AI",
                    "green_score": 90.0
                }, creatives_per_week),
                # Include frontend inputs in response for display
                "zipcode": request.get('zipcode', 'Not specified'),
                "age_range": request.get('age_range', 'Not specified'),
                "interests": request.get('interests', []),
                "preferred_channels": request.get('preferred_channels', []),
                "creatives_per_week": creatives_per_week
            }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error registering wellness business: {str(e)}")

@app.post("/generate/ad")
async def generate_ad(request: dict):
    """Generate personalized ad"""
    try:
        brand_id = request.get('brand_id', 'brand_1')
        audience_segment = request.get('audience_segment', 'wellness_seeker')
        
        # Generate mock ad
        ad_id = f"ad_{len(mock_data['ads']) + 1}"
        ad = {
            "id": ad_id,
            "brand_id": brand_id,
            "headline": f"Personalized Ad for {audience_segment}",
            "body": "This is a personalized ad generated by our AI system.",
            "cta": "Learn More",
            "audience_segment": audience_segment,
            "energy_consumed": 0.001,
            "co2_emissions": 0.0002,
            "created_at": "2024-01-01T00:00:00Z"
        }
        
        mock_data['ads'][ad_id] = ad
        
        return ad
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating ad: {str(e)}")

@app.post("/recommend/channel")
async def recommend_channel(request: dict):
    """Get channel recommendations"""
    try:
        brand_id = request.get('brand_id', 'brand_1')
        audience_segment = request.get('audience_segment', 'wellness_seeker')
        
        return {
            "recommendations": [
                {
                    "channel": "facebook_local",
                    "confidence": 0.85,
                    "reasoning": "Great for local wellness businesses"
                },
                {
                    "channel": "instagram_stories",
                    "confidence": 0.75,
                    "reasoning": "Perfect for visual wellness content"
                }
            ],
            "best_channel": "facebook_local",
            "total_confidence": 0.85
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting channel recommendations: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    print("🌱 Starting Awe Agency Backend (Simplified)")
    print("📍 Backend will run on http://localhost:8002")
    print("📚 API docs available at http://localhost:8002/docs")
    uvicorn.run(app, host="0.0.0.0", port=8002)
