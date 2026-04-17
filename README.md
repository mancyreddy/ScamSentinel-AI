# 🛡️ ScamSentinel AI

An advanced, full-stack application for detecting job and internship scams using a hybrid approach of Deep Learning (BiLSTM) and Rule-Based AI analysis.

## 🚀 Features
- **Multi-Input Support**: Analyze plain text, images (using Tesseract OCR), or PDF offer letters.
- **Hybrid AI Engine**: Combines rule-based detection for known scam patterns with Deep Learning classification.
- **Risk Classification**: Categorizes input as **Safe**, **Suspicious**, or **High Risk (Scam)**.
- **Actionable Guidance**: Provides specific next steps based on the risk level.

---

## 🏗️ Folder Structure
- `/backend`: FastAPI Python server (Analysis engine, OCR, PDF parsing)
- `/src`: React Vite Frontend
- `/colab_training`: Jupyter Notebook for training LSTM/GRU models

---

## 🛠️ Setup Instructions

### 1. Backend (Python 3.8+)
1. `cd backend`
2. `pip install -r requirements.txt`
3. **Important**: Install Tesseract OCR on your system.
   - Windows: [Tesseract Installer](https://github.com/UB-Mannheim/tesseract/wiki)
   - Add Tesseract to your System PATH.
4. Run the server: `python main.py` or `uvicorn main:app --reload`

### 2. Frontend (Node.js)
1. `npm install`
2. `npm run dev`

### 3. Training a Custom Model
1. Open `colab_training/AI_Risk_Analyzer_Training.ipynb` in Google Colab.
2. Run all cells to train.
3. Download `scam_detector_lstm.h5` and `tokenizer.pickle`.
4. Upload them via the "Deep Learning" section in the web app UI to enable advanced classification.

---

## 📝 Dataset Guide
The sample dataset in the notebook uses 3 classes:
- `0`: Safe (Official portals, regular corporate language)
- `1`: Suspicious (Vague requests, urgent but not explicitly asking for money)
- `2`: High Risk (Requests for money, registration fees, suspicious links, earn fast money)

---

## ⚠️ Constraints & Pre-requisites
- **OCR**: Requires `tesseract` binary installed on the host machine.
- **Models**: The default backend uses rule-based analysis if no model is uploaded. Upload the files generated from Colab to activate full DL capabilities.
