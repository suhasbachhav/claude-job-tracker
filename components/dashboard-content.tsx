'use client'

import { KanbanBoard } from './kanban-board'
import { Job } from '@/types'
import { useState } from 'react'

export function DashboardContent() {
  const [jobs, setJobs] = useState<Job[]>([])
  const [loading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleCreateJob = async (job: Omit<Job, 'id' | 'created_at' | 'updated_at' | 'user_id'>) => {
    try {
      const newJob: Job = {
        ...job,
        id: Math.random().toString(36).substr(2, 9),
        user_id: 'user-' + Math.random().toString(36).substr(2, 9),
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      } as Job
      setJobs((prev) => [newJob, ...prev])
      setError(null)
    } catch (err) {
      setError((err as Error).message)
      throw err
    }
  }

  const handleUpdateJob = async (job: Job) => {
    try {
      setJobs((prev) => prev.map((j) => (j.id === job.id ? job : j)))
      setError(null)
    } catch (err) {
      setError((err as Error).message)
      throw err
    }
  }

  const handleDeleteJob = async (jobId: string) => {
    try {
      setJobs((prev) => prev.filter((j) => j.id !== jobId))
      setError(null)
    } catch (err) {
      setError((err as Error).message)
      throw err
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading your jobs...</p>
        </div>
      </div>
    )
  }

  return (
    <>
      {error && (
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="p-4 bg-red-50 border border-red-200 text-red-800 rounded">
            Error: {error}
          </div>
        </div>
      )}
      <KanbanBoard
        jobs={jobs}
        onCreateJob={handleCreateJob}
        onUpdateJob={handleUpdateJob}
        onDeleteJob={handleDeleteJob}
      />
    </>
  )
}
