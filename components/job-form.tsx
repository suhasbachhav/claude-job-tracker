'use client'

import { Job, JobStatus } from '@/types'
import { useState } from 'react'

interface JobFormProps {
  initialJob?: Job
  onSubmit: (job: Partial<Job>) => void | Promise<void>
  onCancel: () => void
}

export function JobForm({ initialJob, onSubmit, onCancel }: JobFormProps) {
  const [company, setCompany] = useState(initialJob?.company || '')
  const [position, setPosition] = useState(initialJob?.position || '')
  const [status, setStatus] = useState<JobStatus>(initialJob?.status || 'applied')
  const [appliedDate, setAppliedDate] = useState(
    initialJob?.applied_date || new Date().toISOString().split('T')[0]
  )
  const [notes, setNotes] = useState(initialJob?.notes || '')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    try {
      await onSubmit({
        company,
        position,
        status,
        applied_date: appliedDate,
        notes: notes || null,
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="card p-6 max-w-md">
      <h2 className="text-lg font-bold mb-4">
        {initialJob ? 'Edit Job' : 'Add New Job'}
      </h2>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Company</label>
          <input
            type="text"
            required
            value={company}
            onChange={(e) => setCompany(e.target.value)}
            className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="e.g., Google, Meta"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Position</label>
          <input
            type="text"
            required
            value={position}
            onChange={(e) => setPosition(e.target.value)}
            className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="e.g., Software Engineer"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Status</label>
          <select
            value={status}
            onChange={(e) => setStatus(e.target.value as JobStatus)}
            className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="applied">Applied</option>
            <option value="interview">Interview</option>
            <option value="offer">Offer</option>
            <option value="rejected">Rejected</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Applied Date</label>
          <input
            type="date"
            required
            value={appliedDate}
            onChange={(e) => setAppliedDate(e.target.value)}
            className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Notes</label>
          <textarea
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            rows={3}
            className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Add any notes about this application..."
          />
        </div>

        <div className="flex gap-2">
          <button
            type="submit"
            disabled={loading}
            className="btn-primary flex-1"
          >
            {loading ? 'Saving...' : initialJob ? 'Update' : 'Create'}
          </button>
          <button
            type="button"
            onClick={onCancel}
            className="btn-secondary flex-1"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  )
}
