import { Header } from "@/components/header"
import { HeroSection } from "@/components/hero-section"
import { ProblemSection } from "@/components/problem-section"
import { MetricsSection } from "@/components/metrics-section"
import { TestimonialsSection } from "@/components/testimonials-section"

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
