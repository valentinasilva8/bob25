import os
import json
import asyncio
from typing import Dict, Any, List, Optional, Tuple
import openai
from openai import AsyncOpenAI
import httpx
import logging

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            self.openai_client = AsyncOpenAI(api_key=api_key)
        else:
            self.openai_client = None
            print("Warning: OpenAI API key not found. AI features will use fallback methods.")
        self.model = "gpt-4o-mini"  # Using smaller model for efficiency
        self.image_model = "dall-e-3"
        
    async def generate_ad_copy(
        self, 
        brand_data: Dict[str, Any], 
        product_data: Dict[str, Any], 
        audience_data: Dict[str, Any], 
        context_signals: Dict[str, Any],
        campaign_goal: str
    ) -> Dict[str, str]:
        """Generate personalized ad copy using AI"""
        
        # Build prompt based on inputs
        prompt = self._build_ad_prompt(
            brand_data, product_data, audience_data, context_signals, campaign_goal
        )
        
        if not self.openai_client:
            # Use fallback generation when OpenAI is not available
            return self._generate_fallback_ad_copy(
                brand_data, product_data, audience_data, context_signals, campaign_goal
            )
        
        try:
            response = await self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert copywriter specializing in personalized, story-driven advertisements. Create compelling ad copy that weaves brand story with product benefits for specific audience segments."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=200,
                temperature=0.7
            )
            
            # Parse the response
            ad_copy = response.choices[0].message.content.strip()
            
            # Extract headline, body, and CTA
            return self._parse_ad_copy(ad_copy)
            
        except Exception as e:
            logger.error(f"Error generating ad copy: {e}")
            # Fallback to template-based generation
            return self._generate_fallback_ad_copy(
                brand_data, product_data, audience_data, context_signals, campaign_goal
            )
    
    def _build_ad_prompt(
        self, 
        brand_data: Dict[str, Any], 
        product_data: Dict[str, Any], 
        audience_data: Dict[str, Any], 
        context_signals: Dict[str, Any],
        campaign_goal: str
    ) -> str:
        """Build the prompt for ad generation with segment-driven messaging"""
        
        # Get segment-specific messaging strategy
        segment_strategy = self._get_segment_messaging_strategy(audience_data.get('segment', 'general'))
        
        prompt = f"""
Create a personalized ad for the following:

BRAND:
- Company: {brand_data.get('company_name', 'N/A')}
- Story: {brand_data.get('story', 'N/A')}
- Mission: {brand_data.get('mission', 'N/A')}
- Tone: {brand_data.get('tone', 'N/A')}
- Differentiators: {', '.join(brand_data.get('differentiators', []))}

PRODUCT:
- Name: {product_data.get('name', 'N/A')}
- Description: {product_data.get('description', 'N/A')}
- Category: {product_data.get('category', 'N/A')}
- Features: {', '.join(product_data.get('features', []))}
- Benefits: {', '.join(product_data.get('benefits', []))}

AUDIENCE SEGMENT: {audience_data.get('segment', 'N/A')}
- Messaging Style: {segment_strategy['messaging_style']}
- Benefits Focus: {', '.join(segment_strategy['benefits_emphasis'])}
- CTA Style: {segment_strategy['cta_style']}
- Device: {audience_data.get('device', 'N/A')}
- Favorite Category: {audience_data.get('favorite_category', 'N/A')}
- Recent Activity: {audience_data.get('clicks_last_30d', 0)} clicks, {audience_data.get('purchases_last_90d', 0)} purchases

CONTEXT SIGNALS:
- Page Category: {context_signals.get('page_category', 'N/A')}
- Device Type: {context_signals.get('device_type', 'N/A')}
- Time of Day: {context_signals.get('time_of_day', 'N/A')}
- Location: {context_signals.get('geo_region', 'N/A')}
- Season: {context_signals.get('season', 'N/A')}

CAMPAIGN GOAL: {campaign_goal}

Create a personalized ad that:
1. Uses {segment_strategy['messaging_style']} messaging style for {audience_data.get('segment', 'general')} segment
2. Emphasizes {', '.join(segment_strategy['benefits_emphasis'])} benefits
3. Adapts to {context_signals.get('time_of_day', 'N/A')} and {context_signals.get('device_type', 'N/A')} context
4. Uses {segment_strategy['cta_style']} call-to-action style
5. Weaves brand story naturally with segment preferences
6. Creates urgency or appeal based on context signals

Format your response as:
HEADLINE: [Your headline here - max 8 words]
BODY: [Your body text here - max 40 words]
CTA: [Your call-to-action here]
"""
        return prompt
    
    def _get_segment_messaging_strategy(self, segment: str) -> Dict[str, Any]:
        """Get messaging strategy for specific audience segment"""
        
        segment_strategies = {
            "eco_conscious_shoppers": {
                "messaging_style": "sustainability_focused",
                "benefits_emphasis": ["environmental_impact", "ethical_sourcing", "long_term_value", "carbon_footprint"],
                "cta_style": "action_oriented",
                "tone_keywords": ["sustainable", "eco-friendly", "green", "responsible", "future"]
            },
            "price_sensitive_buyers": {
                "messaging_style": "value_focused",
                "benefits_emphasis": ["cost_savings", "efficiency", "roi", "affordability", "value"],
                "cta_style": "urgency_driven",
                "tone_keywords": ["save", "affordable", "value", "deal", "budget"]
            },
            "tech_early_adopters": {
                "messaging_style": "innovation_focused",
                "benefits_emphasis": ["cutting_edge", "performance", "future_ready", "advanced", "breakthrough"],
                "cta_style": "exclusive_access",
                "tone_keywords": ["innovative", "advanced", "cutting-edge", "breakthrough", "revolutionary"]
            },
            "luxury_seekers": {
                "messaging_style": "premium_focused",
                "benefits_emphasis": ["quality", "exclusivity", "premium", "sophistication", "status"],
                "cta_style": "exclusive_access",
                "tone_keywords": ["premium", "exclusive", "luxury", "sophisticated", "elite"]
            },
            "convenience_seekers": {
                "messaging_style": "convenience_focused",
                "benefits_emphasis": ["ease_of_use", "time_saving", "convenience", "simplicity", "hassle_free"],
                "cta_style": "easy_action",
                "tone_keywords": ["easy", "convenient", "simple", "quick", "effortless"]
            },
            "health_conscious": {
                "messaging_style": "wellness_focused",
                "benefits_emphasis": ["health_benefits", "wellness", "natural", "organic", "wellbeing"],
                "cta_style": "health_action",
                "tone_keywords": ["healthy", "natural", "wellness", "organic", "beneficial"]
            }
        }
        
        return segment_strategies.get(segment, {
            "messaging_style": "general",
            "benefits_emphasis": ["quality", "value", "reliability"],
            "cta_style": "standard",
            "tone_keywords": ["quality", "reliable", "trusted"]
        })
    
    def _parse_ad_copy(self, ad_copy: str) -> Dict[str, str]:
        """Parse the AI-generated ad copy into structured format"""
        lines = ad_copy.split('\n')
        result = {
            "headline": "Amazing Product Awaits",
            "body": "Discover the perfect solution for your needs today.",
            "cta": "Learn More"
        }
        
        for line in lines:
            line = line.strip()
            if line.startswith("HEADLINE:"):
                result["headline"] = line.replace("HEADLINE:", "").strip()
            elif line.startswith("BODY:"):
                result["body"] = line.replace("BODY:", "").strip()
            elif line.startswith("CTA:"):
                result["cta"] = line.replace("CTA:", "").strip()
        
        return result
    
    def _generate_fallback_ad_copy(
        self, 
        brand_data: Dict[str, Any], 
        product_data: Dict[str, Any], 
        audience_data: Dict[str, Any], 
        context_signals: Dict[str, Any],
        campaign_goal: str
    ) -> Dict[str, str]:
        """Generate fallback ad copy using templates"""
        
        # Template-based generation (keeping within character limits)
        product_name = product_data.get('name', 'Our Product')
        company_name = brand_data.get('company_name', 'us')
        
        templates = {
            "awareness": {
                "headline": "Discover Eco",
                "body": f"Join {company_name} in our mission",
                "cta": "Learn More"
            },
            "conversion": {
                "headline": "Get Eco Today",
                "body": f"Experience the difference today",
                "cta": "Shop Now"
            },
            "engagement": {
                "headline": "Join Us",
                "body": f"Be part of something bigger",
                "cta": "Get Involved"
            }
        }
        
        return templates.get(campaign_goal, templates["awareness"])
    
    async def generate_ad_image(
        self, 
        headline: str, 
        product_name: str, 
        brand_tone: str,
        context_signals: Dict[str, Any]
    ) -> Optional[str]:
        """Generate ad image using DALL-E"""
        
        if not self.openai_client:
            logger.warning("OpenAI client not available. Skipping image generation.")
            return None
        
        try:
            # Build image prompt
            image_prompt = self._build_image_prompt(headline, product_name, brand_tone, context_signals)
            
            response = await self.openai_client.images.generate(
                model=self.image_model,
                prompt=image_prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )
            
            return response.data[0].url
            
        except Exception as e:
            logger.error(f"Error generating ad image: {e}")
            return None
    
    def _build_image_prompt(
        self, 
        headline: str, 
        product_name: str, 
        brand_tone: str,
        context_signals: Dict[str, Any]
    ) -> str:
        """Build prompt for image generation with enhanced context awareness"""
        
        # Map tone to visual style
        tone_styles = {
            "professional": "clean, modern, corporate",
            "casual": "friendly, approachable, warm",
            "friendly": "welcoming, bright, inviting",
            "luxury": "elegant, sophisticated, premium",
            "eco-friendly": "natural, green, sustainable"
        }
        
        style = tone_styles.get(brand_tone.lower(), "clean, modern")
        
        # Add context-based elements
        context_elements = []
        
        # Time-based elements
        time_of_day = context_signals.get("time_of_day", "").lower()
        if time_of_day == "morning":
            context_elements.append("soft morning light, fresh and energizing")
        elif time_of_day == "afternoon":
            context_elements.append("bright natural lighting, active and productive")
        elif time_of_day == "evening":
            context_elements.append("warm evening glow, cozy and intimate")
        elif time_of_day == "night":
            context_elements.append("dramatic night lighting, sophisticated and mysterious")
        
        # Location-based elements
        location = context_signals.get("geo_region", "").lower()
        if "urban" in location or "city" in location:
            context_elements.append("urban, modern, fast-paced environment")
        elif "rural" in location or "country" in location:
            context_elements.append("natural, spacious, community-focused setting")
        elif "suburban" in location:
            context_elements.append("family-friendly, balanced lifestyle setting")
        
        # Seasonal elements
        season = context_signals.get("season", "").lower()
        if season == "spring":
            context_elements.append("fresh spring colors, growth and renewal")
        elif season == "summer":
            context_elements.append("vibrant summer energy, bright and lively")
        elif season == "fall":
            context_elements.append("warm autumn tones, cozy and nostalgic")
        elif season == "winter":
            context_elements.append("cool winter palette, elegant and refined")
        
        # Device-specific elements
        device_type = context_signals.get("device_type", "").lower()
        if device_type == "mobile":
            context_elements.append("vertical mobile-optimized composition")
        elif device_type == "desktop":
            context_elements.append("horizontal desktop-optimized layout")
        
        # Page category elements
        page_category = context_signals.get("page_category", "").lower()
        if "sustainability" in page_category or "eco" in page_category:
            context_elements.append("natural, organic, environmentally conscious")
        elif "technology" in page_category:
            context_elements.append("modern, tech-forward, innovative")
        elif "lifestyle" in page_category:
            context_elements.append("lifestyle-focused, aspirational")
        
        context_str = ", ".join(context_elements) if context_elements else ""
        
        prompt = f"""
Create a professional advertisement image for {product_name}.
Style: {style}
Headline: {headline}
Context: {context_str}
The image should be suitable for digital advertising, with clear text space and engaging visuals.
High quality, commercial photography style that matches the context and mood.
"""
        
        return prompt.strip()
    
    async def analyze_audience_segment(self, audience_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze audience segment characteristics"""
        
        if not audience_data:
            return {"segment": "general", "characteristics": {}}
        
        # Calculate segment statistics
        total_users = len(audience_data)
        total_clicks = sum(user.get('clicks_last_30d', 0) for user in audience_data)
        total_purchases = sum(user.get('purchases_last_90d', 0) for user in audience_data)
        
        # Get most common characteristics
        devices = [user.get('device', 'desktop') for user in audience_data]
        categories = [user.get('favorite_category', 'general') for user in audience_data]
        segments = [user.get('segment', 'general') for user in audience_data]
        
        most_common_device = max(set(devices), key=devices.count) if devices else 'desktop'
        most_common_category = max(set(categories), key=categories.count) if categories else 'general'
        most_common_segment = max(set(segments), key=segments.count) if segments else 'general'
        
        # Calculate engagement metrics
        avg_clicks = total_clicks / total_users if total_users > 0 else 0
        avg_purchases = total_purchases / total_users if total_users > 0 else 0
        
        return {
            "segment": most_common_segment,
            "characteristics": {
                "total_users": total_users,
                "avg_clicks_per_user": avg_clicks,
                "avg_purchases_per_user": avg_purchases,
                "primary_device": most_common_device,
                "primary_category": most_common_category,
                "engagement_level": "high" if avg_clicks > 5 else "medium" if avg_clicks > 2 else "low",
                "purchase_intent": "high" if avg_purchases > 1 else "medium" if avg_purchases > 0 else "low"
            }
        }

# Global AI service instance
ai_service = AIService()
