# Use the official Node.js image as a base
FROM node:16-alpine

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json to install dependencies
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Expose the port your app runs on (adjust to your app's port)
EXPOSE 3000

# Command to run your application
CMD ["npm", "start"]
