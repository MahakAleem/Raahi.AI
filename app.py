import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
from folium import CustomIcon
from streamlit_option_menu import option_menu
import google.generativeai as genai
import os

# st.secrets = {
#     "api_keys": {
#         "gpt_key": os.environ.get("API_KEY")
#     }
# }

# Usage
# Load API key from environment
api_key = os.environ.get("GEMINI_API_KEY")

# Gemini API setup
if not api_key:
    st.error("Please provide your Gemini API key via environment variable 'GEMINI_API_KEY'.")
    st.stop()

genai.configure(api_key=api_key)  # ✅ FIXED HERE
model = genai.GenerativeModel('gemini-2.0-flash')

# Page Config
st.set_page_config(layout="wide", page_title="Explore India", page_icon="🇮🇳")

# Title Section
st.markdown("""
<div style="text-align: center;">
    <h1 style="color: #2E86C1;">🌏 Raahi.AI</h1>
    <h4 style="font-style: italic; color: #566573;">Cultural journeys reimagined with intelligence.</h4>
</div>
""", unsafe_allow_html=True)

# Data
data = pd.DataFrame({
    "state": [
        "Rajasthan", "Kerala", "Uttar Pradesh", "Gujarat",
        "Madhya Pradesh", "Tamil Nadu", "Assam", "Punjab",
        "West Bengal", "Odisha", "Karnataka", "Bihar"
    ],
    "name": [
        "Jaipur Art Festival", "Kathakali", "Taj Mahal", "Rann Utsav",
        "Khajuraho Temples", "Bharatanatyam", "Majuli", "Bhangra",
        "Durga Puja", "Konark Sun Temple", "Hampi", "Nalanda University"
    ],
    "type": [
        "art", "culture", "tourism", "culture",
        "tourism", "culture", "culture", "culture",
        "culture", "tourism", "tourism", "tourism"
    ],
    "lat": [
        26.9124, 9.9312, 27.1751, 23.7337,
        24.8318, 13.0827, 27.0044, 31.1471,
        22.5726, 19.8876, 15.3350, 25.1365
    ],
    "lon": [
        75.7873, 76.2673, 78.0421, 70.8022,
        79.9199, 80.2707, 94.2228, 75.3412,
        88.3639, 86.0968, 76.4620, 85.4430
    ],
    "url": [
        "https://en.wikipedia.org/wiki/Jaipur", "https://en.wikipedia.org/wiki/Kathakali", "https://en.wikipedia.org/wiki/Taj_Mahal", "https://en.wikipedia.org/wiki/Rann_of_Kutch",
        "https://en.wikipedia.org/wiki/Khajuraho_Group_of_Monuments", "https://en.wikipedia.org/wiki/Bharatanatyam", "https://en.wikipedia.org/wiki/Majuli", "https://en.wikipedia.org/wiki/Bhangra_(dance)",
        "https://en.wikipedia.org/wiki/Durga_Puja", "https://en.wikipedia.org/wiki/Konark_Sun_Temple", "https://en.wikipedia.org/wiki/Hampi", "https://en.wikipedia.org/wiki/Nalanda_University"
    ],
    "image_url": [
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQCtFW1hia9gfEsF_pYtAKaxexT2NrcrVgL9g&s",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQJuUzEq1sEDz-v1Ny5WxTq8jZzbmiFF5_2YQ&s",
        "https://s7ap1.scene7.com/is/image/incredibleindia/taj-mahal-agra-uttar-pradesh-2-attr-hero?qlt=82&ts=1726650323712",
        "https://thrillingtravel.in/wp-content/uploads/2024/02/Rann-utsav-guide.jpg",
        "https://media.istockphoto.com/id/528284252/photo/kjaruharo-temples-india.jpg?s=612x612&w=0&k=20&c=-iWM83PbINoAS5i_06cVjIDpe_yT0cE3uw0_iPoeWHM=",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTNX0byPOktSHWK3g9SKd-FviuVFHmYKaowQg&s",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQGQTuPYR3DD4yF6tsPM6J8QzrNuebu26cGMQ&s",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRZktivlC7XNMJLCJIQB7OJ58jRm_YsL9N-bQ&s",
        "https://pragyata.com/wp-content/uploads/2020/10/Durga-Puja-Odisha.jpg",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQxjp0IJRrRoHc0yuziqFxYjuBojswfNPdC1Q&s",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQjsxi6QP57REO1QFV1Hq47Vtc5PPVBAUt_5w&s",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRaAUjZrSmm3NNS32CxwBdeESe1QABdUsK8Rw&s"
    ],
    "description": [
        "An annual art festival held in Jaipur showcasing contemporary and traditional art.",
        "A major form of classical Indian dance that originated in Kerala.",
        "An ivory-white marble mausoleum on the south bank of the Yamuna river in Agra.",
        "A cultural extravaganza showcasing the unique traditions and crafts of the Kutch region.",
        "A group of Hindu and Jain temples famous for their Nagara-style architectural symbolism and erotic sculptures.",
        "A major form of classical Indian dance that originated in Tamil Nadu.",
        "A large river island in the Brahmaputra River, known for its Vaishnavite monasteries.",
        "A vibrant and energetic folk dance and music form originating from the Punjab region.",
        "An annual Hindu festival in South Asia that celebrates the goddess Durga and victory of good over evil.",
        "A 13th-century Sun Temple at Konark, Odisha, known for its intricate architecture.",
        "An ancient village in Karnataka with numerous ruined monuments from the Vijayanagara Empire.",
        "A significant ancient center of higher learning in Bihar, India."
    ]
})

# Sidebar Select
selected = option_menu(
    menu_title=None,
    options=["Art", "Culture", "Tourism"],
    icons=["palette", "globe", "map"],
    menu_icon="cast",
    default_index=2,
    orientation="horizontal"
)

# Filter data
selected_type = selected.lower()
data_filtered = data[data["type"] == selected_type]

# Session state for clicked marker
if "clicked_highlight" not in st.session_state:
    st.session_state.clicked_highlight = None

# Layout columns
col1, col2 = st.columns([2, 1])

# Map View
with col1:
    st.subheader(f"{selected} Map View")
    m = folium.Map(location=[22.5937, 78.9629], zoom_start=4.5, tiles="CartoDB positron")
    m.fit_bounds([[6.5, 68.0], [37.6, 97.25]])
    marker_cluster = MarkerCluster().add_to(m)

    icon_path = "assets/images/custom_icon.png"

    for _, row in data_filtered.iterrows():
        popup_html = f"""
            <div style='width: 300px;'>
                <h4>{row['name']}</h4>
                <img src='{row['image_url']}' alt='{row['name']}' style='width: 100%; height: auto; margin-bottom: 10px;'>
                <p>{row['description']}</p>
                <p><a href='https://www.google.com/maps?q={row['lat']},{row['lon']}' target='_blank'>View on Google Maps</a></p>
                <p><a href='{row['url']}' target='_blank'>More on Wikipedia</a></p>
            </div>
        """
        icon = CustomIcon(icon_path, icon_size=(40, 40))
        folium.Marker(
            location=[row["lat"], row["lon"]],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=row['name'],
            icon=icon
        ).add_to(marker_cluster)

    map_data = st_folium(m, width=750, height=550, returned_objects=["last_object_clicked"])
    clicked_data = map_data.get("last_object_clicked")
    if clicked_data:
        st.session_state.clicked_highlight = (clicked_data["lat"], clicked_data["lng"])

# AI Suggestion Dropdown
with col2:
    st.subheader("Gemini AI Suggestion")

    clicked_row = None
    if st.session_state.clicked_highlight:
        lat, lon = st.session_state.clicked_highlight
        clicked_row = data_filtered[(data_filtered["lat"] == lat) & (data_filtered["lon"] == lon)].squeeze()

    if clicked_row is not None and not clicked_row.empty:
        prompt_text = f"""You're a travel assistant. Provide detailed, helpful suggestions for visiting the place:
{clicked_row['name']} in {clicked_row['state']}, India. Based on this short description:
{clicked_row['description']} — generate insights and recommendations in the following categories:

- Best Time of Year to Visit
- Official Visiting Hours or Timings
- Unique or Lesser-Known Facts
- Entry Ticket Price
- Least Crowded Times or Days to Visit
- Additional Tips for a Smooth Visit

Respond in markdown format with each category as a bold header.
"""

        try:
            response = model.generate_content(prompt_text)
            suggestions = [part.text for part in response.parts if isinstance(part.text, str)]

            if suggestions:
                categories = [
                    "Best Time of Year to Visit",
                    "Official Visiting Hours or Timings",
                    "Unique or Lesser-Known Facts",
                    "Entry Ticket Price",
                    "Least Crowded Times or Days to Visit",
                    "Additional Tips for a Smooth Visit"
                ]

                for category in categories:
                    with st.expander(category):
                        lines = suggestions[0].split("\n")
                        content = []
                        collect = False
                        for line in lines:
                            if line.strip().startswith("**") and category.lower() in line.lower():
                                collect = True
                                continue
                            elif line.strip().startswith("**"):
                                collect = False
                            if collect:
                                content.append(line)
                        st.markdown("\n".join(content) if content else "No data available.")
            else:
                st.warning("No suggestions returned.")
        except Exception as e:
            st.error(f"Gemini API error: {e}")
    else:
        st.info("Click on a marker to get an AI suggestion for that specific location.")
