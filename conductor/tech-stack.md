# AegisShield: Tech Stack

## 🚀 Core Architecture
AegisShield is built as a high-performance, asynchronous Python-based system, leveraging modern frameworks for security, scalability, and real-time responsiveness.

## 🏗️ Core Engine (Backend)
- **FastAPI (Python):** Chosen for its high performance and asynchronous support, ideal for processing threat signals and PAS operations in real-time.
- **Asynchronous Processing:** Utilizing `asyncio` for non-blocking operations, critical for high-concurrency threat detection.

## 🎨 UI & UX (Frontend)
- **Reflex (Pure Python):** Used for a professional, "cool" React-powered SOC experience, allowing for seamless state management between the UI and backend logic.
- **Tailwind CSS v4:** Integrated for the "Cyber-Premium" design system, providing a high-performance styling layer for glassmorphism and neon effects.

## 💾 Persistence & Caching
- **PostgreSQL:** Primary database for storing domain states, user profiles, and persistent Consultant Logs.
- **Redis:** Used for high-speed live telemetry caching and as a message broker for real-time status updates via WebSockets.

## 🤖 AI & ML Engine (Hybrid Architecture)
- **Custom Detection Models:** Specially trained LSTM/GRU neural networks for high-speed network traffic and system log anomaly detection.
- **LLM Integration:** Utilizing GPT-4o, Claude 3.5, or Llama-3 (via Ollama) to power the expert human-readable Consultant Log.
- **RAG (Retrieval-Augmented Generation):** Connecting the LLM to an intelligence knowledge base for grounded security advice.

## 🛡️ Real-Time & Connectivity
- **WebSockets:** For pushing live traffic logs and active shielding alerts to the SOC dashboard.
- **SMTP & Push:** For real-time multi-channel alerts upon critical threat detection or autonomous shielding actions.
