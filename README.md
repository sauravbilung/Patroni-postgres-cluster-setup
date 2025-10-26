# 🐘 PostgreSQL High Availability Cluster with Patroni, ZooKeeper & HAProxy

A fully containerized **PostgreSQL HA cluster** using **Patroni**, **ZooKeeper**, and **HAProxy**, designed for automated failover, leader election, and resilient database connectivity.

---

## ⚙️ Architecture Overview

| Component | Role |
|------------|------|
| **Patroni** | Orchestrates PostgreSQL cluster members, manages replication, leader election, and failover. |
| **ZooKeeper** | Serves as the distributed consensus store (DCS) used by Patroni for coordination. |
| **HAProxy** | Provides a single connection endpoint (`5432`) and routes traffic automatically to the current Patroni leader. |
| **PostgreSQL** | Actual database instances managed by Patroni, running as three nodes (`pg1`, `pg2`, `pg3`). |

---

## 🧩 Components & Configuration

### 1. `docker-compose.yml`
Defines and orchestrates all containers:  
- **ZooKeeper** (coordination)  
- **Three PostgreSQL nodes** (managed by Patroni)  
- **HAProxy** (routing to leader)

#### Exposed Ports
| Component | Port | Description |
|------------|------|-------------|
| `pg1` | 5433 | PostgreSQL (pg1) |
| `pg2` | 5434 | PostgreSQL (pg2) |
| `pg3` | 5435 | PostgreSQL (pg3) |
| `pg1` | 8008 | Patroni REST API |
| `pg2` | 8009 | Patroni REST API |
| `pg3` | 8010 | Patroni REST API |
| `haproxy` | 5432 | Cluster entrypoint (routes to leader) |

> Uses a **tmpfs volume** for `/run/postgresql` to improve socket I/O performance.

---

### 2. Patroni Node Configurations
Each node (`patroni-pg1.yml`, `patroni-pg2.yml`, `patroni-pg3.yml`) contains node-specific settings.

#### Key Parameters
| Setting | Description |
|----------|-------------|
| `restapi.listen` | Patroni REST API listener (8008–8010). |
| `postgresql.listen` | PostgreSQL internal listener (5432). |
| `authentication` | Defines superuser (`postgres`) and replication (`replicator`) credentials. |
| `bootstrap.dcs.ttl` | 30s timeout before failover if the leader becomes unresponsive. |
| `loop_wait` | 5s interval for Patroni’s health loop. |
| `retry_timeout` | 5s retry delay for DCS operations. |
| `maximum_lag_on_failover` | 1MB threshold for replication lag during failover. |
| `use_pg_rewind` | Enables fast recovery after failover. |
| `pg_hba` | Permissive rules for demo/testing; restrict in production. |

---

### 3. `haproxy.cfg`
HAProxy is configured to:
- Forward traffic to the **current Patroni leader** only.
- Automatically detect role changes using Patroni’s REST health check.

---

## 🧠 Running Containers

When the cluster is up, the following containers will run:

```
pg_cluster-pg1-1
pg_cluster-pg2-1
pg_cluster-pg3-1
pg_cluster-haproxy-1
pg_cluster-zookeeper-1 
```

---

## 🧠 Commands

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

### ▶️ ⏹️ ⏸️ Start / Stop / Pause / Unpause a Specific Container
```bash

docker start pg_cluster-pg1-1 
docker stop pg_cluster-pg1-1 
docker pause pg_cluster-pg1-1 
docker unpause pg_cluster-pg1-1
```
These are useful for simulating leader crashes, node freezes, and recovery scenarios.

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
### 🩺 View Health status 

curl http://localhost:8008
curl http://localhost:8009
curl http://localhost:8010
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

## ✅ Example Workflow

```bash
# 1. Start the cluster
docker compose up -d

# 2. Check running containers
docker compose ps

# 3. Simulate leader failure
docker stop pg_cluster-pg1-1

# 4. Observe HAProxy routing and Patroni failover
docker logs -f pg_cluster-haproxy-1

# 5. Restart the stopped node
docker start pg_cluster-pg1-1
```

---

## 📚 References

- [Patroni Documentation](https://patroni.readthedocs.io/)
- [ZooKeeper Docs](https://zookeeper.apache.org/doc/)
- [HAProxy Documentation](https://www.haproxy.org/)
- [PostgreSQL Streaming Replication](https://www.postgresql.org/docs/current/warm-standby.html)

---

**Tags:** PostgreSQL, Patroni, ZooKeeper, HAProxy, Docker, High Availability, Failover
