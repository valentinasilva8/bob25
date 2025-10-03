import { Header } from "@/components/awe/header"
import { HeroSection } from "@/components/awe/hero-section"
import { ProblemSection } from "@/components/awe/problem-section"
import { MetricsSection } from "@/components/awe/metrics-section"
import { TestimonialsSection } from "@/components/awe/testimonials-section"

export default function Home() {
  return (
    <main className="min-h-screen">
      <Header />
      <HeroSection />
      <ProblemSection />
      <MetricsSection />
      <TestimonialsSection />
    </main>
  )
}
