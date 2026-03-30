AI Behavioral Interview Tutor
Live Demo

Project Overview
The AI Behavioral Interview Tutor is an interactive application designed to help job seekers practice for behavioral interviews. It uses a Large Language Model (LLM) to analyze user prompts and generate structured responses using industry-standard frameworks (STAR and SOAR).

Key Features
Intelligent Framework Selection: automatically detects if a question is best answered using STAR (Standard) or SOAR (Strategic/Failure-based) frameworks.
Real-time Streaming: Answers are streamed token-by-token for a responsive user experience.

Context Awareness: Maintains chat history to provide context-aware feedback.
Dockerized Deployment: Fully containerized using Docker for consistent deployment on the university cluster.

Tech Stack
Frontend: Streamlit (Python-based UI)
Backend Logic: Python 3.12
AI Model: Llama 3.1 (hosted via Ollama)
Containerization: Docker & Docker Compose
CI/CD: GitLab CI
Data Persistence (Database)
The application utilizes an embedded SQLite database (interview_history.db).

Why SQLite? We chose a lightweight, file-based database to maintain session history locally within the container.
Function: It records user prompts and AI responses, allowing the "History" feature to function without the overhead of external database dependencies like Postgres.


Project Structure
interview-ai/
├── streamlit_app/
│   ├── app.py             # Main application logic
│   ├── Dockerfile         # Container build instructions
│   └── requirements.txt   # Python dependencies
├── .gitlab-ci.yml         # CI/CD pipeline configuration
├── docker-compose.yml     # Service orchestration
└── configure.sh           # Environment setup script
