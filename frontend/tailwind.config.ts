import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        base: "#f8fafc",
        panel: "#ffffff",
        text: "#0f172a",
        muted: "#64748b",
        line: "#e2e8f0",
        brand: "#1d4ed8",
      },
    },
  },
  plugins: [],
};

export default config;
