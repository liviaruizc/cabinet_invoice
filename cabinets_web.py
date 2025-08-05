import streamlit as st
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER
import tempfile
from datetime import datetime
import os

# --- Classes ---

class CartManager:
    def __init__(self):
        if 'cart' not in st.session_state:
            st.session_state.cart = []

    def add_item(self, item_name, item_type, qty, unit_price, original_price):
        total = qty * unit_price
        st.session_state.cart.append({
            "type": item_type,
            "item": item_name,
            "qty": qty,
            "final": unit_price,
            "original": original_price,
            "total": total
        })

    def clear_cart(self):
        st.session_state.cart = []

    def get_cart(self):
        return st.session_state.cart

    def get_totals(self):
        subtotal = sum(item["total"] for item in st.session_state.cart)
        tax = subtotal * 0.065
        final = subtotal + tax
        return subtotal, tax, final

class ReceiptGenerator:
    def __init__(self, cart):
        self.cart = cart

    def create_pdf(self):
        import tempfile
        from PIL import Image

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            c = canvas.Canvas(tmp.name, pagesize=LETTER)
            width, height = LETTER
            y = height - 50

            # Header (logo & business info can go here)
            c.setFont('Helvetica-Bold', 14)
            c.drawString(50, y - 10, "Mike Renovations LLC")
            c.setFont('Helvetica', 10)
            c.drawString(50, y - 25, "Phone: 239-200-5772")
            c.drawString(50, y - 40, "Email: contact@mikerenovations.com")

            y -= 30

            # Invoice title and date
            c.setFont("Helvetica", 9)
            c.drawString(450, y, datetime.now().strftime("%Y-%m-%d %H:%M"))
            y -= 30

            # Table headers
            c.setFont("Helvetica-Bold", 10)
            c.drawString(50, y, "TYPE")
            c.drawString(150, y, "ITEM")
            c.drawString(280, y, "PRICE W/O DISCOUNT")
            c.drawString(410, y, "QTY")
            c.drawString(460, y, "FINAL PRICE $")
            c.drawString(540, y, "TOTAL $")
            y -= 15
            c.line(50, y, 570, y)
            y -= 15

            # Rows
            c.setFont("Helvetica", 9)
            total_sum = 0
            price_without_discount = 0
            for entry in self.cart:
                c.drawString(50, y, entry["type"])
                c.drawString(150, y, entry["item"][:30])
                c.drawRightString(390, y, f"${entry['original']:.2f}")
                c.drawRightString(430, y, str(entry["qty"]))
                c.drawRightString(510, y, f"${entry['final']:.2f}")
                c.drawRightString(570, y, f"${entry['total']:.2f}")
                y -= 18
                total_sum += entry["total"]
                price_without_discount += entry["original"] * entry["qty"]
                if y < 100:
                    c.showPage()
                    y = height - 50

            # Totals section
            tax = total_sum * 0.065
            final = total_sum + tax

            y -= 20
            c.setFont("Helvetica-Bold", 10)
            c.line(50, y, 570, y)
            y -= 15
            c.drawRightString(510, y, "Price Without Discount:")
            c.drawRightString(570, y, f"${price_without_discount:.2f}")
            y -= 15
            c.drawRightString(510, y, "Subtotal (with discount):")
            c.drawRightString(570, y, f"${total_sum:.2f}")
            y -= 15
            c.drawRightString(510, y, "Tax (6.5%):")
            c.drawRightString(570, y, f"${tax:.2f}")
            y -= 15
            c.drawRightString(510, y, "Final Total:")
            c.drawRightString(570, y, f"${final:.2f}")

            c.save()
            return tmp.name


# --- Load and preprocess data ---
@st.cache_data
def load_data():
    df = pd.read_excel("cabinets_price.xlsx")
    df['TYPES_clean'] = df['TYPES'].str.strip().str.lower()
    return df

df = load_data()
types = df['TYPES_clean'].unique()
pretty_names = [t.title() for t in types]
pretty_to_clean = dict(zip(pretty_names, types))

# --- Streamlit UI ---

st.title("🧰 Cabinet Order System")

cart = CartManager()

selected_type = st.selectbox("Select cabinet type", pretty_names)

filtered_df = df[df['TYPES_clean'] == pretty_to_clean[selected_type]]

selected_item = st.selectbox("Select an item", filtered_df['ITEM'].tolist())
quantity = st.number_input("Quantity", min_value=1, value=1)

if st.button("Add to Cart"):
    item = filtered_df[filtered_df['ITEM'] == selected_item].iloc[0]
    cart.add_item(
        item_name=item['ITEM'],
        item_type=selected_type,
        qty=quantity,
        unit_price=item['FINAL PRICE'],
        original_price=item['ORIGINAL PRICE']
    )
if st.button("Clear Cart"):
    cart.clear_cart()

# Show cart
cart_items = cart.get_cart()
if cart_items:
    st.subheader("🛒 Cart")
    df_cart = pd.DataFrame(cart_items)
    st.table(df_cart[['type', 'item', 'qty', 'original', 'final', 'total']])
else:
    st.info("Cart is empty")


# Generate PDF receipt
if st.button("Generate PDF Invoice"):
    if cart_items:
        receipt = ReceiptGenerator(cart_items)
        pdf_path = receipt.create_pdf()
        with open(pdf_path, "rb") as f:
            st.download_button("📄 Download Invoice", f, file_name="invoice.pdf", mime="application/pdf")
    else:
        st.warning("Your cart is empty!")


