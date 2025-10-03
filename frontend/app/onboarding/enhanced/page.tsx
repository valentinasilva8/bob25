"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { createClient } from "@/lib/supabase/client"

export default function EnhancedOnboarding() {
  const [formData, setFormData] = useState({
    business_name: "",
    mission: "",
    products: "",
    audience: "",
    zipcode: "",
    age_range: "25-35",
    interests: []
  })

  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const supabase = createClient()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
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

      const data = await response.json()

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
                primary: data.channel_recommendations
                  .filter((rec: any) => rec.priority === "high")
                  .map((rec: any) => rec.channel.toLowerCase()),
                secondary: data.channel_recommendations
                  .filter((rec: any) => rec.priority === "medium")
                  .map((rec: any) => rec.channel.toLowerCase()),
                excluded: []
              }
            },
            environmental_score: data.environmental_impact.green_score,
            registration_id: data.registration_id,
            onboarding_completed: true
          })

        if (dbError) {
          console.error('Supabase error:', dbError)
          // Don't throw error, just log it - user still gets results
        }
      }

      setResults(data)
    } catch (err) {
      console.error('Error:', err)
      setError(err instanceof Error ? err.message : 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  const handleInterestChange = (interest: string) => {
    setFormData(prev => ({
      ...prev,
      interests: prev.interests.includes(interest)
        ? prev.interests.filter(i => i !== interest)
        : [...prev.interests, interest]
    }))
  }

  const interestOptions = [
    'yoga', 'meditation', 'wellness', 'mindfulness', 
    'fitness', 'stress-relief', 'nutrition', 'community'
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 via-blue-50 to-purple-50 py-12">
      <div className="max-w-6xl mx-auto px-4">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-green-600 to-blue-600 bg-clip-text text-transparent mb-4">
            Generate Personalized Ads
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Tell us about your wellness business and we'll create targeted, sustainable ads for your audience
          </p>
        </div>

        {/* Error Message */}
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 text-red-700 rounded-lg">
            <div className="flex items-center">
              <div className="text-red-500 mr-2">⚠️</div>
              <span>Error: {error}</span>
            </div>
          </div>
        )}

        {/* Main Form Card */}
        <Card className="p-8 shadow-xl border-0 bg-white/80 backdrop-blur-sm">
          <form onSubmit={handleSubmit} className="space-y-8">
            {/* Basic Information Section */}
            <div className="space-y-6">
              <div className="flex items-center space-x-2 mb-4">
                <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                  <span className="text-green-600 font-semibold">1</span>
                </div>
                <h2 className="text-xl font-semibold text-gray-800">Basic Information</h2>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-2">
                  <label className="block text-sm font-medium text-gray-700">Business Name</label>
                  <Input
                    value={formData.business_name}
                    onChange={(e) => setFormData(prev => ({...prev, business_name: e.target.value}))}
                    placeholder="e.g., Zen Flow Yoga"
                    className="h-12 text-lg"
                    required
                  />
                </div>
                <div className="space-y-2">
                  <label className="block text-sm font-medium text-gray-700">Zip Code</label>
                  <Input
                    value={formData.zipcode}
                    onChange={(e) => setFormData(prev => ({...prev, zipcode: e.target.value}))}
                    placeholder="e.g., 10001"
                    className="h-12 text-lg"
                    required
                  />
                </div>
              </div>

              <div className="space-y-2">
                <label className="block text-sm font-medium text-gray-700">Mission & Story</label>
                <Textarea
                  value={formData.mission}
                  onChange={(e) => setFormData(prev => ({...prev, mission: e.target.value}))}
                  placeholder="Tell us your business story and mission..."
                  rows={3}
                  className="text-lg"
                  required
                />
              </div>

              <div className="space-y-2">
                <label className="block text-sm font-medium text-gray-700">Products & Services</label>
                <Textarea
                  value={formData.products}
                  onChange={(e) => setFormData(prev => ({...prev, products: e.target.value}))}
                  placeholder="e.g., Morning yoga classes, meditation workshops, wellness coaching"
                  rows={2}
                  className="text-lg"
                  required
                />
              </div>

              <div className="space-y-2">
                <label className="block text-sm font-medium text-gray-700">Target Audience</label>
                <Textarea
                  value={formData.audience}
                  onChange={(e) => setFormData(prev => ({...prev, audience: e.target.value}))}
                  placeholder="e.g., Stressed professionals seeking balance"
                  rows={2}
                  className="text-lg"
                  required
                />
              </div>
            </div>

            {/* Demographics Section */}
            <div className="space-y-6">
              <div className="flex items-center space-x-2 mb-4">
                <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                  <span className="text-blue-600 font-semibold">2</span>
                </div>
                <h2 className="text-xl font-semibold text-gray-800">Target Demographics</h2>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-2">
                  <label className="block text-sm font-medium text-gray-700">Age Range</label>
                  <select
                    value={formData.age_range}
                    onChange={(e) => setFormData(prev => ({...prev, age_range: e.target.value}))}
                    className="w-full h-12 p-3 border border-gray-300 rounded-lg text-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  >
                    <option value="18-25">18-25</option>
                    <option value="25-35">25-35</option>
                    <option value="35-45">35-45</option>
                    <option value="45-55">45-55</option>
                    <option value="55+">55+</option>
                  </select>
                </div>
              </div>
            </div>

            {/* Interests Section */}
            <div className="space-y-6">
              <div className="flex items-center space-x-2 mb-4">
                <div className="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center">
                  <span className="text-purple-600 font-semibold">3</span>
                </div>
                <h2 className="text-xl font-semibold text-gray-800">Interests & Focus Areas</h2>
              </div>

              <div className="space-y-2">
                <label className="block text-sm font-medium text-gray-700">Select all that apply</label>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                  {interestOptions.map(interest => (
                    <label key={interest} className="flex items-center space-x-3 p-3 rounded-lg border border-gray-200 hover:bg-green-50 hover:border-green-300 cursor-pointer transition-colors">
                      <input
                        type="checkbox"
                        checked={formData.interests.includes(interest)}
                        onChange={() => handleInterestChange(interest)}
                        className="w-4 h-4 text-green-600 border-gray-300 rounded focus:ring-green-500"
                      />
                      <span className="text-sm font-medium capitalize text-gray-700">{interest}</span>
                    </label>
                  ))}
                </div>
              </div>
            </div>

            {/* Submit Button */}
            <div className="pt-6">
              <Button 
                type="submit" 
                disabled={loading} 
                className="w-full h-14 text-lg font-semibold bg-gradient-to-r from-green-600 to-blue-600 hover:from-green-700 hover:to-blue-700 text-white rounded-lg shadow-lg hover:shadow-xl transition-all duration-200"
              >
                {loading ? (
                  <div className="flex items-center space-x-2">
                    <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                    <span>Generating Ads...</span>
                  </div>
                ) : (
                  "Generate Personalized Ads"
                )}
              </Button>
            </div>
          </form>
        </Card>

        {/* Results Section */}
        {results && (
          <div className="mt-12 space-y-8">
            <div className="text-center">
              <h2 className="text-3xl font-bold text-gray-800 mb-2">Your Personalized Ads</h2>
              <p className="text-gray-600">Generated based on your business profile and target audience</p>
            </div>
            
            {/* Targeting Metrics */}
            <Card className="p-6 bg-gradient-to-r from-green-50 to-blue-50 border-0">
              <h3 className="text-xl font-semibold mb-6 text-gray-800">Targeting Metrics</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                <div className="text-center">
                  <div className="text-2xl font-bold text-green-600">{results.targeting_metrics.zipcode}</div>
                  <div className="text-sm text-gray-600">Location</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-600">{results.targeting_metrics.age_range}</div>
                  <div className="text-sm text-gray-600">Age Range</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-purple-600">{results.targeting_metrics.interests.length}</div>
                  <div className="text-sm text-gray-600">Interests</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-orange-600">{results.targeting_metrics.preferred_channels.length}</div>
                  <div className="text-sm text-gray-600">Channels</div>
                </div>
              </div>
            </Card>

            {/* Generated Ads */}
            <div className="space-y-6">
              <h3 className="text-2xl font-semibold text-gray-800">Generated Ads</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {results.initial_ads.map((ad: any) => (
                  <Card key={ad.id} className="p-6 hover:shadow-lg transition-shadow border-0 bg-white">
                    <div className="space-y-4">
                      <div className="flex items-start justify-between">
                        <h4 className="text-lg font-semibold text-gray-800">{ad.headline}</h4>
                        <Badge variant="secondary" className="bg-green-100 text-green-800">
                          {ad.audience_segment.replace(/_/g, ' ')}
                        </Badge>
                      </div>
                      <p className="text-gray-600 leading-relaxed">{ad.body}</p>
                      <div className="flex items-center justify-between pt-4 border-t border-gray-100">
                        <span className="text-green-600 font-semibold text-lg">{ad.cta}</span>
                        <div className="text-xs text-gray-500">
                          {ad.targeting.location && `📍 ${ad.targeting.location}`}
                          {ad.targeting.age && ` • 👥 ${ad.targeting.age}`}
                        </div>
                      </div>
                    </div>
                  </Card>
                ))}
              </div>
            </div>

            {/* Channel Recommendations */}
            <Card className="p-6 bg-gradient-to-r from-blue-50 to-purple-50 border-0">
              <h3 className="text-xl font-semibold mb-6 text-gray-800">Recommended Channels</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {results.channel_recommendations.map((rec: any, index: number) => (
                  <div key={index} className="flex items-center justify-between p-4 bg-white rounded-lg shadow-sm">
                    <div className="flex-1">
                      <div className="font-semibold text-gray-800">{rec.channel}</div>
                      <p className="text-sm text-gray-600 mt-1">{rec.reason}</p>
                    </div>
                    <Badge 
                      className={`${
                        rec.priority === 'high' 
                          ? 'bg-green-100 text-green-800' 
                          : 'bg-yellow-100 text-yellow-800'
                      }`}
                    >
                      {rec.priority}
                    </Badge>
                  </div>
                ))}
              </div>
            </Card>

            {/* Environmental Impact */}
            <Card className="p-6 bg-gradient-to-r from-green-50 to-emerald-50 border-0">
              <h3 className="text-xl font-semibold mb-6 text-gray-800">Environmental Impact</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-center">
                <div className="space-y-2">
                  <div className="text-3xl font-bold text-green-600">{results.environmental_impact.total_energy_kwh} kWh</div>
                  <div className="text-sm text-gray-600">Energy Used</div>
                </div>
                <div className="space-y-2">
                  <div className="text-3xl font-bold text-green-600">{results.environmental_impact.total_co2_kg} kg</div>
                  <div className="text-sm text-gray-600">CO2 Emissions</div>
                </div>
                <div className="space-y-2">
                  <div className="text-3xl font-bold text-green-600">{results.environmental_impact.green_score}/100</div>
                  <div className="text-sm text-gray-600">Green Score</div>
                </div>
              </div>
            </Card>
          </div>
        )}
      </div>
    </div>
  )
}
