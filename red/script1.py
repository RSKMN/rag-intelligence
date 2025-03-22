import json
import time
import random
import os
from datetime import datetime, timezone

# Initialize serial number counter
serial_no_counter = 0

def generate_next_event(previous_event=None):
    global serial_no_counter
    serial_no_counter += 1
    
    locations = ["home", "office", "park", "street", "restaurant"]
    
    if previous_event:
        last_location = previous_event["location"]
    else:
        last_location = random.choice(locations)
    
    location_transitions = {
        "home": ["street", "office"],
        "office": ["home", "restaurant"],
        "park": ["street", "home"],
        "street": ["park", "restaurant", "office"],
        "restaurant": ["home", "street"]
    }
    
    next_location = random.choice(location_transitions.get(last_location, locations))
    
    story = generate_story(previous_event, next_location)
    
    event = {
        "event_id": serial_no_counter,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "location": next_location,
        "temperature": previous_event["temperature"] + random.uniform(-0.5, 0.5) if previous_event else round(random.uniform(20, 40), 2),
        "humidity": previous_event["humidity"] + random.uniform(-2, 2) if previous_event else round(random.uniform(30, 90), 2),
        "visual": story["visual"],
        "auditory": story["auditory"],
        "olfactory": story["olfactory"],
        "gustatory": story["gustatory"],
        "tactile": story["tactile"],
        "emotion": story["emotion"],
        "metadata": {
            "device_id": f"device_{random.randint(1, 100)}",
            "battery_level": max(0, previous_event["metadata"]["battery_level"] - random.uniform(0.5, 2.0)) if previous_event else round(random.uniform(10, 100), 2)
        }
    }
    
    return event, story["text"]

def generate_story(previous_event, current_location):
    if previous_event:
        prev_location = previous_event["location"]
        transition = f"From {prev_location}, you now find yourself in {current_location}. "
    else:
        transition = f"You begin your journey at {current_location}. "
    
    scenarios = {
        "home": {
            "text": "You settle into your couch, sipping on a warm cup of coffee. The sun gently filters through the windows, casting a golden hue across the room. A book rests on your lap as the aroma of freshly baked cookies drifts in from the kitchen.",
            "visual": "sunlit living room",
            "auditory": "soft rustling of pages",
            "olfactory": "freshly baked cookies",
            "gustatory": "sweet",
            "tactile": "warm and cozy",
            "emotion": "content"
        },
        "office": {
            "text": "The keyboard clatters as you type, with the distant murmur of colleagues in the background. A whiteboard filled with brainstorming ideas stands beside you. The faint scent of coffee lingers in the air, and the chill of the air conditioner keeps the room crisp.",
            "visual": "office workstation",
            "auditory": "keyboard clatter",
            "olfactory": "coffee aroma",
            "gustatory": "bitter",
            "tactile": "cool air",
            "emotion": "focused"
        },
        "park": {
            "text": "Children laugh in the distance as you stroll along the walking path. The trees sway gently, their leaves whispering in the breeze. The scent of fresh grass mingles with the crisp morning air, and a jogger passes by, nodding in greeting.",
            "visual": "green park with walking paths",
            "auditory": "children laughing, birds chirping",
            "olfactory": "fresh grass and earth",
            "gustatory": "neutral",
            "tactile": "breeze on skin",
            "emotion": "peaceful"
        },
        "street": {
            "text": "The city is alive with energy. Street vendors call out their daily specials while pedestrians navigate the bustling sidewalks. The scent of roasted chestnuts and freshly baked bread fills the air as a car horn blares in the distance.",
            "visual": "busy urban street",
            "auditory": "vendors shouting, cars honking",
            "olfactory": "roasted chestnuts, fresh bread",
            "gustatory": "savory",
            "tactile": "crowded but lively",
            "emotion": "energetic"
        },
        "restaurant": {
            "text": "A candle flickers at your table as you glance at the menu. The quiet hum of conversation and soft clinking of glasses create a warm atmosphere. The rich scent of spices and freshly cooked dishes fills the air, making your mouth water in anticipation.",
            "visual": "cozy restaurant with dim lighting",
            "auditory": "soft clinking of glasses, distant chatter",
            "olfactory": "aromatic spices and grilled food",
            "gustatory": "umami and rich flavors",
            "tactile": "smooth tablecloth, warm air",
            "emotion": "relaxed"
        }
    }
    
    scenario = scenarios.get(current_location, {"text": "An uneventful moment passes.", "visual": "unknown", "auditory": "silent", "olfactory": "neutral", "gustatory": "neutral", "tactile": "neutral", "emotion": "neutral"})
    
    with open("scenarios/interaction_story.txt", "a") as f:
        f.write(transition + scenario["text"] + "\n")
    
    return scenario

def simulate_complex_data(file_path):
    previous_event = None
    
    while True:
        event, story = generate_next_event(previous_event)
        previous_event = event  
        
        with open(file_path, "a") as f:
            f.write(json.dumps(event) + "\n")
        
        print(f"Simulated event: {event}")
        print(f"Story: {story}")
        
        time.sleep(random.uniform(3, 5))

if __name__ == "__main__":
    simulate_complex_data("simulated_dataM.jsonl")
