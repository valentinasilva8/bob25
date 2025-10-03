import { TrendingUp, Users, DollarSign, Star } from "lucide-react"

export function MetricsSection() {
  const metrics = [
    {
      icon: TrendingUp,
      value: "127%",
      label: "Average Revenue Growth",
      description: "in the first year",
    },
    {
      icon: Users,
      value: "2,400+",
      label: "Small Businesses Helped",
      description: "across the country",
    },
    {
      icon: DollarSign,
      value: "$8.2M",
      label: "Additional Revenue Generated",
      description: "for our clients",
    },
    {
      icon: Star,
      value: "4.9/5",
      label: "Client Satisfaction",
      description: "from 500+ reviews",
    },
  ]

  return (
    <section className="py-16 bg-gradient-to-b from-background to-muted/30">
      <div className="container mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4">Real Results for Real Businesses</h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            We're proud to help small businesses like yours compete and win in today's market
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {metrics.map((metric, index) => {
            const Icon = metric.icon
            return (
              <div
                key={index}
                className="flex flex-col items-center text-center p-6 rounded-lg bg-card border border-border hover:shadow-lg transition-shadow"
              >
                <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center mb-4">
                  <Icon className="w-8 h-8 text-primary" />
                </div>
                <div className="text-4xl font-bold text-foreground mb-2">{metric.value}</div>
                <div className="text-lg font-semibold text-foreground mb-1">{metric.label}</div>
                <div className="text-sm text-muted-foreground">{metric.description}</div>
              </div>
            )
          })}
        </div>
      </div>
    </section>
  )
}
