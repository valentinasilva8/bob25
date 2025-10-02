from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class DeviceType(str, Enum):
    MOBILE = "mobile"
    DESKTOP = "desktop"
    TABLET = "tablet"

class ChannelType(str, Enum):
    LINKEDIN = "linkedin"
    INSTAGRAM = "instagram"
    GOOGLE_DISPLAY = "google_display"
    FACEBOOK = "facebook"
    TWITTER = "twitter"
    TIKTOK = "tiktok"

class CampaignGoal(str, Enum):
    AWARENESS = "awareness"
    CONVERSION = "conversion"
    ENGAGEMENT = "engagement"
    TRAFFIC = "traffic"

# Brand Models
class BrandUpload(BaseModel):
    company_name: str = Field(..., description="Company name")
    story: str = Field(..., description="Company story and background")
    mission: str = Field(..., description="Company mission statement")
    tone: str = Field(..., description="Brand tone (e.g., professional, casual, friendly)")
    differentiators: List[str] = Field(..., description="Key differentiators")
    target_market: str = Field(..., description="Primary target market")
    sustainability_focus: Optional[bool] = Field(False, description="Sustainability focus")

class BrandResponse(BaseModel):
    id: str
    company_name: str
    story: str
    mission: str
    tone: str
    differentiators: List[str]
    target_market: str
    sustainability_focus: bool
    created_at: datetime

# Product Models
class ProductUpload(BaseModel):
    name: str = Field(..., description="Product name")
    description: str = Field(..., description="Product description")
    category: str = Field(..., description="Product category")
    price: Optional[float] = Field(None, description="Product price")
    features: List[str] = Field(..., description="Key features")
    benefits: List[str] = Field(..., description="Customer benefits")
    sustainability_benefits: Optional[List[str]] = Field(None, description="Sustainability benefits")

class ProductResponse(BaseModel):
    id: str
    name: str
    description: str
    category: str
    price: Optional[float]
    features: List[str]
    benefits: List[str]
    sustainability_benefits: Optional[List[str]]
    brand_id: str
    created_at: datetime

# Audience Models
class AudienceUpload(BaseModel):
    user_id: str = Field(..., description="Hashed user ID")
    segment: str = Field(..., description="Audience segment")
    clicks_last_30d: int = Field(..., description="Clicks in last 30 days")
    purchases_last_90d: int = Field(..., description="Purchases in last 90 days")
    favorite_category: str = Field(..., description="Favorite product category")
    device: DeviceType = Field(..., description="Primary device type")
    age_range: Optional[str] = Field(None, description="Age range")
    location: Optional[str] = Field(None, description="Location")
    interests: Optional[List[str]] = Field(None, description="User interests")

class AudienceResponse(BaseModel):
    id: str
    user_id: str
    segment: str
    clicks_last_30d: int
    purchases_last_90d: int
    favorite_category: str
    device: DeviceType
    age_range: Optional[str]
    location: Optional[str]
    interests: Optional[List[str]]
    brand_id: str
    created_at: datetime

# Ad Generation Models
class AdGenerationRequest(BaseModel):
    brand_id: str = Field(..., description="Brand ID")
    product_id: str = Field(..., description="Product ID")
    audience_segment: str = Field(..., description="Target audience segment")
    context_signals: Dict[str, Any] = Field(..., description="Context signals")
    campaign_goal: CampaignGoal = Field(..., description="Campaign objective")
    include_image: bool = Field(True, description="Generate image with ad")

class ContextSignals(BaseModel):
    page_category: Optional[str] = Field(None, description="Page category")
    geo_region: Optional[str] = Field(None, description="Geographic region")
    device_type: DeviceType = Field(..., description="Device type")
    time_of_day: str = Field(..., description="Time of day")
    weather: Optional[str] = Field(None, description="Weather condition")
    season: Optional[str] = Field(None, description="Season")

class AdResponse(BaseModel):
    id: str
    headline: str = Field(..., max_length=50, description="Ad headline")
    body: str = Field(..., max_length=100, description="Ad body text")
    cta: str = Field(..., description="Call to action")
    image_url: Optional[str] = Field(None, description="Generated image URL")
    brand_id: str
    product_id: str
    audience_segment: str
    context_signals: Dict[str, Any]
    campaign_goal: CampaignGoal
    energy_consumed: float = Field(..., description="Energy consumed in kWh")
    co2_emissions: float = Field(..., description="CO2 emissions in kg")
    created_at: datetime

# Channel Recommendation Models
class ChannelRecommendationRequest(BaseModel):
    brand_id: str = Field(..., description="Brand ID")
    product_id: str = Field(..., description="Product ID")
    audience_segment: str = Field(..., description="Target audience segment")
    campaign_goal: CampaignGoal = Field(..., description="Campaign objective")
    budget: Optional[float] = Field(None, description="Campaign budget")

class ChannelRecommendation(BaseModel):
    channel: ChannelType
    confidence_score: float = Field(..., ge=0, le=1, description="Confidence score")
    estimated_ctr: float = Field(..., ge=0, description="Estimated CTR")
    estimated_cpc: float = Field(..., ge=0, description="Estimated CPC")
    reasoning: str = Field(..., description="Recommendation reasoning")

class ChannelRecommendationResponse(BaseModel):
    recommendations: List[ChannelRecommendation]
    best_channel: ChannelType
    total_confidence: float
    brand_id: str
    product_id: str
    audience_segment: str
    campaign_goal: CampaignGoal

# Feedback Models
class FeedbackRequest(BaseModel):
    ad_id: str = Field(..., description="Ad ID")
    channel: ChannelType = Field(..., description="Channel used")
    clicks: int = Field(..., ge=0, description="Number of clicks")
    impressions: int = Field(..., ge=0, description="Number of impressions")
    conversions: int = Field(..., ge=0, description="Number of conversions")
    spend: float = Field(..., ge=0, description="Amount spent")
    feedback_notes: Optional[str] = Field(None, description="Additional feedback")

class FeedbackResponse(BaseModel):
    id: str
    ad_id: str
    channel: ChannelType
    clicks: int
    impressions: int
    conversions: int
    spend: float
    ctr: float = Field(..., description="Click-through rate")
    conversion_rate: float = Field(..., description="Conversion rate")
    feedback_notes: Optional[str]
    created_at: datetime

# Sustainability Models
class SustainabilityMetrics(BaseModel):
    total_energy_consumed: float = Field(..., description="Total energy consumed in kWh")
    total_co2_emissions: float = Field(..., description="Total CO2 emissions in kg")
    cache_hits: int = Field(..., description="Number of cache hits")
    inference_reuse_count: int = Field(..., description="Number of inference reuses")
    green_scheduled_jobs: int = Field(..., description="Jobs scheduled during low-carbon hours")
    average_energy_per_generation: float = Field(..., description="Average energy per generation")
    carbon_intensity: float = Field(..., description="Carbon intensity in kg CO2/kWh")

class GreenSchedulingRequest(BaseModel):
    job_type: str = Field(..., description="Type of job to schedule")
    priority: str = Field(..., description="Job priority (low, medium, high)")
    estimated_duration: int = Field(..., description="Estimated duration in minutes")
    data: Dict[str, Any] = Field(..., description="Job data")

class GreenSchedulingResponse(BaseModel):
    job_id: str
    scheduled_time: datetime
    estimated_carbon_savings: float = Field(..., description="Estimated carbon savings in kg CO2")
    is_green_scheduled: bool = Field(..., description="Whether job was scheduled during low-carbon hours")
