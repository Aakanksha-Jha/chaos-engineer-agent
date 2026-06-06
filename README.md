# 🛡️ Chaos Engineer Agent (Powered by Hindsight Memory)

An AI SRE agent that mitigates infrastructure incidents by actively evaluating its history of successful and failed actions.

🔗 **Live Demo Link:** [Insert your streamlit app URL here]

## 🧠 Why Memory is the Main Character
Standard AI agents pull static documentation context which remains stagnant regardless of deployment real-world outcomes. 

By integrating a **Hindsight Memory Layer**, our engine captures episodic execution results (`SUCCESS`/`FAILURE`) within a dynamic post-mortem feedback loop. When a failure repeats, the agent automatically adapts to run a secondary execution protocol rather than repeating a costly past mistake.

## 🚀 Technical Architecture
* **Memory Core:** Hindsight Cloud (Episodic Vector Storage)
* **LLM Engine:** OpenRouter (`qwen/qwen3-32b` / `openai/gpt-oss-120b`)
* **Frontend:** Streamlit Dashboard

## 🛠️ Local Setup & Execution
If you want to run this agent locally:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/chaos-engineer-agent.git](https://github.com/your-username/chaos-engineer-agent.git)
   cd chaos-engineer-agent