import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{ts,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        profit: "#10b981",
        loss: "#f43f5e",
      },
    },
  },
  plugins: [],
};

export default config;
