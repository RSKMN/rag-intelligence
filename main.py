import json
import time
import os
from datetime import datetime
from typing import List, Dict
from jiniai import JiniAI as clientAI
import random

# --- JinIAI Client Wrapper ---
class JiniClient:
    def __init__(self, model: str = "llama-3.3-70b-versatile"):
        self.client = clientAI
        self.model = model

    def query(self, user_query: str, context: str, real_time_data: str) -> str:
        prompt = context + "\n" + real_time_data + "\n" + user_query
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )
        response = ""
        for chunk in completion:
            response_chunk = chunk.choices[0].delta.content or ""
            response += response_chunk
        return response

# --- SensorStream for Continuous Data Retrieval ---
class SensorStream:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._file = open(file_path, "r", encoding="utf-8")
        self._file.seek(0, os.SEEK_END)

    def get_latest_events(self) -> List[Dict]:
        events = []
        while True:
            line = self._file.readline()
            if not line:
                break
            try:
                event = json.loads(line)
                events.append(event)
            except json.JSONDecodeError:
                continue
        return events

# --- Episodic Memory Module ---
class EpisodicMemory:
    def __init__(self):
        self.memory_store: List[Dict] = []

    def add_event(self, event: Dict):
        self.memory_store.append(event)
        if len(self.memory_store) > 1000:
            self.memory_store.pop(0)

    def retrieve_memory(self, query: str) -> str:
        relevant_memories = [json.dumps(m) for m in self.memory_store if query.lower() in json.dumps(m).lower()]
        return "\n".join(relevant_memories[-5:])

# --- Predictive Processing Module ---
class Predictor:
    def predict(self, event: Dict) -> str:
        if event["sensor"] == "visual" and "dark" in event["reading"]:
            return "It might rain soon. Take an umbrella."
        elif event["sensor"] == "emotion" and event["reading"] == "anxious":
            return "You seem anxious. Try some breathing exercises."
        return "No strong prediction."

# --- Emotion-Aware Decision Making Module ---
class EmotionAwareDecision:
    def __init__(self):
        self.emotion_bias = {"happy": "risk-taking", "sad": "cautious", "anxious": "conservative"}

    def advise(self, user_query: str, emotion: str) -> str:
        bias = self.emotion_bias.get(emotion, "neutral")
        return f"Based on your {emotion} mood, I suggest a {bias} approach to your decision."

# --- Digital Neocortex: Main Integration ---
class DigitalNeocortex:
    def __init__(self, file_path: str):
        self.sensors = SensorStream(file_path)
        self.memory = EpisodicMemory()
        self.predictor = Predictor()
        self.decision_maker = EmotionAwareDecision()
        self.jini_client = JiniClient()
        self.previous_sensor_data = ""

    def process_event(self, event: Dict):
        self.memory.add_event(event)
        prediction = self.predictor.predict(event)
        print(f"Prediction: {prediction}")

    def generate_query(self) -> str:
        sensor_data = self.sensors.get_latest_events()
        if not sensor_data and not self.previous_sensor_data:
            return "What is the current situation?"
        
        if sensor_data:
            latest_event = sensor_data[-1]
        elif self.previous_sensor_data:
            try:
                parsed_data = json.loads(self.previous_sensor_data)
                latest_event = parsed_data[-1] if isinstance(parsed_data, list) else parsed_data
            except json.JSONDecodeError:
                latest_event = {}
        else:
            latest_event = {}
        
        return f"How does {latest_event.get('sensor', 'unknown')} data impact decision-making?"

    def respond(self, user_query: str) -> str:
        memory_context = self.memory.retrieve_memory(user_query)
        real_time_data = "\n".join([json.dumps(event) for event in self.sensors.get_latest_events()])
        if real_time_data:
            self.previous_sensor_data = real_time_data
        response = self.jini_client.query(user_query, memory_context, real_time_data)
        return response

    def run(self):
        while True:
            events = self.sensors.get_latest_events()
            for event in events:
                print(f"Processing event: {event}")
                self.process_event(event)
            
            generated_query = self.generate_query()
            print(f"Generated Query: {generated_query}")
            response_1 = self.respond(generated_query+"\n\n You are a human, and if any sensory data is given, then you are in a simulated environment. If no sensory data is given, react like any human would. dont mention anything about receiving any data or not, just respond to whatever is asked as usual.")
            print("First LLM Response:", response_1)
            
            time.sleep(random.uniform(3, 4))
            
            updated_events = self.sensors.get_latest_events()
            real_time_update = "\n".join([json.dumps(event) for event in updated_events])
            if real_time_update:
                self.previous_sensor_data = real_time_update
            response_2 = self.jini_client.query(response_1, self.previous_sensor_data+"\n\n You are a human, and if any sensory data is given, then you are in a simulated environment. If no sensory data is given, react like any human would.dont mention anything about receiving any data or not, just respond to whatever is asked as usual.","")
            print("Second LLM Response:", response_2)
            
            time.sleep(random.uniform(3, 4))

# --- Main Execution ---
if __name__ == "__main__":
    file_path = "simulated_data.jsonl"
    brain = DigitalNeocortex(file_path)
    brain.run()