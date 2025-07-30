
import streamlit as st
import plotly.express as px
import pydeck as pdk
import json
from db_connect import (
    load_agg_transaction, load_agg_user, load_agg_user_device,
    load_top_transaction_district, load_top_transaction_pincode,
    load_top_user_district, load_top_user_pincode,
    load_agg_insurance, load_top_insurance_district, load_top_insurance_pincode,
    load_map_insurance_country, load_map_insurance_country_meta
)
from analysis import (
    filter_data, get_kpis, transaction_by_type,
    user_kpis, device_usage, top_kpi_by_location, get_transaction_trend,
    filter_insurance_data, insurance_kpis, insurance_by_type
)

# App Config
st.set_page_config("📊 PhonePe Insights", layout="wide")
st.sidebar.title("📚 Navigation")
view_option = st.sidebar.radio("Choose View", ["Overview", "Top Districts", "Top Pincodes", "Top Users", "Transaction Map", "Insurance Insights"])

# Load all data once
@st.cache_data
def load_data():
    return (
        load_agg_transaction(),
        load_agg_user(),
        load_agg_user_device(),
        load_top_transaction_district(),
        load_top_transaction_pincode(),
        load_top_user_district(),
        load_top_user_pincode(),
        load_agg_insurance(),
        load_map_insurance_country(),
        load_top_insurance_district(),
        load_top_insurance_pincode(),
        load_map_insurance_country_meta()
    )

agg_transaction_df, agg_user_df, agg_user_device_df, top_district_df, top_pincode_df, top_user_district_df, top_user_pincode_df, agg_ins_df, map_ins_country_df, top_ins_dist_df, top_ins_pin_df, map_ins_meta_df = load_data()
    
# ========================================
# OVERVIEW VIEW
# ========================================
if view_option == "Overview":
    st.title("📊 PhonePe Transaction Insights")

    # Sidebar filters
    states = ["All"] + sorted(agg_transaction_df['State'].dropna().unique().tolist())
    years = ["All"] + sorted(agg_transaction_df['Year'].unique().tolist())
    quarters = ["All", 1, 2, 3, 4]

    selected_state = st.sidebar.selectbox("Select State", states)
    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_quarter = st.sidebar.selectbox("Select Quarter", quarters)

    # Filter data
    filtered_trans = filter_data(agg_transaction_df, selected_state, selected_year, selected_quarter)
    filtered_user = filter_data(agg_user_df, selected_state, selected_year, selected_quarter)
    filtered_device = filter_data(agg_user_device_df, selected_state, selected_year, selected_quarter)

    # Tabs for organization
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📌 KPIs", "💡 Transaction Types", "👥 Users & Devices", "📈 Trends", "📂 Raw Data"])

    # with tab1:
    #     # Transaction KPIs
    #     if not filtered_trans.empty:
    #         st.subheader("📌 Transaction Overview")
    #         total_amount, total_count, unique_types = get_kpis(filtered_trans)
    #         col1, col2, col3 = st.columns([2,2,1])
    #         col1.metric("💰 Total Transaction Amount", f"₹{total_amount:,.0f}", border=True)
    #         col2.metric("🔁 Total Transaction Count", f"{total_count:,}", border=True)
    #         col3.metric("🔣 Transaction Types", unique_types, border=True)

    #         st.subheader("💡 Transaction Amount by Type")
    #         chart_data = transaction_by_type(filtered_trans)
    #         if not chart_data.empty:
    #             st.bar_chart(chart_data)
    #         else:
    #             st.info("No chart data available for selected filters.")
    #     else:
    #         st.warning("No transaction data found for selected filters.")
    with tab1:
        st.subheader("📌 Transaction Overview")

        if not filtered_trans.empty:
            # KPIs with better visual balance and professional look
            total_amount, total_count, unique_types = get_kpis(filtered_trans)
            st.markdown("### 🔢 Key Performance Indicators")

            col1, col2, col3 = st.columns([2, 2, 1])
            col1.metric("💰 Total Transaction Amount", f"₹{total_amount:,.0f}", help="Sum of all transactions", border=True)
            col2.metric("🔁 Total Transaction Count", f"{total_count:,}", help="Number of transactions", border=True)
            col3.metric("🔣 Transaction Types", unique_types, help="Unique transaction modes used", border=True)

            st.divider()

            # Bar Chart of Amount by Transaction Type
            st.markdown("### 💡 Transaction Breakdown by Type")

            chart_data = transaction_by_type(filtered_trans)
            if not chart_data.empty:
                import plotly.express as px
                fig = px.bar(
                    chart_data,
                    x=chart_data.index,
                    y=chart_data.values,
                    labels={"x": "Transaction Type", "y": "Total Amount (₹)"},
                    title="Transaction Amount per Type",
                    color_discrete_sequence=["#F39C12"]
                )
                fig.update_layout(xaxis_tickangle=-30)
                st.plotly_chart(fig, use_container_width=True)

                # Optional Insight Box
                st.info("💡 *Insight:* Transaction types like 'Recharge' or 'Merchant Payments' can reveal usage trends across regions or periods.")
            else:
                st.info("No chart data available for selected filters.")
        else:
            st.warning("No transaction data found for selected filters.")

    with tab2:
        st.subheader("👥 User Overview")

        if not filtered_user.empty or not filtered_device.empty:
            # Show KPIs
            if not filtered_user.empty:
                total_app_opens, total_users = user_kpis(filtered_user)
                col1, col2, col3 = st.columns([1, 1, 2])
                col1.metric("📱 App Opens", f"{total_app_opens:,}",  border=True)
                col2.metric("🧑 Registered Users", f"{total_users:,}", border=True)
                col3.markdown("#### 🔍 Insight:")
                col3.markdown(f"""
                    - The number of app opens helps understand **user engagement**
                    - High user count means strong **market penetration**
                    - Use filters (state/year/quarter) to explore more
                """)
            else:
                st.warning("No user data available for the selected filters.")

            st.divider()

            # Device Usage Chart
            if not filtered_device.empty:
                st.subheader("📱 Device Usage Distribution")
                device_data = device_usage(filtered_device)
                if not device_data.empty:
                    fig = px.bar(
                        device_data,
                        x=device_data.index,
                        y=device_data.values,
                        labels={'x': 'Device Brand', 'y': 'App Opens'},
                        title="App Opens by Device Brand",
                        color_discrete_sequence=["#FF6F00"]
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No device usage data found for selected filters.")
            else:
                st.warning("No device data available for the selected filters.")
        else:
            st.warning("No user or device data available.")

    with tab3:
        st.subheader("📱 Device Usage Overview")

        if not filtered_device.empty:
            device_data = device_usage(filtered_device)

            if not device_data.empty:
                # Top 3 Devices as metrics
                sorted_devices = device_data.sort_values(ascending=False)
                top_devices = sorted_devices.head(3)
                st.markdown("### 🔝 Top Device Brands")
                col1, col2, col3 = st.columns(3)
                col1.metric(f"🥇 {top_devices.index[0]}", f"{top_devices.iloc[0]:,} Opens",  border=True)
                col2.metric(f"🥈 {top_devices.index[1]}", f"{top_devices.iloc[1]:,} Opens",  border=True)
                col3.metric(f"🥉 {top_devices.index[2]}", f"{top_devices.iloc[2]:,} Opens",  border=True)

                st.divider()

                # Plotly Bar Chart
                fig = px.bar(
                    device_data.sort_values(ascending=False),
                    x=device_data.index,
                    y=device_data.values,
                    labels={"x": "Device Brand", "y": "App Opens"},
                    title="📊 App Opens by Device Brand",
                    color_discrete_sequence=["#2E86C1"]
                )
                fig.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)

                # Optional Insights
                st.info("💡 *Insight:* A dominant brand indicates strong performance or popularity in that region/period. Use this to target specific device users with campaigns.")
            else:
                st.info("No chart data available for selected filters.")
        else:
            st.warning("No device data found for selected filters.")
    
    # ========================================
    # Transaction Trend Over Time
    # ========================================
    with tab4:

        st.subheader("📈 Transaction Trend Over Time")

        # Dropdown filters for trend
        type_options = ["All"] + sorted(agg_transaction_df["Transaction_type"].dropna().unique())
        selected_trend_type = st.selectbox("Select Transaction Type", type_options, key="trend_type")

        trend_df = get_transaction_trend(filtered_trans, selected_state, selected_trend_type)

        if not trend_df.empty:
            fig = px.line(
                trend_df,
                x="YearQuarter",
                y="Transaction_amount",
                markers=True,
                title="Transaction Trend",
                labels={"Transaction_amount": "Amount (₹)", "YearQuarter": "Period"}
            )
            fig.update_traces(line_color="orange")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data available for selected filters.")

    with tab5:
        # Raw Data Expanders
        with st.expander("Show Filtered Transaction Data"):
            st.dataframe(filtered_trans)

        with st.expander("Show Filtered User Data"):
            st.dataframe(filtered_user)

        with st.expander("Show Filtered Device Data"):
            st.dataframe(filtered_device)

# ========================================
# TOP DISTRICTS VIEW
# ========================================
elif view_option == "Top Districts":
    st.title("🏙️ Top Districts by Transaction Amount")
    top_districts = top_kpi_by_location(top_district_df, col="District")
    if not top_districts.empty:
        st.bar_chart(top_districts)
    else:
        st.info("No data available.")

# ========================================
# TOP PINCODES VIEW
# ========================================
elif view_option == "Top Pincodes":
    st.title("📍 Top Pincodes by Transaction Amount")
    top_pincodes = top_kpi_by_location(top_pincode_df, col="Pincode")
    if not top_pincodes.empty:
        st.bar_chart(top_pincodes)
    else:
        st.info("No data available.")

# ========================================
# TOP USERS VIEW
# ========================================
elif view_option == "Top Users":
    st.title("👥 Top Users Overview")
    st.subheader("🏙️ By District")
    top_users_district = top_kpi_by_location(top_user_district_df, col="District", value="RegisteredUsers")
    st.bar_chart(top_users_district)

    st.subheader("📮 By Pincode")
    top_users_pincode = top_kpi_by_location(top_user_pincode_df, col="Pincode", value="RegisteredUsers")
    st.bar_chart(top_users_pincode)

# ========================================
# TRANSACTION MAP VIEW
# ========================================
elif view_option == "Transaction Map":
    st.sidebar.markdown("---")
    st.sidebar.header("🧭 Map Filters")

    years = ["All"] + sorted(agg_transaction_df["Year"].dropna().unique().tolist())
    states = ["All"] + sorted(agg_transaction_df["State"].dropna().unique().tolist())
    quarters = ["All"] + sorted(agg_transaction_df["Quarter"].dropna().unique().tolist())

    selected_year = st.sidebar.selectbox("Select Year", years, key="map_year")
    selected_state = st.sidebar.selectbox("Select State", states, key="map_state")
    selected_quarter = st.sidebar.selectbox("Select Quarter", quarters, key="map_quarter")

    # Filter Data
    filtered_map_df = filter_data(agg_transaction_df, selected_state, selected_year, selected_quarter)

    # Group by state
    state_summary = filtered_map_df.groupby("State")["Transaction_amount"].sum().reset_index()

    # state names to match GeoJSON
    state_name_map = {
        'andaman-&-nicobar-islands': 'Andaman and Nicobar Islands',
        'andhra-pradesh': 'Andhra Pradesh',
        'arunachal-pradesh': 'Arunachal Pradesh',
        'assam': 'Assam',
        'bihar': 'Bihar',
        'chandigarh': 'Chandigarh',
        'chhattisgarh': 'Chhattisgarh',
        'dadra-&-nagar-haveli-&-daman-&-diu': 'Dadra and Nagar Haveli and Daman and Diu',
        'delhi': 'Delhi',
        'goa': 'Goa',
        'gujarat': 'Gujarat',
        'haryana': 'Haryana',
        'himachal-pradesh': 'Himachal Pradesh',
        'jammu-&-kashmir': 'Jammu and Kashmir',
        'jharkhand': 'Jharkhand',
        'karnataka': 'Karnataka',
        'kerala': 'Kerala',
        'ladakh': 'Ladakh',
        'madhya-pradesh': 'Madhya Pradesh',
        'maharashtra': 'Maharashtra',
        'manipur': 'Manipur',
        'meghalaya': 'Meghalaya',
        'mizoram': 'Mizoram',
        'nagaland': 'Nagaland',
        'odisha': 'Odisha',
        'puducherry': 'Puducherry',
        'punjab': 'Punjab',
        'rajasthan': 'Rajasthan',
        'sikkim': 'Sikkim',
        'tamil-nadu': 'Tamil Nadu',
        'telangana': 'Telangana',
        'tripura': 'Tripura',
        'uttar-pradesh': 'Uttar Pradesh',
        'uttarakhand': 'Uttarakhand',
        'west-bengal': 'West Bengal',
        'lakshadweep': 'Lakshadweep'
    }

    state_summary["State"] = state_summary["State"].map(state_name_map)
    state_summary.rename(columns={"State": "ST_NM"}, inplace=True)

    # plot - map
    st.subheader("📍 State-wise Transaction Map (Choropleth View)")
    fig = px.choropleth(
        state_summary,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey="properties.ST_NM",
        locations="ST_NM",
        color="Transaction_amount",
        color_continuous_scale="YlGnBu",
        title="🗺️ Transaction Amount by State",
        height=600
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 80, "l": 0, "b": 0})
    st.plotly_chart(fig, use_container_width=True)

    # Using pydeck
    # Prepare state coords
    state_coords = {
        "Andaman and Nicobar Islands": [11.7401, 92.6586],
        "Andhra Pradesh": [15.9129, 79.7400],
        "Arunachal Pradesh": [28.2180, 94.7278],
        "Assam": [26.2006, 92.9376],
        "Bihar": [25.0961, 85.3131],
        "Chandigarh": [30.7333, 76.7794],
        "Chhattisgarh": [21.2787, 81.8661],
        "Dadra and Nagar Haveli and Daman and Diu": [20.3974, 72.8328],
        "Delhi": [28.7041, 77.1025],
        "Goa": [15.2993, 74.1240],
        "Gujarat": [22.2587, 71.1924],
        "Haryana": [29.0588, 76.0856],
        "Himachal Pradesh": [31.1048, 77.1734],
        "Jammu and Kashmir": [33.7782, 76.5762],
        "Jharkhand": [23.6102, 85.2799],
        "Karnataka": [15.3173, 75.7139],
        "Kerala": [10.8505, 76.2711],
        "Ladakh": [34.2268, 77.5619],
        "Madhya Pradesh": [22.9734, 78.6569],
        "Maharashtra": [19.7515, 75.7139],
        "Manipur": [24.6637, 93.9063],
        "Meghalaya": [25.4670, 91.3662],
        "Mizoram": [23.1645, 92.9376],
        "Nagaland": [26.1584, 94.5624],
        "Odisha": [20.9517, 85.0985],
        "Puducherry": [11.9416, 79.8083],
        "Punjab": [31.1471, 75.3412],
        "Rajasthan": [27.0238, 74.2179],
        "Sikkim": [27.5330, 88.5122],
        "Tamil Nadu": [11.1271, 78.6569],
        "Telangana": [18.1124, 79.0193],
        "Tripura": [23.9408, 91.9882],
        "Uttar Pradesh": [26.8467, 80.9462],
        "Uttarakhand": [30.0668, 79.0193],
        "West Bengal": [22.9868, 87.8550],
        "Lakshadweep": [10.5667, 72.6417]
    }

    # Filter and map data
    state_df = filtered_map_df.groupby("State")["Transaction_amount"].sum().reset_index()
    state_df["ST_NM"] = state_df["State"].map(state_name_map)
    state_df["lat"] = state_df["ST_NM"].map(lambda x: state_coords.get(x, [None, None])[0])
    state_df["lon"] = state_df["ST_NM"].map(lambda x: state_coords.get(x, [None, None])[1])
    state_df = state_df.dropna(subset=["lat", "lon"])

    # Scale radius
    max_amount = state_df["Transaction_amount"].max()
    state_df["radius"] = state_df["Transaction_amount"] / max_amount * 50000  # scaled to avoid huge overlap

    # Add color
    state_df["color"] = state_df["Transaction_amount"].apply(
        lambda x: [255, int(255 - (x / max_amount) * 200), 0, 140]
    )
    state_df["formatted_amount"] = state_df["Transaction_amount"].apply(lambda x: f"₹{x:,.0f}")

    # pydeck layer
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=state_df,
        get_position='[lon, lat]',
        get_radius="radius",
        get_fill_color="color",
        pickable=True,
        auto_highlight=True,
    )

    # Set view
    view_state = pdk.ViewState(
        longitude=78.9629,
        latitude=22.5937,
        zoom=4,
        pitch=0
    )

    # Render map
    st.subheader("📍 State-wise Transaction Map (Bubble View)")
    st.pydeck_chart(pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "{ST_NM}\n{formatted_amount}"}
    ))

# ========================================
# INSURANCE INSIGHTS VIEW
# ========================================
elif view_option == "Insurance Insights":

    st.title("🏥 Insurance Insights Dashboard")

    states = ["All"] + sorted(agg_ins_df["State"].dropna().unique())
    years = ["All"] + sorted(agg_ins_df["Year"].dropna().unique())
    quarters = ["All"] + sorted(agg_ins_df["Quarter"].dropna().unique())

    selected_state = st.sidebar.selectbox("Select State", states, key="ins_state")
    selected_year = st.sidebar.selectbox("Select Year", years, key="ins_year")
    selected_quarter = st.sidebar.selectbox("Select Quarter", quarters, key="ins_qtr")

    # Filter insurance data
    filtered_ins = filter_insurance_data(agg_ins_df, selected_state, selected_year, selected_quarter)

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📌 Overview", "📍 Regional Insights", "🗃️ Raw Data", "📈 Trends", "🗺️ Map", "📊 Penetration Analysis"])

    with tab1:
        st.subheader("💡 Key Metrics")
        if not filtered_ins.empty:
            total_amount, total_count, unique_types = insurance_kpis(filtered_ins)
            col1, col2, col3 = st.columns([1, 1, 1])
            col1.metric("💵 Total Insurance Amount", f"₹{total_amount:,.0f}", border=True)
            col2.metric("📑 Total Policies", f"{total_count:,}", border=True)
            col3.metric("🔢 Types of Insurance", unique_types, border=True)
            st.divider()
            # Show chart only if more than one insurance type
            insurance_types = filtered_ins["Type"].dropna().unique()
            if len(insurance_types) > 1:
                st.subheader("🧾 Insurance Amount by Type")
                chart_data = insurance_by_type(filtered_ins)
                fig = px.bar(
                    chart_data,
                    x="Type",
                    y="Transaction_amount",
                    color="Type",
                    labels={"Transaction_amount": "Total Amount (₹)", "Type": "Insurance Type"},
                    title="Breakdown by Insurance Type",
                    color_discrete_sequence=px.colors.sequential.Blues
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info(f"ℹ️ Only one insurance type found: **{insurance_types[0]}**. Skipping type chart.")
        else:
            st.warning("No data for selected filters.")

    # Regional Insights Tab
    with tab2:
        st.subheader("🏙️ Top Districts by Insurance Amount")
        district_data = filter_insurance_data(top_ins_dist_df, selected_state, selected_year, selected_quarter)
        if not district_data.empty:
            top_districts = district_data.groupby("District")["Amount"].sum().sort_values(ascending=False).head(10).reset_index()
            fig = px.bar(
                top_districts,
                x="District",
                y="Amount",
                labels={"Amount": "Amount (₹)", "District": "District"},
                title="Top 10 Districts",
                color="Amount",
                color_continuous_scale="Purples"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No district-level data available.")
        st.divider()
        st.subheader("📮 Top Pincodes by Insurance Amount")
        pincode_data = filter_insurance_data(top_ins_pin_df, selected_state, selected_year, selected_quarter)
        if not pincode_data.empty:
            top_pins = pincode_data.groupby("Pincode")["Amount"].sum().sort_values(ascending=False).head(10).reset_index()
            top_pins["Pincode"] = top_pins["Pincode"].astype(str)
            fig = px.bar(
                top_pins,
                x="Pincode",
                y="Amount",
                labels={"Amount": "Amount (₹)", "Pincode": "Pincode"},
                title="Top 10 Pincodes",
                color="Amount",
                color_continuous_scale="Oranges"
            )
            fig.update_layout(
                xaxis=dict(
                    tickmode='linear',
                    tickformat='',
                    type='category'  # force categorical x-axis
                )
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No pincode-level data available.")

    # Raw Data Tab
    with tab3:
        st.subheader("📄 Filtered Insurance Data")
        st.dataframe(filtered_ins)

    # Trend
    with tab4:
        st.subheader("📈 Insurance Trend Over Time")

        if not filtered_ins.empty:

            trend_df = filtered_ins.copy()
            trend_df["YearQuarter"] = trend_df["Year"].astype(str) + " Q" + trend_df["Quarter"].astype(str)
            trend_summary = trend_df.groupby("YearQuarter")["Transaction_amount"].sum().reset_index()

            # Plot line chart using Plotly
            fig = px.line(
                trend_summary,
                x="YearQuarter",
                y="Transaction_amount",
                title="📊 Insurance Transaction Trend Over Time",
                markers=True,
                labels={"Transaction_amount": "Amount (₹)", "YearQuarter": "Period"},
                line_shape="spline"
            )
            fig.update_traces(line_color="#FF6F00", marker=dict(size=8))
            fig.update_layout(xaxis_tickangle=-30)

            st.plotly_chart(fig, use_container_width=True)

            st.info("💡 *Insight:* Sudden spikes or drops may indicate seasonal trends, new product launches, or policy shifts.")
        else:
            st.warning("No trend data available for selected filters.")

    # Map
    with tab5:
        st.subheader("🗺️ Insurance Transaction Map")
        filtered_map = filter_insurance_data(map_ins_country_df, selected_state, selected_year, selected_quarter)

        if not filtered_map.empty:
            district_summary = filtered_map.groupby(["District", "Latitude", "Longitude"])["Metric"].sum().reset_index()

            district_summary = district_summary.sort_values("Metric", ascending=False).head(40000)

            # Bubble Map using PyDeck
            max_metric = district_summary["Metric"].max()
            district_summary["radius"] = district_summary["Metric"] / max_metric * 50000  # scale radius

            district_summary["color"] = district_summary["Metric"].apply(
                lambda x: [255, int(255 - (x / max_metric) * 200), 0, 140]
            )

            layer = pdk.Layer(
                "ScatterplotLayer",
                data=district_summary,
                get_position='[Longitude, Latitude]',
                get_radius="radius",
                get_fill_color="color",
                pickable=True,
                auto_highlight=True,
            )

            view_state = pdk.ViewState(
                latitude=district_summary["Latitude"].mean(),
                longitude=district_summary["Longitude"].mean(),
                zoom=5,
                pitch=0,
            )

            st.pydeck_chart(pdk.Deck(
                layers=[layer],
                initial_view_state=view_state,
                tooltip={"text": "{District}\nMetric: {Metric}"}
            ))

            st.info("💡 *Insight:* Larger bubbles represent higher insurance transaction activity in those districts.")

        else:
            st.warning("No insurance map data available for selected filters.")

    # Penetration
    with tab6:
        st.subheader("📊 Insurance Penetration by State")
        filtered_meta = filter_insurance_data(map_ins_meta_df, selected_state, selected_year, selected_quarter)

        if not filtered_meta.empty:
            percentiles = ["P10", "P20", "P30", "P40", "P50", "P60", "P80", "P90", "P99_5"]
            melted_df = filtered_meta.melt(id_vars=["State"], value_vars=percentiles, var_name="Percentile", value_name="Value")

            fig = px.line(
                melted_df,
                x="Percentile",
                y="Value",
                color="State",
                markers=True,
                title="📈 Insurance Penetration Across States (Percentile View)"
            )
            fig.update_layout(xaxis_title="Percentile Level", yaxis_title="Penetration Value")
            st.plotly_chart(fig, use_container_width=True)

            st.info("💡 *Insight:* States with steep percentile curves have unequal insurance adoption — growth campaigns can focus on lower percentile regions.")
        else:
            st.warning("No penetration data found for selected filters.")

st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: grey;'>"
    "📊 Created by <b>Sai Sudharsan S G</b> | PhonePe Insights Dashboard"
    "</div>",
    unsafe_allow_html=True
)
