# 🛡️ ScamSentinel AI
### Advanced Job Scam & Fraudulent Internship Detection with Hybrid AI

**Built by [Mancy Reddy](https://github.com/mancyreddy)**  
*CSE (AI/ML) Undergraduate · Building real-world AI systems*

---

ScamSentinel AI is a high-performance system designed to protect job seekers from predatory employment scams. By combining **Deep Learning (BiLSTM)** with a comprehensive **Rule-Based Engine**, the platform analyzes job descriptions, offer letters (PDF), and screenshots (OCR) to provide real-time risk assessments.

🚀 **"Building AI that works in the real world — not just in notebooks."**

---

## 🚀 Features
- **🔍 Multi-Input Analysis**: Analyze raw text, uploaded screenshots (Tesseract OCR), or official offer letters (PDF).
- **🧠 Hybrid AI Core**: 
  - **Deep Learning**: BiLSTM architecture for sequential pattern recognition in text.
  - **Rule-Engine**: Heuristic analysis for registration fees, suspicious links, and urgency tactics.
- **🚥 Unified Risk Scoring**: Categorizes results into **Safe**, **Suspicious**, or **High Risk (Scam)** with a unified confidence percentage.
- **📋 Actionable Guidance**: Provides specific security steps (e.g., "Block sender", "Verify email domain") based on the detected risk level.
- **📈 Advanced Model Updates**: Integrated UI for uploading custom trained `.h5` models and `.pickle` tokenizers directly.

---

## 🛠️ Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Frontend** | React + Vite | Clean, glassmorphic UI built for speed and responsiveness. |
| **Backend** | Python (FastAPI) | High-performance API handling inference, OCR, and PDF parsing. |
| **Deep Learning** | TensorFlow / Keras | BiLSTM model trained for multi-class scam classification. |
| **OCR Utility** | Tesseract | Extracts high-accuracy text from images and screenshots. |
| **PDF Engine** | PyPDF2 | Parses digital offer letters for metadata and content analysis. |

---

## 💻 How to Run Locally

### 1. Prerequisites
- **Python 3.8+**
- **Node.js 18+**
- **Tesseract OCR**: [Download here](https://github.com/UB-Mannheim/tesseract/wiki) (Add to System PATH).

### 2. Start the Backend
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate  # On Windows
pip install -r requirements.txt
python main.py
```
*The server will start at `http://127.0.0.1:8000`*

### 3. Start the Frontend
```bash
# From the root directory
npm install
npm run dev
```
*Visit `http://localhost:5173` to start analyzing.*

---

## 📊 AI Model & Dataset
The underlying model uses a 3-class classification approach:
- **Class 0 (Safe)**: Official portals, clear corporate language, and verified domains.
- **Class 1 (Suspicious)**: Vague roles, urgent replies required, or unofficial contact methods.
- **Class 2 (High Risk)**: Requests for money, security deposits, or registration fees.

*Custom models can be trained using the included Jupyter Notebook in `/colab_training`.*

---

## 🌐 Deployment & Hosting
- **Frontend**: Recommended for Vercel or Netlify.
- **Backend**: Best deployed as a Docker container on Render, Railway, or Oracle Cloud (OCI) to handle the Tesseract/TensorFlow dependencies.

---

## 👤 Author
**Mancy Reddy**  
[GitHub](https://github.com/mancyreddy) | [LinkedIn](https://linkedin.com/in/mancyreddy) | [Portfolio](https://mancyreddy.me)

*"Building AI that works in the real world."*
