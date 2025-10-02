from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from datetime import datetime

from models.schemas import (
    AdGenerationRequest, AdResponse, ContextSignals
)
from services.database import db
from services.ai_service import ai_service
from services.carbon_tracker import carbon_tracker
from services.ab_testing import ab_testing_service

router = APIRouter()

@router.post("/ad", response_model=AdResponse)
async def generate_ad(request: AdGenerationRequest):
    """Generate personalized ad copy and image"""
    
    try:
        # Get brand data
        brand = await db.get_brand(request.brand_id)
        if not brand:
            raise HTTPException(status_code=404, detail="Brand not found")
        
        # Get product data
        products = await db.get_products_by_brand(request.brand_id)
        product = next((p for p in products if p['id'] == request.product_id), None)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Get audience data for the segment
        audience_data = await db.get_audience_by_brand(request.brand_id)
        segment_audience = [a for a in audience_data if a['segment'] == request.audience_segment]
        
        if not segment_audience:
            raise HTTPException(status_code=404, detail=f"No audience data found for segment: {request.audience_segment}")
        
        # Analyze audience segment
        audience_analysis = await ai_service.analyze_audience_segment(segment_audience)
        
        # Check for cache hit (simplified - in production, implement proper caching)
        cache_key = f"{request.brand_id}_{request.product_id}_{request.audience_segment}_{hash(str(request.context_signals))}"
        cache_hit = False  # TODO: Implement proper caching mechanism
        
        # Track energy consumption
        energy_data = carbon_tracker.track_generation("gpt-4o-mini", cache_hit=cache_hit)
        
        if cache_hit:
            carbon_tracker.track_inference_reuse()
        
        # Generate ad copy
        ad_copy = await ai_service.generate_ad_copy(
            brand_data=brand,
            product_data=product,
            audience_data=audience_analysis,
            context_signals=request.context_signals,
            campaign_goal=request.campaign_goal.value
        )
        
        # Generate image if requested
        image_url = None
        if request.include_image:
            image_energy = carbon_tracker.track_generation("dall-e", cache_hit=cache_hit)
            energy_data["energy"] += image_energy["energy"]
            energy_data["co2"] += image_energy["co2"]
            
            image_url = await ai_service.generate_ad_image(
                headline=ad_copy["headline"],
                product_name=product["name"],
                brand_tone=brand["tone"],
                context_signals=request.context_signals
            )
        
        # Create ad record
        ad_data = {
            "brand_id": request.brand_id,
            "product_id": request.product_id,
            "headline": ad_copy["headline"],
            "body": ad_copy["body"],
            "cta": ad_copy["cta"],
            "image_url": image_url,
            "audience_segment": request.audience_segment,
            "context_signals": request.context_signals,
            "campaign_goal": request.campaign_goal.value,
            "energy_consumed": energy_data["energy"],
            "co2_emissions": energy_data["co2"],
            "created_at": datetime.now().isoformat()
        }
        
        # Store ad in database
        result = await db.create_ad(ad_data)
        if not result:
            raise HTTPException(status_code=500, detail="Failed to create ad")
        
        return AdResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating ad: {str(e)}")

@router.get("/ad/{ad_id}", response_model=AdResponse)
async def get_ad(ad_id: str):
    """Get generated ad by ID"""
    
    try:
        ad = await db.get_ad(ad_id)
        if not ad:
            raise HTTPException(status_code=404, detail="Ad not found")
        
        return AdResponse(**ad)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving ad: {str(e)}")

@router.post("/ad/batch", response_model=List[AdResponse])
async def generate_ads_batch(requests: list[AdGenerationRequest]):
    """Generate multiple ads in batch for efficiency"""
    
    try:
        results = []
        
        for request in requests:
            try:
                ad = await generate_ad(request)
                results.append(ad)
            except Exception as e:
                # Log error but continue with other ads
                print(f"Error generating ad for request {request}: {e}")
                continue
        
        return results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating ads batch: {str(e)}")

@router.get("/ad/brand/{brand_id}", response_model=List[AdResponse])
async def get_ads_by_brand(brand_id: str):
    """Get all ads for a brand"""
    
    try:
        # This would require adding a method to get ads by brand
        # For now, return empty list
        return []
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving ads: {str(e)}")

@router.post("/ad/refresh/{ad_id}", response_model=AdResponse)
async def refresh_ad(ad_id: str, context_signals: Dict[str, Any]):
    """Refresh an existing ad with new context signals"""
    
    try:
        # Get existing ad
        existing_ad = await db.get_ad(ad_id)
        if not existing_ad:
            raise HTTPException(status_code=404, detail="Ad not found")
        
        # Create new generation request with updated context
        request = AdGenerationRequest(
            brand_id=existing_ad["brand_id"],
            product_id=existing_ad["product_id"],
            audience_segment=existing_ad["audience_segment"],
            context_signals=context_signals,
            campaign_goal=existing_ad["campaign_goal"],
            include_image=bool(existing_ad.get("image_url"))
        )
        
        # Generate refreshed ad
        refreshed_ad = await generate_ad(request)
        
        return refreshed_ad
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error refreshing ad: {str(e)}")

# A/B Testing Endpoints
@router.post("/ab-test/create")
async def create_ab_test(
    test_name: str,
    ad_id: str,
    test_type: str = "headline",
    traffic_split: float = 0.5
):
    """Create an A/B test for an existing ad"""
    
    try:
        # Get the base ad
        base_ad = await db.get_ad(ad_id)
        if not base_ad:
            raise HTTPException(status_code=404, detail="Ad not found")
        
        # Create A/B test
        test_config = ab_testing_service.create_test(
            test_name=test_name,
            base_ad=base_ad,
            test_type=test_type,
            traffic_split=traffic_split
        )
        
        return {
            "message": "A/B test created successfully",
            "test_id": test_config["test_id"],
            "test_name": test_config["test_name"],
            "variants": len(test_config["variants"]),
            "traffic_split": traffic_split
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating A/B test: {str(e)}")

@router.get("/ab-test/{test_id}/variant")
async def get_test_variant(test_id: str, user_id: str):
    """Get variant for a specific user in an A/B test"""
    
    try:
        variant = ab_testing_service.get_variant_for_user(test_id, user_id)
        if not variant:
            raise HTTPException(status_code=404, detail="Test not found")
        
        return {
            "test_id": test_id,
            "user_id": user_id,
            "variant": variant
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting test variant: {str(e)}")

@router.post("/ab-test/{test_id}/impression")
async def record_impression(test_id: str, variant_id: str, user_id: str):
    """Record an impression for a test variant"""
    
    try:
        ab_testing_service.record_impression(test_id, variant_id, user_id)
        return {"message": "Impression recorded successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error recording impression: {str(e)}")

@router.post("/ab-test/{test_id}/click")
async def record_click(test_id: str, variant_id: str, user_id: str):
    """Record a click for a test variant"""
    
    try:
        ab_testing_service.record_click(test_id, variant_id, user_id)
        return {"message": "Click recorded successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error recording click: {str(e)}")

@router.post("/ab-test/{test_id}/conversion")
async def record_conversion(test_id: str, variant_id: str, user_id: str, revenue: float = 0.0):
    """Record a conversion for a test variant"""
    
    try:
        ab_testing_service.record_conversion(test_id, variant_id, user_id, revenue)
        return {"message": "Conversion recorded successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error recording conversion: {str(e)}")

@router.get("/ab-test/{test_id}/results")
async def get_test_results(test_id: str):
    """Get results for an A/B test"""
    
    try:
        results = ab_testing_service.get_test_results(test_id)
        if not results:
            raise HTTPException(status_code=404, detail="Test not found")
        
        return results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting test results: {str(e)}")

@router.post("/ab-test/{test_id}/end")
async def end_test(test_id: str):
    """End an A/B test and get final results"""
    
    try:
        results = ab_testing_service.end_test(test_id)
        if not results:
            raise HTTPException(status_code=404, detail="Test not found")
        
        return {
            "message": "Test ended successfully",
            "results": results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error ending test: {str(e)}")

@router.get("/ab-test/all")
async def get_all_tests():
    """Get all active A/B tests"""
    
    try:
        tests = ab_testing_service.get_all_tests()
        return {"tests": tests}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting tests: {str(e)}")
