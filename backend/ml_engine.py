import re
import numpy as np
import os
import pickle
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "scam_detector.h5")
TOKENIZER_PATH = os.path.join(BASE_DIR, "tokenizer.pickle")

# Load Model if exists
model = None
tokenizer = None

def load_components():
    global model, tokenizer
    try:
        if os.path.exists(MODEL_PATH):
            model = tf.keras.models.load_model(MODEL_PATH)
            print("Loaded custom DL model")
        if os.path.exists(TOKENIZER_PATH):
            with open(TOKENIZER_PATH, 'rb') as handle:
                tokenizer = pickle.load(handle)
    except Exception as e:
        print(f"Failed to load components: {e}")

load_components()

# Rule Based Variables
SUSPICIOUS_PHRASES = [
    "registration fee", "earn money fast", "pay an advance",
    "deposit required", "work from home guaranteed", "no experience required immediate hire",
    "send your bank details", "buy office equipment", "deposit a check",
    "crypto payments", "insurance deposit", "whatsapp only", "telegram manager",
    "background verification fee", "training material cost", 
    "security deposit", "laptop fee", "refundable amount", "hr manager telegram",
    "congratulations you are selected", "direct interview", "no experience required",
    "part time job", "earn extra income", "flexible hours", "work from anywhere",
    "payment for training", "processing fee", "official duty", "commission based",
    "telegram group", "dm me on telegram", "message me on whatsapp"
]
URGENCY_PHRASES = [
    "act fast", "limited spots left", "urgent requirement",
    "apply immediately", "offer expires soon", "hurry", "immediate hire",
    "24 hours", "join immediately"
]
SUSPICIOUS_DOMAINS_PATTERN = r"(?i)\b(?:bit\.ly|tinyurl\.com|freejob|joboffer-urgent|earn-online|t\.me)\b"

def detect_rules(text):
    text_lower = text.lower()
    detected_suspicious = []
    detected_urgency = []
    
    for phrase in SUSPICIOUS_PHRASES:
        if phrase in text_lower:
            detected_suspicious.append(phrase)
    
    for phrase in URGENCY_PHRASES:
        if phrase in text_lower:
            detected_urgency.append(phrase)
            
    suspicious_links = re.findall(SUSPICIOUS_DOMAINS_PATTERN, text_lower)
    
    return {
        "suspicious": detected_suspicious,
        "urgency": detected_urgency,
        "links": list(set(suspicious_links))
    }

def get_action_guidance(risk_level):
    if risk_level == "Safe":
        return [
            "Verify the company website and LinkedIn presence.",
            "Always apply directly through official corporate portals.",
            "Ensure communication comes from a verified company email domain."
        ]
    elif risk_level == "Suspicious":
        return [
            "WARNING: Do not share personal or financial information.",
            "Verify the exact identity of the recruiter via official company contacts.",
            "Check for company reviews on Glassdoor and the authenticity of the contact domain."
        ]
    elif risk_level == "High Risk (Scam)":
        return [
            "CRITICAL DANGER: Do NOT pay any money or click any unknown links in this message.",
            "Block and report the sender immediately.",
            "If you shared info, report this to your local cybercrime portal or bank immediately."
        ]
    return []

# Known Brands for Safety Verification
LEGIT_BRANDS = ["infosys", "google", "microsoft", "amazon", "apple", "ibm", "tata", "accenture", "deloitte"]

def analyze_risk(text: str):
    text_lower = text.lower()
    rule_results = detect_rules(text)
    
    risk_score = 0
    confidence = 0.0
    detected_triggers = list(set(rule_results["suspicious"] + rule_results["urgency"] + rule_results["links"]))
    reasoning_parts = []

    # Brand Recognition
    found_brands = [b for b in LEGIT_BRANDS if b in text_lower]
    if found_brands and risk_score == 0:
        reasoning_parts.append(f"Recognized legitimate brand: {found_brands[0].capitalize()}.")
    
    # Rule based evaluation
    if len(rule_results["suspicious"]) > 0:
        risk_score += 2
        reasoning_parts.append(f"CRITICAL: Found scam keywords: {', '.join(rule_results['suspicious'][:3])}.")
        
    if len(rule_results["links"]) > 0: 
        risk_score += 2
        reasoning_parts.append(f"Detected suspicious shortlinks or unofficial domains: {', '.join(rule_results['links'])}.")
        
    if len(rule_results["urgency"]) > 0: 
        risk_score += 1
        reasoning_parts.append(f"Detected high pressure tactics ('{rule_results['urgency'][0]}').")
        
    # Model evaluation
    dl_confidence = 0.0
    dl_prediction = 0 
    
    if model is not None and tokenizer is not None:
        try:
            seq = tokenizer.texts_to_sequences([text])
            pad_seq = pad_sequences(seq, maxlen=50, padding='post', truncating='post')
            preds = model.predict(pad_seq, verbose=0)[0]
            dl_prediction = np.argmax(preds)
            dl_confidence = float(np.max(preds))
            
            if dl_prediction == 2:
                risk_score += 3
            elif dl_prediction == 1:
                risk_score += 1
        except Exception as e:
            print("Model prediction error:", e)
    
    # Calculate Unified Confidence
    # Combine Rule certainty (0.8+) and DL certainty
    if risk_score >= 3:
        classification = "High Risk (Scam)"
        confidence = max(dl_confidence, 0.85 if len(rule_results["suspicious"]) > 0 else 0.8)
    elif risk_score >= 1:
        classification = "Suspicious"
        confidence = max(dl_confidence, 0.65)
    else:
        classification = "Safe"
        # If no model, provide a more dynamic 'Safe' score rather than fixed 88
        if not model:
            # Base safety on lack of triggers
            confidence = max(0.9, 1.0 - (len(detected_triggers) * 0.1))
        else:
            confidence = dl_confidence
    
    final_percentage = round(confidence * 100, 2)
    
    # Finalize Reasoning based on UNIFIED score
    if dl_prediction == 2:
        reasoning_parts.append(f"AI Model and Rule Engine both confirm high-risk patterns (Scam probability: {final_percentage}%).")
    elif dl_prediction == 1:
        reasoning_parts.append(f"AI Model detected anomalies with {final_percentage}% confidence.")

    return {
        "risk_level": classification,
        "confidence_score": final_percentage,
        "highlighted_phrases": detected_triggers,
        "reasoning": " ".join(reasoning_parts),
        "actions": get_action_guidance(classification)
    }
