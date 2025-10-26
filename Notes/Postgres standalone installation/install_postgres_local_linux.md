
# 🐘 Install PostgreSQL Locally via Terminal (Linux - Ubuntu)

## ✅ Step 1: Update Package Index

```bash
sudo apt update
```

---

## ✅ Step 2: Install PostgreSQL and Client Tools

```bash
sudo apt install postgresql postgresql-client -y
```

This installs:
- PostgreSQL server
- `psql` client (PostgreSQL CLI)
- Creates the default `postgres` user and database

---

## ✅ Step 3: Check and Start the PostgreSQL Service

```bash
sudo systemctl status postgresql
```

If not running, start it:

```bash
sudo systemctl start postgresql
```

Enable PostgreSQL to start on boot:

```bash
sudo systemctl enable postgresql
```

---

## ✅ Step 4: Access PostgreSQL Shell

Switch to the `postgres` user and open `psql`:

```bash
sudo -i -u postgres
psql
```

Exit the `psql` prompt:

```sql
\q
```

Exit from `postgres` shell:

```bash
exit
```

---

## ✅ Step 5: Create a New User and Database (Optional)

Inside the `psql` shell:

```sql
CREATE USER myuser WITH PASSWORD 'mypassword';
CREATE DATABASE mydb OWNER myuser;
GRANT ALL PRIVILEGES ON DATABASE mydb TO myuser;
```

---

## 🧪 Verify the Installation

Log in with the new user:

```bash
psql -U myuser -d mydb
```

Or default:

```bash
psql -U postgres
```

---

🎉 You now have PostgreSQL running locally on your machine!
