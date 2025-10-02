import random
import statistics
from typing import Dict, Any, List, Tuple
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ABTestingService:
    def __init__(self):
        self.active_tests = {}
        self.test_results = {}
        
    def create_test(self, 
                   test_name: str, 
                   base_ad: Dict[str, Any], 
                   test_type: str = "headline",
                   traffic_split: float = 0.5) -> Dict[str, Any]:
        """Create an A/B test for ad variants"""
        
        test_id = f"test_{test_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Generate variants based on test type
        variants = self._generate_variants(base_ad, test_type)
        
        test_config = {
            "test_id": test_id,
            "test_name": test_name,
            "test_type": test_type,
            "base_ad": base_ad,
            "variants": variants,
            "traffic_split": traffic_split,
            "status": "active",
            "created_at": datetime.now().isoformat(),
            "metrics": {
                "impressions": {"control": 0, "variant": 0},
                "clicks": {"control": 0, "variant": 0},
                "conversions": {"control": 0, "variant": 0},
                "revenue": {"control": 0.0, "variant": 0.0}
            }
        }
        
        self.active_tests[test_id] = test_config
        logger.info(f"Created A/B test: {test_id}")
        
        return test_config
    
    def _generate_variants(self, base_ad: Dict[str, Any], test_type: str) -> List[Dict[str, Any]]:
        """Generate test variants based on test type"""
        
        variants = []
        
        if test_type == "headline":
            # Generate headline variants
            headlines = [
                base_ad.get("headline", ""),
                self._generate_headline_variant(base_ad),
                self._generate_headline_variant(base_ad, style="urgency"),
                self._generate_headline_variant(base_ad, style="benefit")
            ]
            
            for i, headline in enumerate(headlines):
                variant = base_ad.copy()
                variant["headline"] = headline
                variant["variant_id"] = f"headline_{i}"
                variants.append(variant)
                
        elif test_type == "cta":
            # Generate CTA variants
            ctas = [
                base_ad.get("cta", ""),
                self._generate_cta_variant(base_ad, style="urgency"),
                self._generate_cta_variant(base_ad, style="benefit"),
                self._generate_cta_variant(base_ad, style="action")
            ]
            
            for i, cta in enumerate(ctas):
                variant = base_ad.copy()
                variant["cta"] = cta
                variant["variant_id"] = f"cta_{i}"
                variants.append(variant)
                
        elif test_type == "body":
            # Generate body text variants
            bodies = [
                base_ad.get("body", ""),
                self._generate_body_variant(base_ad, style="emotional"),
                self._generate_body_variant(base_ad, style="logical"),
                self._generate_body_variant(base_ad, style="social")
            ]
            
            for i, body in enumerate(bodies):
                variant = base_ad.copy()
                variant["body"] = body
                variant["variant_id"] = f"body_{i}"
                variants.append(variant)
        
        return variants
    
    def _generate_headline_variant(self, base_ad: Dict[str, Any], style: str = "default") -> str:
        """Generate headline variant based on style"""
        
        product_name = base_ad.get("product_name", "Product")
        brand_name = base_ad.get("brand_name", "Brand")
        
        if style == "urgency":
            templates = [
                f"Limited Time: {product_name}",
                f"Don't Miss Out on {product_name}",
                f"Last Chance: {product_name}",
                f"Act Now: {product_name}"
            ]
        elif style == "benefit":
            templates = [
                f"Save Money with {product_name}",
                f"Boost Productivity with {product_name}",
                f"Transform Your Life with {product_name}",
                f"Get Results with {product_name}"
            ]
        else:
            templates = [
                f"Discover {product_name}",
                f"Introducing {product_name}",
                f"Meet {product_name}",
                f"Experience {product_name}"
            ]
        
        return random.choice(templates)
    
    def _generate_cta_variant(self, base_ad: Dict[str, Any], style: str = "default") -> str:
        """Generate CTA variant based on style"""
        
        if style == "urgency":
            ctas = ["Act Now", "Get It Today", "Limited Time", "Don't Wait"]
        elif style == "benefit":
            ctas = ["Save Money", "Get Results", "Transform Now", "Boost Success"]
        elif style == "action":
            ctas = ["Learn More", "Discover How", "See Details", "Find Out"]
        else:
            ctas = ["Get Started", "Try Now", "Shop Now", "Learn More"]
        
        return random.choice(ctas)
    
    def _generate_body_variant(self, base_ad: Dict[str, Any], style: str = "default") -> str:
        """Generate body text variant based on style"""
        
        product_name = base_ad.get("product_name", "our product")
        
        if style == "emotional":
            templates = [
                f"Feel the difference with {product_name}. Experience the change you've been waiting for.",
                f"Transform your daily routine with {product_name}. You deserve this upgrade.",
                f"Join thousands who've already made the switch to {product_name}."
            ]
        elif style == "logical":
            templates = [
                f"Data shows {product_name} delivers 40% better results than alternatives.",
                f"Proven technology in {product_name} gives you the edge you need.",
                f"Research-backed {product_name} provides measurable improvements."
            ]
        elif style == "social":
            templates = [
                f"Join 10,000+ satisfied customers who chose {product_name}.",
                f"See why everyone's talking about {product_name}. Be part of the movement.",
                f"Trusted by professionals worldwide. {product_name} is the smart choice."
            ]
        else:
            templates = [
                f"Discover the benefits of {product_name} today.",
                f"Experience the quality of {product_name} for yourself.",
                f"See what makes {product_name} special."
            ]
        
        return random.choice(templates)
    
    def get_variant_for_user(self, test_id: str, user_id: str) -> Dict[str, Any]:
        """Get variant for a specific user (deterministic based on user_id)"""
        
        if test_id not in self.active_tests:
            return None
        
        test = self.active_tests[test_id]
        
        # Use user_id to deterministically assign variant
        user_hash = hash(user_id) % 100
        traffic_split = test["traffic_split"]
        
        if user_hash < (traffic_split * 100):
            # Show control (first variant)
            return test["variants"][0]
        else:
            # Show variant (random from remaining variants)
            variant_variants = test["variants"][1:]
            return random.choice(variant_variants)
    
    def record_impression(self, test_id: str, variant_id: str, user_id: str):
        """Record an impression for a test variant"""
        
        if test_id not in self.active_tests:
            return
        
        test = self.active_tests[test_id]
        
        # Determine if this is control or variant
        is_control = variant_id == test["variants"][0].get("variant_id", "control")
        metric_key = "control" if is_control else "variant"
        
        test["metrics"]["impressions"][metric_key] += 1
        logger.info(f"Recorded impression for {test_id} - {metric_key}")
    
    def record_click(self, test_id: str, variant_id: str, user_id: str):
        """Record a click for a test variant"""
        
        if test_id not in self.active_tests:
            return
        
        test = self.active_tests[test_id]
        
        # Determine if this is control or variant
        is_control = variant_id == test["variants"][0].get("variant_id", "control")
        metric_key = "control" if is_control else "variant"
        
        test["metrics"]["clicks"][metric_key] += 1
        logger.info(f"Recorded click for {test_id} - {metric_key}")
    
    def record_conversion(self, test_id: str, variant_id: str, user_id: str, revenue: float = 0.0):
        """Record a conversion for a test variant"""
        
        if test_id not in self.active_tests:
            return
        
        test = self.active_tests[test_id]
        
        # Determine if this is control or variant
        is_control = variant_id == test["variants"][0].get("variant_id", "control")
        metric_key = "control" if is_control else "variant"
        
        test["metrics"]["conversions"][metric_key] += 1
        test["metrics"]["revenue"][metric_key] += revenue
        logger.info(f"Recorded conversion for {test_id} - {metric_key}, revenue: ${revenue}")
    
    def get_test_results(self, test_id: str) -> Dict[str, Any]:
        """Get results for a specific test"""
        
        if test_id not in self.active_tests:
            return None
        
        test = self.active_tests[test_id]
        metrics = test["metrics"]
        
        # Calculate rates
        control_impressions = metrics["impressions"]["control"]
        variant_impressions = metrics["impressions"]["variant"]
        control_clicks = metrics["clicks"]["control"]
        variant_clicks = metrics["clicks"]["variant"]
        control_conversions = metrics["conversions"]["control"]
        variant_conversions = metrics["conversions"]["variant"]
        control_revenue = metrics["revenue"]["control"]
        variant_revenue = metrics["revenue"]["variant"]
        
        # Calculate CTR
        control_ctr = (control_clicks / control_impressions) if control_impressions > 0 else 0
        variant_ctr = (variant_clicks / variant_impressions) if variant_impressions > 0 else 0
        
        # Calculate conversion rate
        control_conversion_rate = (control_conversions / control_clicks) if control_clicks > 0 else 0
        variant_conversion_rate = (variant_conversions / variant_clicks) if variant_clicks > 0 else 0
        
        # Calculate revenue per impression
        control_rpi = (control_revenue / control_impressions) if control_impressions > 0 else 0
        variant_rpi = (variant_revenue / variant_impressions) if variant_impressions > 0 else 0
        
        # Calculate improvements
        ctr_improvement = ((variant_ctr - control_ctr) / control_ctr * 100) if control_ctr > 0 else 0
        conversion_improvement = ((variant_conversion_rate - control_conversion_rate) / control_conversion_rate * 100) if control_conversion_rate > 0 else 0
        revenue_improvement = ((variant_rpi - control_rpi) / control_rpi * 100) if control_rpi > 0 else 0
        
        # Determine winner
        winner = "variant" if variant_ctr > control_ctr else "control"
        
        results = {
            "test_id": test_id,
            "test_name": test["test_name"],
            "test_type": test["test_type"],
            "status": test["status"],
            "control_metrics": {
                "impressions": control_impressions,
                "clicks": control_clicks,
                "conversions": control_conversions,
                "revenue": control_revenue,
                "ctr": control_ctr,
                "conversion_rate": control_conversion_rate,
                "revenue_per_impression": control_rpi
            },
            "variant_metrics": {
                "impressions": variant_impressions,
                "clicks": variant_clicks,
                "conversions": variant_conversions,
                "revenue": variant_revenue,
                "ctr": variant_ctr,
                "conversion_rate": variant_conversion_rate,
                "revenue_per_impression": variant_rpi
            },
            "improvements": {
                "ctr_improvement_percent": ctr_improvement,
                "conversion_improvement_percent": conversion_improvement,
                "revenue_improvement_percent": revenue_improvement
            },
            "winner": winner,
            "confidence_level": self._calculate_confidence_level(control_impressions, variant_impressions, control_ctr, variant_ctr)
        }
        
        return results
    
    def _calculate_confidence_level(self, control_impressions: int, variant_impressions: int, control_ctr: float, variant_ctr: float) -> str:
        """Calculate confidence level for test results"""
        
        # Simple confidence calculation based on sample size and difference
        total_impressions = control_impressions + variant_impressions
        
        if total_impressions < 100:
            return "low"
        elif total_impressions < 1000:
            return "medium"
        else:
            # Check if difference is statistically significant (simplified)
            ctr_difference = abs(variant_ctr - control_ctr)
            if ctr_difference > 0.02:  # 2% difference
                return "high"
            elif ctr_difference > 0.01:  # 1% difference
                return "medium"
            else:
                return "low"
    
    def get_all_tests(self) -> List[Dict[str, Any]]:
        """Get all active tests"""
        return list(self.active_tests.values())
    
    def end_test(self, test_id: str) -> Dict[str, Any]:
        """End a test and return final results"""
        
        if test_id not in self.active_tests:
            return None
        
        test = self.active_tests[test_id]
        test["status"] = "completed"
        
        results = self.get_test_results(test_id)
        
        # Store results
        self.test_results[test_id] = results
        
        logger.info(f"Ended test: {test_id}")
        
        return results

# Global A/B testing service instance
ab_testing_service = ABTestingService()
