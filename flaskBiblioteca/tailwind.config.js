/** @type {import('tailwindcss').Config} */
module.exports = {
  mode: "JIT",
  content: [
    "./app/frontend/templates/**/*html"
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

