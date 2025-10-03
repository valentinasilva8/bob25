import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"

interface Metric {
  campaign_name: string
  impressions: number
  clicks: number
  conversions: number
  spend: number
  revenue: number
  date: string
}

interface CampaignTableProps {
  metrics: Metric[]
}

export function CampaignTable({ metrics }: CampaignTableProps) {
  const getPerformanceBadge = (roi: number) => {
    if (roi >= 500) return <Badge className="bg-green-500">Excellent</Badge>
    if (roi >= 300) return <Badge className="bg-blue-500">Good</Badge>
    if (roi >= 100) return <Badge className="bg-yellow-500">Fair</Badge>
    return <Badge variant="secondary">Poor</Badge>
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Campaign Performance</CardTitle>
      </CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Campaign</TableHead>
              <TableHead>Date</TableHead>
              <TableHead className="text-right">Impressions</TableHead>
              <TableHead className="text-right">Clicks</TableHead>
              <TableHead className="text-right">Conversions</TableHead>
              <TableHead className="text-right">Spend</TableHead>
              <TableHead className="text-right">Revenue</TableHead>
              <TableHead className="text-right">ROI</TableHead>
              <TableHead>Status</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {metrics.map((metric, index) => {
              const roi =
                Number(metric.spend) > 0
                  ? (((Number(metric.revenue) - Number(metric.spend)) / Number(metric.spend)) * 100).toFixed(0)
                  : "0"
              const ctr = metric.impressions > 0 ? ((metric.clicks / metric.impressions) * 100).toFixed(2) : "0.00"

              return (
                <TableRow key={index}>
                  <TableCell className="font-medium">{metric.campaign_name}</TableCell>
                  <TableCell>{new Date(metric.date).toLocaleDateString()}</TableCell>
                  <TableCell className="text-right">{metric.impressions.toLocaleString()}</TableCell>
                  <TableCell className="text-right">
                    {metric.clicks.toLocaleString()}
                    <span className="text-xs text-muted-foreground ml-1">({ctr}%)</span>
                  </TableCell>
                  <TableCell className="text-right">{metric.conversions.toLocaleString()}</TableCell>
                  <TableCell className="text-right">${Number(metric.spend).toLocaleString()}</TableCell>
                  <TableCell className="text-right">${Number(metric.revenue).toLocaleString()}</TableCell>
                  <TableCell className="text-right font-semibold text-green-600">+{roi}%</TableCell>
                  <TableCell>{getPerformanceBadge(Number(roi))}</TableCell>
                </TableRow>
              )
            })}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  )
}
