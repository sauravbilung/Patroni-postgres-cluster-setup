#!/usr/bin/env python3
import subprocess

NODES = ["pg_cluster-pg1-1", "pg_cluster-pg2-1", "pg_cluster-pg3-1"]

for node in NODES:
try:
result = subprocess.run(
["docker", "exec", node, "patronictl", "-c", "/etc/patroni.yml", "list"],
stdout=subprocess.PIPE,
stderr=subprocess.DEVNULL,
text=True,
check=True
)
print(result.stdout)
break
except subprocess.CalledProcessError:
continue