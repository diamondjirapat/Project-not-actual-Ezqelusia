import subprocess

print("Starting Docker Compose...")
subprocess.run(["docker", "compose", "up", "-d"], check=True)

print("Running ingest.py...")
subprocess.run(["python", "ingest.py"])

print("Running transform.py...")
subprocess.run(["python", "transform.py"])

print("Running publish.py...")
subprocess.run(["python", "publish.py"])

print("All done......")
