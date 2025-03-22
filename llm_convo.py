import json
import time
import streamlit as st
from datetime import datetime
from typing import List, Dict
from jiniai import JiniAI as clientAI

# --- JiniAI Client Wrapper ---
class JiniClient:
    def __init__(self, model: str = "llama-3.3-70b-versatile"):
        self.client = clientAI
        self.model = model

    def query(self, prompt: str) -> str:
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=False,
            stop=None,
        )
        return completion.choices[0].message.content.strip()

# --- SensorStream for Continuous Data Retrieval ---
class SensorStream:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def get_latest_event(self) -> Dict:
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                lines = file.readlines()
                if lines:
                    return json.loads(lines[-1])
        except json.JSONDecodeError:
            return {}
        except FileNotFoundError:
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
        self.llm1 = JiniClient()
        self.llm2 = JiniClient()
        self.opinionAI = JiniClient()
        self.previous_sensor_data = ""

    def process_event(self, event: Dict):
        self.memory.add_event(event)

    def generate_query(self) -> str:
        latest_event = self.sensors.get_latest_event()
        if not latest_event:
            return "No new events detected."
        return json.dumps(latest_event, indent=4)

    def respond(self, user_query: str) -> Dict:
        memory_context = self.memory.retrieve_memory(user_query)
        real_time_data = json.dumps(self.sensors.get_latest_event(), indent=4) if self.sensors.get_latest_event() else ""
        
        llm1_prompt = (
            f"Llm1: Hey, just checking out the latest sensor data. Looks like we're experiencing: \n"
            f"{real_time_data}\n\nWhat do you think?"
        )
        llm1_response = self.llm1.query(llm1_prompt)
        
        llm2_prompt = (
            f"Llm2: Huh, reminds me of past experiences: {memory_context}\n"
            f"Llm1: {llm1_response}\n"
            f"Llm2: But do you think there's anything unusual here?"
        )
        llm2_response = self.llm2.query(llm2_prompt)
        
        opinionAI_prompt = (
            f"OpinionAI: Analyzing conversation between Llm1 and Llm2. Identifying gaps between sensory data interpretation and generated story context.\n"
            f"Sensor Data: {real_time_data}\n"
            f"Llm1: {llm1_response}\n"
            f"Llm2: {llm2_response}\n"
            f"Technical Analysis: "
        )
        opinionAI_response = self.opinionAI.query(opinionAI_prompt)
        
        return {"Llm1": llm1_response, "Llm2": llm2_response, "OpinionAI": opinionAI_response, "SensorData": real_time_data}

# --- Streamlit UI ---
def main():
    st.title("AI-Driven Sensor Analysis & Conversation")
    file_path = "simulated_dataM.jsonl"
    brain = DigitalNeocortex(file_path)
    
    if "conversation" not in st.session_state:
        st.session_state.conversation = []
    
    while True:
        time.sleep(3)
        latest_event = brain.sensors.get_latest_event()
        if latest_event:
            brain.process_event(latest_event)
            generated_query = brain.generate_query()
            if generated_query != "No new events detected.":
                responses = brain.respond(generated_query)
                st.session_state.conversation.append((generated_query, responses))
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write("**Llm1 (Casual Interpretation):**")
                    st.write(responses["Llm1"])
                with col2:
                    st.write("**Llm2 (Contextual Reflection):**")
                    st.write(responses["Llm2"])
                with col3:
                    st.write("**OpinionAI (Technical Analysis):**")
                    st.write(responses["OpinionAI"])
                
                st.write("---")
                st.subheader("Live Sensor Data")
                st.json(responses["SensorData"])

if __name__ == "__main__":
    main()
