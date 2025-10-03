"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
// import { Header } from "@/components/header"
import { Sparkles, TrendingUp, Leaf, Target, ArrowRight, Instagram, Facebook, Youtube } from "lucide-react"
import ScrollVelocity from "@/components/scroll-velocity"
import CountUp from "@/components/count-up"
import SplitTextAnimated from "@/components/split-text-animated"
import "./scroll-velocity.css"

interface GeneratedAd {
  id: string
  headline: string
  body: string
  cta: string
  audience_segment: string
  targeting: any
}

interface ChannelRecommendation {
  channel: string
  reason: string
  priority?: string
}

interface EnvironmentalImpact {
  total_energy_kwh: number
  total_co2_kg: number
  green_score: number
}

interface AdGenerationResults {
  registration_id: string
  brand: {
    company_name: string
    mission: string
  }
  initial_ads: GeneratedAd[]
  channel_recommendations: {
    best_channel: string
    total_confidence: number
    recommendations: ChannelRecommendation[]
  }
  environmental_impact: EnvironmentalImpact
  zipcode?: string
  age_range?: string
  interests?: string[]
  preferred_channels?: string[]
}

const CHANNEL_ICONS: Record<string, any> = {
  Instagram: Instagram,
  Facebook: Facebook,
  YouTube: Youtube,
  "Google Ads": Target,
}

export default function ResultsPage() {
  const router = useRouter()
  const [results, setResults] = useState<AdGenerationResults | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const storedResults = localStorage.getItem("adGenerationResult")
    if (storedResults) {
      setResults(JSON.parse(storedResults))
    } else {
      router.push("/onboarding")
    }
    setLoading(false)
  }, [router])

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-center">
          <Sparkles className="h-12 w-12 animate-pulse text-green-600 mx-auto mb-4" />
          <p className="text-lg text-muted-foreground">Loading your results...</p>
        </div>
      </div>
    )
  }

  if (!results) {
    return null
  }

  const getPriorityColor = (priority: string | undefined) => {
    if (!priority) return "bg-gray-100 text-gray-800 border-gray-200"
    
    switch (priority.toLowerCase()) {
      case "high":
        return "bg-green-100 text-green-800 border-green-200"
      case "medium":
        return "bg-blue-100 text-blue-800 border-blue-200"
      case "low":
        return "bg-orange-100 text-orange-800 border-orange-200"
      default:
        return "bg-gray-100 text-gray-800 border-gray-200"
    }
  }

  const getGreenScoreColor = (score: number) => {
    if (score >= 80) return "text-green-600"
    if (score >= 60) return "text-blue-600"
    return "text-orange-600"
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-green-50 via-blue-50 to-orange-50">
      {/* <Header /> */}

      <div className="container mx-auto px-4 py-12 max-w-6xl">
        {/* Success Header */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center gap-2 bg-green-100 text-green-800 px-4 py-2 rounded-full mb-4">
            <Sparkles className="h-4 w-4" />
            <span className="text-sm font-semibold">Ads Generated Successfully!</span>
          </div>
          <SplitTextAnimated
            text="Your Personalized Ad Campaign"
            className="text-4xl font-bold mb-4"
            tag="h1"
            splitType="chars"
            delay={30}
            duration={0.5}
            from={{ opacity: 0, y: 20 }}
            to={{ opacity: 1, y: 0 }}
          />
          <p className="text-lg text-muted-foreground text-pretty max-w-2xl mx-auto">
            We've created custom ads tailored to your business and analyzed the best channels to reach your audience.
          </p>
        </div>

        {/* Generated Ads Section */}
        <section className="mb-12">
          <div className="flex items-center gap-2 mb-6">
            <Sparkles className="h-6 w-6 text-green-600" />
            <h2 className="text-2xl font-bold">Generated Ads</h2>
          </div>
          <div className="grid gap-6 md:grid-cols-2">
            {results.initial_ads.map((ad, index) => (
              <Card key={index} className="border-2 hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex items-start justify-between gap-2">
                    <CardTitle className="text-xl text-balance">{ad.headline}</CardTitle>
                    <Badge variant="outline" className="shrink-0">
                      Ad {index + 1}
                    </Badge>
                  </div>
                  <CardDescription className="text-xs">Target: {ad.audience_segment}</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <p className="text-sm leading-relaxed text-pretty">{ad.body}</p>
                  <Button className="w-full bg-green-600 hover:bg-green-700">{ad.cta}</Button>
                </CardContent>
              </Card>
            ))}
          </div>
        </section>

        {/* Channel Recommendations Section */}
        <section className="mb-12">
          <div className="flex items-center gap-2 mb-6">
            <TrendingUp className="h-6 w-6 text-blue-600" />
            <h2 className="text-2xl font-bold">Recommended Channels</h2>
          </div>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {results.channel_recommendations.recommendations.map((channel, index) => {
              const Icon = CHANNEL_ICONS[channel.channel] || Target
              return (
                <Card key={index} className="border-2">
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <Icon className="h-5 w-5" />
                        <CardTitle className="text-lg">{channel.channel}</CardTitle>
                      </div>
                      <Badge className={getPriorityColor(channel.priority)}>{channel.priority || "Medium"}</Badge>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-muted-foreground text-pretty">{channel.reason}</p>
                  </CardContent>
                </Card>
              )
            })}
          </div>
        </section>

        <div className="grid gap-6 md:grid-cols-2 mb-12">
          {/* Environmental Impact Section */}
          <section>
            <div className="flex items-center gap-2 mb-6">
              <Leaf className="h-6 w-6 text-green-600" />
              <h2 className="text-2xl font-bold">Environmental Impact</h2>
            </div>
            <Card className="border-2 bg-gradient-to-br from-green-50 to-blue-50 overflow-hidden">
              <CardHeader>
                <CardTitle>Sustainable Advertising</CardTitle>
                <CardDescription>Your campaign's environmental footprint</CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="py-4 -mx-6 bg-green-100/50">
                  <ScrollVelocity
                    texts={["🌱 ECO-FRIENDLY", "♻️ SUSTAINABLE", "🌍 GREEN ADVERTISING"]}
                    velocity={50}
                    className="text-green-700 font-bold text-2xl"
                  />
                </div>

                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium">Energy Used</span>
                  <span className="text-lg font-bold">
                    <CountUp to={results.environmental_impact.total_energy_kwh} duration={2} separator="," /> kWh
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium">CO₂ Emissions</span>
                  <span className="text-lg font-bold">
                    <CountUp to={results.environmental_impact.total_co2_kg} duration={2} separator="," /> kg
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium">Green Score</span>
                  <span
                    className={`text-2xl font-bold ${getGreenScoreColor(results.environmental_impact.green_score)}`}
                  >
                    <CountUp to={results.environmental_impact.green_score} duration={2.5} />
                    /100
                  </span>
                </div>
                <p className="text-xs text-muted-foreground pt-2 border-t">
                  We're committed to low-carbon advertising that's better for the planet.
                </p>
              </CardContent>
            </Card>
          </section>

          {/* Targeting Metrics Section */}
          <section>
            <div className="flex items-center gap-2 mb-6">
              <Target className="h-6 w-6 text-orange-600" />
              <h2 className="text-2xl font-bold">Targeting Summary</h2>
            </div>
            <Card className="border-2 bg-gradient-to-br from-orange-50 to-blue-50">
              <CardHeader>
                <CardTitle>Audience Targeting</CardTitle>
                <CardDescription>Who we'll reach with your ads</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <span className="text-sm font-medium text-muted-foreground">Location</span>
                  <SplitTextAnimated
                    text={`ZIP Code: ${results.zipcode || 'Not specified'}`}
                    className="text-lg font-semibold"
                    tag="p"
                    splitType="chars"
                    delay={20}
                    duration={0.4}
                    textAlign="left"
                  />
                </div>
                <div>
                  <span className="text-sm font-medium text-muted-foreground">Age Range</span>
                  <p className="text-lg font-semibold">{results.age_range || 'Not specified'}</p>
                </div>
                <div>
                  <span className="text-sm font-medium text-muted-foreground">Interests</span>
                  <div className="flex flex-wrap gap-2 mt-2">
                    {(results.interests || []).map((interest, index) => (
                      <Badge key={index} variant="secondary" className="capitalize">
                        {interest}
                      </Badge>
                    ))}
                  </div>
                </div>
              </CardContent>
            </Card>
          </section>
        </div>

        {/* Call to Action */}
        <Card className="border-2 bg-gradient-to-r from-green-600 to-blue-600 text-white">
          <CardContent className="py-8">
            <div className="text-center space-y-4">
              <h3 className="text-2xl font-bold">Ready to Launch Your Campaign?</h3>
              <p className="text-lg text-green-50 max-w-2xl mx-auto text-pretty">
                Let's get your ads live and start connecting with customers who'll love what you do.
              </p>
              <div className="flex flex-col sm:flex-row gap-3 justify-center pt-4">
                <Button size="lg" variant="secondary" className="gap-2">
                  Schedule a Call
                  <ArrowRight className="h-4 w-4" />
                </Button>
                <Button
                  size="lg"
                  variant="outline"
                  className="gap-2 border-white text-white hover:bg-white/10 bg-transparent"
                >
                  Download Report
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </main>
  )
}
