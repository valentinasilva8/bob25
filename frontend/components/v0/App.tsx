"use client"

import { useState } from "react"
import { BusinessRegistrationForm } from "./BusinessRegistrationForm"
import { AdResults } from "./AdResults"

interface BusinessFormData {
  business_name: string
  zipcode: string
  mission: string
  products: string
  audience: string
  age_range: string
  interests: string[]
}

export default function App() {
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (formData: BusinessFormData) => {
    setLoading(true)

    try {
      const response = await fetch('http://localhost:8000/business/register/wellness', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      })

      const data = await response.json()
      setResults(data)
    } catch (error) {
      console.error('Error:', error)
      alert('Error generating ads. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-6xl mx-auto px-4">
        {!results ? (
          <BusinessRegistrationForm onSubmit={handleSubmit} loading={loading} />
        ) : (
          <AdResults results={results} />
        )}
      </div>
    </div>
  )
}
