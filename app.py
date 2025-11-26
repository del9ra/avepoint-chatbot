import streamlit as st
import openai
import requests
from datetime import datetime
from config import CONF_CALENDLY_TOKEN, CONF_OPENAPI_KEY

# OpenAI API key
openai.api_key = CONF_OPENAPI_KEY

# Calendly token
CALENDLY_TOKEN = CONF_CALENDLY_TOKEN

def get_calendly_events():
    """Get upcoming Calendly meetings"""
    headers = {
        "Authorization": f"Bearer {CALENDLY_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        # Get current user
        user_response = requests.get(
            "https://api.calendly.com/users/me",
            headers=headers
        )
        user_uri = user_response.json()["resource"]["uri"]
        
        # Get scheduled events
        events_response = requests.get(
            "https://api.calendly.com/scheduled_events",
            headers=headers,
            params={
                "user": user_uri,
                "count": 10,
                "status": "active"
            }
        )
        
        events = events_response.json().get("collection", [])
        
        if not events:
            return "📅 No upcoming meetings found."
        
        result = "📅 **Your Upcoming Meetings:**\n\n"
        
        # Initialize session state for events
        if 'calendly_events' not in st.session_state:
            st.session_state.calendly_events = {}
        
        st.session_state.calendly_events.clear()  # Clear old data
        
        for i, event in enumerate(events, 1):
            event_uri = event.get("uri", "")
            start_time = event.get("start_time", "")
            
            # Get invitees for this event
            invitees_response = requests.get(
                f"https://api.calendly.com/scheduled_events/{event_uri.split('/')[-1]}/invitees",
                headers=headers
            )
            
            invitees = invitees_response.json().get("collection", [])
            
            # Get invitee name (or use event name as fallback)
            if invitees and len(invitees) > 0:
                invitee_name = invitees[0].get("name", "Meeting")
            else:
                invitee_name = event.get("name", "Meeting")
            
            if start_time:
                dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                formatted_time = dt.strftime("%b %d, %Y at %I:%M %p")
            else:
                formatted_time = "Time TBA"
            
            result += f"**{i}.** {invitee_name}\n   📅 {formatted_time}\n\n"
            
            # Store event URI by number
            st.session_state.calendly_events[str(i)] = event_uri
        
        result += "\n💡 **To cancel a meeting, type:** `cancel meeting [number]`\n"
        result += "Example: `cancel meeting 1`"
        
        return result
    
    except Exception as e:
        return f"❌ Error fetching meetings: {str(e)}"


def cancel_calendly_meeting(event_uri):
    """Cancel a Calendly meeting"""
    headers = {
        "Authorization": f"Bearer {CALENDLY_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(
            f"{event_uri}/cancellation",
            headers=headers,
            json={"reason": "Cancelled via chatbot"}
        )
        
        if response.status_code == 201:
            return "✅ Meeting cancelled successfully!"
        else:
            return f"❌ Failed to cancel: {response.text}"
    
    except Exception as e:
        return f"❌ Error: {str(e)}"
    

def schedule_meeting_link():
    """Create a single-use scheduling link"""
    headers = {
        "Authorization": f"Bearer {CALENDLY_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        # Get current user
        user_response = requests.get(
            "https://api.calendly.com/users/me",
            headers=headers
        )
        user_data = user_response.json()["resource"]
        
        # Get first active event type
        org_uri = user_data["current_organization"]
        event_types_response = requests.get(
            "https://api.calendly.com/event_types",
            headers=headers,
            params={
                "organization": org_uri,
                "active": "true",
                "count": 1
            }
        )
        
        event_types = event_types_response.json().get("collection", [])
        
        if not event_types:
            return "❌ No event types available. Please create an event type in Calendly first."
        
        scheduling_url = event_types[0]["scheduling_url"]
        name = event_types[0]["name"]
        
        return f"📅 **Schedule a Meeting:**\n\n**{name}**\n\nShare this link to book: {scheduling_url}"
    
    except Exception as e:
        return f"❌ Error creating scheduling link: {str(e)}"

def get_weather():
    """Get weather in Jersey City"""
    url = "https://api.open-meteo.com/v1/forecast?latitude=40.71&longitude=-74.01&current_weather=true"
    response = requests.get(url)
    data = response.json()
    
    temp = data['current_weather']['temperature']
    windspeed = data['current_weather']['windspeed']
    
    return f"🌤️ Weather at AvePoint Jersey City office: {temp}°F, wind speed {windspeed} mph"

def recommend_product(user_message):
    """Recommend AvePoint product based on keywords"""
    products = {
        "backup": "AvePoint Cloud Backup - protects Microsoft 365 data",
        "migration": "AvePoint FLY - migrates content to cloud",
        "governance": "AvePoint Policies - automates data governance",
        "compliance": "Compliance Guardian - ensures regulatory compliance"
    }
    
    for key, product in products.items():
        if key in user_message.lower():
            return f"📦 **Recommended Product:**\n\n{product}"
    
    return None

def chat_with_gpt(user_message, chat_history):
    """Chat with OpenAI GPT"""
    
    # Check for cancel command
    if "cancel meeting" in user_message.lower():
        parts = user_message.lower().replace("cancel meeting", "").strip().split()
        if len(parts) >= 1:
            meeting_number = parts[0].strip()
            if hasattr(st.session_state, 'calendly_events') and meeting_number in st.session_state.calendly_events:
                event_uri = st.session_state.calendly_events[meeting_number]
                return cancel_calendly_meeting(event_uri)
            else:
                return "❌ Meeting number not found. Please view your meetings first with 'show my meetings'."
        else:
            return "❌ Please provide a meeting number. Format: `cancel meeting [number]`"
    
    # Check for Calendly commands
    if "meetings" in user_message.lower() or "scheduled" in user_message.lower():
        return get_calendly_events()
    
    if "schedule" in user_message.lower() and "meeting" in user_message.lower():
        return schedule_meeting_link()
    
    # Check weather
    if "weather" in user_message.lower():
        return get_weather()
    
    # If user wants summarization, skip product check
    if not ("summarize" in user_message.lower()):
        # Check product recommendation
        product_rec = recommend_product(user_message)
        if product_rec:
            return product_rec
    
    # Build messages for GPT
    messages = [
        {"role": "system", "content": "You are AvePoint Office Assistant. Help with: 1) Information about AvePoint products and company, 2) Summarizing text when user says 'summarize this:', 3) General questions, 4) Calendar management (show meetings, schedule and cancel meetings). Be concise and helpful."}
    ]
    
    # Add chat history
    for msg in chat_history:
        messages.append({"role": "user", "content": msg["user"]})
        messages.append({"role": "assistant", "content": msg["bot"]})
    
    # Add current question
    messages.append({"role": "user", "content": user_message})
    
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7
    )
    
    return response.choices[0].message.content

# Streamlit UI
st.set_page_config(page_title="AvePoint Office Assistant", page_icon="🤖")

st.title("🤖 AvePoint Office Assistant")
st.markdown("**AI-powered chatbot prototype**")

st.sidebar.header("About")
st.sidebar.info(
    """
    **Features:**
    - Answer questions about AvePoint
    - Summarize text
    - Check weather at Jersey City office
    - Recommend AvePoint products
    - View upcoming Calendly meetings
    - Schedule meetings
    - Cancel meetings
    
    **Tech Stack:**
    - Python
    - OpenAI GPT-3.5
    - Calendly API
    - Open-Meteo Weather API
    - Streamlit
    """
)

# Sample prompts
st.markdown("### Try asking:")
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("📋 What does AvePoint do?"):
        st.session_state.demo_prompt = "What does AvePoint do?"
with col2:
    if st.button("📅 Show meetings"):
        st.session_state.demo_prompt = "Show my meetings"
with col3:
    if st.button("➕ Schedule meeting"):
        st.session_state.demo_prompt = "Schedule a meeting"
with col4:
    if st.button("🌤️ Check weather"):
        st.session_state.demo_prompt = "What's the weather?"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle demo prompts FIRST
if "demo_prompt" in st.session_state and st.session_state.demo_prompt:
    prompt = st.session_state.demo_prompt
    st.session_state.demo_prompt = None
    
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            chat_history = []
            for i in range(0, len(st.session_state.messages)-1, 2):
                if i+1 < len(st.session_state.messages):
                    chat_history.append({
                        "user": st.session_state.messages[i]["content"],
                        "bot": st.session_state.messages[i+1]["content"]
                    })
            
            response = chat_with_gpt(prompt, chat_history)
            st.markdown(response)
    
    # Add bot response
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

# Chat input
if prompt := st.chat_input("Ask me anything..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            chat_history = []
            for i in range(0, len(st.session_state.messages)-1, 2):
                if i+1 < len(st.session_state.messages):
                    chat_history.append({
                        "user": st.session_state.messages[i]["content"],
                        "bot": st.session_state.messages[i+1]["content"]
                    })
            
            response = chat_with_gpt(prompt, chat_history)
            st.markdown(response)
    
    # Add bot response
    st.session_state.messages.append({"role": "assistant", "content": response})

# Clear button
if st.sidebar.button("Clear Chat History"):
    st.session_state.messages = []
    st.rerun()