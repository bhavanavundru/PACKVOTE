/** @type {import('tailwindcss').Config} */
const config = {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        primary: "#00B4D8",
        darkbg: "#0B0C10",
        lightbg: "#1F2833",
      },
    },
  },
  plugins: [],
};

export default config;