# Use an official Node.js image as the base
FROM node:18-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json to the container
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application files into the container
COPY . .

# Expose the port the app will run on
EXPOSE 3000

# Command to run the app in development mode
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3000"]
