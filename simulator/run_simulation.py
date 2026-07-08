import time
import random
import httpx
from simulator.config import INGESTION_URL, DEVICE_ID, DEVICE_TOKEN, INTERVAL_SECONDS


def generate_simulated_readings(step: int):
    """
    Generates a realistic smart composting sensor transition:
    - Steps 1-5  : Active decomposing (Hot temperature 58°C - 50°C)
    - Steps 6-10 : Cooling phase (Decreasing 45°C - 30°C)
    - Steps 11-15: Stable ready state (Ambient room temperature ~26°C, moisture 50%, age > 14 days)
    """
    # Base variables
    version = "0.1.0"
    schema = 1
    
    if step <= 5:
        # Active Composting
        status = "active_composting"
        raw_temp = 58.0 - (step * 1.5) + random.uniform(-0.5, 0.5)
        raw_humidity = 65.0 + random.uniform(-1.0, 1.0)
        cycle_age = 1.0 + (step * 0.5)
    elif step <= 10:
        # Cooling Stabilizing
        status = "cooling_stabilizing"
        raw_temp = 48.0 - ((step - 5) * 3.5) + random.uniform(-0.5, 0.5)
        raw_humidity = 55.0 + random.uniform(-1.0, 1.0)
        cycle_age = 4.0 + ((step - 5) * 1.0)
    else:
        # Ready Candidate
        status = "ready_candidate"
        raw_temp = 26.5 + random.uniform(-0.3, 0.3)
        raw_humidity = 48.0 + random.uniform(-0.5, 0.5)
        cycle_age = 14.0 + ((step - 10) * 0.2)

    # Clean filtering math simulation
    filtered_temp = raw_temp + random.uniform(-0.1, 0.1)
    trend_avg_temp = filtered_temp - 0.2
    
    payload = {
        "device_id": DEVICE_ID,
        "firmware_version": version,
        "schema_version": schema,
        "timestamp": int(time.time()),
        "readings": {
            "temperature_c": {
                "raw": round(raw_temp, 2),
                "filtered": round(filtered_temp, 2),
                "trend_avg": round(trend_avg_temp, 2),
                "quality": "good",
                "error": False
            },
            "humidity_pct": {
                "raw": round(raw_humidity, 2),
                "quality": "good",
                "error": False
            }
        },
        "status": status,
        "quality_flag": "good",
        "cycle_age_days": round(cycle_age, 2),
        "battery_pct": 98 - step
    }
    return payload


def main():
    print("=" * 60)
    print("      EcoBuck IoT Device Simulation Client Started")
    print("=" * 60)
    print(f"Target Ingestion URL : {INGESTION_URL}")
    print(f"Device Identifier    : {DEVICE_ID}")
    print("=" * 60)

    headers = {
        "X-Device-Token": DEVICE_TOKEN,
        "Content-Type": "application/json"
    }

    # Simulate 15 upload iterations
    for step in range(1, 16):
        print(f"\n[Simulation Step {step}/15]")
        
        # 1. Generate payload
        payload = generate_simulated_readings(step)
        print(f"State   : {payload['status']}")
        print(f"Temp    : {payload['readings']['temperature_c']['filtered']}°C")
        print(f"Moisture: {payload['readings']['humidity_pct']['raw']}%")
        print(f"Age Days: {payload['cycle_age_days']}")
        
        # 2. Post request
        try:
            r = httpx.post(INGESTION_URL, json=payload, headers=headers)
            print(f"Response Status Code : {r.status_code}")
            if r.status_code == 202:
                print("Result               : Telemetry successfully accepted by backend.")
            else:
                print(f"Error Result         : {r.json()}")
        except Exception as e:
            print(f"Connection Error     : Failed to post to backend. {e}")

        # Sleep
        time.sleep(INTERVAL_SECONDS)

    print("\n" + "=" * 60)
    print("      Simulation Complete. All steps executed successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()
