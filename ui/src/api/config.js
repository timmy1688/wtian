/**
 * Backend base URL, resolved at build time.
 * - Production build: falls back to the public domain below.
 * - `npm run serve`: `.env.development` sets "/api", proxied by vue.config.js to a local backend.
 * Override per environment with VUE_APP_API_BASE_URL in `.env.*.local`.
 */
const PRODUCTION_API_BASE_URL = 'https://wtian.cloud/api';

export const API_BASE_URL = process.env.VUE_APP_API_BASE_URL || PRODUCTION_API_BASE_URL;
