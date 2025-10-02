import os
from supabase import create_client, Client
from typing import Optional, Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class DatabaseService:
    def __init__(self):
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")
        
        if not self.supabase_url or not self.supabase_key:
            logger.warning("Supabase credentials not found. Using mock database.")
            self.client = None
            self.mock_data = {
                "brands": {},
                "products": {},
                "audience": {},
                "ads": {},
                "feedback": {},
                "channel_recommendations": {}
            }
        else:
            self.client: Client = create_client(self.supabase_url, self.supabase_key)
    
    async def init_tables(self):
        """Initialize database tables if they don't exist"""
        if not self.client:
            logger.info("Using mock database - no table initialization needed")
            return
        
        # Create tables using Supabase SQL
        tables_sql = """
        -- Brands table
        CREATE TABLE IF NOT EXISTS brands (
            id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            company_name VARCHAR(255) NOT NULL,
            story TEXT NOT NULL,
            mission TEXT NOT NULL,
            tone VARCHAR(100) NOT NULL,
            differentiators TEXT[] NOT NULL,
            target_market VARCHAR(255) NOT NULL,
            sustainability_focus BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );

        -- Products table
        CREATE TABLE IF NOT EXISTS products (
            id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            brand_id UUID REFERENCES brands(id) ON DELETE CASCADE,
            name VARCHAR(255) NOT NULL,
            description TEXT NOT NULL,
            category VARCHAR(100) NOT NULL,
            price DECIMAL(10,2),
            features TEXT[] NOT NULL,
            benefits TEXT[] NOT NULL,
            sustainability_benefits TEXT[],
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );

        -- Audience table
        CREATE TABLE IF NOT EXISTS audience (
            id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            brand_id UUID REFERENCES brands(id) ON DELETE CASCADE,
            user_id VARCHAR(255) NOT NULL,
            segment VARCHAR(100) NOT NULL,
            clicks_last_30d INTEGER NOT NULL,
            purchases_last_90d INTEGER NOT NULL,
            favorite_category VARCHAR(100) NOT NULL,
            device VARCHAR(20) NOT NULL,
            age_range VARCHAR(20),
            location VARCHAR(100),
            interests TEXT[],
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );

        -- Ads table
        CREATE TABLE IF NOT EXISTS ads (
            id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            brand_id UUID REFERENCES brands(id) ON DELETE CASCADE,
            product_id UUID REFERENCES products(id) ON DELETE CASCADE,
            headline VARCHAR(100) NOT NULL,
            body TEXT NOT NULL,
            cta VARCHAR(100) NOT NULL,
            image_url TEXT,
            audience_segment VARCHAR(100) NOT NULL,
            context_signals JSONB NOT NULL,
            campaign_goal VARCHAR(50) NOT NULL,
            energy_consumed DECIMAL(10,6) NOT NULL,
            co2_emissions DECIMAL(10,6) NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );

        -- Feedback table
        CREATE TABLE IF NOT EXISTS feedback (
            id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            ad_id UUID REFERENCES ads(id) ON DELETE CASCADE,
            channel VARCHAR(50) NOT NULL,
            clicks INTEGER NOT NULL,
            impressions INTEGER NOT NULL,
            conversions INTEGER NOT NULL,
            spend DECIMAL(10,2) NOT NULL,
            ctr DECIMAL(5,4) NOT NULL,
            conversion_rate DECIMAL(5,4) NOT NULL,
            feedback_notes TEXT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );

        -- Channel recommendations table
        CREATE TABLE IF NOT EXISTS channel_recommendations (
            id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            brand_id UUID REFERENCES brands(id) ON DELETE CASCADE,
            product_id UUID REFERENCES products(id) ON DELETE CASCADE,
            audience_segment VARCHAR(100) NOT NULL,
            campaign_goal VARCHAR(50) NOT NULL,
            recommendations JSONB NOT NULL,
            best_channel VARCHAR(50) NOT NULL,
            total_confidence DECIMAL(3,2) NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        """
        
        try:
            self.client.rpc('exec_sql', {'sql': tables_sql}).execute()
            logger.info("Database tables initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing database tables: {e}")
    
    # Brand operations
    async def create_brand(self, brand_data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.client:
            brand_id = f"brand_{len(self.mock_data['brands']) + 1}"
            brand_data['id'] = brand_id
            brand_data['created_at'] = "2024-01-01T00:00:00Z"
            self.mock_data['brands'][brand_id] = brand_data
            return brand_data
        
        result = self.client.table('brands').insert(brand_data).execute()
        return result.data[0] if result.data else None
    
    async def get_brand(self, brand_id: str) -> Optional[Dict[str, Any]]:
        if not self.client:
            return self.mock_data['brands'].get(brand_id)
        
        result = self.client.table('brands').select('*').eq('id', brand_id).execute()
        return result.data[0] if result.data else None
    
    # Product operations
    async def create_product(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.client:
            product_id = f"product_{len(self.mock_data['products']) + 1}"
            product_data['id'] = product_id
            product_data['created_at'] = "2024-01-01T00:00:00Z"
            self.mock_data['products'][product_id] = product_data
            return product_data
        
        result = self.client.table('products').insert(product_data).execute()
        return result.data[0] if result.data else None
    
    async def get_products_by_brand(self, brand_id: str) -> List[Dict[str, Any]]:
        if not self.client:
            return [p for p in self.mock_data['products'].values() if p['brand_id'] == brand_id]
        
        result = self.client.table('products').select('*').eq('brand_id', brand_id).execute()
        return result.data if result.data else []
    
    # Audience operations
    async def create_audience_batch(self, audience_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not self.client:
            results = []
            for data in audience_data:
                audience_id = f"audience_{len(self.mock_data['audience']) + 1}"
                data['id'] = audience_id
                data['created_at'] = "2024-01-01T00:00:00Z"
                self.mock_data['audience'][audience_id] = data
                results.append(data)
            return results
        
        result = self.client.table('audience').insert(audience_data).execute()
        return result.data if result.data else []
    
    async def get_audience_by_brand(self, brand_id: str) -> List[Dict[str, Any]]:
        if not self.client:
            return [a for a in self.mock_data['audience'].values() if a['brand_id'] == brand_id]
        
        result = self.client.table('audience').select('*').eq('brand_id', brand_id).execute()
        return result.data if result.data else []
    
    # Ad operations
    async def create_ad(self, ad_data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.client:
            ad_id = f"ad_{len(self.mock_data['ads']) + 1}"
            ad_data['id'] = ad_id
            ad_data['created_at'] = "2024-01-01T00:00:00Z"
            self.mock_data['ads'][ad_id] = ad_data
            return ad_data
        
        result = self.client.table('ads').insert(ad_data).execute()
        return result.data[0] if result.data else None
    
    async def get_ad(self, ad_id: str) -> Optional[Dict[str, Any]]:
        if not self.client:
            return self.mock_data['ads'].get(ad_id)
        
        result = self.client.table('ads').select('*').eq('id', ad_id).execute()
        return result.data[0] if result.data else None
    
    # Feedback operations
    async def create_feedback(self, feedback_data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.client:
            feedback_id = f"feedback_{len(self.mock_data['feedback']) + 1}"
            feedback_data['id'] = feedback_id
            feedback_data['created_at'] = "2024-01-01T00:00:00Z"
            self.mock_data['feedback'][feedback_id] = feedback_data
            return feedback_data
        
        result = self.client.table('feedback').insert(feedback_data).execute()
        return result.data[0] if result.data else None
    
    # Channel recommendation operations
    async def create_channel_recommendation(self, rec_data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.client:
            rec_id = f"rec_{len(self.mock_data['channel_recommendations']) + 1}"
            rec_data['id'] = rec_id
            rec_data['created_at'] = "2024-01-01T00:00:00Z"
            self.mock_data['channel_recommendations'][rec_id] = rec_data
            return rec_data
        
        result = self.client.table('channel_recommendations').insert(rec_data).execute()
        return result.data[0] if result.data else None
    
    async def get_channel_recommendations_by_brand(self, brand_id: str) -> List[Dict[str, Any]]:
        if not self.client:
            return [r for r in self.mock_data['channel_recommendations'].values() if r['brand_id'] == brand_id]
        
        result = self.client.table('channel_recommendations').select('*').eq('brand_id', brand_id).execute()
        return result.data if result.data else []

# Global database instance
db = DatabaseService()

async def init_database():
    """Initialize the database"""
    await db.init_tables()
