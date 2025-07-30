# PhonePe-Insights-Dashboard

An interactive dashboard built using **Streamlit** to explore and analyze PhonePe's **aggregate transaction data**,**aggregate user data**,**aggregate userdevice data**,**insurance transaction data** across Indian states, districts, and pincodes.

---

## 🚀 Features

- 📌 Key metrics: Total Transaction Amount, Total Transaction Count, Transaction Types, Total Insurance Amount, Policy Count, Insurance Types
- 🗂️ Filterable by **State**, **Year**, and **Quarter**
- 📊 Visual insights: bar charts for transaction, insurance type breakdown and line charts for trend over time
- 🏙️ Top Districts & 📮 Pincodes
- 🌍 PyDeck-based **bubble map** showing insurance transactions spatially and **bubble map**,**Choropleth map** showing transaction amount filterable by **State**, **Year**, and **Quarter**
- 📈 Tabbed layout for smooth navigation
- ✅ Fast performance using `@st.cache_data` and modular code structure

---

## 📂 Project Structure

app.py ---> main streamlit app
analysis.py ---> all business logic functions
db_connect.py ---> connect and loads data from postgreSQL
requirements.txt ---> python dependencies

---

## 📈 Key Business Insights

> High-volume regions: Maharashtra, Karnataka, Tamil Nadu — consistently strong across both transaction and insurance data.

> Top-performing districts/pincodes: revealed in both sections.

> Low-activity regions: can be identified using maps/charts — useful for targeted growth strategies.

> UI/UX: Clear tabs, filters, metrics, and interactive visuals for fast decision-making.
