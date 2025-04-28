/** @type {import('tailwindcss').Config} */
module.exports = {
  mode: "JIT",
  content: [
    "./app/frontend/templates/**/*.html",
    "./app/frontend/static/js/*.js"
  ],
  theme: {
    
    fontFamily:{
      sans: ["Helvética", "sans-serif"],
      serif: ["Roboto","Times", "serif"],
    },
    
    extend: {

    },
  },
  plugins: [],
}

