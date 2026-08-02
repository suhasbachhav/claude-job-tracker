export type JobStatus = 'applied' | 'interview' | 'offer' | 'rejected'

export interface Job {
  id: string
  user_id: string
  company: string
  position: string
  status: JobStatus
  notes: string | null
  applied_date: string
  created_at: string
  updated_at: string
}

export interface User {
  id: string
  email: string
  created_at: string
  updated_at: string
}

export interface AuthUser {
  id: string
  email?: string
}
