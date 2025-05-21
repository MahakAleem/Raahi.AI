import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
from streamlit_option_menu import option_menu
import google.generativeai as genai

# Gemini API setup
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    st.error("Please provide your Gemini API key in Streamlit secrets.")
    st.stop()
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

# Page Config
st.set_page_config(layout="wide", page_title="Explore India", page_icon="🇮🇳")

# Dummy data
data = pd.DataFrame({
    "state": ["Rajasthan", "Kerala", "Uttar Pradesh", "Gujarat", "Madhya Pradesh", "Tamil Nadu", "Assam", "Punjab", "West Bengal", "Odisha", "Karnataka", "Bihar"],
    "name": ["Jaipur Art Festival", "Kathakali", "Taj Mahal", "Rann Utsav", "Khajuraho Temples", "Bharatanatyam", "Majuli", "Bhangra", "Durga Puja", "Konark Sun Temple", "Hampi", "Nalanda University"],
    "type": ["art", "culture", "tourism", "culture", "tourism", "culture", "culture", "culture", "culture", "tourism", "tourism", "tourism"],
    "lat": [26.9124, 9.9312, 27.1751, 23.7337, 24.8318, 13.0827, 27.0044, 31.1471, 22.5726, 19.8876, 15.3350, 25.1365],
    "lon": [75.7873, 76.2673, 78.0421, 70.8022, 79.9199, 80.2707, 94.2228, 75.3412, 88.3639, 86.0968, 76.4620, 85.4430],
    "url": ["https://en.wikipedia.org/wiki/Jaipur", "https://en.wikipedia.org/wiki/Kathakali", "https://en.wikipedia.org/wiki/Taj_Mahal", "https://en.wikipedia.org/wiki/Rann_of_Kutch", "https://en.wikipedia.org/wiki/Khajuraho_Group_of_Monuments", "https://en.wikipedia.org/wiki/Bharatanatyam", "https://en.wikipedia.org/wiki/Majuli", "https://en.wikipedia.org/wiki/Bhangra_(dance)", "https://en.wikipedia.org/wiki/Durga_Puja", "https://en.wikipedia.org/wiki/Konark_Sun_Temple", "https://en.wikipedia.org/wiki/Hampi", "https://en.wikipedia.org/wiki/Nalanda_University"],
    "image_url": ["https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/Hawa_Mahal_Jaipur.jpg/300px-Hawa_Mahal_Jaipur.jpg", "https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/Kathakali_dancer_at_Kerala_Kathakali_Centre.jpg/300px-Kathakali_dancer_at_Kerala_Kathakali_Centre.jpg", "https://s7ap1.scene7.com/is/image/incredibleindia/taj-mahal-agra-uttar-pradesh-2-attr-hero?qlt=82&ts=1726650323712", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR8K3DnapDfNZ19h5mXckppFcNBw-Ker0QZww&s", "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Bharatanatyam_dancer.jpg/300px-Bharatanatyam_dancer.jpg", "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c9/Majuli_Island_Assam.jpg/300px-Majuli_Island_Assam.jpg", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Bhangra_performance_in_Surajkund_Mela_2012.jpg/300px-Bhangra_performance_in_Surajkund_Mela_2012.jpg", "https://upload.wikimedia.org/wikipedia/commons/thumb/9/99/Durga_Puja_Idol_Immersion_Kolkata_2019_IMG_7539.jpg/300px-Durga_Puja_Idol_Immersion_Kolkata_2019_IMG_7539.jpg", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQokUVzngWT9CAVTqMGRan_gBuQCwfhRQK4Rg&s", "https://assets-news.housing.com/news/wp-content/uploads/2022/08/31020547/places-to-visit-in-hampi-FEATURE-compressed.jpg", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTcxpTs4-h_L3kngXwJ68njjJf1OfMm8ll1MQ&s", "https://upload.wikimedia.org/wikipedia/commons/thumb/5/57/Nalanda_University_stupa.jpg/300px-Nalanda_University_stupa.jpg"],
    "description": ["An annual art festival held in Jaipur showcasing contemporary and traditional art.", "A major form of classical Indian dance that originated in Kerala.", "An ivory-white marble mausoleum on the south bank of the Yamuna river in Agra.", "A cultural extravaganza showcasing the unique traditions and crafts of the Kutch region.", "A group of Hindu and Jain temples famous for their Nagara-style architectural symbolism and erotic sculptures.", "A major form of classical Indian dance that originated in Tamil Nadu.", "A large river island in the Brahmaputra River, known for its Vaishnavite monasteries.", "A vibrant and energetic folk dance and music form originating from the Punjab region.", "An annual Hindu festival in South Asia that celebrates the goddess Durga and victory of good over evil.", "A 13th-century Sun Temple at Konark, Odisha, known for its intricate architecture.", "An ancient village in Karnataka with numerous ruined monuments from the Vijayanagara Empire.", "A significant ancient center of higher learning in Bihar, India."]
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

    for _, row in data_filtered.iterrows():
        color = {"art": "#FF5733", "culture": "#2E86C1", "tourism": "#1E8449"}[selected_type]
        emoji = {"art": "🎨", "culture": "🎭", "tourism": "🗺️"}[selected_type]

        popup_html = f"""
            <div style="width: 300px;">
                <h4>{emoji} {row['name']}</h4>
                <img src="{row['image_url']}" alt="{row['name']}" style="width: 100%; height: auto; margin-bottom: 10px;">
                <p>{row['description']}</p>
                <p><a href="https://www.google.com/maps?q={row['lat']},{row['lon']}" target="_blank">View on Google Maps</a></p>
                <p><a href="{row['url']}" target="_blank">More on Wikipedia</a></p>
            </div>
        """
icon_path = f"assets/images/custom_icon.png"  
icon = folium.CustomIcon(icon_image=icon_path, icon_size=(32, 32))

folium.Marker(
    location=[row["lat"], row["lon"]],
    popup=folium.Popup(popup_html, max_width=300),
    tooltip=f"{emoji} {row['name']}",
    icon=icon
    ).add_to(marker_cluster)


map_data = st_folium(m, width=750, height=550, returned_objects=["last_object_clicked"])

clicked_data = map_data.get("last_object_clicked")
if clicked_data:
        st.session_state.clicked_highlight = (clicked_data["lat"], clicked_data["lng"])

# Gemini AI Suggestions
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