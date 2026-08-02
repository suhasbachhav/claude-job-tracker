'use client'

import { Job, JobStatus } from '@/types'
import { useState } from 'react'
import { JobCard } from './job-card'
import { JobForm } from './job-form'

const statusGroups: JobStatus[] = ['applied', 'interview', 'offer', 'rejected']
const statusLabels: Record<JobStatus, string> = {
  applied: '📨 Applied',
  interview: '👥 Interview',
  offer: '🎉 Offer',
  rejected: '❌ Rejected',
}

const statusCounts: Record<JobStatus, string> = {
  applied: 'bg-blue-100 text-blue-800',
  interview: 'bg-amber-100 text-amber-800',
  offer: 'bg-emerald-100 text-emerald-800',
  rejected: 'bg-red-100 text-red-800',
}

interface KanbanBoardProps {
  jobs: Job[]
  onCreateJob: (job: Omit<Job, 'id' | 'created_at' | 'updated_at' | 'user_id'>) => void | Promise<void>
  onUpdateJob: (job: Job) => void | Promise<void>
  onDeleteJob: (jobId: string) => void | Promise<void>
}

export function KanbanBoard({
  jobs,
  onCreateJob,
  onUpdateJob,
  onDeleteJob,
}: KanbanBoardProps) {
  const [draggedJob, setDraggedJob] = useState<Job | null>(null)
  const [showAddForm, setShowAddForm] = useState(false)

  const handleDragStart = (e: React.DragEvent, job: Job) => {
    setDraggedJob(job)
    e.dataTransfer.effectAllowed = 'move'
  }

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    e.dataTransfer.dropEffect = 'move'
  }

  const handleDrop = async (e: React.DragEvent, status: JobStatus) => {
    e.preventDefault()
    if (draggedJob && draggedJob.status !== status) {
      await onUpdateJob({
        ...draggedJob,
        status,
      })
    }
    setDraggedJob(null)
  }

  const getJobsByStatus = (status: JobStatus) =>
    jobs.filter((job) => job.status === status)

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8 flex justify-between items-center">
          <div>
            <h2 className="text-3xl font-bold text-gray-900">Job Applications</h2>
            <p className="text-sm text-gray-600 mt-1">
              Total: <span className="font-semibold">{jobs.length}</span>
            </p>
          </div>
          <button
            onClick={() => setShowAddForm(true)}
            className="btn-primary px-6 py-3 text-lg"
          >
            + Add Job
          </button>
        </div>

        {showAddForm && (
          <div className="mb-8 max-w-md">
            <JobForm
              onSubmit={async (job) => {
                await onCreateJob(job as Omit<Job, 'id' | 'created_at' | 'updated_at' | 'user_id'>)
                setShowAddForm(false)
              }}
              onCancel={() => setShowAddForm(false)}
            />
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {statusGroups.map((status) => {
            const statusJobs = getJobsByStatus(status)
            return (
              <div
                key={status}
                onDragOver={handleDragOver}
                onDrop={(e) => handleDrop(e, status)}
                className="bg-white rounded-lg shadow-sm p-4 min-h-96 border-t-4 border-gray-300"
              >
                <div className="flex items-center justify-between mb-4">
                  <h3 className="font-bold text-gray-900">{statusLabels[status]}</h3>
                  <span className={`px-3 py-1 rounded-full text-sm font-semibold ${statusCounts[status]}`}>
                    {statusJobs.length}
                  </span>
                </div>

                <div className="space-y-3 min-h-80">
                  {statusJobs.length === 0 ? (
                    <div className="text-center py-8 text-gray-400">
                      <p className="text-sm">No jobs yet</p>
                    </div>
                  ) : (
                    statusJobs.map((job) => (
                      <JobCard
                        key={job.id}
                        job={job}
                        onEdit={onUpdateJob}
                        onDelete={onDeleteJob}
                        onDragStart={handleDragStart}
                      />
                    ))
                  )}
                </div>
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}
