import asyncio
import random
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Any, List
import json

from services.database import db
from services.ai_service import ai_service
from services.carbon_tracker import carbon_tracker
from services.ab_testing import ab_testing_service
from services.business_metrics import business_metrics_service

class DemoDataGenerator:
    def __init__(self):
        self.brand_data = {
            "company_name": "EcoTech Solutions",
            "story": "Founded in 2020 by environmental engineers, EcoTech Solutions emerged from a simple mission: make sustainable technology accessible to small businesses. Our founders, Sarah and Michael, started in their garage, building energy-efficient devices that could help local businesses reduce their carbon footprint while saving money.",
            "mission": "To democratize sustainable technology and help small businesses thrive while protecting our planet",
            "tone": "professional",
            "differentiators": ["100% renewable energy", "Carbon neutral operations", "Local sourcing", "Proven ROI"],
            "target_market": "Small to medium businesses",
            "sustainability_focus": True
        }
        
        # Load real datasets
        self.ads_dataset = None
        self.logistic_dataset = None
        self._load_datasets()
        
        self.products_data = [
            {
                "name": "Smart Energy Monitor",
                "description": "Real-time energy monitoring device that helps businesses track and optimize their electricity usage",
                "category": "sustainability_technology",
                "price": 299.99,
                "features": ["Real-time monitoring", "Mobile app", "Energy alerts", "Historical data"],
                "benefits": ["Reduce energy costs by 20%", "Identify waste patterns", "Improve efficiency", "Track ROI"],
                "sustainability_benefits": ["Lower carbon footprint", "Energy conservation", "Environmental impact tracking"]
            },
            {
                "name": "Solar Panel Controller",
                "description": "Advanced controller for solar panel systems with AI-powered optimization",
                "category": "renewable_energy",
                "price": 599.99,
                "features": ["AI optimization", "Weather prediction", "Remote monitoring", "Grid integration"],
                "benefits": ["Maximize solar efficiency", "Reduce grid dependence", "Lower electricity bills", "Future-proof investment"],
                "sustainability_benefits": ["100% renewable energy", "Zero emissions", "Sustainable power generation"]
            },
            {
                "name": "Carbon Footprint Tracker",
                "description": "Comprehensive carbon footprint tracking and reduction platform for businesses",
                "category": "sustainability_software",
                "price": 199.99,
                "features": ["Automated tracking", "Reduction recommendations", "Reporting dashboard", "Compliance tools"],
                "benefits": ["Meet sustainability goals", "Improve brand image", "Compliance reporting", "Cost savings"],
                "sustainability_benefits": ["Carbon neutrality", "Environmental responsibility", "Sustainable business practices"]
            }
        ]
        
        self.audience_segments = [
            "eco_conscious_shoppers",
            "price_sensitive_buyers", 
            "tech_early_adopters",
            "luxury_seekers",
            "convenience_seekers",
            "health_conscious"
        ]
        
        self.context_signals = [
            {
                "page_category": "sustainability",
                "geo_region": "Urban",
                "device_type": "mobile",
                "time_of_day": "morning",
                "season": "spring"
            },
            {
                "page_category": "technology",
                "geo_region": "Suburban",
                "device_type": "desktop",
                "time_of_day": "afternoon",
                "season": "fall"
            },
            {
                "page_category": "business",
                "geo_region": "Rural",
                "device_type": "tablet",
                "time_of_day": "evening",
                "season": "winter"
            }
        ]
    
    def _load_datasets(self):
        """Load the real datasets"""
        try:
            # Load ads dataset
            self.ads_dataset = pd.read_csv('/Users/valentinasilva/Downloads/Dataset_Ads.csv')
            print(f"✅ Loaded ads dataset: {len(self.ads_dataset)} records")
            
            # Load logistic regression dataset
            self.logistic_dataset = pd.read_csv('/Users/valentinasilva/Downloads/logistic Regression.csv')
            print(f"✅ Loaded logistic dataset: {len(self.logistic_dataset)} records")
            
        except Exception as e:
            print(f"⚠️ Could not load datasets: {e}")
            print("Using synthetic data instead")
            self.ads_dataset = None
            self.logistic_dataset = None
    
    async def generate_demo_data(self):
        """Generate comprehensive demo data for the competition"""
        
        print("🚀 Generating demo data for EcoAd AI...")
        
        # 1. Create brand
        print("📝 Creating brand data...")
        brand_result = await db.create_brand(self.brand_data)
        brand_id = brand_result["id"]
        print(f"✅ Brand created: {brand_id}")
        
        # 2. Create products
        print("📦 Creating product data...")
        product_ids = []
        for product in self.products_data:
            product["brand_id"] = brand_id
            product_result = await db.create_product(product)
            product_ids.append(product_result["id"])
        print(f"✅ Products created: {len(product_ids)}")
        
        # 3. Create audience data
        print("👥 Creating audience data...")
        audience_data = self._generate_audience_data(brand_id)
        audience_results = await db.create_audience_batch(audience_data)
        print(f"✅ Audience data created: {len(audience_results)} users")
        
        # 4. Generate ads for different segments and contexts
        print("🎯 Generating personalized ads...")
        ads = await self._generate_personalized_ads(brand_id, product_ids, audience_results)
        print(f"✅ Ads generated: {len(ads)}")
        
        # 5. Create A/B tests
        print("🧪 Creating A/B tests...")
        ab_tests = await self._create_ab_tests(ads)
        print(f"✅ A/B tests created: {len(ab_tests)}")
        
        # 6. Generate campaign performance data
        print("📊 Generating campaign performance data...")
        await self._generate_campaign_performance(ads)
        print("✅ Campaign performance data generated")
        
        # 7. Generate sustainability metrics
        print("🌱 Generating sustainability metrics...")
        await self._generate_sustainability_data()
        print("✅ Sustainability metrics generated")
        
        print("\n🎉 Demo data generation complete!")
        print(f"📋 Summary:")
        print(f"   - Brand: {brand_id}")
        print(f"   - Products: {len(product_ids)}")
        print(f"   - Audience: {len(audience_results)} users")
        print(f"   - Ads: {len(ads)}")
        print(f"   - A/B Tests: {len(ab_tests)}")
        
        return {
            "brand_id": brand_id,
            "product_ids": product_ids,
            "audience_count": len(audience_results),
            "ads": ads,
            "ab_tests": ab_tests
        }
    
    def _generate_audience_data(self, brand_id: str) -> List[Dict[str, Any]]:
        """Generate diverse audience data using real datasets"""
        
        audience_data = []
        
        if self.logistic_dataset is not None:
            # Use real data from logistic regression dataset
            sample_size = min(100, len(self.logistic_dataset))
            sample_data = self.logistic_dataset.sample(n=sample_size, random_state=42)
            
            for i, row in sample_data.iterrows():
                # Map real data to our audience format
                age = int(row['Age'])
                income = float(row['Area Income'])
                daily_time = float(row['Daily Time Spent on Site'])
                internet_usage = float(row['Daily Internet Usage'])
                clicked = int(row['Clicked on Ad'])
                
                # Determine segment based on real behavior
                segment = self._determine_segment_from_data(age, income, daily_time, internet_usage, clicked)
                
                # Map device type based on internet usage
                if internet_usage > 200:
                    device = "desktop"
                elif internet_usage > 150:
                    device = "tablet"
                else:
                    device = "mobile"
                
                # Map location from the dataset
                location = row['City'] if pd.notna(row['City']) else "Unknown"
                
                user_data = {
                    "brand_id": brand_id,
                    "user_id": f"user_{i+1:03d}",
                    "segment": segment,
                    "clicks_last_30d": max(1, int(daily_time / 10)),  # Estimate clicks from time spent
                    "purchases_last_90d": clicked,  # Use actual click data
                    "favorite_category": self._map_ad_topic_to_category(row['Ad Topic Line']),
                    "device": device,
                    "age_range": self._get_age_range(age),
                    "location": location,
                    "interests": self._get_interests_for_segment(segment),
                    "income": income,
                    "daily_time_spent": daily_time,
                    "internet_usage": internet_usage,
                    "created_at": datetime.now().isoformat()
                }
                
                audience_data.append(user_data)
        else:
            # Fallback to synthetic data
            for i in range(50):
                segment = random.choice(self.audience_segments)
                
                if segment == "eco_conscious_shoppers":
                    clicks = random.randint(10, 25)
                    purchases = random.randint(2, 5)
                    device = random.choice(["mobile", "desktop"])
                elif segment == "price_sensitive_buyers":
                    clicks = random.randint(5, 15)
                    purchases = random.randint(1, 3)
                    device = random.choice(["mobile", "desktop"])
                elif segment == "tech_early_adopters":
                    clicks = random.randint(15, 30)
                    purchases = random.randint(3, 7)
                    device = "desktop"
                else:
                    clicks = random.randint(5, 20)
                    purchases = random.randint(1, 4)
                    device = random.choice(["mobile", "desktop", "tablet"])
                
                user_data = {
                    "brand_id": brand_id,
                    "user_id": f"user_{i+1:03d}",
                    "segment": segment,
                    "clicks_last_30d": clicks,
                    "purchases_last_90d": purchases,
                    "favorite_category": random.choice(["sustainability_technology", "renewable_energy", "sustainability_software"]),
                    "device": device,
                    "age_range": random.choice(["25-35", "35-45", "45-55", "55-65"]),
                    "location": random.choice(["San Francisco", "New York", "Austin", "Seattle", "Boston"]),
                    "interests": self._get_interests_for_segment(segment),
                    "created_at": datetime.now().isoformat()
                }
                
                audience_data.append(user_data)
        
        return audience_data
    
    def _determine_segment_from_data(self, age: int, income: float, daily_time: float, internet_usage: float, clicked: int) -> str:
        """Determine audience segment based on real behavioral data"""
        
        # High engagement + high income = luxury seekers
        if daily_time > 80 and income > 70000:
            return "luxury_seekers"
        
        # High engagement + tech usage = tech early adopters
        elif internet_usage > 200 and daily_time > 70:
            return "tech_early_adopters"
        
        # Low income = price sensitive
        elif income < 40000:
            return "price_sensitive_buyers"
        
        # High engagement + clicked = eco conscious
        elif clicked == 1 and daily_time > 60:
            return "eco_conscious_shoppers"
        
        # High time spent = convenience seekers
        elif daily_time > 75:
            return "convenience_seekers"
        
        # Default to health conscious
        else:
            return "health_conscious"
    
    def _map_ad_topic_to_category(self, ad_topic: str) -> str:
        """Map ad topic to product category"""
        if pd.isna(ad_topic):
            return "sustainability_technology"
        
        topic_lower = ad_topic.lower()
        if any(word in topic_lower for word in ["energy", "solar", "renewable"]):
            return "renewable_energy"
        elif any(word in topic_lower for word in ["software", "platform", "system"]):
            return "sustainability_software"
        else:
            return "sustainability_technology"
    
    def _get_age_range(self, age: int) -> str:
        """Convert age to age range"""
        if age < 25:
            return "18-25"
        elif age < 35:
            return "25-35"
        elif age < 45:
            return "35-45"
        elif age < 55:
            return "45-55"
        else:
            return "55-65"
    
    def _get_interests_for_segment(self, segment: str) -> List[str]:
        """Get interests based on audience segment"""
        
        interest_mapping = {
            "eco_conscious_shoppers": ["sustainability", "environment", "green_technology", "renewable_energy"],
            "price_sensitive_buyers": ["cost_savings", "efficiency", "budget_planning", "roi"],
            "tech_early_adopters": ["technology", "innovation", "automation", "ai"],
            "luxury_seekers": ["premium_products", "quality", "exclusivity", "sophistication"],
            "convenience_seekers": ["ease_of_use", "automation", "time_saving", "simplicity"],
            "health_conscious": ["wellness", "health", "natural_products", "sustainability"]
        }
        
        return interest_mapping.get(segment, ["general", "business", "technology"])
    
    async def _generate_personalized_ads(self, brand_id: str, product_ids: List[str], audience_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate personalized ads for different segments and contexts"""
        
        ads = []
        
        # Group audience by segment
        audience_by_segment = {}
        for user in audience_data:
            segment = user["segment"]
            if segment not in audience_by_segment:
                audience_by_segment[segment] = []
            audience_by_segment[segment].append(user)
        
        # Generate ads for each segment
        for segment, users in audience_by_segment.items():
            if not users:
                continue
                
            # Pick a random product for this segment
            product_id = random.choice(product_ids)
            product = next((p for p in self.products_data if p["name"] in [p["name"] for p in self.products_data]), self.products_data[0])
            
            # Generate ads for different contexts
            for context in self.context_signals:
                try:
                    # Analyze audience segment
                    audience_analysis = await ai_service.analyze_audience_segment(users[:5])  # Use first 5 users for analysis
                    
                    # Generate ad copy
                    ad_copy = await ai_service.generate_ad_copy(
                        brand_data=self.brand_data,
                        product_data=product,
                        audience_data=audience_analysis,
                        context_signals=context,
                        campaign_goal=random.choice(["awareness", "conversion", "engagement"])
                    )
                    
                    # Generate image
                    image_url = await ai_service.generate_ad_image(
                        headline=ad_copy["headline"],
                        product_name=product["name"],
                        brand_tone=self.brand_data["tone"],
                        context_signals=context
                    )
                    
                    # Track energy consumption
                    energy_data = carbon_tracker.track_generation("gpt-4o-mini", cache_hit=False)
                    if image_url:
                        image_energy = carbon_tracker.track_generation("dall-e", cache_hit=False)
                        energy_data["energy"] += image_energy["energy"]
                        energy_data["co2"] += image_energy["co2"]
                    
                    # Create ad record
                    ad_data = {
                        "brand_id": brand_id,
                        "product_id": product_id,
                        "headline": ad_copy["headline"],
                        "body": ad_copy["body"],
                        "cta": ad_copy["cta"],
                        "image_url": image_url,
                        "audience_segment": segment,
                        "context_signals": context,
                        "campaign_goal": random.choice(["awareness", "conversion", "engagement"]),
                        "energy_consumed": energy_data["energy"],
                        "co2_emissions": energy_data["co2"],
                        "created_at": datetime.now().isoformat()
                    }
                    
                    # Store ad
                    result = await db.create_ad(ad_data)
                    if result:
                        ads.append(result)
                        
                except Exception as e:
                    print(f"Error generating ad for segment {segment}: {e}")
                    continue
        
        return ads
    
    async def _create_ab_tests(self, ads: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create A/B tests for generated ads"""
        
        ab_tests = []
        
        # Create A/B tests for a few ads
        for i, ad in enumerate(ads[:3]):  # Test first 3 ads
            try:
                test_config = ab_testing_service.create_test(
                    test_name=f"Headline Test {i+1}",
                    base_ad=ad,
                    test_type="headline",
                    traffic_split=0.5
                )
                ab_tests.append(test_config)
                
                # Simulate some test data
                for j in range(20):  # Simulate 20 users
                    user_id = f"test_user_{j}"
                    variant = ab_testing_service.get_variant_for_user(test_config["test_id"], user_id)
                    if variant:
                        # Simulate impressions and clicks
                        ab_testing_service.record_impression(test_config["test_id"], variant["variant_id"], user_id)
                        if random.random() < 0.1:  # 10% click rate
                            ab_testing_service.record_click(test_config["test_id"], variant["variant_id"], user_id)
                            if random.random() < 0.05:  # 5% conversion rate
                                ab_testing_service.record_conversion(test_config["test_id"], variant["variant_id"], user_id, random.uniform(50, 500))
                
            except Exception as e:
                print(f"Error creating A/B test for ad {ad.get('id', 'unknown')}: {e}")
                continue
        
        return ab_tests
    
    async def _generate_campaign_performance(self, ads: List[Dict[str, Any]]):
        """Generate campaign performance data using real dataset"""
        
        # Create campaign performance data
        campaign_id = "demo_campaign_1"
        
        if self.ads_dataset is not None:
            # Use real performance data from ads dataset
            sample_size = min(len(ads), len(self.ads_dataset))
            sample_data = self.ads_dataset.sample(n=sample_size, random_state=42)
            
            for i, (ad, row) in enumerate(zip(ads, sample_data.iterrows())):
                _, row_data = row
                
                # Use real performance metrics
                impressions = int(row_data['Clicks'] * 20)  # Estimate impressions from clicks
                clicks = int(row_data['Clicks'])
                conversions = int(clicks * row_data['Conversion Rate'])
                spend = random.uniform(50, 500)  # Random spend
                revenue = conversions * random.uniform(50, 200)  # Revenue based on conversions
                
                # Map ad placement to channel
                ad_placement = row_data['Ad Placement'].lower()
                if 'social' in ad_placement:
                    channel = random.choice(["linkedin", "instagram", "facebook"])
                elif 'search' in ad_placement:
                    channel = "google_display"
                else:
                    channel = random.choice(["linkedin", "instagram", "google_display", "facebook"])
                
                # Track performance
                business_metrics_service.track_campaign_performance(
                    campaign_id=campaign_id,
                    ad_id=ad["id"],
                    channel=channel,
                    impressions=impressions,
                    clicks=clicks,
                    conversions=conversions,
                    spend=spend,
                    revenue=revenue
                )
        else:
            # Fallback to synthetic data
            for i, ad in enumerate(ads):
                impressions = random.randint(1000, 10000)
                clicks = random.randint(50, 500)
                conversions = random.randint(5, 50)
                spend = random.uniform(100, 1000)
                revenue = random.uniform(200, 2000)
                
                business_metrics_service.track_campaign_performance(
                    campaign_id=campaign_id,
                    ad_id=ad["id"],
                    channel=random.choice(["linkedin", "instagram", "google_display", "facebook"]),
                    impressions=impressions,
                    clicks=clicks,
                    conversions=conversions,
                    spend=spend,
                    revenue=revenue
                )
    
    async def _generate_sustainability_data(self):
        """Generate sustainability metrics data"""
        
        # Simulate some carbon tracking
        for _ in range(10):
            carbon_tracker.track_generation("gpt-4o-mini", cache_hit=False)
        
        for _ in range(5):
            carbon_tracker.track_generation("dall-e", cache_hit=False)
        
        # Simulate some cache hits
        for _ in range(3):
            carbon_tracker.track_generation("gpt-4o-mini", cache_hit=True)
            carbon_tracker.track_inference_reuse()
        
        # Simulate green scheduled jobs
        carbon_tracker.green_scheduled_jobs = 5

async def main():
    """Main function to generate demo data"""
    
    generator = DemoDataGenerator()
    await generator.generate_demo_data()
    
    print("\n🎯 Demo data generation complete!")
    print("You can now test the API endpoints with realistic data.")
    print("\n📋 Key endpoints to test:")
    print("  - GET /upload/brand/{brand_id}")
    print("  - GET /upload/brand/{brand_id}/products")
    print("  - GET /upload/brand/{brand_id}/audience")
    print("  - GET /generate/ad/{ad_id}")
    print("  - GET /recommend/channel/brand/{brand_id}")
    print("  - GET /sustainability/metrics")
    print("  - GET /ab-test/all")
    print("  - GET /feedback/campaign/demo_campaign_1/roi")

if __name__ == "__main__":
    asyncio.run(main())
