-- Safe table update script - only adds columns, no sample data
-- This script safely enhances the business_profiles table without foreign key issues

-- Add new columns for targeting metrics (if they don't exist)
ALTER TABLE public.business_profiles 
ADD COLUMN IF NOT EXISTS business_name TEXT,
ADD COLUMN IF NOT EXISTS zipcode VARCHAR(10),
ADD COLUMN IF NOT EXISTS age_range VARCHAR(10),
ADD COLUMN IF NOT EXISTS interests TEXT[], -- Array of interests
ADD COLUMN IF NOT EXISTS preferred_channels TEXT[], -- Array of preferred channels
ADD COLUMN IF NOT EXISTS targeting_data JSONB, -- Store complex targeting data
ADD COLUMN IF NOT EXISTS environmental_score DECIMAL(5,2) DEFAULT 95.0,
ADD COLUMN IF NOT EXISTS registration_id VARCHAR(100);

-- Update existing records to have business_name (if not set)
UPDATE public.business_profiles 
SET business_name = COALESCE(business_name, 'Unnamed Business')
WHERE business_name IS NULL;

-- Make business_name NOT NULL after setting defaults
ALTER TABLE public.business_profiles 
ALTER COLUMN business_name SET NOT NULL;

-- Create indexes for better performance on new columns
CREATE INDEX IF NOT EXISTS business_profiles_zipcode_idx ON public.business_profiles(zipcode);
CREATE INDEX IF NOT EXISTS business_profiles_age_range_idx ON public.business_profiles(age_range);
CREATE INDEX IF NOT EXISTS business_profiles_interests_idx ON public.business_profiles USING GIN(interests);
CREATE INDEX IF NOT EXISTS business_profiles_registration_id_idx ON public.business_profiles(registration_id);

-- Create a function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger to automatically update updated_at
DROP TRIGGER IF EXISTS update_business_profiles_updated_at ON public.business_profiles;
CREATE TRIGGER update_business_profiles_updated_at
    BEFORE UPDATE ON public.business_profiles
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Add comments for documentation
COMMENT ON COLUMN public.business_profiles.business_name IS 'Official business name';
COMMENT ON COLUMN public.business_profiles.zipcode IS 'Business location zip code for local targeting';
COMMENT ON COLUMN public.business_profiles.age_range IS 'Target audience age range (e.g., 25-35)';
COMMENT ON COLUMN public.business_profiles.interests IS 'Array of target audience interests';
COMMENT ON COLUMN public.business_profiles.preferred_channels IS 'Array of preferred advertising channels';
COMMENT ON COLUMN public.business_profiles.targeting_data IS 'JSON object containing complex targeting parameters';
COMMENT ON COLUMN public.business_profiles.environmental_score IS 'Environmental impact score (0-100)';
COMMENT ON COLUMN public.business_profiles.registration_id IS 'Unique registration identifier for tracking';

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

-- Show success message
DO $$
BEGIN
    RAISE NOTICE '✅ Business profiles table enhanced successfully!';
    RAISE NOTICE '📊 New columns added: business_name, zipcode, age_range, interests, preferred_channels, targeting_data, environmental_score, registration_id';
    RAISE NOTICE '🔍 New functions created: get_businesses_by_targeting()';
    RAISE NOTICE '📋 New view created: business_profiles_with_targeting';
    RAISE NOTICE '🎯 Ready for enhanced targeting and personalization!';
END $$;
