# 🎓 LearnMate AI — Agentic AI for Personalized Course Pathways

**AICTE Problem Statement #12 | Agentic AI | IBM watsonx.ai | IBM Granite**

LearnMate AI is an intelligent, agentic AI-powered learning platform designed to create personalized learning pathways for students based on their skills, interests, learning goals, and progress.

Powered by **IBM Granite models and IBM watsonx.ai**, LearnMate AI uses a multi-agent architecture where specialized AI agents collaborate to assess student capabilities, recommend relevant courses, generate personalized learning roadmaps, monitor progress, and adapt learning recommendations dynamically.

Our goal is to make learning more personalized, structured, and accessible by transforming the traditional one-size-fits-all learning experience into an intelligent, adaptive journey.

---

## 🚀 Key Features

- **Personalized Student Assessment:** Evaluates students' existing skills, knowledge levels, interests, and career goals.
- **AI-Generated Learning Roadmaps:** Creates structured learning pathways with recommended topics, courses, and milestones.
- **Intelligent Course Recommendations:** Suggests relevant courses and learning resources based on individual student profiles.
- **Progress Tracking:** Monitors student learning activities, completed milestones, and overall progress.
- **Adaptive Learning:** Dynamically adjusts learning recommendations based on student performance and progress.
- **AI Learning Coach:** Provides interactive, AI-powered learning guidance and answers student queries.
- **Student Dashboard:** Offers a centralized view of learning goals, roadmaps, progress, and recommendations.

---

## 🧠 Agentic AI Architecture

LearnMate AI follows a multi-agent architecture consisting of five specialized AI agents. Each agent performs a dedicated task and collaborates with other agents to deliver personalized learning experiences.

| AI Agent | Responsibility |
|---|---|
| Assessment Agent | Analyzes student skills, interests, knowledge levels, and learning requirements. |
| Learning Path Agent | Generates personalized learning roadmaps with structured topics and milestones. |
| Course Recommendation Agent | Identifies and recommends suitable courses and learning resources. |
| Progress Tracking Agent | Monitors student progress and evaluates learning milestones. |
| Adaptive Learning Agent | Adjusts learning pathways and recommendations based on student performance. |

### How Agentic AI Works

1. **Student Input:** Students provide their interests, existing skills, knowledge level, and learning goals.
2. **Assessment:** The Assessment Agent analyzes the student profile.
3. **Pathway Generation:** The Learning Path Agent creates a personalized roadmap.
4. **Course Discovery:** The Course Recommendation Agent identifies relevant learning resources.
5. **Progress Monitoring:** The Progress Tracking Agent monitors learning activities.
6. **Continuous Adaptation:** The Adaptive Learning Agent refines recommendations based on student progress.

The agents leverage IBM Granite models through IBM watsonx.ai to support intelligent reasoning and personalized recommendations.

---

## 🏗️ System Architecture

LearnMate AI is built using a modular architecture with separate frontend, backend, AI agent, and cloud data layers.

### Technology Stack

| Layer | Technology |
|---|---|
| Frontend | React 18 |
| Frontend Build Tool | Vite 5 |
| Backend | Python 3.13 |
| API Framework | Flask 3.x |
| AI Models | IBM Granite 13B Instruct v2 / Granite Chat |
| AI Platform | IBM watsonx.ai |
| Database | IBM Cloudant |
| Course Resources | IBM SkillsBuild and external course resources |
| API Communication | REST API |
| Authentication | JWT / IBM IAM integration |
| Data Validation | Pydantic |
| Deployment Server | Gunicorn |

### Architecture Flow

```text
          STUDENT
             |
             v
     REACT + VITE FRONTEND
             |
             v
        FLASK REST API
             |
             v
      AI AGENT ORCHESTRATION
             |
     +-------+-------+
     |       |       |
     v       v       v
 Assessment Learning Course
  Agent     Path    Recommendation
            Agent      Agent
     |       |       |
     +-------+-------+
             |
       +-----+------+
       |            |
       v            v
   Progress     Adaptive
   Tracking     Learning
    Agent        Agent
       |            |
       +------+-----+
              |
              v
       IBM WATSONX.AI
        IBM GRANITE
              |
              v
       IBM CLOUDANT
              |
              v
    PERSONALIZED LEARNING
          EXPERIENCE
```

---

## 🛠️ Technologies Used

### IBM Technologies

**IBM Granite**
- Provides the foundation for AI-powered reasoning and personalized learning recommendations.
- Supports student assessment, learning pathway generation, and adaptive guidance.

**IBM watsonx.ai**
- Provides access to IBM Granite foundation models.
- Enables AI-powered processing and generation through model APIs.

**IBM Cloudant**
- Provides cloud-based document storage.
- Stores student profiles, learning roadmaps, and progress information.

**IBM SkillsBuild**
- Serves as a learning resource for discovering relevant educational courses and materials.

### Development Technologies

- Python 3.13
- Flask 3.x
- React 18
- Vite 5
- JavaScript
- REST APIs
- JSON

---

## 📂 Project Structure

```text
LearnMate-AI/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   │   ├── Onboarding.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── RoadmapView.jsx
│   │   │   ├── CoachChat.jsx
│   │   │   └── Assessment.jsx
│   │   │
│   │   ├── services/
│   │   ├── App.jsx
│   │   └── main.jsx
│   │
│   ├── package.json
│   └── vite.config.js
│
├── backend/
│   ├── agents/
│   │   ├── assessment_agent.py
│   │   ├── roadmap_agent.py
│   │   ├── progress_agent.py
│   │   ├── recommendation_agent.py
│   │   └── adaptive_learning_agent.py
│   │
│   ├── models/
│   ├── routes/
│   ├── services/
│   │   ├── granite_client.py
│   │   └── course_catalog.py
│   │
│   ├── app.py
│   └── requirements.txt
│
├── .gitignore
├── .env.example
└── README.md
```

---

## ⚙️ Installation and Setup

Follow these steps to run LearnMate AI locally.

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/LearnMate-AI.git
```

```bash
cd LearnMate-AI
```

### 2. Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the environment.

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Configure IBM watsonx.ai

Create a `.env` file inside the backend directory and configure your IBM credentials.

```env
IBM_WATSONX_API_KEY=your_api_key
IBM_WATSONX_PROJECT_ID=your_project_id
IBM_GRANITE_MODEL_ID=your_model_id
IBM_GRANITE_CHAT_MODEL=your_chat_model_id

CLOUDANT_URL=your_cloudant_url
```

**Important:** Obtain credentials from your own IBM Cloud and watsonx.ai account. Never commit your `.env` file or expose API keys in your GitHub repository.

### 4. Start the Backend

```bash
python app.py
```

The Flask backend will start on the configured local port.

### 5. Frontend Setup

Open another terminal and navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Open the local URL displayed by Vite in your browser.

---

## 🔗 API Endpoints

LearnMate AI uses REST APIs to connect the React frontend with the Flask backend.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/health` | Checks backend health. |
| POST | `/api/students` | Creates or registers a student profile. |
| GET | `/api/students` | Retrieves student information. |
| POST | `/api/roadmaps` | Generates a personalized learning roadmap. |
| GET | `/api/roadmaps` | Retrieves learning roadmaps. |

Additional endpoints support assessment, course recommendations, progress tracking, and AI learning interactions.

*Refer to the backend route definitions for the complete list of implemented endpoints.*

---

## 🎯 Expected Impact

LearnMate AI aims to address common challenges in traditional learning environments:

- Reduces confusion when selecting courses and learning resources.
- Provides structured learning pathways based on individual goals.
- Helps students identify skill gaps and areas for improvement.
- Encourages continuous learning through progress monitoring.
- Improves learning experiences through adaptive AI recommendations.
- Makes personalized educational guidance more accessible.

---

## 🔮 Future Enhancements

- Integration with additional educational platforms and course providers.
- Advanced skill-gap analysis.
- AI-powered career pathway recommendations.
- Learning analytics and performance visualization.
- Multilingual learning assistance.
- Enhanced agent collaboration and orchestration.
- Deployment on scalable cloud infrastructure.

---

## ☁️ Deployment

The application is designed with a separate React frontend and Flask backend, allowing independent deployment.

- **Frontend:** Vercel
- **Backend:** Python-compatible hosting or IBM Cloud infrastructure.
- **Database:** IBM Cloudant
- **AI Services:** IBM watsonx.ai

Deployment configuration and environment variables must be configured separately for each hosting environment.

---

## 👩‍💻 Project Information

| Detail | Information |
|---|---|
| Project Name | LearnMate AI |
| Problem Statement | AICTE Problem Statement #12 |
| Domain | Agentic AI / EdTech |
| Project Type | AI-Powered Personalized Learning Platform |
| AI Model | IBM Granite |
| AI Platform | IBM watsonx.ai |
| Cloud Platform | IBM Cloud |

---

## 📜 License

This project is developed for educational and demonstration purposes as part of the AICTE problem statement initiative.

---

**LearnMate AI — Learn Smarter. Grow Faster. Your Learning, Your Pathway.** 🎓
