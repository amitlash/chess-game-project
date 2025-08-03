FROM node:18-alpine

WORKDIR /app


#COPY frontend/package*.json ./
COPY frontend/ .
RUN npm install 

#COPY frontend/ .

# For production
RUN npm run build || (echo "BUILD FAILED" && exit 1)
RUN npm install -g serve
CMD ["serve", "-s", "dist", "-l", "3000"]

# For development (optional)
# CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3000"]
