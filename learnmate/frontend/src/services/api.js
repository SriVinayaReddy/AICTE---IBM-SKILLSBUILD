import axios from 'axios'

const API = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 60000,
  headers: { 'Content-Type': 'application/json' },
})

// Student APIs
export const studentAPI = {
  create: (data) => API.post('/students/', data),
  get: (id) => API.get(`/students/${id}`),
  update: (id, data) => API.put(`/students/${id}`, data),
  addGoal: (id, data) => API.post(`/students/${id}/goals`, data),
  quickAssess: (id, data) => API.post(`/students/${id}/assess`, data),
  startAssessment: (id, data) => API.post(`/students/${id}/assess/start`, data),
  chatAssessment: (id, data) => API.post(`/students/${id}/assess/chat`, data),
  getDomains: () => API.get('/students/domains'),
}

// Roadmap APIs
export const roadmapAPI = {
  generate: (data) => API.post('/roadmaps/generate', data),
  get: (id) => API.get(`/roadmaps/${id}`),
  updateProgress: (id, data) => API.put(`/roadmaps/${id}/progress`, data),
  adapt: (id, data) => API.post(`/roadmaps/${id}/adapt`, data),
  getReport: (id, studentId) => API.get(`/roadmaps/${id}/report?student_id=${studentId}`),
  getRecommendation: (id, studentId) => API.get(`/roadmaps/${id}/recommendation?student_id=${studentId}`),
  chat: (data) => API.post('/roadmaps/chat', data),
}

export const healthAPI = {
  check: () => API.get('/health'),
}

export default API
