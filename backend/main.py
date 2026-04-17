import os
import shutil
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import PyPDF2
from PIL import Image
import pytesseract
import io
import io
from ml_engine import analyze_risk, load_components, MODEL_PATH, TOKENIZER_PATH

# --- Tesseract Path Configuration for Windows ---
if os.name == 'nt':
    # Common installation paths for Tesseract-OCR on Windows
    common_paths = [
        r'C:\Program Files\Tesseract-OCR\tesseract.exe',
        r'C:\Users\\' + os.getlogin() + r'\AppData\Local\Tesseract-OCR\tesseract.exe'
    ]
    for path in common_paths:
        if os.path.exists(path):
            pytesseract.pytesseract.tesseract_cmd = path
            print(f"Auto-detected Tesseract at: {path}")
            break

app = FastAPI(title="ScamSentinel AI - Risk Analysis API")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- PDF Extraction ---
def extract_text_from_pdf(file_bytes):
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"PDF extraction failed: {str(e)}")

# --- Image OCR ---
def extract_text_from_image(file_bytes):
    try:
        image = Image.open(io.BytesIO(file_bytes))
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Image OCR failed. Ensure Tesseract is installed: {str(e)}")

@app.post("/analyze")
async def analyze(
    text: str = Form(None),
    file: UploadFile = File(None)
):
    print(f"Received analyze request: text_len={len(text) if text else 0}, file={file.filename if file else 'None'}")
    content = ""
    
    if text:
        content = text
    elif file:
        file_bytes = await file.read()
        filename = file.filename.lower()
        
        if filename.endswith(".pdf"):
            content = extract_text_from_pdf(file_bytes)
        elif filename.endswith((".png", ".jpg", ".jpeg", ".webp")):
            content = extract_text_from_image(file_bytes)
        else:
            # Try to read as raw text if unknown extension
            try:
                content = file_bytes.decode("utf-8")
            except:
                raise HTTPException(status_code=400, detail="Unsupported file format.")
    
    if not content.strip():
        raise HTTPException(status_code=400, detail="No readable text content found.")
    
    result = analyze_risk(content)
    result["extracted_text"] = content[:1000] # Return snippet for verification
    return result

@app.post("/upload-model")
async def upload_model(file: UploadFile = File(...)):
    if not file.filename.endswith(".h5") and not file.filename.endswith(".pt"):
        raise HTTPException(status_code=400, detail="Only .h5 or .pt models allowed.")
    
    with open(MODEL_PATH, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    load_components() # Reload ml_engine components
    return {"message": "Model uploaded and loaded successfully."}

@app.post("/upload-tokenizer")
async def upload_tokenizer(file: UploadFile = File(...)):
    if not file.filename.endswith(".pickle"):
        raise HTTPException(status_code=400, detail="Only .pickle tokenizer files allowed.")
    
    with open(TOKENIZER_PATH, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    load_components() # Reload ml_engine components
    return {"message": "Tokenizer uploaded and loaded successfully."}

@app.get("/")
def health_check():
    return {"status": "ScamSentinel AI Backend is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
