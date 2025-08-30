import pathlib
import random
import time

out = pathlib.Path("data/raw/auth.log")
out.parent.mkdir(parents=True, exist_ok=True)

users = ["root", "admin", "mythik", "guest"]
ips = ["203.0.113.12", "198.51.100.77", "192.0.2.55", "127.0.0.1"]
actions = [
    "Failed password for {user} from {ip} port 4242 ssh2",
    "Accepted password for {user} from {ip} port 2222 ssh2",
    "Invalid user {user} from {ip}",
    "Did not receive identification string from {ip}",
]

lines = []
now = time.time()
for i in range(50):
    u = random.choice(users)
    ip = random.choice(ips)
    act = random.choice(actions).format(user=u, ip=ip)
    ts = time.strftime("%b %d %H:%M:%S", time.gmtime(now - (50 - i) * 3))
    lines.append(f"{ts} vps01 sshd[{1000+i}]: {act}")

out.write_text("\n".join(lines))
print(f"Wrote sample log with {len(lines)} lines to {out}")
