/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
      "./modules/**/templates/*.html",
      "./templates/**/*.html", /* El ** busca en subcarpetas también */
      "./static/**/*.js"
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}