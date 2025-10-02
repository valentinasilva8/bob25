from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import List, Optional
import pandas as pd
import json
import io
from datetime import datetime

from models.schemas import (
    BrandUpload, BrandResponse, ProductUpload, ProductResponse,
    AudienceUpload, AudienceResponse
)
from services.database import db
from services.carbon_tracker import carbon_tracker

router = APIRouter()

@router.post("/brand", response_model=BrandResponse)
async def upload_brand(brand_data: BrandUpload):
    """Upload brand information and company story"""
    
    try:
        # Track energy for this operation
        energy_data = carbon_tracker.track_generation("gpt-4o-mini", cache_hit=False)
        
        # Convert to dict for database storage
        brand_dict = brand_data.dict()
        brand_dict["created_at"] = datetime.now().isoformat()
        
        # Store in database
        result = await db.create_brand(brand_dict)
        
        if not result:
            raise HTTPException(status_code=500, detail="Failed to create brand")
        
        return BrandResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading brand: {str(e)}")

@router.post("/products", response_model=List[ProductResponse])
async def upload_products(
    brand_id: str = Form(...),
    file: Optional[UploadFile] = File(None),
    products_json: Optional[str] = Form(None)
):
    """Upload product information via CSV or JSON"""
    
    try:
        # Track energy for this operation
        energy_data = carbon_tracker.track_generation("gpt-4o-mini", cache_hit=False)
        
        products_data = []
        
        if file and file.filename.endswith('.csv'):
            # Process CSV file
            content = await file.read()
            df = pd.read_csv(io.StringIO(content.decode('utf-8')))
            
            for _, row in df.iterrows():
                product_data = {
                    "brand_id": brand_id,
                    "name": str(row.get('name', '')),
                    "description": str(row.get('description', '')),
                    "category": str(row.get('category', '')),
                    "price": float(row.get('price', 0)) if pd.notna(row.get('price')) else None,
                    "features": str(row.get('features', '')).split(',') if pd.notna(row.get('features')) else [],
                    "benefits": str(row.get('benefits', '')).split(',') if pd.notna(row.get('benefits')) else [],
                    "sustainability_benefits": str(row.get('sustainability_benefits', '')).split(',') if pd.notna(row.get('sustainability_benefits')) else None,
                    "created_at": datetime.now().isoformat()
                }
                products_data.append(product_data)
        
        elif products_json:
            # Process JSON data
            products_list = json.loads(products_json)
            
            for product in products_list:
                product_data = {
                    "brand_id": brand_id,
                    "name": product.get('name', ''),
                    "description": product.get('description', ''),
                    "category": product.get('category', ''),
                    "price": product.get('price'),
                    "features": product.get('features', []),
                    "benefits": product.get('benefits', []),
                    "sustainability_benefits": product.get('sustainability_benefits'),
                    "created_at": datetime.now().isoformat()
                }
                products_data.append(product_data)
        
        else:
            raise HTTPException(status_code=400, detail="Either CSV file or JSON data is required")
        
        # Store products in database
        results = []
        for product_data in products_data:
            result = await db.create_product(product_data)
            if result:
                results.append(ProductResponse(**result))
        
        return results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading products: {str(e)}")

@router.post("/audience", response_model=List[AudienceResponse])
async def upload_audience(
    brand_id: str = Form(...),
    file: Optional[UploadFile] = File(None),
    audience_json: Optional[str] = Form(None)
):
    """Upload audience data via CSV or JSON"""
    
    try:
        # Track energy for this operation
        energy_data = carbon_tracker.track_generation("gpt-4o-mini", cache_hit=False)
        
        audience_data = []
        
        if file and file.filename.endswith('.csv'):
            # Process CSV file
            content = await file.read()
            df = pd.read_csv(io.StringIO(content.decode('utf-8')))
            
            for _, row in df.iterrows():
                audience_item = {
                    "brand_id": brand_id,
                    "user_id": str(row.get('user_id', '')),
                    "segment": str(row.get('segment', '')),
                    "clicks_last_30d": int(row.get('clicks_last_30d', 0)),
                    "purchases_last_90d": int(row.get('purchases_last_90d', 0)),
                    "favorite_category": str(row.get('favorite_category', '')),
                    "device": str(row.get('device', 'desktop')),
                    "age_range": str(row.get('age_range', '')) if pd.notna(row.get('age_range')) else None,
                    "location": str(row.get('location', '')) if pd.notna(row.get('location')) else None,
                    "interests": str(row.get('interests', '')).split(',') if pd.notna(row.get('interests')) else None,
                    "created_at": datetime.now().isoformat()
                }
                audience_data.append(audience_item)
        
        elif audience_json:
            # Process JSON data
            audience_list = json.loads(audience_json)
            
            for audience in audience_list:
                audience_item = {
                    "brand_id": brand_id,
                    "user_id": audience.get('user_id', ''),
                    "segment": audience.get('segment', ''),
                    "clicks_last_30d": audience.get('clicks_last_30d', 0),
                    "purchases_last_90d": audience.get('purchases_last_90d', 0),
                    "favorite_category": audience.get('favorite_category', ''),
                    "device": audience.get('device', 'desktop'),
                    "age_range": audience.get('age_range'),
                    "location": audience.get('location'),
                    "interests": audience.get('interests'),
                    "created_at": datetime.now().isoformat()
                }
                audience_data.append(audience_item)
        
        else:
            raise HTTPException(status_code=400, detail="Either CSV file or JSON data is required")
        
        # Store audience data in database
        results = await db.create_audience_batch(audience_data)
        
        return [AudienceResponse(**result) for result in results]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading audience data: {str(e)}")

@router.get("/brand/{brand_id}", response_model=BrandResponse)
async def get_brand(brand_id: str):
    """Get brand information by ID"""
    
    try:
        brand = await db.get_brand(brand_id)
        if not brand:
            raise HTTPException(status_code=404, detail="Brand not found")
        
        return BrandResponse(**brand)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving brand: {str(e)}")

@router.get("/brand/{brand_id}/products", response_model=List[ProductResponse])
async def get_products_by_brand(brand_id: str):
    """Get all products for a brand"""
    
    try:
        products = await db.get_products_by_brand(brand_id)
        return [ProductResponse(**product) for product in products]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving products: {str(e)}")

@router.get("/brand/{brand_id}/audience", response_model=List[AudienceResponse])
async def get_audience_by_brand(brand_id: str):
    """Get all audience data for a brand"""
    
    try:
        audience = await db.get_audience_by_brand(brand_id)
        return [AudienceResponse(**member) for member in audience]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving audience data: {str(e)}")
