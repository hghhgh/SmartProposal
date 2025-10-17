# 🧠 SmartProposal — Intelligent Proposal Evaluation System

**SmartProposal** is an AI-powered application designed to automatically analyze, correct, and evaluate academic or research proposal documents in `.odt` format.  
It assists reviewers and researchers by identifying structural, grammatical, and content-related issues, generating comments, and offering an approval decision.

---

## 🚀 Overview

SmartProposal receives a `.odt` file (e.g., a research proposal), analyzes its contents for:
- ✅ Grammar and spelling accuracy  
- ✅ Structural and formatting compliance  
- ✅ Completeness of answers to required sections  
- ✅ Domain relevance and technical adequacy  
- ✅ Presence of tables, figures, and layout consistency  

It then produces:
- A **detailed annotated report** with suggestions for improvement  
- Or an **automated approval decision** with justification

---

## 🧱 Architecture

The system is modular and designed for collaborative AI development.

```
smartproposal/
├── app/
│   ├── api/               # FastAPI endpoints (upload, analysis, report)
│   ├── core/              # Configuration, logging, utilities
│   ├── nlp/               # AI/NLP modules (grammar, QA, scoring)
│   ├── odt_parser/        # File parser and structure extractor
│   ├── report/            # Report and comment generator
│   └── main.py            # Application entry point
├── tests/                 # Unit and integration tests
├── requirements.txt       # Dependencies
└── README.md              # This file
```

---

## 🧩 Main Modules

| Module | Description |
|---------|--------------|
| **ODT Parser** | Extracts text, headings, and tables from `.odt` files. |
| **NLP Preprocessing** | Tokenization, normalization, and embedding generation. |
| **Grammar & Spell Checker** | Corrects and comments on grammar/spelling using AI models. |
| **Completeness & QA Checker** | Detects unanswered questions and incomplete sections. |
| **Content Quality & Relevance** | Evaluates proposal depth, clarity, and technical adequacy. |
| **Formatting & Layout Checker** | Ensures proper formatting, fonts, margins, and layout. |
| **Report Generator** | Creates annotated `.odt` and JSON reports with comments. |
| **Backend API & Logic** | FastAPI backend for processing and data handling. |
| **Frontend (React)** | User-friendly web interface for uploads and feedback. |
| **DevOps & Documentation** | CI/CD, Dockerization, deployment, and wiki maintenance. |

---

## 🧠 Technology Stack

- **Python 3.10+**
- **FastAPI** for backend APIs
- **React + TailwindCSS** for frontend
- **Transformers (BERT, Sentence-BERT)** for NLP
- **odfpy** for `.odt` parsing
- **LanguageTool** for grammar correction
- **Docker & GitHub Actions** for deployment and CI/CD

---

## ⚙️ Installation

### Prerequisites
- Python ≥ 3.10  
- Docker (optional for containerized deployment)  
- Git

### Clone & Setup
```bash
git clone https://github.com/hghhgh/SmartProposal.git
cd smartproposal
pip install -r requirements.txt
```

### Run Locally
```bash
uvicorn app.main:app --reload
```
Visit [http://localhost:8000/docs](http://localhost:8000/docs) for the interactive API.

---

## 🧪 Testing

```bash
pytest --maxfail=1 --disable-warnings -q
```

All modules include dedicated unit and integration tests.

---

## 🧭 Development Workflow

1. **Fork** the repository  
2. **Create a feature branch**: `git checkout -b feature/your-feature`  
3. **Commit** your changes  
4. **Push** to your fork  
5. **Open a Pull Request**  

Each PR triggers automated CI checks (linting, tests, build).

---

## 🗂️ Project Management

This project follows milestone-based agile development:

| Milestone | Focus |
|------------|--------|
| **M1** | Setup & Design |
| **M2** | Data & Model Research |
| **M3** | Core Development |
| **M4** | Integration & Testing |
| **M5** | Model Fine-Tuning |
| **M6** | Deployment & Documentation |

Each module includes about 40 issues (400+ total), managed via GitHub Projects.

---

## 🌐 Frontend Preview

The React frontend allows users to:
- Upload `.odt` proposals
- Track analysis progress
- View grammar and content feedback
- Download annotated reports

---

## 🧰 DevOps

- **Dockerized services** for easy deployment  
- **GitHub Actions CI/CD** for automatic testing and build  
- **Environment variables** managed via `.env`

### Run with Docker
```bash
docker-compose up --build
```

---

## 📚 Documentation

- `docs/` directory and project Wiki contain detailed API and model documentation.  
- `CONTRIBUTING.md` explains coding standards and PR review process.

---

## 🧑‍💻 Contributors

This project is collaboratively developed by **M.Sc. Artificial Intelligence students**, each responsible for a submodule and 20+ tasks.

---

## 📜 License

MIT License © 2025 SmartProposal-AI

---

## 💡 Future Enhancements

- Add multilingual support (Persian, English, Arabic)
- Integrate plagiarism detection
- Offer grading rubric customization
- Cloud-based collaboration platform for reviewers

---

**SmartProposal** — *Empowering academic research through intelligent automation.*
