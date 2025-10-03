-- Enhance business_profiles table with targeting metrics
-- This script adds new columns for enhanced targeting and personalization

-- Add new columns for targeting metrics
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

-- Example of what targeting_data JSONB might contain:
-- {
--   "demographics": {
--     "age_range": "25-35",
--     "gender": "all",
--     "income_level": "middle"
--   },
--   "location": {
--     "zipcode": "10001",
--     "city": "New York",
--     "state": "NY",
--     "radius_km": 10
--   },
--   "interests": ["yoga", "meditation", "wellness"],
--   "behavior": {
--     "device_preference": "mobile",
--     "time_preference": "evening",
--     "frequency": "weekly"
--   },
--   "channels": {
--     "primary": ["instagram", "facebook"],
--     "secondary": ["google_ads", "email"],
--     "excluded": ["tiktok"]
--   }
-- }
