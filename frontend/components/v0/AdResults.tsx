"use client"

import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"

interface AdResultsProps {
  results: {
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
}

export function AdResults({ results }: AdResultsProps) {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center">
        <h2 className="text-2xl font-bold mb-2">Generated Ads & Recommendations</h2>
        <p className="text-gray-600">Personalized content for {results.brand.company_name}</p>
      </div>

      {/* Targeting Metrics */}
      <Card className="p-6">
        <h3 className="text-lg font-semibold mb-4">Targeting Metrics</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
          <div>
            <span className="font-medium">Location:</span> {results.targeting_metrics.zipcode}
          </div>
          <div>
            <span className="font-medium">Age:</span> {results.targeting_metrics.age_range}
          </div>
          <div>
            <span className="font-medium">Interests:</span> {results.targeting_metrics.interests.join(', ')}
          </div>
          <div>
            <span className="font-medium">Registration ID:</span> {results.registration_id}
          </div>
        </div>
      </Card>

      {/* Generated Ads */}
      <div className="space-y-4">
        <h3 className="text-lg font-semibold">Generated Ads</h3>
        {results.initial_ads.map((ad, index) => (
          <Card key={ad.id} className="p-6">
            <div className="space-y-3">
              <div className="flex justify-between items-start">
                <h4 className="font-semibold text-lg">{ad.headline}</h4>
                <Badge variant="secondary">{ad.audience_segment}</Badge>
              </div>
              <p className="text-gray-600">{ad.body}</p>
              <div className="flex justify-between items-center">
                <span className="text-sm text-blue-600 font-medium">{ad.cta}</span>
                <div className="text-xs text-gray-500">
                  <strong>Targeting:</strong> {JSON.stringify(ad.targeting)}
                </div>
              </div>
            </div>
          </Card>
        ))}
      </div>

      {/* Channel Recommendations */}
      <Card className="p-6">
        <h3 className="text-lg font-semibold mb-4">Recommended Channels</h3>
        <div className="space-y-2">
          {results.channel_recommendations.map((rec, index) => (
            <div key={index} className="flex justify-between items-center p-3 bg-gray-50 rounded">
              <div>
                <span className="font-medium">{rec.channel}</span>
                <p className="text-sm text-gray-600">{rec.reason}</p>
              </div>
              <Badge 
                variant={rec.priority === 'high' ? 'default' : 'secondary'}
                className={rec.priority === 'high' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}
              >
                {rec.priority}
              </Badge>
            </div>
          ))}
        </div>
      </Card>

      {/* Environmental Impact */}
      <Card className="p-6">
        <h3 className="text-lg font-semibold mb-4">Environmental Impact</h3>
        <div className="grid grid-cols-3 gap-4 text-center">
          <div>
            <div className="text-2xl font-bold text-green-600">{results.environmental_impact.total_energy_kwh} kWh</div>
            <div className="text-sm text-gray-600">Energy Used</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-green-600">{results.environmental_impact.total_co2_kg} kg</div>
            <div className="text-sm text-gray-600">CO2 Emissions</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-green-600">{results.environmental_impact.green_score}/100</div>
            <div className="text-sm text-gray-600">Green Score</div>
          </div>
        </div>
      </Card>
    </div>
  )
}
