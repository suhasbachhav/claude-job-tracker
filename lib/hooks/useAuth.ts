'use client'

import { useAuthContext } from '@/components/auth-context'

export function useAuth() {
  return useAuthContext()
}
