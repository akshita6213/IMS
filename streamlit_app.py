import streamlit as st
import pandas as pd

# Load the data
data_path = 'data/data.csv'


@st.cache_data
def load_data():
    return pd.read_csv(data_path)


data = load_data()

# Combine 'YEAR' and 'MONTH' into a 'Date' column
data['Date'] = pd.to_datetime(data['YEAR'].astype(str) + '-' + data['MONTH'].astype(str) + '-01')

# Custom CSS for enhanced UI
st.markdown("""
    <style>
        /* General App Styling */
        .reportview-container {
            background: #f8f9fa;
            color: #333;
        }
        .css-1y0vyt0 {
            background-color: #007bff;
        }
        .css-1y0vyt0 h1, .css-1y0vyt0 h2, .css-1y0vyt0 h3, .css-1y0vyt0 h4, .css-1y0vyt0 h5, .css-1y0vyt0 h6, .css-1y0vyt0 p, .css-1y0vyt0 div, .css-1y0vyt0 span {
            color: #fff;
        }
        .stButton>button {
            color: #fff;
            background-color: #28a745;
            border: none;
            border-radius: 5px;
            padding: 10px 24px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            transition-duration: 0.4s;
        }
        .stButton>button:hover {
            background-color: #218838;
        }
        .stTextInput>div>div>input {
            border-radius: 5px;
            padding: 10px;
            border: 2px solid #007bff;
            transition: border-color 0.2s;
        }
        .stTextInput>div>div>input:focus {
            border-color: #0056b3;
        }
        .stNumberInput>div>div>input {
            border-radius: 5px;
            padding: 10px;
            border: 2px solid #007bff;
            transition: border-color 0.2s;
        }
        .stNumberInput>div>div>input:focus {
            border-color: #0056b3;
        }
        .stSelectbox>div>div>div {
            border-radius: 5px;
            border: 2px solid #007bff;
        }
        .stSelectbox>div>div>div:hover {
            border-color: #0056b3;
        }
        /* Sidebar Styling */
        .sidebar .sidebar-content {
            background: #007bff;
            color: #fff;
            padding-top: 2rem;
        }
        .sidebar .sidebar-content h1, .sidebar .sidebar-content h2, .sidebar .sidebar-content h3, .sidebar .sidebar-content h4, .sidebar .sidebar-content h5, .sidebar .sidebar-content h6, .sidebar .sidebar-content p, .sidebar .sidebar-content div, .sidebar .sidebar-content span {
            color: #fff;
        }
        .sidebar .sidebar-content .stRadio>div>label {
            color: #fff;
        }
        .sidebar .sidebar-content .stRadio>div>label:hover {
            color: #f8f9fa;
        }
        .stSidebar .stSidebarHeader {
            border-bottom: 1px solid #0056b3;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar Navigation with Icons
st.sidebar.title("Navigation")
page = st.sidebar.radio("", ["🏠 Home", "🛠️ Manage Items", "📈 Sales Forecasting", "📊 Sales Details"])

# Page Layout
if page == "🏠 Home":
    st.title("Welcome to Inventory Management System")
    st.image("data/image.png", caption="Welcome to Our Inventory Management System", use_column_width=True)
    st.write("""
        **Welcome!** Here you can manage your inventory, view item sales, and access sales forecasting tools.

        **Features:**
        - Manage items in your inventory
        - View item sales data
        - Access sales forecasting tools
        - View detailed sales information
    """)

elif page == "🛠️ Manage Items":
    st.title("Manage Inventory Items")

    # Display items
    st.subheader("Item Sales Data")
    item_sales = data.groupby('ITEM DESCRIPTION')['RETAIL SALES'].sum().reset_index()
    st.dataframe(item_sales)

    # Add a new item
    st.subheader("Add a New Item")
    item_desc = st.text_input("Item Description")
    year = st.number_input("Year", min_value=2000, max_value=2100, step=1)
    month = st.number_input("Month", min_value=1, max_value=12, step=1)
    sales = st.number_input("Retail Sales", min_value=0.0, step=0.01)

    if st.button("Add Item"):
        new_data = pd.DataFrame({
            'ITEM DESCRIPTION': [item_desc],
            'YEAR': [year],
            'MONTH': [month],
            'RETAIL SALES': [sales]
        })
        data = pd.concat([data, new_data], ignore_index=True)
        data.to_csv(data_path, index=False)
        st.success("Item added successfully!")

    # Delete an item
    st.subheader("Delete an Item")
    item_to_delete = st.selectbox("Select Item to Delete", data['ITEM DESCRIPTION'].unique())

    if st.button("Delete Item"):
        data = data[data['ITEM DESCRIPTION'] != item_to_delete]
        data.to_csv(data_path, index=False)
        st.success("Item deleted successfully!")

elif page == "📈 Sales Forecasting":
    st.title("Sales Forecasting")
    st.write("Access the sales forecasting tool [here](https://salesforecastak.streamlit.app/)")

elif page == "📊 Sales Details":
    st.title("Sales Details")

    # Select item
    st.subheader("View Sales Details")
    selected_item = st.selectbox("Select Item", data['ITEM DESCRIPTION'].unique())

    # Get details for the selected item
    if selected_item:
        item_data = data[data['ITEM DESCRIPTION'] == selected_item]
        total_sales = item_data['RETAIL SALES'].sum()
        supplier = item_data['SUPPLIER'].unique()

        st.write(f"**Item Description:** {selected_item}")
        st.write(f"**Total Sales:** ${total_sales:.2f}")
        st.write(f"**Supplier:** {', '.join(supplier)}")
