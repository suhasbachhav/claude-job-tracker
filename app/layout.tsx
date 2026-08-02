import type { Metadata } from 'next'
import { AuthProvider } from '@/components/auth-context'
import './globals.css'

export const metadata: Metadata = {
  title: 'Job Application Tracker',
  description: 'Track your job applications with ease',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  )
}
