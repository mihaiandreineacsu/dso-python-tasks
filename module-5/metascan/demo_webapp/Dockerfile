# Use the official Nginx image from the Docker Hub
FROM nginx:alpine

WORKDIR /var/www/html/example

COPY . /usr/share/nginx/html/

# Expose port 80 to the outside world
EXPOSE 80

# Start Nginx when the container is run
CMD ["nginx", "-g", "daemon off;"]
