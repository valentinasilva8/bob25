"use client"

import { useState } from "react"
import { createClient } from "@/components/awe/lib/supabase/client"

interface BusinessFormData {
  business_name: string
  zipcode: string
  mission: string
  products: string
  audience: string
  age_range: string
  interests: string[]
}

interface AdResults {
  registration_id: string
  brand: {
    company_name: string
    mission: string
  }
  targeting_metrics: {
    zipcode: string
    age_range: string
    interests: string[]
  }
  initial_ads: Array<{
    id: string
    headline: string
    body: string
    cta: string
    audience_segment: string
    targeting: any
  }>
  channel_recommendations: Array<{
    channel: string
    reason: string
    priority: string
  }>
  environmental_impact: {
    total_energy_kwh: number
    total_co2_kg: number
    green_score: number
  }
}

export function V0IntegrationWrapper() {
  const [results, setResults] = useState<AdResults | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const supabase = createClient()

  const handleFormSubmit = async (formData: BusinessFormData) => {
    setLoading(true)
    setError(null)

    try {
      // 1. Call your backend API
      const response = await fetch('http://localhost:8000/business/register/wellness', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const apiResults: AdResults = await response.json()

      // 2. Save to Supabase
      const { data: user } = await supabase.auth.getUser()
      
      if (user.user) {
        const { error: dbError } = await supabase
          .from('business_profiles')
          .insert({
            user_id: user.user.id,
            business_name: formData.business_name,
            business_story: formData.mission,
            products_services: formData.products,
            target_audience: formData.audience,
            growth_goals: "Expand reach and impact",
            zipcode: formData.zipcode,
            age_range: formData.age_range,
            interests: formData.interests,
            preferred_channels: ["social", "email"],
            targeting_data: {
              demographics: {
                age_range: formData.age_range,
                gender: "all",
                income_level: "middle"
              },
              location: {
                zipcode: formData.zipcode,
                radius_km: 10
              },
              interests: formData.interests,
              behavior: {
                device_preference: "mobile",
                time_preference: "evening",
                frequency: "weekly"
              },
              channels: {
                primary: apiResults.channel_recommendations
                  .filter(rec => rec.priority === "high")
                  .map(rec => rec.channel.toLowerCase()),
                secondary: apiResults.channel_recommendations
                  .filter(rec => rec.priority === "medium")
                  .map(rec => rec.channel.toLowerCase()),
                excluded: []
              }
            },
            environmental_score: apiResults.environmental_impact.green_score,
            registration_id: apiResults.registration_id,
            onboarding_completed: true
          })

        if (dbError) {
          console.error('Supabase error:', dbError)
          // Don't throw error, just log it - user still gets results
        }
      }

      // 3. Set results for display
      setResults(apiResults)

    } catch (err) {
      console.error('Error:', err)
      setError(err instanceof Error ? err.message : 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  // This will be replaced by your v0 component
  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-6xl mx-auto px-4">
        {error && (
          <div className="mb-6 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
            Error: {error}
          </div>
        )}
        
        {/* Your v0 component will go here */}
        {/* Make sure to pass handleFormSubmit as a prop */}
        
        {results && (
          <div className="mt-8">
            <h2 className="text-2xl font-bold mb-4">Generated Results</h2>
            <pre className="bg-gray-100 p-4 rounded text-sm overflow-auto">
              {JSON.stringify(results, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </div>
  )
}
