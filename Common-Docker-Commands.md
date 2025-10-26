## 🧠 Common Docker Commands

Below are frequently used commands to manage, inspect, and test the Patroni PostgreSQL HA cluster.

---

### 🏗️ Start the Cluster
```bash
docker compose up -d
```
Starts ZooKeeper, all Patroni PostgreSQL nodes (`pg1`, `pg2`, `pg3`), and HAProxy in detached mode.

---

### 🧹 Stop and Remove All Containers
```bash
docker compose down
```
Stops and removes all containers, networks, and temporary volumes created by `docker-compose.yml`.

---

### 🔁 Restart a Service
```bash
docker compose restart haproxy
docker compose restart pg1
```
Restarts an individual container (useful for testing failover or config reload).

---

### 🔍 Check Container Status
```bash
docker compose ps
```
Displays the running state, ports, and container names for all services.

---

### 📜 View Logs
```bash
docker logs pg_cluster-pg1-1
docker logs pg_cluster-pg2-1
docker logs pg_cluster-pg3-1
docker logs pg_cluster-haproxy-1
```
Shows runtime logs for each service. Add `-f` to follow logs live (e.g., `docker logs -f pg_cluster-haproxy-1`).

---

### 🧩 Access a Running Container
```bash
docker exec -it pg_cluster-pg1-1 /bin/bash
```
Opens an interactive shell inside a container for debugging or manual `psql` access.

---

### 🧱 Rebuild Containers After Config Changes
```bash
docker compose up -d --build
```
Rebuilds and restarts containers if configuration or image versions change.

---

### 🧹 Clean Up Unused Resources
```bash
docker system prune -a
```
Removes all stopped containers, unused networks, and dangling images.  
> ⚠️ Use with caution — this deletes **all** unused Docker artifacts on your system.

---

### 🔄 Restart the Entire Cluster
```bash
docker compose restart
```
Gracefully restarts all running containers in the HA cluster.

---

### 🧭 View Network Details
```bash
docker network ls
docker inspect pg_cluster-pg1-1
```
Displays Docker network information and connection details between containers.

---

### ⚡ Quick Summary
| Action | Command |
|--------|----------|
| Start cluster | `docker compose up -d` |
| Stop cluster | `docker compose down` |
| Restart single service | `docker compose restart <service>` |
| View logs | `docker logs <container>` |
| Shell into container | `docker exec -it <container> /bin/bash` |
| Check status | `docker compose ps` |
| Rebuild containers | `docker compose up -d --build` |
| Restart all | `docker compose restart` |

---

These commands cover 99% of your workflow needs for running and testing the Patroni + HAProxy cluster.
