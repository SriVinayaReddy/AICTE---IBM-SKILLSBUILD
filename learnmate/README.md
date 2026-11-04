# LearnMate – Agentic AI for Personalized Course Pathways
## Problem Statement #12 | IBM Granite + IBM Cloud Lite

<div align="center">
  <img src="https://img.shields.io/badge/IBM-Granite_AI-0062ff?style=for-the-badge&logo=ibm" />
  <img src="https://img.shields.io/badge/IBM_Cloud-Lite-054ada?style=for-the-badge&logo=ibm" />
  <img src="https://img.shields.io/badge/Flask-Backend-000000?style=for-the-badge&logo=flask" />
  <img src="https://img.shields.io/badge/React-Frontend-61DAFB?style=for-the-badge&logo=react" />
</div>

---

## Overview

**LearnMate** is an Agentic AI-powered learning coach that helps students discover the right learning path aligned with their goals and interests. It uses **IBM Granite** (via IBM watsonx.ai) to:

- 🧠 **Assess** a student's current skill level through conversation
- 🗺️ **Generate** a fully personalized multi-step course roadmap
- 📊 **Track** progress and adapt the roadmap dynamically
- 💬 **Coach** students via an AI conversational interface
- 📅 **Report** weekly AI progress summaries

---

## Architecture

```
learnmate/
├── backend/              # Python Flask API
│   ├── app.py            # Flask entry point
│   ├── config.py         # Environment configuration
│   ├── agents/
│   │   ├── assessment_agent.py   # Skill evaluation (IBM Granite)
│   │   ├── roadmap_agent.py      # Roadmap generation (IBM Granite)
│   │   └── progress_agent.py    # Adaptive progress tracking
│   ├── models/
│   │   ├── student.py    # Student profile data model
│   │   └── roadmap.py    # Roadmap & course data model
│   ├── routes/
│   │   ├── student_routes.py    # /api/students endpoints
│   │   └── roadmap_routes.py   # /api/roadmaps endpoints
│   ├── utils/
│   │   ├── granite_client.py   # IBM Granite AI wrapper
│   │   ├── db.py               # IBM Cloudant + in-memory store
│   │   └── course_catalog.py   # Curated course data
│   └── requirements.txt
├── frontend/             # React + Vite SPA
│   ├── src/
│   │   ├── App.jsx
│   │   ├── pages/
│   │   │   ├── Onboarding.jsx   # 3-step signup flow
│   │   │   ├── Dashboard.jsx    # Progress overview
│   │   │   ├── RoadmapView.jsx  # Step-by-step roadmap
│   │   │   ├── CoachChat.jsx    # AI chat interface
│   │   │   └── Assessment.jsx  # Skill assessment
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   └── StepCard.jsx
│   │   └── services/api.js      # Axios API client
│   └── package.json
├── env.example           # Environment variables template
└── README.md
```

---

## IBM Cloud Services Used

| Service | Purpose |
|---|---|
| **IBM watsonx.ai** | Core AI inference via IBM Granite models |
| **IBM Granite 13B Instruct** | Roadmap generation, course recommendations |
| **IBM Granite 13B Chat** | Conversational assessment & coaching |
| **IBM Slate Embeddings** | Semantic skill matching |
| **IBM Cloudant** | Student profiles & roadmap persistence (NoSQL) |
| **IBM SkillsBuild** | Integrated free course catalog |

---

## Quick Start

### 1. Clone and configure

```bash
# Copy the environment file
cp env.example .env
# Edit .env with your IBM credentials
```

### 2. Backend Setup

```bash
cd learnmate/backend
pip install -r requirements.txt
python app.py
# API runs at http://localhost:5000
```

### 3. Frontend Setup

```bash
cd learnmate/frontend
npm install
npm run dev
# UI runs at http://localhost:3000
```

---

## IBM Granite Configuration

Get your credentials from [IBM watsonx.ai](https://cloud.ibm.com/catalog/services/watson-machine-learning):

```env
IBM_WATSONX_API_KEY=<your_api_key>
IBM_WATSONX_PROJECT_ID=<your_project_id>
IBM_WATSONX_URL=https://us-south.ml.cloud.ibm.com
IBM_GRANITE_MODEL_ID=ibm/granite-13b-instruct-v2
IBM_GRANITE_CHAT_MODEL=ibm/granite-13b-chat-v2
```

> **Demo Mode**: Without credentials, the app runs in demo mode with fallback responses.

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/students/` | Create student profile |
| `GET` | `/api/students/:id` | Get profile |
| `POST` | `/api/students/:id/assess` | Quick skill assessment |
| `POST` | `/api/students/:id/goals` | Add learning goal |
| `POST` | `/api/roadmaps/generate` | 🤖 Generate AI roadmap |
| `GET` | `/api/roadmaps/:id` | Get roadmap |
| `PUT` | `/api/roadmaps/:id/progress` | Update step progress |
| `POST` | `/api/roadmaps/:id/adapt` | 🤖 Adapt roadmap with AI |
| `GET` | `/api/roadmaps/:id/report` | 🤖 Weekly AI report |
| `POST` | `/api/roadmaps/chat` | 🤖 Chat with AI coach |
| `GET` | `/api/health` | Health check |

---

## Supported Learning Domains

- Frontend Development
- Backend Development
- Full Stack Development
- Data Science & ML
- Cybersecurity
- UI/UX Design
- Mobile Development
- Cloud & DevOps
- Blockchain
- Game Development

---

## Features

- ✅ **Agentic AI**: Multiple specialized agents (Assessment, Roadmap, Progress)
- ✅ **IBM Granite Integration**: Real LLM-powered responses
- ✅ **IBM Cloudant**: Cloud NoSQL persistence with local fallback
- ✅ **Personalized Roadmaps**: 5-8 progressive steps with real course links
- ✅ **Progress Tracking**: Click-to-update step completion
- ✅ **Adaptive Learning**: Roadmap evolves based on student feedback
- ✅ **Conversational Coach**: Full chat interface with context memory
- ✅ **Weekly Reports**: AI-generated progress summaries
- ✅ **Demo Mode**: Works without IBM credentials for local testing

---

*Developed for AICTE Problem Statement #12 – Agentic AI for Personalized Course Pathways*
