# Base image
FROM node:20-alpine

# Install SVGO
RUN npm install -g svgo

# Execute the SVGO command when the container starts
ENTRYPOINT ["svgo", "-f", "/data_input", "-o", "/data_output"]