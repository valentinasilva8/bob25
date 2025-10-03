"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Input } from "@/components/ui/input"
import { Progress } from "@/components/ui/progress"
import { createBrowserClient } from "@supabase/ssr"
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
    businessStory: "",
    productsServices: "",
    targetAudience: "",
    growthGoals: "",
  })

  const supabase = createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
  )

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

  const handleSubmit = async () => {
    setIsSubmitting(true)
    setError(null)

    try {
      const {
        data: { user },
      } = await supabase.auth.getUser()

      if (!user) {
        throw new Error("No user found")
      }

      const { error: insertError } = await supabase.from("business_profiles").insert({
        user_id: user.id,
        business_name: formData.businessName,
        business_story: formData.businessStory,
        products_services: formData.productsServices,
        target_audience: formData.targetAudience,
        growth_goals: formData.growthGoals,
        onboarding_completed: true,
      })

      if (insertError) throw insertError

      router.push("/dashboard")
    } catch (err) {
      console.error("Error saving onboarding data:", err)
      setError(err instanceof Error ? err.message : "Failed to save your information")
    } finally {
      setIsSubmitting(false)
    }
  }

  const isStepValid = () => {
    switch (currentStep) {
      case 1:
        return formData.businessName.trim().length > 0
      case 2:
        return formData.businessStory.trim().length > 0
      case 3:
        return formData.productsServices.trim().length > 0
      case 4:
        return formData.targetAudience.trim().length > 0
      case 5:
        return formData.growthGoals.trim().length > 0
      default:
        return false
    }
  }

  return (
    <div className="flex min-h-screen w-full items-center justify-center p-6 md:p-10 bg-gradient-to-br from-blue-50 to-green-50">
      <div className="w-full max-w-2xl">
        <Link href="/" className="flex items-center gap-2 mb-6 hover:opacity-80 transition-opacity">
          <Image src="/awe-logo.svg" alt="AWE Logo" width={40} height={40} />
          <span className="text-2xl font-bold text-primary">awe</span>
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
              {currentStep === 2 && "Tell us your story"}
              {currentStep === 3 && "What do you offer?"}
              {currentStep === 4 && "Who are your customers?"}
              {currentStep === 5 && "What are your goals?"}
            </CardTitle>
            <CardDescription>
              {currentStep === 1 && "Let's start with the basics - what do you call your business?"}
              {currentStep === 2 && "Share your business's mission and what makes you unique"}
              {currentStep === 3 && "Describe the products or services you provide"}
              {currentStep === 4 && "Help us understand who you're trying to reach"}
              {currentStep === 5 && "Let us know how you want to grow your business"}
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

              {currentStep === 3 && (
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

              {currentStep === 4 && (
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

              {currentStep === 5 && (
                <div className="space-y-2">
                  <Label htmlFor="growthGoals">Growth Goals</Label>
                  <Textarea
                    id="growthGoals"
                    placeholder="What are you hoping to achieve? More customers, increased revenue, brand awareness, or something else? Be specific about your targets..."
                    value={formData.growthGoals}
                    onChange={(e) => setFormData({ ...formData, growthGoals: e.target.value })}
                    rows={6}
                    className="resize-none"
                  />
                  <p className="text-xs text-muted-foreground">
                    Clear goals help us measure success and optimize your campaigns
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
