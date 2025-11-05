import api from './axios'

export interface DashboardStats {
  // Admin/Registrar stats
  total_students?: number
  total_courses?: number
  active_sections?: number
  pending_requests?: number
  published_results?: number
  ineligible_students?: number
  
  // Faculty stats
  my_sections?: number
  my_students?: number
  pending_attendance?: number
  draft_results?: number
  
  // Student stats
  enrolled_courses?: number
  attendance_rate?: number
  completed_results?: number
  
  // Error/message
  error?: string
  message?: string
}

export const dashboardApi = {
  getStats: async (): Promise<DashboardStats> => {
    const response = await api.get<DashboardStats>('/api/dashboard/stats/')
    return response.data
  },
}
