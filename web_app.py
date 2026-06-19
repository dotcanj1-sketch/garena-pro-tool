import streamlit as st
import requests
import json
import urllib.parse
import urllib3
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- PAGE CONFIGURATION (Yeh hamesha top par hona chahiye) ---
st.set_page_config(page_title="Arafat Bind Tool VIP", page_icon="💎", layout="centered", initial_sidebar_state="expanded")

# --- PREMIUM CUSTOM CSS ---
st.markdown("""
    <style>
    /* Dark Premium Background */
    .stApp { background-color: #0b0f19; color: #e2e8f0; }
    
    /* Hide Default Streamlit Watermarks */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Neon Gradient Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #ff007f 0%, #7928ca 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 24px;
        font-size: 16px;
        font-weight: 700;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 0, 127, 0.4);
        width: 100%;
    }
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(255, 0, 127, 0.6);
        color: white;
    }
    
    /* Premium Input Fields */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 1px solid #1e293b;
        background-color: #161b22;
        color: #00ffff;
        padding: 14px;
        font-family: monospace;
        font-size: 15px;
    }
    .stTextInput > div > div > input:focus {
        border-color: #00ffff;
        box-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
    }
    
    /* Data Display Cards */
    .premium-card {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 20px;
        border-left: 5px solid #00ffff;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
    }
    .premium-card h4 { color: #fff; margin-top: 0; }
    .data-row { display: flex; justify-content: space-between; border-bottom: 1px solid #1f2937; padding: 10px 0; }
    .data-label { color: #9ca3af; font-weight: 600; }
    .data-value { color: #34d399; font-weight: bold; font-family: monospace; }
    
    /* Main Title Styling */
    .main-title {
        text-align: center;
        background: -webkit-linear-gradient(#00ffff, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        font-size: 2.5rem;
        margin-bottom: 0;
    }
    </style>
""", unsafe_allow_html=True)

# --- HELPER FUNCTIONS ---
def convert_seconds(s):
    d, h = divmod(s, 86400)
    h, m = divmod(h, 3600)
    m, s = divmod(m, 60)
    return f"{d}d {h}h {m}m {s}s"

# --- HEADER SECTION ---
st.markdown("<h1 class='main-title'>💎 ARAFAT PRO TOOL</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #9ca3af; margin-bottom: 30px;'>Secure & Lightning Fast Bind Management</p>", unsafe_allow_html=True)

# --- PREMIUM SIDEBAR ---
st.sidebar.markdown("<h2 style='text-align: center; color: #00ffff;'>Navigation</h2>", unsafe_allow_html=True)
menu_options = {
    "🔍 Check Bind Info": "check_info",
    "🔑 Generate Access Token": "eat_token",
    "🗑️ Revoke Token": "revoke",
    "👨‍💻 Owner Details": "owner"
}
choice = st.sidebar.radio("", list(menu_options.keys()))
st.sidebar.divider()
st.sidebar.markdown("<p style='text-align: center; color: #6b7280; font-size: 12px;'>v2.0 Premium Edition</p>", unsafe_allow_html=True)

# --- APP LOGIC & UI ---

if menu_options[choice] == "owner":
    st.markdown("""
    <div class='premium-card' style='border-left-color: #ff007f;'>
        <h4>👨‍💻 Developer Information</h4>
        <div class='data-row'><span class='data-label'>Name</span><span class='data-value' style='color:#00ffff;'>SPIDEY</span></div>
        <div class='data-row'><span class='data-label'>Telegram</span><span class='data-value'>@ARAFAT_CONTACG</span></div>
        <div class='data-row'><span class='data-label'>Channel</span><span class='data-value'>t.me/arafat_source</span></div>
        <div class='data-row'><span class='data-label'>Status</span><span class='data-value' style='color:#ff007f;'>Premium Verified ✓</span></div>
    </div>
    """, unsafe_allow_html=True)

elif menu_options[choice] == "check_info":
    st.markdown("### 🔍 Account Binding Status")
    access_token = st.text_input("Paste Access Token Here:", placeholder="ey...")
    
    if st.button("Fetch Details"):
        if not access_token:
            st.error("⚠️ Please enter a valid token!")
        else:
            with st.spinner("Decrypting data from server..."):
                try:
                    # Player Info Request
                    player_url = f"https://api-otrss.garena.com/support/callback/?access_token={access_token}"
                    p_res = requests.get(player_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15, allow_redirects=True)
                    query_params = urllib.parse.parse_qs(urllib.parse.urlparse(p_res.url).query)
                    
                    uid = query_params.get("account_id", ["Unknown"])[0]
                    nickname = urllib.parse.unquote(query_params.get("nickname", ["Unknown"])[0])
                    
                    # Bind Info Request
                    url = "https://100067.connect.garena.com/game/account_security/bind:get_bind_info"
                    response = requests.get(url, params={'app_id': "100067", 'access_token': access_token}, headers={'User-Agent': "GarenaMSDK/4.0.30"}, timeout=15)
                    
                    email, email_to_be, countdown = "N/A", "N/A", 0
                    if response.status_code == 200:
                        data = response.json()
                        email = data.get("email", "None") or "None"
                        email_to_be = data.get("email_to_be", "None") or "None"
                        countdown = data.get("request_exec_countdown", 0)

                    st.toast("Data fetched successfully!", icon="✅")
                    
                    # Beautiful Output Card
                    st.markdown(f"""
                    <div class='premium-card'>
                        <h4>🎮 Player Profile</h4>
                        <div class='data-row'><span class='data-label'>Nickname</span><span class='data-value' style='color:#fff;'>{nickname}</span></div>
                        <div class='data-row'><span class='data-label'>Account UID</span><span class='data-value' style='color:#ff007f;'>{uid}</span></div>
                        <br>
                        <h4>📧 Security Details</h4>
                        <div class='data-row'><span class='data-label'>Current Email</span><span class='data-value'>{email}</span></div>
                        <div class='data-row'><span class='data-label'>Pending Email</span><span class='data-value' style='color:#fbbf24;'>{email_to_be}</span></div>
                        <div class='data-row'><span class='data-label'>Unbind Countdown</span><span class='data-value'>{convert_seconds(countdown) if email_to_be != 'None' else 'N/A'}</span></div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.balloons() # Premium Celebration effect!
                except Exception as e:
                    st.error(f"Connection Failed: {e}")

elif menu_options[choice] == "eat_token":
    st.markdown("### 🔑 Token Generator")
    user_input = st.text_input("Enter EAT Token OR URL:", placeholder="https://api-otrss.garena.com/...")
    
    if st.button("Generate Secure Token"):
        if not user_input:
            st.error("⚠️ Input cannot be empty!")
        else:
            with st.spinner("Bypassing security layers..."):
                eat_token = user_input.strip()
                if "http" in user_input or "?" in user_input:
                    parsed_url = urllib.parse.urlparse(user_input)
                    if 'eat' in urllib.parse.parse_qs(parsed_url.query):
                        eat_token = urllib.parse.parse_qs(parsed_url.query)['eat'][0]
                
                api_url = f"https://api-otrss.garena.com/support/callback/?access_token={eat_token}"
                try:
                    res = requests.get(api_url, headers={"User-Agent": "Mozilla/5.0"}, allow_redirects=True, timeout=15)
                    final_params = urllib.parse.parse_qs(urllib.parse.urlparse(res.url).query)
                    
                    if 'access_token' in final_params:
                        acc_tok = final_params['access_token'][0]
                        nickname = urllib.parse.unquote(final_params.get('nickname', ['Unknown'])[0])
                        
                        st.markdown(f"""
                        <div class='premium-card' style='border-left-color: #34d399;'>
                            <h4 style='color: #34d399;'>✅ Token Generated</h4>
                            <div class='data-row'><span class='data-label'>Account</span><span class='data-value' style='color:#fff;'>{nickname}</span></div>
                            <br>
                            <span class='data-label'>Access Token:</span>
                            <div style='background: #000; padding: 10px; border-radius: 8px; margin-top: 5px; word-break: break-all; border: 1px solid #1f2937;'>
                                <code style='color: #00ffff;'>{acc_tok}</code>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.error("Token invalid or expired.")
                except Exception as e:
                    st.error("Error generating token.")

elif menu_options[choice] == "revoke":
    st.markdown("### 🗑️ Emergency Logout")
    st.info("💡 This will instantly log the account out from all external sessions.")
    access_token = st.text_input("Target Access Token:", type="password", placeholder="Paste token here to destroy session")
    
    if st.button("Revoke Access Instantly"):
        if not access_token:
            st.error("⚠️ Token is required!")
        else:
            with st.spinner("Sending termination signal..."):
                refresh_token = "1380dcb63ab3a077dc05bdf0b25ba4497c403a5b4eae96d7203010eafa6c83a8"
                logout_url = f"https://100067.connect.garena.com/oauth/logout?access_token={access_token}&refresh_token={refresh_token}"
                try:
                    res = requests.get(logout_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
                    if res.status_code == 200 and "error" not in res.text:
                        st.markdown("""
                        <div class='premium-card' style='border-left-color: #ef4444;'>
                            <h4 style='color: #ef4444;'>🚨 Session Terminated</h4>
                            <p style='color: #9ca3af;'>The access token has been completely revoked and logged out of Garena servers.</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.error("Failed to revoke token.")
                except Exception as e:
                    st.error("Server connection failed.")
                    