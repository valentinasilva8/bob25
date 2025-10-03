"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Input } from "@/components/ui/input"
import { Progress } from "@/components/ui/progress"
// import { createBrowserClient } from "@supabase/ssr"
import { ArrowRight, ArrowLeft, Sparkles } from "lucide-react"
import Link from "next/link"
import Image from "next/image"

export default function OnboardingPage() {
  const router = useRouter()
  const [currentStep, setCurrentStep] = useState(1)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const [formData, setFormData] = useState({
    businessName: "",
    zipcode: "",
    businessStory: "",
    productsServices: "",
    targetAudience: "",
    ageRange: "",
    interests: "",
    preferredChannels: "",
  })

  // const supabase = createBrowserClient(
  //   process.env.NEXT_PUBLIC_SUPABASE_URL!,
  //   process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
  // )

  const totalSteps = 8
  const progress = (currentStep / totalSteps) * 100

  const handleNext = () => {
    if (currentStep < totalSteps) {
      setCurrentStep(currentStep + 1)
    }
  }

  const handleBack = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1)
    }
  }

  const handleSubmit = async () => {
    setIsSubmitting(true)
    setError(null)

    try {
      console.log('Submitting form data:', formData)
      
      // Call your backend API to generate personalized ads
      const response = await fetch('http://localhost:8002/business/register/wellness', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          business_name: formData.businessName,
          mission: formData.businessStory,
          products: formData.productsServices,
          audience: formData.targetAudience,
          zipcode: formData.zipcode,
          age_range: formData.ageRange,
          interests: formData.interests.split(',').map(i => i.trim()),
          preferred_channels: formData.preferredChannels.split(',').map(c => c.trim()),
        }),
      })

      console.log('Response status:', response.status)
      
      if (!response.ok) {
        const errorText = await response.text()
        console.error('Backend error:', errorText)
        throw new Error(`Backend error: ${response.status} - ${errorText}`)
      }

      const result = await response.json()
      console.log('Backend response:', result)
      
      // Store the result in localStorage for the results page
      localStorage.setItem('adGenerationResult', JSON.stringify(result))
      
      // Redirect to results page
      router.push("/register/results")
    } catch (err) {
      console.error("Error generating ads:", err)
      setError(err instanceof Error ? err.message : "Failed to generate personalized ads")
    } finally {
      setIsSubmitting(false)
    }
  }

  const isStepValid = () => {
    switch (currentStep) {
      case 1:
        return formData.businessName.trim().length > 0
      case 2:
        return formData.zipcode.trim().length > 0
      case 3:
        return formData.businessStory.trim().length > 0
      case 4:
        return formData.productsServices.trim().length > 0
      case 5:
        return formData.targetAudience.trim().length > 0
      case 6:
        return formData.ageRange.trim().length > 0
      case 7:
        return formData.interests.trim().length > 0
      case 8:
        return formData.preferredChannels.trim().length > 0
      default:
        return false
    }
  }

  return (
    <div className="flex min-h-screen w-full items-center justify-center p-6 md:p-10 bg-gradient-to-br from-blue-50 to-green-50">
      <div className="w-full max-w-2xl">
        <Link href="/" className="flex items-center mb-6 hover:opacity-80 transition-opacity">
          <Image src="/awe-logo.jpg" alt="AWE Logo" width={48} height={48} className="rounded" />
        </Link>

        <Card>
          <CardHeader>
            <div className="flex items-center gap-2 mb-2">
              <Sparkles className="h-5 w-5 text-primary" />
              <span className="text-sm font-medium text-primary">
                Step {currentStep} of {totalSteps}
              </span>
            </div>
            <Progress value={progress} className="mb-4" />
            <CardTitle className="text-2xl">
              {currentStep === 1 && "What's your business name?"}
              {currentStep === 2 && "Where are you located?"}
              {currentStep === 3 && "Tell us your story"}
              {currentStep === 4 && "What do you offer?"}
              {currentStep === 5 && "Who are your customers?"}
              {currentStep === 6 && "What's your target age range?"}
              {currentStep === 7 && "What are your interests?"}
              {currentStep === 8 && "What are your preferred channels?"}
            </CardTitle>
            <CardDescription>
              {currentStep === 1 && "Let's start with the basics - what do you call your business?"}
              {currentStep === 2 && "Help us target the right local audience"}
              {currentStep === 3 && "Share your business's mission and what makes you unique"}
              {currentStep === 4 && "Describe the products or services you provide"}
              {currentStep === 5 && "Help us understand who you're trying to reach"}
              {currentStep === 6 && "What age group are you targeting?"}
              {currentStep === 7 && "What topics interest your target audience?"}
              {currentStep === 8 && "Where do you want to advertise?"}
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {currentStep === 1 && (
                <div className="space-y-2">
                  <Label htmlFor="businessName">Business Name</Label>
                  <Input
                    id="businessName"
                    placeholder="Enter your business name"
                    value={formData.businessName}
                    onChange={(e) => setFormData({ ...formData, businessName: e.target.value })}
                    className="text-lg"
                  />
                  <p className="text-xs text-muted-foreground">
                    This is how we'll refer to your business throughout the platform
                  </p>
                </div>
              )}

              {currentStep === 2 && (
                <div className="space-y-2">
                  <Label htmlFor="zipcode">ZIP Code</Label>
                  <Input
                    id="zipcode"
                    placeholder="e.g., 11201"
                    value={formData.zipcode}
                    onChange={(e) => setFormData({ ...formData, zipcode: e.target.value })}
                    className="text-lg"
                  />
                  <p className="text-xs text-muted-foreground">
                    We'll use this to target local customers
                  </p>
                </div>
              )}

              {currentStep === 3 && (
                <div className="space-y-2">
                  <Label htmlFor="businessStory">Business Story & Mission</Label>
                  <Textarea
                    id="businessStory"
                    placeholder="Tell us about your business journey, what inspired you to start, and what drives you every day..."
                    value={formData.businessStory}
                    onChange={(e) => setFormData({ ...formData, businessStory: e.target.value })}
                    rows={6}
                    className="resize-none"
                  />
                  <p className="text-xs text-muted-foreground">
                    This helps us create marketing that truly reflects your passion
                  </p>
                </div>
              )}

              {currentStep === 4 && (
                <div className="space-y-2">
                  <Label htmlFor="productsServices">Products & Services</Label>
                  <Textarea
                    id="productsServices"
                    placeholder="Describe what you sell or the services you provide. Include key features, benefits, and what makes them special..."
                    value={formData.productsServices}
                    onChange={(e) => setFormData({ ...formData, productsServices: e.target.value })}
                    rows={6}
                    className="resize-none"
                  />
                  <p className="text-xs text-muted-foreground">
                    We'll use this to highlight what makes your offerings stand out
                  </p>
                </div>
              )}

              {currentStep === 5 && (
                <div className="space-y-2">
                  <Label htmlFor="targetAudience">Target Audience</Label>
                  <Textarea
                    id="targetAudience"
                    placeholder="Who are your ideal customers? Consider demographics, interests, pain points, and what they value most..."
                    value={formData.targetAudience}
                    onChange={(e) => setFormData({ ...formData, targetAudience: e.target.value })}
                    rows={6}
                    className="resize-none"
                  />
                  <p className="text-xs text-muted-foreground">
                    Understanding your audience helps us reach the right people
                  </p>
                </div>
              )}

              {currentStep === 6 && (
                <div className="space-y-2">
                  <Label htmlFor="ageRange">Target Age Range</Label>
                  <Input
                    id="ageRange"
                    placeholder="e.g., 25-45"
                    value={formData.ageRange}
                    onChange={(e) => setFormData({ ...formData, ageRange: e.target.value })}
                    className="text-lg"
                  />
                  <p className="text-xs text-muted-foreground">
                    Helps us create age-appropriate messaging
                  </p>
                </div>
              )}

              {currentStep === 7 && (
                <div className="space-y-2">
                  <Label htmlFor="interests">Interests (comma-separated)</Label>
                  <Input
                    id="interests"
                    placeholder="e.g., yoga, meditation, wellness, fitness"
                    value={formData.interests}
                    onChange={(e) => setFormData({ ...formData, interests: e.target.value })}
                    className="text-lg"
                  />
                  <p className="text-xs text-muted-foreground">
                    What topics interest your target audience?
                  </p>
                </div>
              )}

              {currentStep === 8 && (
                <div className="space-y-2">
                  <Label htmlFor="preferredChannels">Preferred Channels (comma-separated)</Label>
                  <Input
                    id="preferredChannels"
                    placeholder="e.g., social, email, local_events, google_ads"
                    value={formData.preferredChannels}
                    onChange={(e) => setFormData({ ...formData, preferredChannels: e.target.value })}
                    className="text-lg"
                  />
                  <p className="text-xs text-muted-foreground">
                    Where do you want to advertise?
                  </p>
                </div>
              )}

              {error && <div className="rounded-md bg-destructive/10 p-3 text-sm text-destructive">{error}</div>}

              <div className="flex gap-3 pt-4">
                {currentStep > 1 && (
                  <Button type="button" variant="outline" onClick={handleBack} className="flex-1 bg-transparent">
                    <ArrowLeft className="mr-2 h-4 w-4" />
                    Back
                  </Button>
                )}

                {currentStep < totalSteps ? (
                  <Button type="button" onClick={handleNext} disabled={!isStepValid()} className="flex-1">
                    Next
                    <ArrowRight className="ml-2 h-4 w-4" />
                  </Button>
                ) : (
                  <Button
                    type="button"
                    onClick={handleSubmit}
                    disabled={!isStepValid() || isSubmitting}
                    className="flex-1"
                  >
                    {isSubmitting ? "Saving..." : "Complete Setup"}
                  </Button>
                )}
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
