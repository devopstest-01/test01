FROM nginx
FROM ubuntu:18.04

EXPOSE 80

# Copy nginx configuration file
COPY nginx.conf /etc/nginx/nginx.conf
