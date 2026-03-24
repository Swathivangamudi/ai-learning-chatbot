import streamlit as st
import speech_recognition as sr
from groq import Groq
import os
from PIL import Image
import pytesseract
import fitz  # PyMuPDF
import docx
import streamlit as st
from groq import Groq

# === Setup ===
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# === Speech Recognition ===
def recognize_speech():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            st.info("🎤 Listening... Please speak now...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
            text = recognizer.recognize_google(audio, language="en-IN")
            return text
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        return f"Speech recognition error: {e}"
    except OSError as e:
        return f"Microphone error: {e}"
    except Exception as e:
        return f"Error: {e}"

# === Groq Response ===
def generate_explanation(query):
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful AI tutor. Explain clearly step-by-step."},
            {"role": "user", "content": query}
        ],
        model="llama-3.1-8b-instant",
    )
    return chat_completion.choices[0].message.content

# === Diagram (fallback) ===
def generate_diagram_prompt(query):
    return "⚠️ Diagram generation is not supported with Groq API."

# === File Extraction ===
def extract_text_from_pdf(uploaded_pdf):
    doc = fitz.open(stream=uploaded_pdf.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_docx(uploaded_docx):
    doc = docx.Document(uploaded_docx)
    return "\n".join([para.text for para in doc.paragraphs])

# === UI Setup ===
st.set_page_config(page_title="AI-Powered Learning Companion", page_icon="🎓", layout="wide")

st.markdown("""
    <style>
    div[data-testid="stRadio"] label {
        color: black !important;
        font-weight: bold !important;
    }
    div[data-testid="stRadio"] label[data-selected="true"] {
        color: #003366 !important;
    }
    .stApp { background-color: #fee0f9 !important; }
    section[data-testid="stSidebar"] { background-color: #FADADD !important; padding: 15px; border-radius: 10px; }
    .stSidebar h2, .stSidebar h3, .stSidebar label, .stSidebar div { color: black !important; font-weight: bold; }
    h1, h2 { color: black !important; }
    .stTextInput>label { color: black !important; font-weight: bold !important; }
    .stTextInput>div>div>input { background-color: #BEE1E6 !important; color: black !important; border-radius: 5px !important; padding: 10px; }
    .stButton>button { color: white !important; background-color: #008585 !important; font-weight: bold; }
    .ai-response {
        color: black !important;
        font-weight: bold !important;
        font-size: 16px !important;
        padding: 15px;
        background-color: #f0f0f0 !important;
        border-radius: 10px;
        width: 100% !important;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar image
if os.path.exists("chatbot_sticker.png"):
    st.sidebar.image("chatbot_sticker.png", width=120, caption="Chatbot Assistant")
else:
    st.sidebar.info("AI Chatbot Assistant")

# Language selection
st.sidebar.subheader("🌍 Select Language")
language = st.sidebar.radio("Choose:", ["English", "Telugu", "Hindi"], index=0)

# File upload
st.sidebar.header("📂 Upload Image or File")
uploaded = st.sidebar.file_uploader(
    "Upload image (JPG/PNG) or document (PDF, DOCX, TXT)",
    type=["jpg", "jpeg", "png", "pdf", "docx", "txt"]
)

extracted_text = ""

if uploaded:
    try:
        if uploaded.type.startswith("image"):
            image = Image.open(uploaded)
            st.sidebar.image(image, caption="Uploaded Image", use_container_width=True)
            extracted_text = pytesseract.image_to_string(image)

            if extracted_text.strip():
                st.sidebar.subheader("📝 Extracted Text from Image")
                st.sidebar.write(extracted_text)
            else:
                st.sidebar.warning("No text found in image.")

        elif uploaded.type == "application/pdf":
            extracted_text = extract_text_from_pdf(uploaded)
            st.sidebar.subheader("📄 Extracted Text from PDF")
            st.sidebar.write(extracted_text[:1000])

        elif uploaded.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            extracted_text = extract_text_from_docx(uploaded)
            st.sidebar.subheader("📄 Extracted Text from DOCX")
            st.sidebar.write(extracted_text[:1000])

        elif uploaded.type == "text/plain":
            extracted_text = uploaded.read().decode("utf-8", errors="ignore")
            st.sidebar.subheader("📄 Extracted Text from TXT")
            st.sidebar.write(extracted_text[:1000])

        else:
            st.sidebar.warning("Unsupported file type.")

    except Exception as e:
        st.sidebar.error(f"File processing error: {e}")

# Main UI
if language == "Telugu":
    st.markdown("<h1 style='color:black;'>🎓 AI ఆధారిత విద్యా సహాయకుడు</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='color:black;'>AI గురువును అడగండి</h2>", unsafe_allow_html=True)
elif language == "Hindi":
    st.markdown("<h1 style='color:black;'>🎓 एआई-संचालित शिक्षण साथी</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='color:black;'>एआई ट्यूटर से पूछें</h2>", unsafe_allow_html=True)
else:
    st.markdown("<h1 style='color:black;'>🎓 AI-Powered Learning Companion</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='color:black;'>Ask the AI Tutor</h2>", unsafe_allow_html=True)

# Input mode
input_mode = st.radio("Choose input type:", ["Text", "Voice"], horizontal=True)

voice_query = None
text_query = ""

if input_mode == "Text":
    text_query = st.text_input("Enter your question")

elif input_mode == "Voice":
    if st.button("🎤 Speak your question"):
        voice_result = recognize_speech()

        if voice_result and not (str(voice_result).startswith("Error") or voice_result is None):
            voice_query = voice_result
            st.success(f"Recognized speech: {voice_query}")
        else:
            st.error(f"{voice_result}")

# Final query logic
final_query = ""

if extracted_text.strip():
    final_query = extracted_text.strip()
elif voice_query:
    final_query = voice_query.strip()
elif text_query.strip():
    final_query = text_query.strip()

# Answer generation
if st.button("Get Answer"):
    if final_query:
        with st.spinner("Generating answer..."):
            try:
                ai_response = generate_explanation(final_query)
                st.markdown(f"<div class='ai-response'>{ai_response}</div>", unsafe_allow_html=True)

                if any(word in final_query.lower() for word in ["diagram", "figure", "chart", "graph"]):
                    st.info(generate_diagram_prompt(final_query))

            except Exception as e:
                st.error(f"Error generating response: {e}")
    else:
        st.warning("Please provide a question by typing, speaking, or uploading an image/file.")

# Sidebar AI response
if extracted_text.strip():
    try:
        ai_response_file = generate_explanation(extracted_text)
        st.sidebar.markdown(f"<div class='ai-response'>{ai_response_file}</div>", unsafe_allow_html=True)
    except Exception as e:
        st.sidebar.error(f"Error generating AI response for uploaded content: {e}")