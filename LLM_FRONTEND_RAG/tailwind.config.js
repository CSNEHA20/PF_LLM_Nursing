/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                primary: "#b30f3d",
                secondary: "#0F172A",
                background: "#f0dae0",
                surface: "#FFFFFF",
                accent: "#ff4e42",
                danger: "#EF4444",
                text_primary: "#111827",
                text_secondary: "#6B7280"
            },
            fontFamily: {
                sans: ['Inter', 'sans-serif'],
            },
        },
    },
    plugins: [],
}
