"""
Sample data for testing the EcoAd AI backend
"""

# Sample brand data
SAMPLE_BRAND = {
    "company_name": "EcoTech Solutions",
    "story": "Founded in 2020 by a team of passionate environmentalists and tech enthusiasts, EcoTech Solutions emerged from a simple belief: technology should serve both people and the planet. Our journey began when our founders noticed the massive carbon footprint of traditional tech companies and decided to create an alternative that prioritizes sustainability without compromising on innovation.",
    "mission": "To make technology accessible, affordable, and sustainable for small businesses while reducing the environmental impact of digital operations.",
    "tone": "professional",
    "differentiators": [
        "100% renewable energy powered",
        "Carbon neutral operations",
        "Local sourcing and manufacturing",
        "Transparent sustainability reporting",
        "Community-focused approach"
    ],
    "target_market": "Small to medium businesses",
    "sustainability_focus": True
}

# Sample product data
SAMPLE_PRODUCTS = [
    {
        "name": "EcoCloud Hosting",
        "description": "Sustainable cloud hosting powered by 100% renewable energy with carbon-neutral data centers",
        "category": "cloud_services",
        "price": 29.99,
        "features": [
            "100% renewable energy",
            "Carbon neutral",
            "99.9% uptime guarantee",
            "24/7 support",
            "Automatic backups"
        ],
        "benefits": [
            "Reduce your carbon footprint",
            "Lower energy costs",
            "Reliable performance",
            "Peace of mind",
            "Future-proof technology"
        ],
        "sustainability_benefits": [
            "Zero carbon emissions",
            "Supports renewable energy",
            "Efficient resource utilization",
            "Green certifications"
        ]
    },
    {
        "name": "Green Analytics Dashboard",
        "description": "AI-powered analytics platform that tracks both business performance and environmental impact",
        "category": "analytics",
        "price": 49.99,
        "features": [
            "Real-time analytics",
            "Carbon footprint tracking",
            "Sustainability metrics",
            "Custom reports",
            "API integration"
        ],
        "benefits": [
            "Make data-driven decisions",
            "Track environmental impact",
            "Improve efficiency",
            "Meet sustainability goals",
            "Stand out to eco-conscious customers"
        ],
        "sustainability_benefits": [
            "Helps reduce waste",
            "Optimizes resource usage",
            "Tracks carbon savings",
            "Supports green initiatives"
        ]
    }
]

# Sample audience data
SAMPLE_AUDIENCE = [
    {
        "user_id": "user_001",
        "segment": "eco_conscious_business_owners",
        "clicks_last_30d": 25,
        "purchases_last_90d": 2,
        "favorite_category": "sustainable_technology",
        "device": "desktop",
        "age_range": "35-45",
        "location": "San Francisco",
        "interests": ["sustainability", "technology", "business_growth", "environmental_impact"]
    },
    {
        "user_id": "user_002",
        "segment": "tech_enthusiasts",
        "clicks_last_30d": 18,
        "purchases_last_90d": 1,
        "favorite_category": "cloud_services",
        "device": "mobile",
        "age_range": "25-35",
        "location": "Austin",
        "interests": ["technology", "innovation", "efficiency", "automation"]
    },
    {
        "user_id": "user_003",
        "segment": "small_business_owners",
        "clicks_last_30d": 12,
        "purchases_last_90d": 3,
        "favorite_category": "business_tools",
        "device": "tablet",
        "age_range": "40-50",
        "location": "Portland",
        "interests": ["business_growth", "cost_savings", "efficiency", "sustainability"]
    },
    {
        "user_id": "user_004",
        "segment": "eco_conscious_business_owners",
        "clicks_last_30d": 30,
        "purchases_last_90d": 4,
        "favorite_category": "sustainable_products",
        "device": "desktop",
        "age_range": "30-40",
        "location": "Seattle",
        "interests": ["sustainability", "environmental_impact", "green_business", "renewable_energy"]
    },
    {
        "user_id": "user_005",
        "segment": "tech_enthusiasts",
        "clicks_last_30d": 22,
        "purchases_last_90d": 1,
        "favorite_category": "analytics",
        "device": "mobile",
        "age_range": "28-38",
        "location": "Denver",
        "interests": ["data_analytics", "technology", "innovation", "efficiency"]
    }
]

# Sample context signals
SAMPLE_CONTEXT_SIGNALS = {
    "page_category": "sustainability",
    "geo_region": "San Francisco Bay Area",
    "device_type": "mobile",
    "time_of_day": "morning",
    "weather": "sunny",
    "season": "spring"
}

# Sample campaign goals
SAMPLE_CAMPAIGN_GOALS = [
    "awareness",
    "conversion", 
    "engagement",
    "traffic"
]

# Sample channel types
SAMPLE_CHANNELS = [
    "linkedin",
    "instagram", 
    "google_display",
    "facebook",
    "twitter",
    "tiktok"
]

# Sample feedback data
SAMPLE_FEEDBACK = {
    "ad_id": "ad_123",
    "channel": "linkedin",
    "clicks": 45,
    "impressions": 2500,
    "conversions": 8,
    "spend": 150.00,
    "feedback_notes": "Great performance on LinkedIn, especially with eco-conscious audience"
}

# Sample CSV data for testing
SAMPLE_AUDIENCE_CSV = """user_id,segment,clicks_last_30d,purchases_last_90d,favorite_category,device,age_range,location,interests
user_001,eco_conscious_business_owners,25,2,sustainable_technology,desktop,35-45,San Francisco,"sustainability,technology,business_growth,environmental_impact"
user_002,tech_enthusiasts,18,1,cloud_services,mobile,25-35,Austin,"technology,innovation,efficiency,automation"
user_003,small_business_owners,12,3,business_tools,tablet,40-50,Portland,"business_growth,cost_savings,efficiency,sustainability"
user_004,eco_conscious_business_owners,30,4,sustainable_products,desktop,30-40,Seattle,"sustainability,environmental_impact,green_business,renewable_energy"
user_005,tech_enthusiasts,22,1,analytics,mobile,28-38,Denver,"data_analytics,technology,innovation,efficiency"
"""

SAMPLE_PRODUCTS_CSV = """name,description,category,price,features,benefits,sustainability_benefits
EcoCloud Hosting,Sustainable cloud hosting powered by 100% renewable energy,cloud_services,29.99,"100% renewable energy,Carbon neutral,99.9% uptime guarantee,24/7 support,Automatic backups","Reduce your carbon footprint,Lower energy costs,Reliable performance,Peace of mind,Future-proof technology","Zero carbon emissions,Supports renewable energy,Efficient resource utilization,Green certifications"
Green Analytics Dashboard,AI-powered analytics platform that tracks both business performance and environmental impact,analytics,49.99,"Real-time analytics,Carbon footprint tracking,Sustainability metrics,Custom reports,API integration","Make data-driven decisions,Track environmental impact,Improve efficiency,Meet sustainability goals,Stand out to eco-conscious customers","Helps reduce waste,Optimizes resource usage,Tracks carbon savings,Supports green initiatives"
"""
