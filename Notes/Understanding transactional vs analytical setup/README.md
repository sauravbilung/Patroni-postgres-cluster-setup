
# ⚙️ Transactional vs Analytical PostgreSQL Setup with HAProxy

Design, configure, and test **transactional (OLTP)** vs **analytical (OLAP)** workloads in a **PostgreSQL High Availability Cluster** managed by **Patroni** and load balanced by **HAProxy**.

---

## 🧩 1. Overview of the Setup

| Port | Purpose | Description |
|------|----------|--------------|
| **5432** | Transactional (Leader Only) | Strictly consistent read + write traffic |
| **5433** | Analytical (Replicas Only) | Scalable read-only queries (reporting, dashboards) |
| **5434** | Hybrid (Any Node) | High availability reads from any available node |

---

## 🧠 2. Transactional Workloads (OLTP)

- Frequent small reads and writes  
- Requires strong consistency and ACID compliance  
- Example: Orders, payments, inventory updates  

HAProxy routes traffic to whichever node reports `"role": "primary"` from its Patroni `/health` API.  
Replicas are ignored for transactional traffic to ensure all reads see the latest committed data.

---

## 📊 3. Analytical Workloads (OLAP)

- Read-heavy, aggregate queries  
- Can tolerate slight replication lag (milliseconds–seconds)  
- Example: BI dashboards, reporting systems, analytics APIs  

HAProxy routes traffic to nodes reporting `"role": "replica"`.  
This spreads query load and improves overall cluster performance.

---

## 🔁 4. Hybrid Reads (Port 5434)

Hybrid reads provide **availability over consistency** — if the leader is down, reads continue from replicas.

| Port | Behavior | Use Case |
|------|-----------|----------|
| 5432 | Leader only | Strict OLTP |
| 5433 | Replicas only | OLAP / Reporting |
| 5434 | Leader + Replicas | High Availability Reads |

---

## 🚀 5. Real-World Use Cases

| Scenario | Recommended Port | Reason |
|-----------|------------------|--------|
| Online payments / transactions | 5432 | Strong consistency required |
| Inventory sync | 5432 | Writes and updates must be serialized |
| BI dashboard | 5433 | Reads from replicas reduce leader load |
| Grafana metrics | 5434 | Continue even during failover |
| Analytics microservice | 5433 / 5434 | Tolerates eventual consistency |

---

## 🧪 6. Testing the Setup

```bash
# Start the entire Patroni + HAProxy PostgreSQL cluster
docker compose up -d

# (Optional) Install PostgreSQL client on host
sudo apt update && sudo apt install postgresql-client -y

# Check the current leader
docker exec -it pg_cluster-pg1-1 patronictl list

# Inspect Docker network to view internal container IPs
docker network ls
docker network inspect pg_cluster_default
```

### 🔎 Test Routing Across HAProxy Ports

```bash
# Transactional (Leader only)
psql -h localhost -p 5432 -U postgres -c "SELECT inet_server_addr(), pg_is_in_recovery();"

# Analytical (Replicas only)
psql -h localhost -p 5433 -U postgres -c "SELECT inet_server_addr(), pg_is_in_recovery();"

# Hybrid (Any available node)
psql -h localhost -p 5434 -U postgres -c "SELECT inet_server_addr(), pg_is_in_recovery();"
```

**Interpretation:**
- `pg_is_in_recovery() = false` → Query routed to **Leader**
- `pg_is_in_recovery() = true` → Query routed to **Replica**

### ⚠️ Simulate Failover

```bash
# Stop the current leader (example: pg1)
docker stop pg_cluster-pg1-1
```

Patroni will automatically elect a **new leader**.  
Re-run the same `psql` queries to confirm traffic is re-routed by HAProxy.

---

## ✅ Summary

| Type | Port | Routes To | Consistency | Use Case |
|------|------|------------|--------------|-----------|
| Transactional | 5432 | Leader | Strong | OLTP apps |
| Analytical | 5433 | Replicas | Eventual | Reports |
| Hybrid | 5434 | Any | Mixed | HA Reads |

---
