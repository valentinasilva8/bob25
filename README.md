# AWE Agency - AI-Powered Adtech Platform

## 🌐 **LIVE DEMO**

### **🚀 INSTANT ACCESS - FRONTEND ONLY**
**Visit: [https://bob25.vercel.app/](https://bob25.vercel.app/)**

**⚠️ IMPORTANT:** This live version shows the complete UI/UX experience but **cannot process form submissions** (backend not deployed). 

**For Full Demo Experience:**
- **Option 1:** Run locally (see instructions below) for complete functionality
- **Option 2:** Watch the screen recording demo in the submitted PowerPoint
- **Option 3:** Screen recording available for download in the GitHub repository

## 📖 **About**

AWE Agency is an AI-powered adtech platform dedicated to empowering small fitness and wellness businesses with personalized, sustainable marketing solutions. Our mission is to level the playing field for small business owners by providing them with the same sophisticated marketing tools that large corporations use, while maintaining their authentic voice and community-focused values.

We believe in fostering a community of wellness entrepreneurs who value sustainability, authentic storytelling, and meaningful connections with their customers. Our platform generates unique ad campaigns that not only drive business growth but also track environmental impact, helping businesses make a positive difference for both their communities and the planet.

## 🚀 **Local Development Setup** (Required for Full Demo)

**⚠️ IMPORTANT:** To experience the complete AI-powered ad generation pipeline, you must run the application locally. The live Vercel version only shows the frontend UI.

**For Full Demo Experience:**

### **Manual Setup**
```bash
# Terminal 1 - Backend
python3 start_backend.py

# Terminal 2 - Frontend  
cd frontend && npm install && npm run dev
```

### **Local Access:**
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8002
- **API Documentation:** http://localhost:8002/docs

### **Alternative: Screen Recording Demo**
If you prefer not to run the application locally, you can watch the complete demo:
- **PowerPoint Submission:** Screen recording included in the submitted PowerPoint
- **GitHub Repository:** [AWE DEMO.mov](demo/AWE%20DEMO.mov) - Complete walkthrough video
- **Shows:** Complete user journey from form submission to AI-generated ads
- **Duration:** Full demonstration of the platform's capabilities

---

## 🎯 **Step-by-Step Demo Guide for Judges**

### **1. Landing Page Experience** ✅ **WORKS ON LIVE VERSION**
- **Visit:** [https://bob25.vercel.app/](https://bob25.vercel.app/)
- **Notice:** "AWE — not A-I. It's A-WE" tagline emphasizing human-centered approach
- **Explore:** All UI buttons are fully functional - navigate through different sections
- **Learn More:** Check out the Sustainability tab to understand our environmental approach
- **Start Demo:** Click either "Get Started" or "See How We Help" to begin the demo of our services

### **2. Registration Process (5 Steps)** ⚠️ **REQUIRES LOCAL SETUP TO RECEIVE ADS RECOMMENDATIONS**
**Step 1: Business Information**
- **Business Name:** Enter one of these demo companies (case-insensitive):
  - `Solstice Yoga Studio`
  - `Iron Will Fitness` 
  - `Zen Pilates Studio`
  - `Flow State Dance`
  - `Mindful Movement Wellness`
- **Zip Code:** Enter any ZIP code (e.g., 90210)

**Step 2: Business Details**
- **Mission & Story:** Describe what inspired you to start this business and what makes you unique
- **Products & Services:** Describe what you offer - products, services, classes, etc.

**Step 3: Target Audience**
- **Target Audience:** Describe your ideal customers, their pain points, interests, and what they value most

**Step 4: Demographics & Interests**
- **Age Range:** Select from 18-25, 25-35, 35-45, 45-55, or 55+
- **Interests:** Select from Yoga, Meditation, Wellness, Mindfulness, Fitness, Stress Relief, Nutrition, Community

**Step 5: Creative Needs**
- **Creatives per Week:** Select from:
  - 1-2 creatives per week
  - 3-5 creatives per week
  - 6-10 creatives per week
  - 11-20 creatives per week
  - 20+ creatives per week
- **Note:** This affects environmental impact calculations

### **3. Results Page - AI-Generated Ads**
After completing the form, you'll see:

**Personalized Ad Campaigns:**
- **Unique ad variations** tailored to the specific business using their story & mission to craft the perfect tone
- **Smart audience targeting** - each ad targets specific audience segments like:
  - `yoga_enthusiasts` - Experienced practitioners seeking community
  - `busy_professionals` - Working adults needing stress relief and balance
  - `new_to_yoga` - Beginners looking for accessible, welcoming classes
  - `wellness_seekers` - Health-conscious individuals exploring holistic practices
  - `fitness_enthusiasts` - Active people wanting to complement their workouts
- **Channel recommendations** (Social Media, Local Advertising, Email) - automatically selected based on the business type and target audience
- **Environmental impact metrics** based on creative volume
- **Targeting summary** with audience insights

### **4. Explore the Full Website**
- **Navigation:** Use the header menu to explore all sections
- **Sustainability:** Visit the Sustainability tab to learn about our environmental approach and technical implementation
- **Solutions:** Check out our service offerings and approach
- **Testimonials:** Read about client success stories
- **Pricing:** View our service packages
- **Contact:** Learn how to get in touch with our team

---

## 🧠 **Understanding the Personalized Ads**

### **Why Each Ad is Unique:**

**1. Business-Specific Content:**
- **Solstice Yoga Studio:** Focuses on mindfulness, community, and holistic wellness
- **Iron Will Fitness:** Emphasizes strength, determination, and transformation
- **Zen Pilates Studio:** Highlights precision, balance, and mind-body connection
- **Flow State Dance:** Celebrates movement, creativity, and self-expression
- **Mindful Movement Wellness:** Combines meditation, gentle movement, and healing

**2. Audience Targeting Logic:**
- **Age Range:** Influences language complexity and cultural references
- **Location:** Affects local community messaging and regional preferences
- **Goals:** Shapes call-to-action and value propositions
- **Values:** Determines emotional tone and brand alignment
- **Audience Segments:** Each ad targets a specific demographic:
  - **`yoga_enthusiasts`** - For experienced practitioners who value community and advanced practices
  - **`busy_professionals`** - For working adults who need stress relief and time-efficient wellness
  - **`new_to_yoga`** - For beginners who need encouragement and accessibility messaging
  - **`wellness_seekers`** - For health-conscious individuals exploring holistic approaches
  - **`fitness_enthusiasts`** - For active people looking to complement their existing routines

**3. Channel-Specific Optimization:**
- **Social Media:** Shorter, more visual content with hashtags
  - **Yoga Studios:** 
    - 18-25: Instagram, TikTok with trending wellness hashtags
    - 25-35: Instagram, Facebook with lifestyle-focused mindfulness
    - 35-45: Facebook, LinkedIn with professional wellness content
    - 45+: Facebook with community-focused, educational content
  - **Fitness Centers:**
    - 18-25: TikTok with high-energy workout challenges
    - 25-35: Instagram with lifestyle fitness content
    - 35-45: Facebook, LinkedIn with health-focused messaging
    - 45+: Facebook with gentle fitness and health education
  - **Pilates Studios:** Instagram with precise movement demonstrations (all ages)
  - **Dance Studios:** TikTok, Instagram with dynamic movement content (all ages)
  - **Wellness Centers:** Facebook, LinkedIn with holistic health education (all ages)
- **Local Advertising:** Community-focused, location-specific messaging
  - **Yoga/Pilates:** Community boards, local wellness events, partner studios
  - **Fitness Centers:** Gym partnerships, sports clubs, corporate wellness programs
  - **Dance Studios:** Local dance schools, performance venues, arts communities
  - **Wellness Centers:** Healthcare providers, holistic practitioners, community centers
- **Email:** Longer-form, relationship-building content
  - **Yoga Studios:** Class schedules, meditation guides, wellness tips
  - **Fitness Centers:** Workout plans, nutrition advice, progress tracking
  - **Pilates Studios:** Technique tutorials, posture guides, equipment tips
  - **Dance Studios:** Choreography videos, performance announcements, skill development
  - **Wellness Centers:** Health education, treatment options, holistic approaches

**4. Environmental Impact Scaling:**
- **1-2 creatives/week:** 1.5x multiplier (small studio)
- **3-5 creatives/week:** 3.0x multiplier (growing business)
- **6-10 creatives/week:** 6.0x multiplier (established studio)
- **11-20 creatives/week:** 12.0x multiplier (multi-location)
- **20+ creatives/week:** 25.0x multiplier (franchise level)

---

## 🏗️ **Technical Architecture**

### **Frontend (Next.js/React)**
- **Live URL:** [https://bob25.vercel.app/](https://bob25.vercel.app/)
- **Framework:** Next.js 14 with TypeScript
- **Styling:** Tailwind CSS with custom components
- **State Management:** React hooks and localStorage

### **Backend (FastAPI)**
- **API Endpoint:** Handles business registration and ad generation
- **Demo Data:** 5 pre-configured fitness/wellness studios
- **Case-Insensitive Matching:** Works with any capitalization
- **Dynamic Calculations:** Environmental metrics based on usage

### **Backend-Frontend Integration:**

**API Communication:**
- **Frontend:** Next.js React application running on port 3000
- **Backend:** FastAPI Python server running on port 8002
- **Communication:** HTTP POST requests with JSON payloads
- **CORS:** Enabled for cross-origin requests between frontend and backend

**Data Flow Process:**
1. **User Input:** User completes 5-step registration form on frontend
2. **Data Validation:** Frontend validates all required fields before submission
3. **API Request:** Frontend sends POST request to `http://localhost:8002/business/register/wellness`
4. **Backend Processing:**
   - Receives JSON payload with business data
   - Performs case-insensitive business name matching against `demo_companies.json`
   - Loads pre-configured demo data for matched business
   - Calculates environmental impact based on `creatives_per_week` input
   - Generates personalized ad variations with audience targeting
5. **Response:** Backend returns structured JSON with:
   - Generated ads with headlines, body text, CTAs
   - Audience segments (yoga_enthusiasts, busy_professionals, etc.)
   - Channel recommendations with confidence scores
   - Environmental impact metrics (energy, CO₂, green score)
   - Targeting summary with demographics
6. **Frontend Display:** Results page renders with animations and metrics

**Error Handling:**
- **Network Errors:** Frontend displays user-friendly error messages
- **Validation Errors:** Form validation prevents invalid submissions
- **Loading States:** Spinner and loading text during API calls

**Data Storage:**
- **Frontend:** Uses `localStorage` to persist results between page navigation
- **Backend:** Stateless - processes each request independently
- **Demo Data:** Static JSON file with 5 pre-configured fitness/wellness studios

---

## 🎨 **Key Features**

- **5-step registration form** with creative volume input
- **Dynamic environmental metrics** based on usage
- **AI-generated ad content** for fitness/wellness studios
- **Mock authentication** system
- **Modern, responsive UI** with animations
- **Self-contained demo data** (no external APIs)
- **Case-insensitive** company name matching
- **Responsive design** for all devices

## 🧪 **Testing & Quality**

The application includes:
- ✅ **Health checks** for both services
- ✅ **Error handling** and graceful failures
- ✅ **Real-time environmental impact calculations**
- ✅ **Smooth animations and transitions**
- ✅ **Mobile-responsive design**

## 📋 **Requirements** (For Local Development)

- Python 3.8+
- Node.js 16+
- npm or yarn

## 🛑 **Stopping the Application** (Local Only)

```bash
# Stop all processes manually
Ctrl+C in both terminals

# Or kill processes on specific ports
lsof -ti:3000,8002 | xargs kill -9 2>/dev/null || true
```

---

## ✅ **How to Verify if the App Started Successfully**

### **Backend Verification:**
1. **Health Check:** Visit `http://localhost:8002/health`
   - ✅ **Success:** You should see `{"status":"healthy","carbon_tracking":true}`
   - ❌ **Error:** If you see connection refused, the backend isn't running

2. **API Documentation:** Visit `http://localhost:8002/docs`
   - ✅ **Success:** You should see the Swagger UI documentation page
   - ❌ **Error:** If you see connection refused, the backend isn't running

### **Frontend Verification:**
1. **Main Application:** Visit `http://localhost:3000`
   - ✅ **Success:** You should see the AWE Agency landing page with rotating images
   - ❌ **Error:** If you see connection refused, the frontend isn't running

2. **Registration Page:** Visit `http://localhost:3000/register`
   - ✅ **Success:** You should see the 5-step registration form
   - ❌ **Error:** If you see a 404 or error page, there's a routing issue

### **Full Integration Test:**
1. **Complete Registration:** Fill out the form with one of the demo companies
2. **Submit Form:** Click submit and wait for processing
3. **Results Page:** You should see AI-generated ads and environmental metrics
   - ✅ **Success:** Personalized ads appear with targeting information
   - ❌ **Error:** If you see an error message, check that both services are running

### **Troubleshooting:**
- **Port 3000 in use:** Kill existing processes with `lsof -ti:3000 | xargs kill -9`
- **Port 8002 in use:** Kill existing processes with `lsof -ti:8002 | xargs kill -9`
- **Backend not starting:** Check Python version with `python3 --version` (needs 3.8+)
- **Frontend not starting:** Check Node version with `node --version` (needs 16+)

---

## 🏆 **Summary**

**AWE Agency** demonstrates how AI can create personalized, sustainable marketing solutions for small fitness and wellness businesses. The platform generates unique ad campaigns tailored to each business's story, values, and audience while tracking environmental impact.




