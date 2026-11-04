import { useState } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Navbar from './components/Navbar.jsx'
import Onboarding from './pages/Onboarding.jsx'
import Dashboard from './pages/Dashboard.jsx'
import RoadmapView from './pages/RoadmapView.jsx'
import CoachChat from './pages/CoachChat.jsx'
import Assessment from './pages/Assessment.jsx'

function App() {
  const [studentId, setStudentId] = useState(
    () => localStorage.getItem('learnmate_student_id') || null
  )

  const handleStudentCreated = (id) => {
    localStorage.setItem('learnmate_student_id', id)
    setStudentId(id)
  }

  if (!studentId) {
    return <Onboarding onStudentCreated={handleStudentCreated} />
  }

  return (
    <BrowserRouter>
      <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
        <Navbar studentId={studentId} onReset={() => {
          localStorage.removeItem('learnmate_student_id')
          setStudentId(null)
        }} />
        <main style={{ flex: 1, padding: '24px', maxWidth: '1200px', margin: '0 auto', width: '100%' }}>
          <Routes>
            <Route path="/" element={<Dashboard studentId={studentId} />} />
            <Route path="/roadmap/:roadmapId" element={<RoadmapView studentId={studentId} />} />
            <Route path="/coach" element={<CoachChat studentId={studentId} />} />
            <Route path="/assess" element={<Assessment studentId={studentId} />} />
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}

export default App
