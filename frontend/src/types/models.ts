/**
 * Type definitions for API models
 */

// Student model
export interface Student {
  id: number
  reg_no: string
  name: string
  program: string
  status: 'Active' | 'Inactive' | 'Graduated' | 'Suspended'
}

// Course model
export interface Course {
  id: number
  code: string
  title: string
  credits: number
  program: string
}

// Term model
export interface Term {
  id: number
  name: string
  status: 'Active' | 'Inactive' | 'Archived'
  start_date: string
  end_date: string
}

// Section model
export interface Section {
  id: number
  course: number
  term: number
  teacher: string
  capacity: number
}

// Enrollment model
export interface Enrollment {
  id: number
  student: number
  section: number
  enrolled_at: string
  status: string
}

// Assessment model
export interface Assessment {
  id: number
  section: number
  name: string
  max_score: number
  weight: number
}

// Assessment Score model
export interface AssessmentScore {
  id: number
  assessment: number
  student: number
  score: number
  remarks?: string
}

// Attendance model
export interface Attendance {
  id: number
  section: number
  student: number
  date: string
  status: 'Present' | 'Absent' | 'Late' | 'Excused'
}

// Pagination response
export interface PaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

// API error response
export interface ApiError {
  detail?: string
  [key: string]: unknown
}
