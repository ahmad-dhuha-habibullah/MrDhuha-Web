/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{html,njk,md,js}",
    "./.eleventy.js"
  ],
  theme: {
    extend: {
      colors: {
        primary: '#E05A11',
        secondary: '#1A3636',
        surface: '#F8FAFC',
        border: '#E2E8F0',
        text: '#1E293B',
        textLight: '#64748B'
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        serif: ['Merriweather', 'serif'],
      }
    }
  },
  plugins: [],
}
