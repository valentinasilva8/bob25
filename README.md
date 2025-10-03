# AWE Agency - AI-Powered Adtech Platform

## 🌐 **LIVE DEMO** (For Competition Judges)

### **🚀 INSTANT ACCESS - NO SETUP REQUIRED**
**Visit: [https://bob25.vercel.app/](https://bob25.vercel.app/)**

The application is live and ready to demo! No installation or setup required.

---

## 🎯 **Step-by-Step Demo Guide for Judges**

### **1. Landing Page Experience**
- **Visit:** [https://bob25.vercel.app/](https://bob25.vercel.app/)
- **Observe:** Beautiful hero section with rotating wellness business images
- **Notice:** "AWE — not A-I. It's A-WE" tagline emphasizing human-centered approach
- **Click:** "Get Started" button to begin the demo

### **2. Registration Process (5 Steps)**
**Step 1: Business Information**
- **Business Name:** Enter one of these demo companies (case-insensitive):
  - `Solstice Yoga Studio`
  - `Iron Will Fitness` 
  - `Zen Pilates Studio`
  - `Flow State Dance`
  - `Mindful Movement Wellness`
- **Location:** Enter any ZIP code (e.g., 90210)
- **Age Range:** Select any range (e.g., 25-35)

**Step 2: Business Goals**
- **Primary Goal:** Select any option (e.g., "Increase brand awareness")
- **Target Audience:** Select any option (e.g., "Fitness enthusiasts")

**Step 3: Budget & Timeline**
- **Monthly Budget:** Select any range (e.g., "$1,000 - $5,000")
- **Campaign Duration:** Select any option (e.g., "3-6 months")

**Step 4: Brand Voice**
- **Tone:** Select any option (e.g., "Professional")
- **Values:** Select any options (e.g., "Sustainability", "Community")

**Step 5: Creative Needs**
- **Creatives per Week:** Select any option (e.g., "3-5")
- **Note:** This affects environmental impact calculations

### **3. Results Page - AI-Generated Ads**
After completing the form, you'll see:

**Personalized Ad Campaigns:**
- **3 unique ad variations** tailored to the specific business
- **Channel recommendations** (Social Media, Local Advertising, Email)
- **Environmental impact metrics** based on creative volume
- **Targeting summary** with audience insights

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

**3. Channel-Specific Optimization:**
- **Social Media:** Shorter, more visual content with hashtags
- **Local Advertising:** Community-focused, location-specific messaging
- **Email:** Longer-form, relationship-building content

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

### **Data Flow:**
1. User fills 5-step form
2. Frontend sends data to backend API
3. Backend matches business name to demo data
4. AI generates personalized ads and recommendations
5. Environmental impact calculated based on creative volume
6. Results displayed with animations and metrics

---

## 🚀 **Local Development Setup** (Optional)

If you want to run locally for development:

### **Option 1: One-Command Setup**
```bash
chmod +x run.sh
./run.sh
```

### **Option 2: Manual Setup**
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
# Stop all processes
./restart_clean.sh

# Or manually
Ctrl+C in both terminals
```

---

## 🏆 **Competition Demo Summary**

**AWE Agency** demonstrates how AI can create personalized, sustainable marketing solutions for small fitness and wellness businesses. The platform generates unique ad campaigns tailored to each business's story, values, and audience while tracking environmental impact.

**Live Demo:** [https://bob25.vercel.app/](https://bob25.vercel.app/)

**Built for AWE Agency Competition** 🏆
