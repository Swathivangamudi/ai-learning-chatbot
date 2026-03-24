# 🎓 AI Learning Companion

An interactive **AI-powered learning chatbot** built using **Streamlit** and **Groq API** that helps users understand concepts easily through multiple input modes like text, voice, images, and documents.

---

## 🚀 Live Demo

👉 **Try the app here:**
https://smart-ai-tutor.streamlit.app/

---

## ✨ Features

* 💬 **Text-based Q&A** – Ask any question and get clear explanations
* 🎤 **Voice Input** – Speak your question (local support)
* 🖼️ **Image OCR** – Extract and understand text from images
* 📄 **Document Support** – Upload PDF, DOCX, or TXT files
* 🌍 **Multilingual UI** – Supports English, Telugu, and Hindi
* 🤖 **AI Tutor** – Step-by-step explanations using Groq LLM
* ⚡ **Fast Responses** – Powered by LLaMA 3.1 via Groq

---

## 🛠️ Tech Stack

* **Frontend/UI:** Streamlit
* **AI Model:** Groq (LLaMA 3.1)
* **Speech Recognition:** SpeechRecognition
* **OCR:** Tesseract (pytesseract)
* **File Processing:** PyMuPDF, python-docx
* **Language:** Python

---

## 📂 Project Structure

```
ai-learning-chatbot/
│
├── app.py                 # Main Streamlit app
├── requirements.txt       # Dependencies
├── README.md              # Project documentation
├── chatbot_sticker.png    # UI asset
├── .gitignore             # Ignored files
└── .streamlit/            # (local only, not pushed)
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/Swathivangamudi/ai-learning-chatbot.git
cd ai-learning-chatbot
```

---

### 2️⃣ Create virtual environment (recommended)

```bash
python -m venv venv
```

Activate it:

* Windows:

```bash
venv\Scripts\activate
```

* Mac/Linux:

```bash
source venv/bin/activate
```

---

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Set up API Key

Create a folder:

```
.streamlit/
```

Create file:

```
secrets.toml
```

Add your Groq API key:

```toml
GROQ_API_KEY = "your_api_key_here"
```

---

### 5️⃣ Run the app locally

```bash
streamlit run app.py
```

👉 Open in browser:

```
http://localhost:8501
```

---

## ⚠️ Notes

* 🎤 Voice input works only on local systems (not on cloud deployment)
* 🧾 Tesseract OCR requires installation on your system
* 🔐 Never upload `secrets.toml` to GitHub

---

## 🌐 Deployment

This app is deployed using **Streamlit Community Cloud**.

### Steps:

1. Push code to GitHub
2. Connect repository to Streamlit Cloud
3. Add secrets (API key) in dashboard
4. Deploy 🚀

---

## 📌 Future Improvements

* 🔊 Add Text-to-Speech (voice output)
* 💬 Chat history (ChatGPT-style UI)
* 📊 Diagram generation support
* 🌐 Mobile optimization

---

## 👩‍💻 Author

**Swathi Vangamudi**

* GitHub: https://github.com/Swathivangamudi

---

