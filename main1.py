import json
import time
import os
import sys
from datetime import datetime, timezone
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

    def get_latest_event(self) -> Dict:
        with open(self.file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
            if lines:
                try:
                    return json.loads(lines[-1])
                except json.JSONDecodeError:
                    return {}
        return {}

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

# --- Digital Neocortex: Main Integration ---
class DigitalNeocortex:
    def __init__(self, file_path: str):
        self.sensors = SensorStream(file_path)
        self.memory = EpisodicMemory()
        self.jini_client = JiniClient()
        self.previous_sensor_data = ""
        self.running = True

    def process_event(self, event: Dict):
        self.memory.add_event(event)
        print(f"Processing event: {event}")

    def generate_query(self) -> str:
        latest_event = self.sensors.get_latest_event()
        if not latest_event:
            return "No new events detected."
        return json.dumps(latest_event)

    def respond(self, user_query: str) -> str:
        memory_context = self.memory.retrieve_memory(user_query)
        real_time_data = json.dumps(self.sensors.get_latest_event()) if self.sensors.get_latest_event() else ""
        if real_time_data:
            self.previous_sensor_data = real_time_data
        response = self.jini_client.query(user_query, memory_context, real_time_data)
        return response

    def run(self):
        while self.running:
            time.sleep(3)
            latest_event = self.sensors.get_latest_event()
            if latest_event:
                self.process_event(latest_event)
                generated_query = self.generate_query()
                if generated_query != "No new events detected.":
                    print(f"Generated Query: {generated_query}")
                    response = self.respond(generated_query)
                    print(f"LLM Response: {response}")

# --- Main Execution ---
if __name__ == "__main__":
    file_path = "simulated_dataM.jsonl"
    brain = DigitalNeocortex(file_path)
    brain.run()
