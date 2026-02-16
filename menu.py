import streamlit as st
import pandas as pd
from datetime import datetime


st.set_page_config(page_title="რესტორნის სისტემა", layout="wide")


menu_data = {
    "ცივი კერძები": {
        "პური": 2.0, "ყველი": 15.0, "მჟავე": 8.0, "ზეთის ხილი": 7.0,
        "იკრა+კარაქი": 25.0, "სათალი": 18.0, "ბადრიჯანი": 12.0, "ცეზარი": 18.0
    },
    "ცხელი კერძები": {
        "ხაშლამა": 25.0, "ოსტრი": 16.0, "ჩაქაფული": 22.0, "ტოლმა": 15.0,
        "ქაბაბი": 15.0, "შილა ფლავი": 12.0, "გოჭი": 25.0, "სოკო კეცზე": 12.0
    },
    "თევზეული": {
        "ხეკი შემწვარი": 15.0, "კალმახი შემწვარი": 16.0, "ორაგული": 28.0, "სიომგა": 35.0
    },
    "სასმელები": {
        "ლიმონათი": 3.5, "მინერალური": 2.5, "ღვინო (1ლ)": 15.0
    }
}


if 'cart' not in st.session_state:
    st.session_state.cart = []

st.title("🍽️ რესტორნის მართვის პანელი")


st.sidebar.header("🔍 ძებნა")
search_query = st.sidebar.text_input("ჩაწერეთ კერძის სახელი").lower()

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📜 მენიუ")
    for category, items in menu_data.items():
        with st.expander(category, expanded=True):
            for item, price in items.items():
                if search_query in item.lower():
                    c1, c2, c3 = st.columns([3, 1, 1])
                    c1.write(f"**{item}** - {price} GEL")
                    qty = c2.number_input(f"რაოდ.", min_value=1, value=1, key=f"qty_{item}")
                    if c3.button("➕", key=f"add_{item}"):
                        st.session_state.cart.append({"კერძი": item, "ფასი": price, "რაოდენობა": qty, "ჯამი": price * qty})
                        st.toast(f"{item} დაემატა!")


with col2:
    st.subheader("🧾 კალათა")
    if st.session_state.cart:
        df = pd.DataFrame(st.session_state.cart)
        st.table(df[["კერძი", "რაოდენობა", "ჯამი"]])
        
        subtotal = df["ჯამი"].sum()
        service = subtotal * 0.10
        total = subtotal + service
        
        st.write(f"**ჯამი:** {subtotal:.2f} GEL")
        st.write(f"**მომსახურება (10%):** {service:.2f} GEL")
        st.divider()
        st.write(f"### 💰 სულ: {total:.2f} GEL")
        
        if st.button("🗑️ კალათის გასუფთავება"):
            st.session_state.cart = []
            st.rerun()
            
        if st.button("✅ შეკვეთის დასრულება"):
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            receipt_text = f"შეკვეთა - {now}\n" + df.to_string() + f"\n\nსულ: {total:.2f} GEL"
            st.download_button("📥 ჩეკის ჩამოტვირთვა", receipt_text, file_name=f"receipt_{now}.txt")
    else:
        st.info("კალათა ცარიელია")