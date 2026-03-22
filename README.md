# eduction
# 🎓 Education Tutor for Remote India

> An AI-powered tutoring system that makes quality education accessible and affordable for rural India — built with ScaleDown + Gemini 2.5 Flash.

---

## 🧠 The Problem

Rural Indian students like **Priya** (15 years old, studying in Rajasthan) have:
- No personal tutor
- 1 teacher for 40 students
- Only a state-board textbook
- Slow 2G internet connection

A naive AI tutor that sends a full 340-page textbook (~85,000 tokens) to an LLM costs **₹17 per query** — financially impossible for rural India at scale.

---

## 💡 The Solution

A smart 3-step pipeline that reduces cost by **96%**:

```
Student Question
      ↓
STEP 1 → Read textbook PDF (415 pages = ~85,000 tokens)
      ↓
STEP 2 → ScaleDown API compresses → ~3,400 tokens
         (finds only the relevant paragraphs)
      ↓
STEP 3 → Gemini 2.5 Flash answers from compressed content
      ↓
Focused, accurate answer at ₹0.68/query
```

| | Before | After |
|---|---|---|
| Tokens per query | 85,000 | ~3,400 |
| Cost per query | ₹17.00 | ₹0.68 |
| Savings | — | **96%** |
| 1000 students × 10 Q/day | ₹1,70,000/day | ₹6,800/day |

---

## 🚀 Features

- 📄 **PDF Ingestion** — Reads any state-board textbook PDF
- ⚡ **Smart Caching** — PDF extracted once, cached for instant future loads
- 🔍 **ScaleDown Compression** — Drops 96% of irrelevant textbook content
- 🤖 **Gemini 2.5 Flash** — Answers only from relevant textbook content
- 💰 **Cost Tracking** — Shows real-time cost savings per query
- 🌐 **Streamlit Web App** — Beautiful UI accessible from any browser
- 💬 **Chat Interface** — Conversational Q&A with history

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| `Python 3.10+` | Core language |
| `ScaleDown API` | Textbook compression (85K → 3.4K tokens) |
| `Gemini 2.5 Flash` | Answer generation |
| `pypdf` | PDF text extraction |
| `Streamlit` | Web interface |
| `python-dotenv` | API key management |

---

## 📁 Project Structure

```
education-tutor/
├── app.py               # Streamlit web app
├── education_tutor.py   # CLI version
├── requirements.txt     # Dependencies
├── .env                 # API keys (not committed)
├── textbook.pdf         # Your textbook (not committed)
└── textbook_cache.pkl   # Auto-generated cache (not committed)
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/education-tutor.git
cd education-tutor
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Create `.env` file
```env
SCALEDOWN_API_KEY=your_scaledown_key_here
GEMINI_API_KEY=your_gemini_key_here
```

Get your keys:
- **ScaleDown** → [scaledown.ai/getapikey](https://scaledown.ai/getapikey)
- **Gemini** → [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

### 4. Add your textbook PDF
Rename your textbook PDF to `textbook.pdf` and place it in the project folder.

### 5. Run the web app
```bash
python -m streamlit run app.py
```

### 6. Or run the CLI version
```bash
python education_tutor.py
```

---

## 🖥️ Web App Usage

1. Open browser at `http://localhost:8501`
2. Enter your **ScaleDown API key** in the sidebar
3. Enter your **Gemini API key** in the sidebar
4. Upload your **textbook PDF**
5. Type any question and click **Ask ➤**

### Example questions:
```
What is a for loop?
Explain functions with an example
What is the difference between a list and a tuple?
How does exception handling work?
What is recursion?
```

---

## 💰 Cost Analysis

Based on **Gemini 2.5 Flash** pricing ($0.075 per 1M input tokens):

| Scenario | Tokens | Cost (INR) |
|---|---|---|
| Full book (no ScaleDown) | 85,000 | ₹0.54/query |
| With ScaleDown | ~3,400 | ₹0.02/query |
| **Savings** | **96%** | **₹0.52 saved** |

At scale — **1,000 students asking 10 questions/day**:
- ❌ Without pipeline: ₹5,400/day
- ✅ With pipeline: ₹200/day

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│              Student's Question              │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│         STEP 1: PDF Extraction               │
│  pypdf reads 415 pages → ~85,000 tokens     │
│  Cached after first run (instant later)     │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│         STEP 2: ScaleDown Compress           │
│  Sends: full textbook + question            │
│  Returns: only relevant paragraphs          │
│  85,000 tokens → ~3,400 tokens (96% less)  │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│         STEP 3: Gemini 2.5 Flash             │
│  Sees: ONLY compressed relevant content     │
│  Returns: focused, accurate answer          │
│  System prompt: patient tutor persona       │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│              Student Gets Answer             │
│         + Cost savings displayed            │
└─────────────────────────────────────────────┘
```

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

---

## 📄 License

MIT License — feel free to use for educational purposes.

---

## 🙏 Acknowledgements

- Built as part of the **HPE + Intel AI Workshop**
- Textbook: *Introduction to Python Programming* — OpenStax (CC BY 4.0)
- Powered by [ScaleDown](https://scaledown.ai) and [Google Gemini](https://aistudio.google.com)

---

## 👨‍💻 Author

Made with ❤️ for rural India's students
