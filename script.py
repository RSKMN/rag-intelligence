import json
import time
import random
from datetime import datetime

def generate_temperature():
    # Return temperature as string instead of a numeric value
    return f"{round(random.uniform(20, 40), 2)}"  # Celsius as string

def generate_humidity():
    # Return humidity as string
    return f"{round(random.uniform(30, 90), 2)}"  # Percentage as string

def generate_visual():
    scenes = ["a busy street", "a quiet park", "a vibrant market", "a serene lake", "an abstract painting"]
    return random.choice(scenes)

def generate_auditory():
    sounds = ["birds chirping", "cars honking", "distant conversation", "soft piano music", "thunder rumbling"]
    return random.choice(sounds)

def generate_olfactory():
    smells = ["fresh coffee", "baked bread", "wet earth", "aromatic spices", "burnt rubber"]
    return random.choice(smells)

def generate_gustatory():
    tastes = ["sweet", "salty", "bitter", "umami", "sour"]
    return random.choice(tastes)

def generate_tactile():
    textures = ["smooth", "rough", "cold", "warm", "sticky"]
    return random.choice(textures)

def generate_emotion():
    emotions = ["happy", "sad", "excited", "anxious", "calm"]
    return random.choice(emotions)

# Mapping sensor types to their corresponding reading generators
sensor_functions = {
    "temperature": generate_temperature,
    "humidity": generate_humidity,
    "visual": generate_visual,
    "auditory": generate_auditory,
    "olfactory": generate_olfactory,
    "gustatory": generate_gustatory,
    "tactile": generate_tactile,
    "emotion": generate_emotion,
}

def simulate_complex_data(file_path):
    sensor_types = list(sensor_functions.keys())
    locations = ["home", "office", "park", "street", "restaurant"]
    
    while True:
        sensor = random.choice(sensor_types)
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "sensor": sensor,
            # Wrap the reading value in str() to ensure it's always a string.
            "reading": str(sensor_functions[sensor]()),
            "intensity": round(random.uniform(0, 1), 2),
            "metadata": {
                "location": random.choice(locations),
                "device_id": f"device_{random.randint(1, 100)}",
                "battery_level": round(random.uniform(10, 100), 2)
            }
        }
        with open(file_path, "a") as f:
            f.write(json.dumps(event) + "\n")
        print(f"Simulated event: {event}")
        time.sleep(random.uniform(4, 6))

if __name__ == "__main__":
    simulate_complex_data("simulated_data.jsonl")
