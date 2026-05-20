# -----------------------------
# Builder Stage
# -----------------------------
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY app/package*.json ./

# Install dependencies
RUN npm install

# Copy application source
COPY app/ .

# -----------------------------
# Production Stage
# -----------------------------
FROM node:20-alpine

WORKDIR /app

# Create non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Copy app from builder
COPY --from=builder /app /app

# Set ownership
RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 3000

CMD ["npm", "start"]