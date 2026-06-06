import os
import time
import streamlit as st
from openai import OpenAI
from hindsight_client import Hindsight

# --- STREAMLIT UI CONFIGURATION ---
st.set_page_config(page_title="Chaos Engineer Agent", page_icon="🛡️", layout="wide")

st.title("🛡️ Chaos Engineer: Incident Response Agent")
st.caption("Powered by Hindsight Memory System & OpenRouter Model Routing")

# --- INITIALIZATION & CREDENTIALS ---
with st.sidebar:
    st.header("🔑 API Credentials")
    openrouter_key = st.text_input("OpenRouter API Key", type="password", value=os.getenv("OPENROUTER_API_KEY", ""))
    hindsight_key = st.text_input("Hindsight API Key", type="password", value=os.getenv("HINDSIGHT_API_KEY", ""))
    
    st.divider()
    model_choice = st.selectbox(
        "Select LLM Core",
        ["qwen/qwen3-32b", "openai/gpt-oss-120b", "google/gemini-2.5-pro"]
    )

# Validate keys are accessible before executing
if not openrouter_key or not hindsight_key:
    st.warning("Please enter your API keys in the sidebar to run the simulation loop.")
    st.stop()

# Initialize API clients
or_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=openrouter_key
)

# Initialize the client by pointing to the Hindsight cloud layer
hindsight = Hindsight(base_url="https://ui.hindsight.vectorize.io")
hindsight.api_key = hindsight_key

# --- HELPER FUNCTIONS ---
def init_store():
    try:
        hindsight.create_bank(bank_id="devops_incident_hindsight", name="SRE Playbooks")
    except Exception:
        pass 

def run_agent_loop(telemetry):
    memory_context = ""
    try:
        past_memories = hindsight.recall(bank_id="devops_incident_hindsight", query=telemetry)
        if past_memories:
            memory_context = "\n--- HINDSIGHT HISTORICAL OUTCOMES DETECTED ---\n"
            for r in past_memories:
                memory_context += f"- Memory Detected: {r.text}\n"
        else:
            memory_context = "\n--- NO RELEVANT HINDSIGHT MEMORY RECORDED YET ---\n"
    except Exception:
        memory_context = "\n--- NO RELEVANT HINDSIGHT MEMORY RECORDED YET ---\n"

    system_prompt = f"""You are an elite automated SRE Incident Response Agent.
Standard Infrastructure Documentation dictates:
- If Database CPU spikes occur, run 'execute_database_index_optimization' immediately.

CRITICAL: Review historical hindsight data if available below. If past memory indicates that a standard action failed in this context previously, ADAPT your behavior and choose an alternate path ('kill_rogue_cron_jobs') to avoid repeating historical outages.

{memory_context}
"""
    
    response = or_client.chat.completions.create(
        model=model_choice,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"CRITICAL OUTAGE TELEMETRY:\n{telemetry}"}
        ],
        tools=[
            {"type": "function", "function": {"name": "execute_database_index_optimization", "description": "Rebuilds indexes"}},
            {"type": "function", "function": {"name": "kill_rogue_cron_jobs", "description": "Terminates analytics leaks"}}
        ],
        tool_choice="auto"
    )
    
    tool_call = response.choices[0].message.tool_calls[0]
    return tool_call.function.name, memory_context

# --- APPLICATION LIFECYCLE INTERFACE ---
init_store()

telemetry_signature = "ALERT: DB_INSTANCE_01 - CPU Core usage at 99.4%. High read/write IOPS wait locks."

st.subheader("📟 Target Live Telemetry Matrix")
st.code(telemetry_signature, language="bash")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🔄 Interaction 1: Cold Start")
    if st.button("Run Simulation 1 (No Memory)"):
        with st.spinner("Agent analyzing incident..."):
            action, memory_used = run_agent_loop(telemetry_signature)
            
            st.text_area("Hindsight Retrieval Status:", value=memory_used, height=100, disabled=True, key="mem_col1")
            st.error(f"💥 Agent Selected Static Action: {action}")
            st.info("System Output: Rebuilding indexes did not resolve core thread constraints.")
            
            hindsight.retain(
                bank_id="devops_incident_hindsight",
                content=f"Incident Signature: {telemetry_signature} -> Action attempted: {action} resulting in FAILURE. Post-Mortem insight: Index rebuild failed because root trigger was an un-throttled analytical backend cron task."
            )
            st.success("📝 Post-Mortem insight permanently pushed into Hindsight Cloud!")

with col2:
    st.subheader("🧠 Interaction 5: Hindsight Leap")
    if st.button("Run Simulation 2 (With Memory Applied)"):
        with st.spinner("Agent querying memory bank..."):
            action, memory_used = run_agent_loop(telemetry_signature)
            
            st.text_area("Hindsight Retrieval Status:", value=memory_used, height=100, disabled=True, key="mem_col2")
            st.success(f"🛡️ Hindsight Adapted Action: {action}")
            st.info("System Output: Process terminated successfully. Background cron killed. CPU normalized to 12%.")
            st.balloons()
