// Mock authentication system for demo purposes
// This replaces Supabase for the competition demo

export interface MockUser {
  id: string
  email: string
  name: string
}

export interface MockProfile {
  id: string
  user_id: string
  business_name: string
  mission: string
  products: string
  audience: string
  zipcode: string
  age_range: string
  interests: string[]
  onboarding_completed: boolean
}

// Mock data storage (in real app, this would be in a database)
let mockUsers: MockUser[] = []
let mockProfiles: MockProfile[] = []
let currentUser: MockUser | null = null

export const mockAuth = {
  // Sign up
  signUp: async (email: string, password: string, name: string) => {
    const existingUser = mockUsers.find(u => u.email === email)
    if (existingUser) {
      throw new Error('User already exists')
    }
    
    const newUser: MockUser = {
      id: `user_${Date.now()}`,
      email,
      name
    }
    
    mockUsers.push(newUser)
    currentUser = newUser
    
    return { user: newUser, error: null }
  },

  // Sign in
  signIn: async (email: string, password: string) => {
    const user = mockUsers.find(u => u.email === email)
    if (!user) {
      throw new Error('Invalid credentials')
    }
    
    currentUser = user
    return { user, error: null }
  },

  // Sign out
  signOut: async () => {
    currentUser = null
    return { error: null }
  },

  // Get current user
  getUser: async () => {
    return { user: currentUser, error: null }
  },

  // Create business profile
  createProfile: async (profileData: Omit<MockProfile, 'id' | 'user_id'>) => {
    if (!currentUser) {
      throw new Error('Not authenticated')
    }
    
    const newProfile: MockProfile = {
      id: `profile_${Date.now()}`,
      user_id: currentUser.id,
      ...profileData
    }
    
    mockProfiles.push(newProfile)
    return { data: newProfile, error: null }
  },

  // Get business profile
  getProfile: async (userId: string) => {
    const profile = mockProfiles.find(p => p.user_id === userId)
    return { data: profile, error: null }
  },

  // Update profile
  updateProfile: async (userId: string, updates: Partial<MockProfile>) => {
    const profileIndex = mockProfiles.findIndex(p => p.user_id === userId)
    if (profileIndex === -1) {
      throw new Error('Profile not found')
    }
    
    mockProfiles[profileIndex] = { ...mockProfiles[profileIndex], ...updates }
    return { data: mockProfiles[profileIndex], error: null }
  },

  // Mock ad metrics
  getAdMetrics: async (userId: string) => {
    // Return mock metrics data
    return {
      data: [
        {
          id: 'metric_1',
          user_id: userId,
          date: new Date().toISOString(),
          impressions: 1250,
          clicks: 45,
          conversions: 8,
          spend: 125.50,
          revenue: 450.00
        },
        {
          id: 'metric_2',
          user_id: userId,
          date: new Date(Date.now() - 86400000).toISOString(),
          impressions: 980,
          clicks: 32,
          conversions: 5,
          spend: 98.75,
          revenue: 320.00
        }
      ],
      error: null
    }
  }
}

// Initialize with a demo user for testing
mockUsers.push({
  id: 'demo_user_1',
  email: 'demo@awe.com',
  name: 'Demo User'
})

mockProfiles.push({
  id: 'demo_profile_1',
  user_id: 'demo_user_1',
  business_name: 'Demo Wellness Studio',
  mission: 'Helping people achieve their wellness goals',
  products: 'Yoga classes, meditation sessions, wellness workshops',
  audience: 'Adults 25-60 interested in wellness and mindfulness',
  zipcode: '10001',
  age_range: '25-45',
  interests: ['yoga', 'meditation', 'wellness'],
  onboarding_completed: true
})
