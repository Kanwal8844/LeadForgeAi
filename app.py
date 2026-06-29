import streamlit as st
import pandas as pd
import sqlite3
import time
from scraper import run_lead_scraper

# --- DATABASE SETUP ---
conn = sqlite3.connect('users.db', check_same_thread=False)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, searches INTEGER, is_paid INTEGER)')
c.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, email TEXT, message TEXT)')
conn.commit()

# --- PROFESSIONAL CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .review-card { background: #1c2026; padding: 15px; border-radius: 10px; border: 1px solid #333; margin-bottom: 10px; }
    .stButton>button { width: 100%; border-radius: 5px; background-color: #007BFF; color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.markdown("## ⚙️ **LeadForge Pro Panel**")

with st.sidebar.expander("💳 Upgrade to Pro ($20/mo)", expanded=True):
    st.write("Payoneer: `hussantv70@gmail.com`")
    st.code("031100209")
    st.write("PayPal: `lalababy339@gmail.com`")
    st.code("TQJspttZKoTCStwvneek6pSZUKK3C7dWMn")
    st.markdown("---")
    st.markdown("📩 **Payment ke baad Screenshot WhatsApp karein:**")
    st.link_button("💬 WhatsApp Support", "https://wa.me/923404462517")

# --- MAIN DASHBOARD ---
st.markdown("<h1 style='text-align: center; color: #007BFF;'>🚀 LeadForge Pro</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    user_email = st.text_input("📧 Enter your Gmail:")
    business_type = st.text_input("🏢 Business Type (e.g., Plumbers)")
    location = st.text_input("📍 Location (e.g., New York)")
    
    if st.button("🚀 START HUNTING"):
        if not user_email: 
            st.error("Please enter your email to start.")
        else:
            # Check for free search
            c.execute('SELECT searches FROM users WHERE email = ?', (user_email,))
            data = c.fetchone()
            if data and data[0] >= 1:
                st.warning("⚠️ Free search limit reached. Please Upgrade to Pro!")
            else:
                with st.spinner("Scraping real-time data..."):
                    df = run_lead_scraper(business_type, location)
                    if df is not None and not df.empty:
                        st.success(f"✅ Found {len(df)} leads!")
                        st.dataframe(df)
                        # Save search count in DB
                        c.execute('INSERT OR REPLACE INTO users (email, searches) VALUES (?, ?)', (user_email, 1))
                        conn.commit()
                        st.download_button("💾 DOWNLOAD CSV", df.to_csv(index=False), "leads.csv", "text/csv")
                    else:
                        st.warning("⚠️ No leads found. Try a different city.")

with col2:
    st.markdown("### ⭐ **Trusted by Professionals**")
    reviews = [
        ("John D.", "Excellent tool, saved me so much time!"),
        ("Sarah K.", "The quality of leads is top-notch."),
        ("Ali R.", "Best lead scraper I have ever used."),
        ("Mike T.", "Very fast and accurate results."),
        ("Emma W.", "My sales pipeline is full now."),
        ("David L.", "Highly recommended for B2B."),
        ("Kevin S.", "Worth every penny for the data accuracy!")
    ]
    for name, review in reviews:
        st.markdown(f"<div class='review-card'><b>{name}</b><br>{review}</div>", unsafe_allow_html=True)

# Admin Section
with st.sidebar.expander("Admin Control"):
    if st.text_input("Admin Key", type="password") == "Admin123":
        if st.button("View Messages"):
            for msg in c.execute('SELECT * FROM messages').fetchall():
                st.write(f"**{msg[1]}**: {msg[2]}")