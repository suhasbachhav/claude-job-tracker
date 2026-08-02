import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        status: {
          applied: '#3b82f6',    // blue
          interview: '#f59e0b',   // amber
          offer: '#10b981',       // emerald
          rejected: '#ef4444',    // red
        },
      },
    },
  },
  plugins: [],
}
export default config
