/** @type {import('tailwindcss').Config} */
const withMT = require("@material-tailwind/html/utils/withMT");
module.exports = withMT({
  content: ["./app/templates/**/*.html"],
  theme: {
    extend: {
      animation: {
        "border-move": "border-move 3s linear infinite",
      },
      keyframes: {
        "border-move": {
          "0%": { borderColor: "rgb(255, 99, 71)" }, // Tomato
          "33%": { borderColor: "rgb(60, 179, 113)" }, // MediumSeaGreen
          "66%": { borderColor: "rgb(30, 144, 255)" }, // DodgerBlue
          "100%": { borderColor: "rgb(255, 99, 71)" }, // Back to Tomato
        },
      },
    },
  },
  plugins: [require("daisyui"), require("flowbite/plugin")],
});
