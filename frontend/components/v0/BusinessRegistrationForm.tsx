"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Card } from "@/components/ui/card"

interface BusinessRegistrationFormProps {
  onSubmit: (data: BusinessFormData) => void
  loading?: boolean
}

interface BusinessFormData {
  business_name: string
  zipcode: string
  mission: string
  products: string
  audience: string
  age_range: string
  interests: string[]
}

export function BusinessRegistrationForm({ onSubmit, loading = false }: BusinessRegistrationFormProps) {
  const [formData, setFormData] = useState<BusinessFormData>({
    business_name: "",
    zipcode: "",
    mission: "",
    products: "",
    audience: "",
    age_range: "25-35",
    interests: []
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSubmit(formData)
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
    <Card className="p-8 max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-center mb-2">Generate Personalized Ads</h1>
        <p className="text-center text-gray-600">Tell us about your business and we'll create targeted ads for your audience</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Basic Info */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium mb-2">Business Name</label>
            <Input
              value={formData.business_name}
              onChange={(e) => setFormData(prev => ({...prev, business_name: e.target.value}))}
              placeholder="e.g., Zen Flow Yoga"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-2">Zip Code</label>
            <Input
              value={formData.zipcode}
              onChange={(e) => setFormData(prev => ({...prev, zipcode: e.target.value}))}
              placeholder="e.g., 10001"
              required
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">Mission/Story</label>
          <Textarea
            value={formData.mission}
            onChange={(e) => setFormData(prev => ({...prev, mission: e.target.value}))}
            placeholder="Tell us your business story and mission..."
            rows={3}
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">Products/Services</label>
          <Textarea
            value={formData.products}
            onChange={(e) => setFormData(prev => ({...prev, products: e.target.value}))}
            placeholder="e.g., Morning yoga classes, meditation workshops, wellness coaching"
            rows={2}
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">Target Audience</label>
          <Textarea
            value={formData.audience}
            onChange={(e) => setFormData(prev => ({...prev, audience: e.target.value}))}
            placeholder="e.g., Stressed professionals seeking balance"
            rows={2}
            required
          />
        </div>

        {/* Demographics */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium mb-2">Age Range</label>
            <select
              value={formData.age_range}
              onChange={(e) => setFormData(prev => ({...prev, age_range: e.target.value}))}
              className="w-full p-2 border rounded-md"
            >
              <option value="18-25">18-25</option>
              <option value="25-35">25-35</option>
              <option value="35-45">35-45</option>
              <option value="45-55">45-55</option>
              <option value="55+">55+</option>
            </select>
          </div>
        </div>

        {/* Interests */}
        <div>
          <label className="block text-sm font-medium mb-2">Interests (select all that apply)</label>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
            {interestOptions.map(interest => (
              <label key={interest} className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  checked={formData.interests.includes(interest)}
                  onChange={() => handleInterestChange(interest)}
                  className="rounded"
                />
                <span className="text-sm capitalize">{interest}</span>
              </label>
            ))}
          </div>
        </div>

        <Button type="submit" disabled={loading} className="w-full">
          {loading ? "Generating Ads..." : "Generate Personalized Ads"}
        </Button>
      </form>
    </Card>
  )
}
