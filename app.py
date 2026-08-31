import streamlit as st
import pandas as pd
import joblib
import base64
import os

from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Car Price Prediction",
    page_icon="🚗",
    layout="wide"
)


# ============================================================
# BACKGROUND IMAGE FUNCTION
# ============================================================

def get_base64_image(image_path):

    if os.path.exists(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(
                image_file.read()
            ).decode()

    return None


# ============================================================
# LOAD BACKGROUND IMAGES
# ============================================================

background_image = get_base64_image("car_showroom_bg.png")
prediction_image = get_base64_image("prediction_bg.png")


# ============================================================
# BACKGROUND CSS
# ============================================================

if background_image:

    background_css = f"""
    background-image:
        linear-gradient(
            rgba(3, 8, 18, 0.70),
            rgba(3, 8, 18, 0.80)
        ),
        url("data:image/png;base64,{background_image}");

    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
    """

else:

    background_css = """
    background: linear-gradient(
        135deg,
        #020617,
        #0f172a
    );
    """


# ============================================================
# PREDICTION BACKGROUND CSS
# ============================================================

if prediction_image:

    prediction_background_css = f"""
    background-image:
        linear-gradient(
            rgba(0, 0, 0, 0.30),
            rgba(0, 0, 0, 0.45)
        ),
        url("data:image/png;base64,{prediction_image}");

    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    """

else:

    prediction_background_css = """
    background: linear-gradient(
        135deg,
        #7c5aa6,
        #5b3b85
    );
    """


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    f"""
<style>

/* ============================================================
   MAIN APP BACKGROUND
============================================================ */

.stApp {{
    {background_css}
}}


/* ============================================================
   REMOVE DEFAULT STREAMLIT ELEMENTS
============================================================ */

#MainMenu {{
    visibility: hidden;
}}

footer {{
    visibility: hidden;
}}

header {{
    background: transparent !important;
}}


/* ============================================================
   MAIN CONTAINER
============================================================ */

.block-container {{
    max-width: 1100px;
    padding-top: 45px;
    padding-bottom: 45px;
}}


/* ============================================================
   TITLE
============================================================ */

.main-title {{
    text-align: center;
    font-family: Georgia, "Times New Roman", serif;
    font-size: 50px;
    font-weight: 800;
    color: #FFFFFF;
    margin-bottom: 8px;

    text-shadow:
        0px 3px 10px
        rgba(0, 0, 0, 0.60);
}}


/* ============================================================
   SUBTITLE
============================================================ */

.sub-title {{
    text-align: center;
    font-size: 17px;
    color: #E2E8F0;
    font-weight: 500;
    margin-bottom: 30px;
}}


/* ============================================================
   DIVIDER
============================================================ */

hr {{
    border-color:
        rgba(255, 255, 255, 0.20) !important;
}}


/* ============================================================
   SECTION HEADING
============================================================ */

.section-heading {{
    font-size: 26px;
    font-weight: 750;
    color: #FFFFFF;

    margin-top: 30px;
    margin-bottom: 22px;

    text-shadow:
        0px 2px 8px
        rgba(0, 0, 0, 0.50);
}}


/* ============================================================
   INPUT LABELS
============================================================ */

.stSelectbox label,
.stNumberInput label,
.stSlider label {{
    color: #F8FAFC !important;
    font-weight: 600 !important;
}}


/* ============================================================
   SELECT BOX
============================================================ */

div[data-baseweb="select"] > div {{
    background-color:
        rgba(255, 255, 255, 0.95) !important;

    border-radius: 10px !important;
}}

div[data-baseweb="select"] span {{
    color: #1E293B !important;
}}


/* ============================================================
   NUMBER INPUT
============================================================ */

.stNumberInput input {{
    background-color:
        rgba(255, 255, 255, 0.95) !important;

    color: #1E293B !important;

    border-radius: 8px !important;
}}

div[data-baseweb="input"] {{
    background-color:
        rgba(255, 255, 255, 0.95) !important;

    border-radius: 8px !important;
}}


/* ============================================================
   SLIDER
============================================================ */

.stSlider {{
    color: #FFFFFF !important;
}}


/* ============================================================
   PREDICT BUTTON
============================================================ */

.stButton > button {{
    width: 100%;
    height: 58px;

    border-radius: 12px;

    background: linear-gradient(
        135deg,
        #F4F0F5,
        #E2DDE5
    );

    color: #2D2433 !important;

    font-size: 22px;
    font-weight: 1000 !important;
    letter-spacing: 0.2px;

    border: 1px solid rgba(255,255,255,0.60);

    transition: all 0.3s ease;
}}


.stButton > button:hover {{
    background: linear-gradient(
        135deg,
        #F8F5F9,
        #EAE1EC
    ) !important;

    color: #1F1724 !important;

    transform: translateY(-2px);
}}


/* ============================================================
   DOWNLOAD BUTTON
============================================================ */

.stDownloadButton > button {{
    width: 100%;
    height: 54px;

    border-radius: 12px;

    background: linear-gradient(
        135deg,
        #16A34A,
        #15803D
    );

    color: #FFFFFF;

    font-size: 17px;
    font-weight: 600;

    border: none;

    box-shadow:
        0px 6px 16px
        rgba(22, 163, 74, 0.30);

    transition: all 0.3s ease;
}}


.stDownloadButton > button:hover {{
    background: linear-gradient(
        135deg,
        #22C55E,
        #16A34A
    );

    transform: translateY(-2px);
}}


/* ============================================================
   PREDICTION CARD
============================================================ */

.prediction-card {{
    {prediction_background_css}

    min-height: 265px;

    padding: 35px 25px;

    border-radius: 22px;

    text-align: center;

    margin-top: 20px;
    margin-bottom: 25px;

    display: flex;
    flex-direction: column;

    justify-content: center;
    align-items: center;

    border:
        1px solid rgba(255, 255, 255, 0.35);

    box-shadow:
        0px 12px 30px
        rgba(0, 0, 0, 0.55);
}}


/* ============================================================
   PREDICTION LABEL
============================================================ */

.prediction-label {{
    color: #FFFFFF !important;

    font-size: 22px !important;

    font-weight: 700 !important;

    margin-bottom: 20px !important;

    line-height: 1.3 !important;

    text-shadow:
        0px 2px 8px
        rgba(0, 0, 0, 0.95) !important;
}}


/* ============================================================
   PREDICTION PRICE
============================================================ */

.prediction-price {{
    color: #FFFFFF !important;

    font-size: 58px !important;

    font-weight: 800 !important;

    line-height: 1.2 !important;

    margin: 0 !important;

    padding: 0 !important;

    text-shadow:
        0px 4px 12px
        rgba(0, 0, 0, 0.95) !important;
}}


/* ============================================================
   DATAFRAME
============================================================ */

[data-testid="stDataFrame"] {{
    background-color:
        rgba(255, 255, 255, 0.98);

    border-radius: 12px;
}}


/* ============================================================
   SUCCESS MESSAGE
============================================================ */

.stAlert {{
    background-color:
        rgba(220, 252, 231, 0.96);

    border-radius: 12px;

    border:
        1px solid rgba(134, 239, 172, 0.90);
}}


/* ============================================================
   EXPANDER
============================================================ */

.streamlit-expanderHeader {{
    background-color:
        rgba(255, 255, 255, 0.95);

    border-radius: 10px;

    color: #1E293B !important;
}}


/* ============================================================
   FOOTER
============================================================ */

.footer-note {{
    text-align: center;

    color: #FFFFFF;

    font-size: 14px;

    padding: 15px;

    background-color:
        rgba(15, 23, 42, 0.80);

    border-radius: 10px;

    font-weight: 500;

    border:
        1px solid rgba(255, 255, 255, 0.15);
}}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    return pd.read_csv("cleaned_car_data.csv")


# ============================================================
# LOAD MODEL
# ============================================================

@st.cache_resource
def load_model():
    return joblib.load("car_price_model.pkl")


# ============================================================
# LOAD FILES
# ============================================================

try:
    df = load_data()

except FileNotFoundError:
    st.error(" cleaned_car_data.csv file was not found.")
    st.stop()


try:
    model = load_model()

except FileNotFoundError:
    st.error(" car_price_model.pkl file was not found.")
    st.stop()


# ============================================================
# FORMAT PRICE FUNCTION
# ============================================================

def format_price(price):

    if price >= 10000000:
        return f"₹ {price / 10000000:.2f} Crore"

    return f"₹ {price / 100000:.2f} Lakh"


# ============================================================
# CREATE PDF REPORT
# ============================================================

def create_pdf_report(
    brand,
    car_name,
    model_name,
    vehicle_age,
    km_driven,
    fuel_type,
    transmission_type,
    engine,
    max_power,
    mileage,
    seats,
    seller_type,
    display_price
):

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    elements = []

    styles = getSampleStyleSheet()


    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        fontSize=22,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#1e3a5f"),
        spaceAfter=10
    )


    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontSize=11,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#64748b"),
        spaceAfter=20
    )


    elements.append(
        Paragraph(
            "Car Price Prediction Report",
            title_style
        )
    )

    elements.append(
        Paragraph(
            "Estimated Market Selling Price Report",
            subtitle_style
        )
    )


    price_data = [
        [
            "Estimated Selling Price",
            display_price
        ]
    ]


    price_table = Table(
        price_data,
        colWidths=[
            3.2 * inch,
            2.2 * inch
        ]
    )


    price_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, -1),
                colors.HexColor("#ede9fe")
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, -1),
                colors.HexColor("#5b3b85")
            ),
            (
                "FONTNAME",
                (0, 0),
                (-1, -1),
                "Helvetica-Bold"
            ),
            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                13
            ),
            (
                "ALIGN",
                (0, 0),
                (-1, -1),
                "CENTER"
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),
            (
                "BOX",
                (0, 0),
                (-1, -1),
                1,
                colors.HexColor("#a78bfa")
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.HexColor("#cbd5e1")
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                12
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                12
            )
        ])
    )

    elements.append(price_table)
    elements.append(Spacer(1, 25))


    table_data = [

        ["Category", "Detail", "Value"],

        ["Vehicle", "Brand", str(brand)],
        ["Vehicle", "Car Name", str(car_name)],
        ["Vehicle", "Model", str(model_name)],
        ["Vehicle", "Vehicle Age", f"{vehicle_age} Years"],
        ["Vehicle", "KM Driven", f"{km_driven:,} km"],

        ["Specifications", "Fuel Type", str(fuel_type)],
        ["Specifications", "Transmission Type", str(transmission_type)],
        ["Specifications", "Engine", f"{engine:,} CC"],
        ["Specifications", "Max Power", f"{max_power:.2f} BHP"],

        ["Additional Details", "Mileage", f"{mileage:.2f} km/l"],
        ["Additional Details", "Seats", str(seats)],
        ["Additional Details", "Seller Type", str(seller_type)],

        ["Prediction", "Estimated Selling Price", str(display_price)]

    ]


    report_table = Table(
        table_data,
        colWidths=[
            1.7 * inch,
            2.2 * inch,
            2.2 * inch
        ],
        repeatRows=1
    )


    report_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor("#6d4c9b")
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),
            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),
            (
                "ALIGN",
                (0, 0),
                (-1, 0),
                "CENTER"
            ),
            (
                "BACKGROUND",
                (0, 1),
                (-1, -1),
                colors.white
            ),
            (
                "TEXTCOLOR",
                (0, 1),
                (-1, -1),
                colors.HexColor("#1e293b")
            ),
            (
                "FONTNAME",
                (0, 1),
                (-1, -1),
                "Helvetica"
            ),
            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                10
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.HexColor("#cbd5e1")
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                9
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                9
            )
        ])
    )

    elements.append(report_table)
    elements.append(Spacer(1, 25))


    note_style = ParagraphStyle(
        "Note",
        parent=styles["Normal"],
        fontSize=9,
        textColor=colors.HexColor("#64748b"),
        alignment=TA_CENTER
    )


    elements.append(
        Paragraph(
            "Note: This predicted price is an estimated market selling price generated using a Machine Learning model.",
            note_style
        )
    )


    document.build(elements)

    buffer.seek(0)

    return buffer.getvalue()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🚗 Car Price Prediction</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Enter your vehicle details and get an estimated market selling price.</div>',
    unsafe_allow_html=True
)

st.divider()


# ============================================================
# ENTER CAR DETAILS
# ============================================================

st.markdown(
    '<div class="section-heading">🚘 Enter Car Details</div>',
    unsafe_allow_html=True
)


# ============================================================
# ROW 1
# ============================================================

col1, col2, col3 = st.columns(3)


with col1:

    brand = st.selectbox(
        "Brand",
        sorted(
            df["brand"]
            .dropna()
            .astype(str)
            .unique()
        )
    )


with col2:

    brand_cars = df[
        df["brand"].astype(str) == str(brand)
    ]

    car_name = st.selectbox(
        "Car Name",
        sorted(
            brand_cars["car_name"]
            .dropna()
            .astype(str)
            .unique()
        )
    )


with col3:

    selected_car_data = brand_cars[
        brand_cars["car_name"].astype(str)
        == str(car_name)
    ]

    model_name = st.selectbox(
        "Model",
        sorted(
            selected_car_data["model"]
            .dropna()
            .astype(str)
            .unique()
        )
    )


# ============================================================
# FILTER SELECTED DATA
# ============================================================

selected_data = df[
    (df["brand"].astype(str) == str(brand))
    &
    (df["car_name"].astype(str) == str(car_name))
    &
    (df["model"].astype(str) == str(model_name))
]


if selected_data.empty:

    selected_data = df[
        (df["brand"].astype(str) == str(brand))
        &
        (df["car_name"].astype(str) == str(car_name))
    ]


# ============================================================
# DEFAULT VALUES
# ============================================================

default_age = int(selected_data["vehicle_age"].median())
default_km = int(selected_data["km_driven"].median())
default_mileage = float(selected_data["mileage"].median())
default_engine = int(selected_data["engine"].median())
default_power = float(selected_data["max_power"].median())


# ============================================================
# ROW 2
# ============================================================

col1, col2, col3 = st.columns(3)


with col1:

    vehicle_age = st.slider(
        "Vehicle Age (Years)",
        min_value=int(df["vehicle_age"].min()),
        max_value=int(df["vehicle_age"].max()),
        value=default_age
    )


with col2:

    km_driven = st.number_input(
        "KM Driven",
        min_value=0,
        value=default_km,
        step=1000
    )


with col3:

    seller_type = st.selectbox(
        "Seller Type",
        sorted(
            selected_data["seller_type"]
            .dropna()
            .astype(str)
            .unique()
        )
    )


# ============================================================
# ROW 3
# ============================================================

col1, col2, col3 = st.columns(3)


with col1:

    fuel_type = st.selectbox(
        "Fuel Type",
        sorted(
            selected_data["fuel_type"]
            .dropna()
            .astype(str)
            .unique()
        )
    )


with col2:

    transmission_type = st.selectbox(
        "Transmission Type",
        sorted(
            selected_data["transmission_type"]
            .dropna()
            .astype(str)
            .unique()
        )
    )


with col3:

    seats = st.selectbox(
        "Seats",
        sorted(
            selected_data["seats"]
            .dropna()
            .unique()
        )
    )


# ============================================================
# ROW 4
# ============================================================

col1, col2, col3 = st.columns(3)


with col1:

    mileage = st.number_input(
        "Mileage (km/l)",
        min_value=0.0,
        value=default_mileage,
        step=0.1
    )


with col2:

    engine = st.number_input(
        "Engine (CC)",
        min_value=0,
        value=default_engine,
        step=50
    )


with col3:

    max_power = st.number_input(
        "Max Power (BHP)",
        min_value=0.0,
        value=default_power,
        step=1.0
    )


# ============================================================
# SPACE
# ============================================================

st.write("")
st.write("")


# ============================================================
# PREDICT BUTTON
# ============================================================

predict_button = st.button(
    "🔮 Predict Car Price",
    width="stretch"
)


# ============================================================
# PREDICTION
# ============================================================

if predict_button:


    # CREATE INPUT DATA

    input_data = pd.DataFrame({

        "car_name": [car_name],
        "brand": [brand],
        "model": [model_name],
        "vehicle_age": [vehicle_age],
        "km_driven": [km_driven],
        "seller_type": [seller_type],
        "fuel_type": [fuel_type],
        "transmission_type": [transmission_type],
        "mileage": [mileage],
        "engine": [engine],
        "max_power": [max_power],
        "seats": [seats]

    })


    # MAKE PREDICTION

    prediction = model.predict(input_data)

    predicted_price = float(prediction[0])

    display_price = format_price(predicted_price)


    # PREDICTED PRICE HEADING

    st.markdown(
        '<div class="section-heading">📈 Predicted Price</div>',
        unsafe_allow_html=True
    )


    # PREDICTION CARD

    st.markdown(
        f"""
        <div class="prediction-card">
            <div class="prediction-label">
                Estimated Market Selling Price
            </div>
            <div class="prediction-price">
                {display_price}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


    # SUCCESS MESSAGE

    st.success(
        f"Prediction completed successfully for "
        f"{brand} {car_name}!"
    )


    # VEHICLE DETAILS

    st.markdown(
        '<div class="section-heading">📋 Vehicle Details</div>',
        unsafe_allow_html=True
    )


    # CREATE REPORT DATA

    detailed_report = pd.DataFrame({

        "Category": [
            "Vehicle",
            "Vehicle",
            "Vehicle",
            "Vehicle",
            "Vehicle",

            "Specifications",
            "Specifications",
            "Specifications",
            "Specifications",

            "Additional Details",
            "Additional Details",
            "Additional Details",

            "Prediction"
        ],

        "Details": [
            "Brand",
            "Car Name",
            "Model",
            "Vehicle Age",
            "KM Driven",

            "Fuel Type",
            "Transmission Type",
            "Engine",
            "Max Power",

            "Mileage",
            "Seats",
            "Seller Type",

            "Estimated Selling Price"
        ],

        "Value": [
            str(brand),
            str(car_name),
            str(model_name),
            f"{vehicle_age} Years",
            f"{km_driven:,} km",

            str(fuel_type),
            str(transmission_type),
            f"{engine:,} CC",
            f"{max_power:.2f} BHP",

            f"{mileage:.2f} km/l",
            str(seats),
            str(seller_type),

            str(display_price)
        ]

    })


    detailed_report = detailed_report.astype(str)


    # DISPLAY REPORT

    st.dataframe(
        detailed_report,
        width="stretch",
        hide_index=True
    )


    st.write("")


    # CREATE PDF

    pdf_file = create_pdf_report(

        brand,
        car_name,
        model_name,
        vehicle_age,
        km_driven,
        fuel_type,
        transmission_type,
        engine,
        max_power,
        mileage,
        seats,
        seller_type,
        display_price

    )


    # DOWNLOAD PDF

    download_col1, download_col2, download_col3 = st.columns(
        [1, 2, 1]
    )


    with download_col2:

        st.download_button(

            label="📄 Download Vehicle Report as PDF",

            data=pdf_file,

            file_name=f"{brand}_{car_name}_Price_Report.pdf",

            mime="application/pdf",

            width="stretch"

        )


    # COMPLETE INPUT DETAILS

    with st.expander(
        "🔍 View Complete Input Details"
    ):

        input_display = input_data.astype(str)

        st.dataframe(
            input_display,
            width="stretch",
            hide_index=True
        )


# ============================================================
# FOOTER
# ============================================================

st.write("")

st.divider()


st.markdown(
    """
    <div class="footer-note">
    💡 Note: The predicted price is an estimated market selling price generated using a trained Machine Learning model.
    </div>
    """,
    unsafe_allow_html=True
)