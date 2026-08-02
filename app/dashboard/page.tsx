import { ProtectedRoute } from '@/components/protected-route'
import { Header } from '@/components/header'
import { DashboardContent } from '@/components/dashboard-content'

export default function DashboardPage() {
  return (
    <ProtectedRoute>
      <Header />
      <DashboardContent />
    </ProtectedRoute>
  )
}
