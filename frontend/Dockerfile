# build
FROM node:20-alpine AS build
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci
COPY . .
RUN npm run build

# serve
FROM nginx:1.27-alpine
COPY --from=build /app/dist/ /usr/share/nginx/html/

# Copy custom Nginx SPA config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Keep config.js overridable via ConfigMap:
RUN echo 'if [ ! -f /usr/share/nginx/html/config.js ]; then echo "window._CONFIG_={API_URL:\"\"}" > /usr/share/nginx/html/config.js; fi' > /docker-entrypoint.d/99-config.sh && chmod +x /docker-entrypoint.d/99-config.sh
EXPOSE 80


