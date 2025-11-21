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
   * Mark attendance for a section (creates individual records)
   */
  async markAttendance(sectionId: number, data: {
    date: string
    records: Array<{
      student: number
      status: 'Present' | 'Absent' | 'Late' | 'Excused'
    }>
  }): Promise<Attendance[]> {
    // Create attendance records individually
    const results = await Promise.all(
      data.records.map((record) =>
        api.post<Attendance>('/api/attendance/', {
          section: sectionId,
          student: record.student,
          date: data.date,
          present: record.status === 'Present',
          status: record.status,
        })
      )
    )
    return results.map((r) => r.data)
  },

  /**
   * Get attendance for a specific section
   */
  async getBySectionId(sectionId: number, params?: {
    date?: string
  }): Promise<PaginatedResponse<Attendance>> {
    const response = await api.get<PaginatedResponse<Attendance>>(
      '/api/attendance/',
      { params: { ...params, section: sectionId } }
    )
    return response.data
  },
}
