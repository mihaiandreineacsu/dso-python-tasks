# Use an official Alpine as a parent image
FROM alpine:latest

# Update the package list and install nmap
RUN apk update && apk add --no-cache nmap

# Set the entrypoint to run nmap --help and then start sh
ENTRYPOINT ["sh", "-c", "nmap --help && exec sh"]
