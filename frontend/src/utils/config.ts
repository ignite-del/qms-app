// Environment variables
const API_HOST = process.env.REACT_APP_API_URL || 'localhost';
const API_PORT = process.env.REACT_APP_API_PORT || '8000';
const IS_PROD = process.env.NODE_ENV === 'production';

// Construct the API URL
export const API_URL = IS_PROD
  ? `https://${API_HOST}`  // In production, Render handles HTTPS
  : `http://${API_HOST}:${API_PORT}`; // In development, use host:port

export const config = {
  apiUrl: API_URL,
  isProd: IS_PROD,
}; 