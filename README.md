# AWE Agency - AI-Powered Adtech Platform


## 🚀 Quick Start (For Competition Judges)

### Option 1: One-Command Setup (Recommended)
```bash
chmod +x run.sh
./run.sh
```

### Option 2: Docker (Alternative)
```bash
docker-compose up --build
```

### Option 3: Manual Setup
```bash
# Terminal 1 - Backend
python3 start_backend.py

# Terminal 2 - Frontend  
cd frontend && npm install && npm run dev
```

## 🌐 Access the Application

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8002
- **API Documentation:** http://localhost:8002/docs

## 🎯 Demo Instructions

1. **Go to** http://localhost:3000
2. **Click "Get Started"** or "Register"
3. **Try these demo companies:**
   - Solstice Yoga Studio
   - Iron Will Fitness
   - Zen Pilates Studio
   - Flow State Dance
   - Mindful Movement Wellness
4. **Fill out the 5-step form** with any data
5. **See AI-generated ads** and environmental impact metrics

## 🏗️ Architecture

- **Frontend:** Next.js/React with TypeScript
- **Backend:** Python/FastAPI (single file)
- **Data:** Self-contained JSON demo data
- **Authentication:** Mock system (no external services)

## 📋 Requirements

- Python 3.8+
- Node.js 16+
- npm or yarn

## 🛠️ Development

```bash
# Install dependencies
pip3 install -r backend/requirements.txt
cd frontend && npm install

# Start development servers
python3 start_backend.py  # Terminal 1
cd frontend && npm run dev  # Terminal 2
```

## 🐳 Docker Deployment

```bash
# Build and run
docker-compose up --build

# Or build individual image
docker build -t awe-agency .
docker run -p 3000:3000 -p 8002:8002 awe-agency
```

## ☁️ Cloud Deployment

### Vercel (Frontend)
1. Connect GitHub repository
2. Deploy automatically
3. Update backend URL in environment variables

### Railway/Render (Backend)
1. Connect GitHub repository
2. Deploy `backend/simple_main.py`
3. Update frontend API URL

## 🧪 Testing

The application includes:
- ✅ **Health checks** for both services
- ✅ **Error handling** and graceful failures
- ✅ **Case-insensitive** company name matching
- ✅ **Responsive design** for all devices

## 🎨 Features

- **5-step registration form** with creative volume input
- **Dynamic environmental metrics** based on usage
- **AI-generated ad content** for fitness/wellness studios
- **Mock authentication** system
- **Modern, responsive UI** with animations
- **Self-contained demo data** (no external APIs)

## 🛑 Stopping the Application

```bash
# Stop all processes
./restart_clean.sh

# Or manually
Ctrl+C in both terminals
```

## 📞 Support

This is a competition demo. All functionality is self-contained and requires no external services or API keys.

---

**Built for AWE Agency Competition** 🏆
