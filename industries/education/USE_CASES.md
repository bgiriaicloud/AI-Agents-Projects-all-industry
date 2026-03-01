# 📋 Education AI Agent Use Cases

## 1. Interactive AI Tutor (The "Socratic" Agent)
**Industry:** Education / EdTech
**Description:** Instead of giving answers, this agent asks probing questions to lead students to the solution, mimicking a human tutor.

### 🛠️ Tools Used
- **Brain**: Claude 3.5 Sonnet (for high-quality pedagogical reasoning).
- **Memory**: Long-term student progress tracking via PostgreSQL.
- **Search**: Wikipedia / Khan Academy API for verified facts.

---

## 2. Automated Grading Assistant
**Industry:** Education / Administration
**Description:** Grades open-ended essays and provides detailed, constructive feedback based on a rubric, highlighting specific areas for improvement.

### 🛠️ Tools Used
- **Logic**: LangGraph (for multi-pass evaluation).
- **Brain**: Gemini 2.0 Pro (for handling long-form text analysis).

---

## 3. Curriculum Generator Agent
**Industry:** Education / Instructional Design
**Description:** Generates a 12-week course outline, lesson plans, and quiz questions based on a single topic prompt.

### 🛠️ Tools Used
- **Framework**: CrewAI (Agent 1: Researcher, Agent 2: Designer, Agent 3: Reviewer).
