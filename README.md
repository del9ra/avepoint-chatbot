# AvePoint Office Assistant - AI Chatbot Prototype

## Overview

AI-powered chatbot that helps with meeting management, company information, and day-to-day office tasks. Built as a proof-of-concept to demonstrate AI integration with business tools.

## Features

- **Answer questions** about AvePoint products and services using OpenAI GPT-3.5
- **Manage meetings** via Calendly API (view, schedule, and cancel)
- **Check weather** at AvePoint Jersey City office
- **Summarize text** for quick document review
- **Recommend products** based on user needs
- **Clean interface** with quick action buttons

## Tech Stack

- **Backend:** Python 3.11
- **AI:** OpenAI GPT-3.5-turbo API
- **Calendar:** Calendly API
- **Weather:** Open-Meteo API
- **UI:** Streamlit
- **Dependencies:** openai, streamlit, requests

## Setup Instructions

### Prerequisites

- Python 3.11 or higher
- OpenAI API key ([get one here](https://platform.openai.com/api-keys))
- Calendly API token ([get one here](https://calendly.com/integrations/api_webhooks))

### Installation

1. **Clone or download this repository**

2. **Install dependencies:**
```
   pip install -r requirements.txt
```

3. **Configure API keys:**
   
   Open `config.py` and add your API keys at the top:
```python
   CONF_OPENAPI_KEY = "your-openai-key-here"
   CONF_CALENDLY_TOKEN = "your-calendly-token-here"
```

4. **Run the application:**
```
   streamlit run app.py
```

5. **Open in browser:**
   
   Streamlit will automatically open `http://localhost:8501`

## Usage Examples

### Ask about AvePoint
```
"What does AvePoint do?"
"Tell me about AvePoint products"
```

### Manage meetings
```
"Show my meetings"
"Show booking links"  
"Schedule a meeting"
"Cancel meeting 1"
```

### Get weather
```
"What's the weather?"
"Check weather at the office"
```

### Summarize text
```
"Summarize this: [paste your text here]"
```

### Product recommendations
```
"I need a backup solution"
"Looking for data governance tools"
```

## Project Structure
```
avepoint-chatbot/
├── app.py                # Main application file
├── config.py             # API keys
├── README.md             # This file
├── requirements.txt      # Python dependencies
└── PRESENTATION.md       # Technical write-up
```

## Requirements File
```
openai==1.12.0
streamlit==1.31.0
requests==2.31.0
```

## Troubleshooting

**Error: "OpenAI API key not found"**
- Make sure you've added your API key in `app.py`
- Check that the key is valid on OpenAI's platform

**Error: "Calendly authentication failed"**
- Verify your Calendly token is correct
- Make sure the token has the required permissions

**Streamlit won't start**
- Check that port 8501 is available
- Try running on a different port: `streamlit run app.py --server.port 8502`

## Screenshots
<img width="1435" height="659" alt="Screenshot 2025-11-26 at 09 13 22" src="https://github.com/user-attachments/assets/24b9a23c-42c8-42f1-850b-d5f5c5bc20b4" />
<img width="1436" height="652" alt="Screenshot 2025-11-26 at 09 14 08" src="https://github.com/user-attachments/assets/75825589-5c7d-40f0-93ae-9764329a5a5e" />
<img width="1264" height="636" alt="Screenshot 2025-11-26 at 09 15 27" src="https://github.com/user-attachments/assets/a6b34dd2-272e-4258-8753-18241e9a694f" />
<img width="1415" height="652" alt="Screenshot 2025-11-26 at 09 16 24" src="https://github.com/user-attachments/assets/f517a85f-cb5f-4d4a-8c6d-fa8bb69d8492" />
