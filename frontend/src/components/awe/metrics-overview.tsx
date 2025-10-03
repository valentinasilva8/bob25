import { Card, CardContent, CardHeader, CardTitle } from "@/components/awe/ui/card"
import { TrendingUp, MousePointerClick, DollarSign, Target } from "lucide-react"

interface Metric {
  impressions: number
  clicks: number
  conversions: number
  spend: number
  revenue: number
}

interface MetricsOverviewProps {
  metrics: Metric[]
}

export function MetricsOverview({ metrics }: MetricsOverviewProps) {
  const totals = metrics.reduce(
    (acc, metric) => ({
      impressions: acc.impressions + metric.impressions,
      clicks: acc.clicks + metric.clicks,
      conversions: acc.conversions + metric.conversions,
      spend: acc.spend + Number(metric.spend),
      revenue: acc.revenue + Number(metric.revenue),
    }),
    { impressions: 0, clicks: 0, conversions: 0, spend: 0, revenue: 0 },
  )

  const ctr = totals.impressions > 0 ? ((totals.clicks / totals.impressions) * 100).toFixed(2) : "0.00"
  const roi = totals.spend > 0 ? (((totals.revenue - totals.spend) / totals.spend) * 100).toFixed(0) : "0"
  const conversionRate = totals.clicks > 0 ? ((totals.conversions / totals.clicks) * 100).toFixed(2) : "0.00"

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4 mb-8">
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Total Impressions</CardTitle>
          <TrendingUp className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{totals.impressions.toLocaleString()}</div>
          <p className="text-xs text-muted-foreground">CTR: {ctr}%</p>
        </CardContent>
      </Card>
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Total Clicks</CardTitle>
          <MousePointerClick className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{totals.clicks.toLocaleString()}</div>
          <p className="text-xs text-muted-foreground">Conversion Rate: {conversionRate}%</p>
        </CardContent>
      </Card>
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Total Revenue</CardTitle>
          <DollarSign className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">${totals.revenue.toLocaleString()}</div>
          <p className="text-xs text-muted-foreground">ROI: {roi}%</p>
        </CardContent>
      </Card>
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Total Conversions</CardTitle>
          <Target className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{totals.conversions.toLocaleString()}</div>
          <p className="text-xs text-muted-foreground">Spend: ${totals.spend.toLocaleString()}</p>
        </CardContent>
      </Card>
    </div>
  )
}
