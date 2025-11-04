module.exports = {
  content: ["./index.html", "./src//*.{ts,tsx}"],
  theme: { extend: {} },
  plugins: []
};

frontend/postcss.config.cjs

module.exports = { plugins: { tailwindcss: {}, autoprefixer: {} } };

