import { redirect } from "next/navigation"
import { createClient } from "@/lib/supabase/server"
import { DashboardHeader } from "@/components/dashboard-header"
import { MetricsOverview } from "@/components/metrics-overview"
import { CampaignTable } from "@/components/campaign-table"

export default async function DashboardPage() {
  const supabase = await createClient()

  const {
    data: { user },
    error,
  } = await supabase.auth.getUser()

  if (error || !user) {
    redirect("/auth/login")
  }

  // Fetch ad metrics for the user
  const { data: metrics, error: metricsError } = await supabase
    .from("ad_metrics")
    .select("*")
    .eq("user_id", user.id)
    .order("date", { ascending: false })

  // If no metrics exist, create some sample data
  if (!metrics || metrics.length === 0) {
    // Insert sample data for demonstration
    const sampleMetrics = [
      {
        user_id: user.id,
        campaign_name: "Summer Sale 2024",
        impressions: 45230,
        clicks: 3420,
        conversions: 287,
        spend: 1250.0,
        revenue: 8640.0,
        date: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString().split("T")[0],
      },
      {
        user_id: user.id,
        campaign_name: "Holiday Special",
        impressions: 38920,
        clicks: 2890,
        conversions: 234,
        spend: 980.0,
        revenue: 7020.0,
        date: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString().split("T")[0],
      },
      {
        user_id: user.id,
        campaign_name: "Back to School",
        impressions: 52100,
        clicks: 4120,
        conversions: 356,
        spend: 1450.0,
        revenue: 10680.0,
        date: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString().split("T")[0],
      },
      {
        user_id: user.id,
        campaign_name: "Spring Collection",
        impressions: 41500,
        clicks: 3250,
        conversions: 298,
        spend: 1100.0,
        revenue: 8940.0,
        date: new Date(Date.now() - 4 * 24 * 60 * 60 * 1000).toISOString().split("T")[0],
      },
      {
        user_id: user.id,
        campaign_name: "Weekend Flash Sale",
        impressions: 28900,
        clicks: 2340,
        conversions: 189,
        spend: 750.0,
        revenue: 5670.0,
        date: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString().split("T")[0],
      },
    ]

    await supabase.from("ad_metrics").insert(sampleMetrics)

    // Refetch the data
    const { data: newMetrics } = await supabase
      .from("ad_metrics")
      .select("*")
      .eq("user_id", user.id)
      .order("date", { ascending: false })

    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-green-50">
        <DashboardHeader user={user} />
        <main className="container mx-auto px-4 py-8">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Your Ad Performance</h1>
            <p className="text-gray-600">Track your marketing campaigns and see how they&apos;re performing</p>
          </div>
          <MetricsOverview metrics={newMetrics || []} />
          <CampaignTable metrics={newMetrics || []} />
        </main>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-green-50">
      <DashboardHeader user={user} />
      <main className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Your Ad Performance</h1>
          <p className="text-gray-600">Track your marketing campaigns and see how they&apos;re performing</p>
        </div>
        <MetricsOverview metrics={metrics} />
        <CampaignTable metrics={metrics} />
      </main>
    </div>
  )
}
