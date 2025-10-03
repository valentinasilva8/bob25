"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { mockAuth, type MockUser, type MockProfile } from "@/lib/mock-auth"
import { DashboardHeader } from "@/components/dashboard-header"
import { MetricsOverview } from "@/components/metrics-overview"
import { CampaignTable } from "@/components/campaign-table"
import { BusinessProfileEditor } from "@/components/business-profile-editor"

export default function DashboardPage() {
  const [user, setUser] = useState<MockUser | null>(null)
  const [profile, setProfile] = useState<MockProfile | null>(null)
  const [metrics, setMetrics] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const router = useRouter()

  useEffect(() => {
    const loadDashboard = async () => {
      try {
        const { user: currentUser } = await mockAuth.getUser()
        if (!currentUser) {
          router.push("/auth/login")
          return
        }

        setUser(currentUser)
        
        const { data: userProfile } = await mockAuth.getProfile(currentUser.id)
        setProfile(userProfile)
        
        const { data: userMetrics } = await mockAuth.getAdMetrics(currentUser.id)
        setMetrics(userMetrics)
      } catch (error) {
        console.error("Error loading dashboard:", error)
        router.push("/auth/login")
      } finally {
        setLoading(false)
      }
    }

    loadDashboard()
  }, [router])

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto"></div>
          <p className="mt-2 text-muted-foreground">Loading dashboard...</p>
        </div>
      </div>
    )
  }

  if (!user) {
    return null
  }

  return (
    <div className="min-h-screen bg-background">
      <DashboardHeader user={user} />
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold">Dashboard</h1>
          <p className="text-muted-foreground">Welcome back, {user.name}!</p>
        </div>

        <div className="grid gap-8">
          <MetricsOverview metrics={metrics} />
          <CampaignTable campaigns={metrics} />
          {profile && <BusinessProfileEditor initialProfile={profile} userId={user.id} />}
        </div>
      </div>
    </div>
  )
}