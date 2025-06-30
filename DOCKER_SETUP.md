# Docker Compose Multi-Service Setup

This repository contains multiple microservices that can be orchestrated together using Docker Compose. There are several approaches to combine all the services:

## Services Overview

- **auth** (port 8001) - Authentication service with PostgreSQL (port 5431)
- **catalogo** (port 8002) - Catalog service with PostgreSQL (port 5432) 
- **habilidades** (port 8003) - Skills service with PostgreSQL (port 5433)
- **plantios** (port 8004) - Planting service with PostgreSQL (port 5434)
- **tutoriais_tarefas** (port 8005) - Tutorials/Tasks service with PostgreSQL (port 5435)

All services are connected via a shared network called `shared-network`.

## Approach 1: Include (Recommended)

The main `docker-compose.yml` file uses the modern `include` feature to combine all service compose files:

```bash
# Start all services
docker-compose up -d

# Stop all services  
docker-compose down

# View logs
docker-compose logs

# View status
docker-compose ps
```

## Approach 2: Multiple -f Flags

Use the provided script to run with multiple compose files:

```bash
# Start all services
./run-all-services.sh up -d

# Stop all services
./run-all-services.sh down

# View logs
./run-all-services.sh logs

# View status
./run-all-services.sh ps
```

## Approach 3: Extends (Alternative)

Use the `docker-compose.extends.yml` file which demonstrates the `extends` approach:

```bash
# Start all services using extends approach
docker-compose -f docker-compose.extends.yml up -d

# Stop all services
docker-compose -f docker-compose.extends.yml down
```

**Note**: The extends approach has some limitations with volume name conflicts since each service defines a volume named "db_data". In production, you'd want to rename these to be unique.

## Network Setup

All services communicate through a shared Docker network called `shared-network`. This allows services to reference each other by container name (e.g., `auth:8000`, `catalogo:8000`, etc.).

## Service Dependencies

The services have the following dependency relationships:
- **catalogo**, **habilidades**, **plantios**, and **tutoriais_tarefas** all depend on the **auth** service
- Each service depends on its own PostgreSQL database

## Port Mapping

| Service           | External Port | Internal Port | Database Port |
| ----------------- | ------------- | ------------- | ------------- |
| auth              | 8001          | 8000          | 5431          |
| catalogo          | 8002          | 8000          | 5432          |
| habilidades       | 8003          | 8000          | 5433          |
| plantios          | 8004          | 8000          | 5434          |
| tutoriais_tarefas | 8005          | 8000          | 5435          |

## Getting Started

1. **Create the shared network** (if using the script approach):
   ```bash
   docker network create shared-network
   ```

2. **Start all services** using your preferred approach:
   ```bash
   # Option 1: Include approach (recommended)
   docker-compose up -d
   
   # Option 2: Multiple files script
   ./run-all-services.sh up -d
   
   # Option 3: Extends approach  
   docker-compose -f docker-compose.extends.yml up -d
   ```

3. **Verify services are running**:
   ```bash
   docker-compose ps
   ```

4. **Access services**:
   - Auth: http://localhost:8001
   - Catalogo: http://localhost:8002
   - Habilidades: http://localhost:8003
   - Plantios: http://localhost:8004
   - Tutoriais Tarefas: http://localhost:8005

## Troubleshooting

- If you encounter network issues, ensure the `shared-network` exists:
  ```bash
  docker network ls | grep shared-network
  ```

- If services can't connect to each other, verify they're on the same network:
  ```bash
  docker network inspect shared-network
  ```

- Check service logs for debugging:
  ```bash
  docker-compose logs [service-name]
  ```
