'use client'

import { Job, JobStatus } from '@/types'
import { useState } from 'react'
import { JobForm } from './job-form'

const statusColors: Record<JobStatus, string> = {
  applied: 'bg-blue-50 border-l-4 border-l-blue-500',
  interview: 'bg-amber-50 border-l-4 border-l-amber-500',
  offer: 'bg-emerald-50 border-l-4 border-l-emerald-500',
  rejected: 'bg-red-50 border-l-4 border-l-red-500',
}

interface JobCardProps {
  job: Job
  onEdit: (job: Job) => void | Promise<void>
  onDelete: (jobId: string) => void | Promise<void>
  onDragStart: (e: React.DragEvent, job: Job) => void
}

export function JobCard({ job, onEdit, onDelete, onDragStart }: JobCardProps) {
  const [showEditForm, setShowEditForm] = useState(false)
  const [deleting, setDeleting] = useState(false)

  const handleDelete = async () => {
    if (window.confirm(`Delete "${job.company}" - "${job.position}"?`)) {
      setDeleting(true)
      try {
        await onDelete(job.id)
      } finally {
        setDeleting(false)
      }
    }
  }

  if (showEditForm) {
    return (
      <JobForm
        initialJob={job}
        onSubmit={async (updated) => {
          await onEdit({ ...job, ...updated } as Job)
          setShowEditForm(false)
        }}
        onCancel={() => setShowEditForm(false)}
      />
    )
  }

  const appliedDate = new Date(job.applied_date).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  })

  return (
    <div
      draggable
      onDragStart={(e) => onDragStart(e, job)}
      className={`card p-4 cursor-move hover:shadow-md transition ${statusColors[job.status]}`}
    >
      <h3 className="font-semibold text-gray-900">{job.company}</h3>
      <p className="text-sm text-gray-600">{job.position}</p>
      <p className="text-xs text-gray-500 mt-2">Applied: {appliedDate}</p>

      {job.notes && (
        <p className="text-sm text-gray-700 mt-2 italic">&quot;{job.notes}&quot;</p>
      )}

      <div className="mt-4 flex gap-2">
        <button
          onClick={() => setShowEditForm(true)}
          className="flex-1 px-2 py-1 text-xs font-medium text-blue-600 hover:bg-blue-100 rounded transition"
        >
          Edit
        </button>
        <button
          onClick={handleDelete}
          disabled={deleting}
          className="flex-1 px-2 py-1 text-xs font-medium text-red-600 hover:bg-red-100 rounded transition disabled:opacity-50"
        >
          {deleting ? 'Deleting...' : 'Delete'}
        </button>
      </div>
    </div>
  )
}
