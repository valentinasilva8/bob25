"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Input } from "@/components/ui/input"
import { Progress } from "@/components/ui/progress"
import { Checkbox } from "@/components/ui/checkbox"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { ArrowRight, ArrowLeft, Sparkles, Loader2 } from "lucide-react"
import Link from "next/link"
import Image from "next/image"

const AGE_RANGES = ["18-25", "25-35", "35-45", "45-55", "55+"]

const INTERESTS = [
  { id: "yoga", label: "Yoga" },
  { id: "meditation", label: "Meditation" },
  { id: "wellness", label: "Wellness" },
  { id: "mindfulness", label: "Mindfulness" },
  { id: "fitness", label: "Fitness" },
  { id: "stress-relief", label: "Stress Relief" },
  { id: "nutrition", label: "Nutrition" },
  { id: "community", label: "Community" },
]

export default function RegisterPage() {
  const router = useRouter()
  const [currentStep, setCurrentStep] = useState(1)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const [formData, setFormData] = useState({
    businessName: "",
    zipcode: "",
    mission: "",
    products: "",
    audience: "",
    ageRange: "",
    interests: [] as string[],
    creativesPerWeek: "",
  })

  const totalSteps = 5
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

  const handleInterestToggle = (interestId: string) => {
    setFormData((prev) => ({
      ...prev,
      interests: prev.interests.includes(interestId)
        ? prev.interests.filter((id) => id !== interestId)
        : [...prev.interests, interestId],
    }))
  }

  const handleSubmit = async () => {
    setIsSubmitting(true)
    setError(null)

    try {
      const response = await fetch("http://localhost:8002/business/register/wellness", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          business_name: formData.businessName,
          zipcode: formData.zipcode,
          mission: formData.mission,
          products: formData.products,
          audience: formData.audience,
          age_range: formData.ageRange,
          interests: formData.interests,
          creatives_per_week: formData.creativesPerWeek,
          preferred_channels: ["social", "local", "email"], // Default channels
        }),
      })

      if (!response.ok) {
        throw new Error("Failed to generate ads")
      }

      const data = await response.json()

      // Store the results in localStorage to display on the results page
      localStorage.setItem("adGenerationResult", JSON.stringify(data))

      router.push("/register/results")
    } catch (err) {
      console.error("Error generating ads:", err)
      setError(err instanceof Error ? err.message : "Failed to generate ads. Please try again.")
    } finally {
      setIsSubmitting(false)
    }
  }

  const isStepValid = () => {
    switch (currentStep) {
      case 1:
        return formData.businessName.trim().length > 0 && formData.zipcode.trim().length > 0
      case 2:
        return formData.mission.trim().length > 0 && formData.products.trim().length > 0
      case 3:
        return formData.audience.trim().length > 0
      case 4:
        return formData.ageRange.length > 0 && formData.interests.length > 0
      case 5:
        return formData.creativesPerWeek.length > 0
      default:
        return false
    }
  }

  return (
    <div className="flex min-h-screen w-full items-center justify-center p-6 md:p-10 bg-gradient-to-br from-green-50 via-blue-50 to-orange-50">
      <div className="w-full max-w-2xl">
        <Link href="/" className="flex items-center gap-2 mb-6 hover:opacity-80 transition-opacity">
          <Image src="/awe-logo.svg" alt="AWE Logo" width={40} height={40} />
          <span className="text-2xl font-bold text-primary">awe</span>
        </Link>

        <Card className="border-2">
          <CardHeader>
            <div className="flex items-center gap-2 mb-2">
              <Sparkles className="h-5 w-5 text-green-600" />
              <span className="text-sm font-medium text-green-600">
                Step {currentStep} of {totalSteps}
              </span>
            </div>
            <Progress value={progress} className="mb-4" />
            <CardTitle className="text-2xl">
              {currentStep === 1 && "Let's start with the basics"}
              {currentStep === 2 && "Tell us about your business"}
              {currentStep === 3 && "Who do you serve?"}
              {currentStep === 4 && "Define your audience"}
              {currentStep === 5 && "Your creative needs"}
            </CardTitle>
            <CardDescription>
              {currentStep === 1 && "We'll use this information to create personalized ads for your business"}
              {currentStep === 2 && "Help us understand what makes your business special"}
              {currentStep === 3 && "Describe your ideal customers and what they're looking for"}
              {currentStep === 4 && "Select demographics and interests to target the right people"}
              {currentStep === 5 && "Help us understand your creative production needs"}
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-6">
              {currentStep === 1 && (
                <div className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="businessName">Business Name *</Label>
                    <Input
                      id="businessName"
                      placeholder="Enter your business name or try a demo company"
                      value={formData.businessName}
                      onChange={(e) => setFormData({ ...formData, businessName: e.target.value })}
                      className="text-lg"
                    />
                    <div className="text-xs text-muted-foreground">
                      <strong>Demo fitness & wellness studios:</strong> Solstice Yoga Studio, Iron Will Fitness, Zen Pilates Studio, Flow State Dance, Mindful Movement Wellness
                    </div>
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="zipcode">Zip Code *</Label>
                    <Input
                      id="zipcode"
                      placeholder="Enter your zip code"
                      value={formData.zipcode}
                      onChange={(e) => setFormData({ ...formData, zipcode: e.target.value })}
                      className="text-lg"
                      maxLength={10}
                    />
                    <p className="text-xs text-muted-foreground">
                      We'll use this to target local customers in your area
                    </p>
                  </div>
                </div>
              )}

              {currentStep === 2 && (
                <div className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="mission">Mission & Story *</Label>
                    <Textarea
                      id="mission"
                      placeholder="What inspired you to start this business? What's your mission and what makes you unique?"
                      value={formData.mission}
                      onChange={(e) => setFormData({ ...formData, mission: e.target.value })}
                      rows={5}
                      className="resize-none"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="products">Products & Services *</Label>
                    <Textarea
                      id="products"
                      placeholder="Describe what you offer - products, services, classes, etc."
                      value={formData.products}
                      onChange={(e) => setFormData({ ...formData, products: e.target.value })}
                      rows={5}
                      className="resize-none"
                    />
                  </div>
                </div>
              )}

              {currentStep === 3 && (
                <div className="space-y-2">
                  <Label htmlFor="audience">Target Audience *</Label>
                  <Textarea
                    id="audience"
                    placeholder="Who are your ideal customers? What are their pain points, interests, and what they value most?"
                    value={formData.audience}
                    onChange={(e) => setFormData({ ...formData, audience: e.target.value })}
                    rows={8}
                    className="resize-none"
                  />
                  <p className="text-xs text-muted-foreground">
                    Be specific about demographics, lifestyle, challenges, and goals
                  </p>
                </div>
              )}

              {currentStep === 4 && (
                <div className="space-y-6">
                  <div className="space-y-3">
                    <Label htmlFor="ageRange">Age Range *</Label>
                    <Select
                      value={formData.ageRange}
                      onValueChange={(value) => setFormData({ ...formData, ageRange: value })}
                    >
                      <SelectTrigger id="ageRange">
                        <SelectValue placeholder="Select age range" />
                      </SelectTrigger>
                      <SelectContent>
                        {AGE_RANGES.map((range) => (
                          <SelectItem key={range} value={range}>
                            {range}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-3">
                    <Label>Interests * (Select all that apply)</Label>
                    <div className="grid grid-cols-2 gap-3">
                      {INTERESTS.map((interest) => (
                        <div key={interest.id} className="flex items-center space-x-2">
                          <Checkbox
                            id={interest.id}
                            checked={formData.interests.includes(interest.id)}
                            onCheckedChange={() => handleInterestToggle(interest.id)}
                          />
                          <label
                            htmlFor={interest.id}
                            className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 cursor-pointer"
                          >
                            {interest.label}
                          </label>
                        </div>
                      ))}
                    </div>
                    <p className="text-xs text-muted-foreground">
                      Select at least one interest to help us target the right audience
                    </p>
                  </div>
                </div>
              )}

              {currentStep === 5 && (
                <div className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="creativesPerWeek">How many creatives do you need per week on average? *</Label>
                    <Select
                      value={formData.creativesPerWeek}
                      onValueChange={(value) => setFormData({ ...formData, creativesPerWeek: value })}
                    >
                      <SelectTrigger id="creativesPerWeek">
                        <SelectValue placeholder="Select your creative needs" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="1-2">1-2 creatives per week</SelectItem>
                        <SelectItem value="3-5">3-5 creatives per week</SelectItem>
                        <SelectItem value="6-10">6-10 creatives per week</SelectItem>
                        <SelectItem value="11-20">11-20 creatives per week</SelectItem>
                        <SelectItem value="20+">20+ creatives per week</SelectItem>
                      </SelectContent>
                    </Select>
                    <p className="text-xs text-muted-foreground">
                      This helps us calculate your environmental impact and optimize our ad generation
                    </p>
                  </div>
                </div>
              )}

              {error && (
                <div className="rounded-md bg-destructive/10 p-3 text-sm text-destructive border border-destructive/20">
                  {error}
                </div>
              )}

              <div className="flex gap-3 pt-4">
                {currentStep > 1 && (
                  <Button type="button" variant="outline" onClick={handleBack} className="flex-1 bg-transparent">
                    <ArrowLeft className="mr-2 h-4 w-4" />
                    Back
                  </Button>
                )}

                {currentStep < totalSteps ? (
                  <Button
                    type="button"
                    onClick={handleNext}
                    disabled={!isStepValid()}
                    className="flex-1 bg-green-600 hover:bg-green-700"
                  >
                    Next
                    <ArrowRight className="ml-2 h-4 w-4" />
                  </Button>
                ) : (
                  <Button
                    type="button"
                    onClick={handleSubmit}
                    disabled={!isStepValid() || isSubmitting}
                    className="flex-1 bg-green-600 hover:bg-green-700"
                  >
                    {isSubmitting ? (
                      <>
                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                        Generating Your Ads...
                      </>
                    ) : (
                      <>
                        <Sparkles className="mr-2 h-4 w-4" />
                        Generate My Ads
                      </>
                    )}
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
