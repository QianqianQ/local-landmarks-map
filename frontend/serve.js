const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const path = require('path');

const app = express();
const PORT = 4200;

// Proxy API requests to Flask backend
app.use('/api', createProxyMiddleware({
  target: 'http://localhost:5000',
  changeOrigin: true,
  logLevel: 'debug'
}));

// Serve Angular static files
const distPath = path.join(__dirname, 'dist', 'landmarks-map');
app.use(express.static(distPath));

// Fallback to index.html for Angular routing
app.get('*', (req, res) => {
  res.sendFile(path.join(distPath, 'index.html'));
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Angular development server running on http://0.0.0.0:${PORT}`);
});