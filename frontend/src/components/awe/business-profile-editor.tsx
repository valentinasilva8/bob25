"use client"

import { useState } from "react"
import { Button } from "@/components/awe/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/awe/ui/card"
import { Label } from "@/components/awe/ui/label"
import { Textarea } from "@/components/awe/ui/textarea"
import { Input } from "@/components/awe/ui/input"
import { createBrowserClient } from "@supabase/ssr"
import { Pencil, Save, X } from "lucide-react"

interface BusinessProfile {
  business_name: string
  business_story: string
  products_services: string
  target_audience: string
  growth_goals: string
}

interface BusinessProfileEditorProps {
  initialProfile: BusinessProfile
  userId: string
}

export function BusinessProfileEditor({ initialProfile, userId }: BusinessProfileEditorProps) {
  const [isEditing, setIsEditing] = useState(false)
  const [isSaving, setIsSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState(false)

  const [formData, setFormData] = useState<BusinessProfile>(initialProfile)

  const supabase = createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
  )

  const handleSave = async () => {
    setIsSaving(true)
    setError(null)
    setSuccess(false)

    try {
      const { error: updateError } = await supabase
        .from("business_profiles")
        .update({
          business_name: formData.business_name,
          business_story: formData.business_story,
          products_services: formData.products_services,
          target_audience: formData.target_audience,
          growth_goals: formData.growth_goals,
          updated_at: new Date().toISOString(),
        })
        .eq("user_id", userId)

      if (updateError) throw updateError

      setSuccess(true)
      setIsEditing(false)
      setTimeout(() => setSuccess(false), 3000)
    } catch (err) {
      console.error("Error updating profile:", err)
      setError(err instanceof Error ? err.message : "Failed to update profile")
    } finally {
      setIsSaving(false)
    }
  }

  const handleCancel = () => {
    setFormData(initialProfile)
    setIsEditing(false)
    setError(null)
  }

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle>Business Profile</CardTitle>
            <CardDescription>View and edit your business information</CardDescription>
          </div>
          {!isEditing && (
            <Button onClick={() => setIsEditing(true)} variant="outline" size="sm">
              <Pencil className="h-4 w-4 mr-2" />
              Edit
            </Button>
          )}
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          {/* Business Name */}
          <div className="space-y-2">
            <Label htmlFor="businessName">Business Name</Label>
            {isEditing ? (
              <Input
                id="businessName"
                value={formData.business_name}
                onChange={(e) => setFormData({ ...formData, business_name: e.target.value })}
                placeholder="Enter your business name"
              />
            ) : (
              <p className="text-sm text-gray-700 bg-gray-50 p-3 rounded-md">{formData.business_name}</p>
            )}
          </div>

          {/* Business Story */}
          <div className="space-y-2">
            <Label htmlFor="businessStory">Business Story & Mission</Label>
            {isEditing ? (
              <Textarea
                id="businessStory"
                value={formData.business_story}
                onChange={(e) => setFormData({ ...formData, business_story: e.target.value })}
                rows={4}
                className="resize-none"
                placeholder="Tell us about your business journey..."
              />
            ) : (
              <p className="text-sm text-gray-700 bg-gray-50 p-3 rounded-md whitespace-pre-wrap">
                {formData.business_story}
              </p>
            )}
          </div>

          {/* Products & Services */}
          <div className="space-y-2">
            <Label htmlFor="productsServices">Products & Services</Label>
            {isEditing ? (
              <Textarea
                id="productsServices"
                value={formData.products_services}
                onChange={(e) => setFormData({ ...formData, products_services: e.target.value })}
                rows={4}
                className="resize-none"
                placeholder="Describe what you sell or the services you provide..."
              />
            ) : (
              <p className="text-sm text-gray-700 bg-gray-50 p-3 rounded-md whitespace-pre-wrap">
                {formData.products_services}
              </p>
            )}
          </div>

          {/* Target Audience */}
          <div className="space-y-2">
            <Label htmlFor="targetAudience">Target Audience</Label>
            {isEditing ? (
              <Textarea
                id="targetAudience"
                value={formData.target_audience}
                onChange={(e) => setFormData({ ...formData, target_audience: e.target.value })}
                rows={4}
                className="resize-none"
                placeholder="Who are your ideal customers..."
              />
            ) : (
              <p className="text-sm text-gray-700 bg-gray-50 p-3 rounded-md whitespace-pre-wrap">
                {formData.target_audience}
              </p>
            )}
          </div>

          {/* Growth Goals */}
          <div className="space-y-2">
            <Label htmlFor="growthGoals">Growth Goals</Label>
            {isEditing ? (
              <Textarea
                id="growthGoals"
                value={formData.growth_goals}
                onChange={(e) => setFormData({ ...formData, growth_goals: e.target.value })}
                rows={4}
                className="resize-none"
                placeholder="What are you hoping to achieve..."
              />
            ) : (
              <p className="text-sm text-gray-700 bg-gray-50 p-3 rounded-md whitespace-pre-wrap">
                {formData.growth_goals}
              </p>
            )}
          </div>

          {/* Action Buttons */}
          {isEditing && (
            <div className="flex gap-3 pt-4">
              <Button onClick={handleCancel} variant="outline" className="flex-1 bg-transparent" disabled={isSaving}>
                <X className="h-4 w-4 mr-2" />
                Cancel
              </Button>
              <Button onClick={handleSave} className="flex-1" disabled={isSaving}>
                <Save className="h-4 w-4 mr-2" />
                {isSaving ? "Saving..." : "Save Changes"}
              </Button>
            </div>
          )}

          {/* Success/Error Messages */}
          {success && (
            <div className="rounded-md bg-green-50 p-3 text-sm text-green-800">Profile updated successfully!</div>
          )}
          {error && <div className="rounded-md bg-destructive/10 p-3 text-sm text-destructive">{error}</div>}
        </div>
      </CardContent>
    </Card>
  )
}
