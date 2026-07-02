FROM node:lts-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

# Required runtime environment variables. Provide them when running the container (eg. with
#   docker run -e NEXT_PUBLIC_API_URL='http://api:3001' -e NODE_ENV=production <image>) or via docker-compose env_file.
# Note: For Next.js, variables prefixed with `NEXT_PUBLIC_` are exposed to the browser. If you build the app for production
# they should be provided at build-time or injected into the running server depending on your deployment strategy.
# - NEXT_PUBLIC_API_URL: URL for the API (e.g. "http://api:3001")
# - NODE_ENV: 'development' or 'production'
# - PORT: port to run the app/server
ENV NEXT_PUBLIC_API_URL=
ENV NODE_ENV=development
ENV PORT=3000

EXPOSE ${PORT}

CMD ["npm", "run", "dev"]