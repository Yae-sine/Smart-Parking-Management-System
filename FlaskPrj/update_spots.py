import json
import random
import time

def generate_status():
    return {
        "spot1": random.choice(["available", "occupied"]),
        "spot2": random.choice(["available", "occupied"]),
        "spot3": random.choice(["available", "occupied"]),
        "spot4": random.choice(["available", "occupied"]),
    }

while True:
    status = generate_status()
    with open("status.json", "w") as f:
        json.dump(status, f)
    print("Updated:", status)
    time.sleep(2)