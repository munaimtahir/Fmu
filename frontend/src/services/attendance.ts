/**
 * Attendance API service
 */
import api from '@/api/axios'
import { Attendance, PaginatedResponse } from '@/types'

export const attendanceService = {
  /**
   * Get attendance records with filters
   */
  async getAll(params?: {
    page?: number
    section?: number
    student?: number
    date?: string
  }): Promise<PaginatedResponse<Attendance>> {
    const response = await api.get<PaginatedResponse<Attendance>>('/api/attendance/', {
      params,
    })
    return response.data
  },

  /**
   * Mark attendance for a section
   */
  async markAttendance(sectionId: number, data: {
    date: string
    records: Array<{
      student: number
      status: 'Present' | 'Absent' | 'Late' | 'Excused'
    }>
  }): Promise<void> {
    await api.post(`/api/sections/${sectionId}/attendance/`, data)
  },

  /**
   * Get attendance for a specific section
   */
  async getBySectionId(sectionId: number, params?: {
    date?: string
  }): Promise<PaginatedResponse<Attendance>> {
    const response = await api.get<PaginatedResponse<Attendance>>(
      `/api/sections/${sectionId}/attendance/`,
      { params }
    )
    return response.data
  },
}
