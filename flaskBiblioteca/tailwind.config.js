/** @type {import('tailwindcss').Config} */
module.exports = {
  mode: "JIT",
  content: [
    "./app/frontend/templates/**/*html"
  ],
  theme: {
    
    fontFamily:{
      sans: ['Roboto', 'Helvética', "sans-"],
    },
    extend: {
      gridTemplateColumns:{
        'struct': '2fr 5fr 5fr 1fr;',
        '16': 'repeat(16, minmax(0, 1fr))',
      },

    },
  },
  plugins: [],
}

