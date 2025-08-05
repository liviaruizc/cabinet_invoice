# 🛠️ Cabinet Order System

This is a user-friendly web app for managing cabinet orders, developed with **Python** and **Streamlit**.

It allows users to:
- Browse cabinets by type
- Add items with quantity to a shopping cart
- View totals with and without discounts
- Generate a PDF receipt with your company logo and contact info

---

## 🚀 Features

- 📂 Load cabinet data from an Excel file
- ✅ Clean and categorized dropdown selection
- ➕ Add / 🗑 Remove / 🧹 Clear cart
- 🧾 Generate printable PDF receipts
- 💲 Shows original and final prices
- 🖼 Customizable logo and header

---

## 📁 File Structure

cabinet-order-system/
├── cabinet_app_streamlit.py # Main app
├── cabinets_price.xlsx # Excel file with cabinet data
├── logo.jpg # Your company logo (optional)
├── requirements.txt # Python dependencies
└── README.md # This file

yaml
Copy
Edit

---

## 🔧 Requirements

- Python 3.8+
- Required Python packages:

streamlit
pandas
reportlab
pillow
openpyxl

cpp
Copy
Edit

Install them using:

```bash
pip install -r requirements.txt
📊 Excel Format (cabinets_price.xlsx)
Your Excel file must have at least the following columns:

TYPES	ITEM	ORIGINAL PRICE	FINAL PRICE
Base	B09	100.00	80.00
Wall	W1230	90.00	72.00

▶️ Running the App
In your terminal:

bash
Copy
Edit
streamlit run cabinets_web.py
The app will launch at (https://cabinetinvoice-generator.streamlit.app/).

If you're using Streamlit Cloud:

Push your project to GitHub

Go to https://streamlit.io/cloud

Connect your GitHub repo

Deploy your app with 1 click

🖨️ PDF Receipt
Receipts include:

Logo and business header (from logo.jpg)

Table with:

TYPE, ITEM, ORIGINAL PRICE, FINAL PRICE, QTY, TOTAL

Subtotal, tax, and grand total

Make sure the logo is named logo.jpg or logo.png and located in the same folder.
