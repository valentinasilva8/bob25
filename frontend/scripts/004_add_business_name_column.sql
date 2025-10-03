-- Add business_name column to business_profiles table
ALTER TABLE public.business_profiles
ADD COLUMN business_name TEXT NOT NULL DEFAULT '';

-- Remove the default after adding the column
ALTER TABLE public.business_profiles
ALTER COLUMN business_name DROP DEFAULT;
