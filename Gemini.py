import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import google.generativeai as genai

# Gemini API setup
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    st.error("Please provide your Gemini API key in Streamlit secrets.")
    st.stop()
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

# Sample Data
data = pd.DataFrame({
    "state": ["Kerala", "Tamil Nadu", "Uttar Pradesh"],
    "name": ["Kathakali", "Bharatanatyam", "Taj Mahal"],
    "type": ["culture", "art", "tourism"],
    "lat": [9.9312, 13.0827, 27.1751],
    "lon": [76.2673, 80.2707, 78.0421],
    "url": [
        "https://en.wikipedia.org/wiki/Kathakali",
        "https://en.wikipedia.org/wiki/Bharatanatyam",
        "https://en.wikipedia.org/wiki/Taj_Mahal"
    ],
    "image_url": [
        "https://upload.wikimedia.org/wikipedia/commons/9/94/Kathakali_dancer_at_Kerala_Kathakali_Centre.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/8/87/Bharatanatyam_dancer.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/6/6d/Taj_Mahal_in_March_2004.jpg"
    ],
    "description": [
        "Classical dance from Kerala.",
        "Classical dance from Tamil Nadu.",
        "A marble mausoleum in Agra, India."
    ]
})

# Sidebar selection
selected = st.selectbox("Choose a Category", ["Art", "Culture", "Tourism"])
selected_type = selected.lower()
filtered_data = data[data["type"] == selected_type]

# Map with attractive emoji markers
st.subheader(f"{selected} Spots in India")
m = folium.Map(location=[20.5937, 78.9629], zoom_start=5, tiles="CartoDB positron")
marker_cluster = MarkerCluster().add_to(m)

emoji = {"art": "🎨", "culture": "🎭", "tourism": "🗺️"}

for _, row in filtered_data.iterrows():
    html_marker = f"""
    <div style="
        background-color: white;
        border: 2px solid #555;
        border-radius: 50%;
        padding: 6px;
        text-align: center;
        font-size: 20px;
        box-shadow: 0 0 6px rgba(0,0,0,0.3);">
        {emoji.get(row['type'], '📍')}
    </div>
    """
    popup_html = f"""
    <div style="width: 250px;">
        <h4>{emoji.get(row['type'], '')} {row['name']}</h4>
        <img src="{row['image_url']}" style="width:100%; margin-bottom:10px;" />
        <p>{row['description']}</p>
        <p><a href="{row['url']}" target="_blank">Learn More</a></p>
    </div>
    """
    folium.Marker(
        location=[row["lat"], row["lon"]],
        icon=folium.DivIcon(html=html_marker),
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=row["name"]
    ).add_to(marker_cluster)

st_data = st_folium(m, height=550, width=800)

# Gemini AI Suggestions
st.subheader(f"Gemini AI Suggestions for {selected}")
prompt_text = (
    f"Give 3 unique and engaging suggestions for someone exploring {selected.lower()} in India, "
    "based on these locations: "
)
for _, row in filtered_data.iterrows():
    prompt_text += f"{row['name']} ({row['description']}). "

prompt_text += "Make it creative and concise."

try:
    response = model.generate_content(prompt_text)
    suggestions = [part.text for part in response.parts if isinstance(part.text, str)]
    st.info("Here are some AI-curated ideas:")
    for suggestion in suggestions:
        st.markdown(f"- {suggestion}")
except Exception as e:
    st.error(f"Gemini error: {e}")
