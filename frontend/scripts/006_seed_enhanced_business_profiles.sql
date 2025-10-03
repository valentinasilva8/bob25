-- Seed enhanced business_profiles table with sample data
-- This script inserts sample business profiles with targeting metrics

-- Insert sample wellness businesses with enhanced targeting data
-- Note: These are sample records for demonstration. In production, you would insert
-- records with real user_id values from the auth.users table.

-- First, let's create a function to safely insert sample data
CREATE OR REPLACE FUNCTION insert_sample_business_profiles()
RETURNS void AS $$
DECLARE
    sample_user_id UUID;
BEGIN
    -- Try to get an existing user, or create a sample one for demo purposes
    SELECT id INTO sample_user_id FROM auth.users LIMIT 1;
    
    -- If no users exist, we'll skip the insert and just show the structure
    IF sample_user_id IS NULL THEN
        RAISE NOTICE 'No users found in auth.users table. Sample data insertion skipped.';
        RAISE NOTICE 'To insert sample data, first create a user account through the frontend.';
        RETURN;
    END IF;
    
    -- Insert sample data with the real user_id
    INSERT INTO public.business_profiles (
        user_id,
        business_name,
        business_story,
        products_services,
        target_audience,
        growth_goals,
        zipcode,
        age_range,
        interests,
        preferred_channels,
        targeting_data,
        environmental_score,
        registration_id,
        onboarding_completed
    ) VALUES 
    (
        sample_user_id, -- Use real user_id
    'Solstice Yoga Studio',
    'Founded by two sisters who turned an empty storefront into a welcoming studio powered by renewable energy. We believe wellness should be accessible to everyone in our community.',
    'Morning yoga classes, meditation workshops, wellness coaching, community events',
    'Health-conscious individuals seeking balance and community connection',
    'Expand to offer online classes and reach 500+ community members',
    '10001',
    '25-45',
    ARRAY['yoga', 'meditation', 'wellness', 'community'],
    ARRAY['instagram', 'facebook', 'email'],
    '{
        "demographics": {
            "age_range": "25-45",
            "gender": "all",
            "income_level": "middle"
        },
        "location": {
            "zipcode": "10001",
            "city": "New York",
            "state": "NY",
            "radius_km": 5
        },
        "interests": ["yoga", "meditation", "wellness", "community"],
        "behavior": {
            "device_preference": "mobile",
            "time_preference": "morning",
            "frequency": "weekly"
        },
        "channels": {
            "primary": ["instagram", "facebook"],
            "secondary": ["google_ads", "email"],
            "excluded": ["tiktok"]
        }
    }'::jsonb,
    95.0,
    'reg_solstice_yoga_studio',
    true
),
(
    gen_random_uuid(),
    'EcoPet Supplies',
    'A family-owned pet supply store focused on sustainable, eco-friendly products for conscious pet owners.',
    'Organic pet food, eco-friendly toys, sustainable accessories, grooming services',
    'Eco-conscious pet owners who prioritize sustainability',
    'Become the go-to sustainable pet store in our region',
    '90210',
    '30-50',
    ARRAY['pets', 'sustainability', 'eco-friendly', 'animals'],
    ARRAY['facebook', 'google_ads', 'local_events'],
    '{
        "demographics": {
            "age_range": "30-50",
            "gender": "all",
            "income_level": "middle_high"
        },
        "location": {
            "zipcode": "90210",
            "city": "Beverly Hills",
            "state": "CA",
            "radius_km": 15
        },
        "interests": ["pets", "sustainability", "eco-friendly", "animals"],
        "behavior": {
            "device_preference": "desktop",
            "time_preference": "weekend",
            "frequency": "monthly"
        },
        "channels": {
            "primary": ["facebook", "google_ads"],
            "secondary": ["local_events", "email"],
            "excluded": ["tiktok", "snapchat"]
        }
    }'::jsonb,
    88.0,
    'reg_ecopet_supplies',
    true
),
(
    gen_random_uuid(),
    'FitFusion Boutique Fitness',
    'A boutique fitness studio offering personalized training and group classes in a supportive community environment.',
    'Personal training, group fitness classes, nutrition coaching, wellness workshops',
    'Fitness enthusiasts seeking personalized, community-focused training',
    'Open 3 additional locations and launch online training program',
    '60601',
    '25-40',
    ARRAY['fitness', 'health', 'wellness', 'community'],
    ARRAY['instagram', 'tiktok', 'google_ads'],
    '{
        "demographics": {
            "age_range": "25-40",
            "gender": "all",
            "income_level": "middle"
        },
        "location": {
            "zipcode": "60601",
            "city": "Chicago",
            "state": "IL",
            "radius_km": 8
        },
        "interests": ["fitness", "health", "wellness", "community"],
        "behavior": {
            "device_preference": "mobile",
            "time_preference": "evening",
            "frequency": "daily"
        },
        "channels": {
            "primary": ["instagram", "tiktok"],
            "secondary": ["google_ads", "facebook"],
            "excluded": ["linkedin"]
        }
    }'::jsonb,
    92.0,
    'reg_fitfusion_boutique',
    true
    );
    
    RAISE NOTICE 'Sample business profiles inserted successfully!';
    
EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'Error inserting sample data: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

-- Execute the function to insert sample data
SELECT insert_sample_business_profiles();

-- Create a view for easy querying of business profiles with targeting data
CREATE OR REPLACE VIEW public.business_profiles_with_targeting AS
SELECT 
    bp.*,
    bp.targeting_data->>'demographics' as demographics,
    bp.targeting_data->>'location' as location_data,
    bp.targeting_data->>'behavior' as behavior_data,
    bp.targeting_data->>'channels' as channels_data
FROM public.business_profiles bp;

-- Create a function to get businesses by targeting criteria
CREATE OR REPLACE FUNCTION get_businesses_by_targeting(
    p_zipcode VARCHAR(10) DEFAULT NULL,
    p_age_range VARCHAR(10) DEFAULT NULL,
    p_interests TEXT[] DEFAULT NULL
)
RETURNS TABLE (
    business_name TEXT,
    products_services TEXT,
    zipcode VARCHAR(10),
    age_range VARCHAR(10),
    interests TEXT[],
    environmental_score DECIMAL(5,2)
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        bp.business_name,
        bp.products_services,
        bp.zipcode,
        bp.age_range,
        bp.interests,
        bp.environmental_score
    FROM public.business_profiles bp
    WHERE 
        (p_zipcode IS NULL OR bp.zipcode = p_zipcode)
        AND (p_age_range IS NULL OR bp.age_range = p_age_range)
        AND (p_interests IS NULL OR bp.interests && p_interests)
    ORDER BY bp.environmental_score DESC, bp.created_at DESC;
END;
$$ LANGUAGE plpgsql;

-- Grant necessary permissions
GRANT SELECT ON public.business_profiles_with_targeting TO authenticated;
GRANT EXECUTE ON FUNCTION get_businesses_by_targeting TO authenticated;
