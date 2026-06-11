import streamlit as st
from data import KOS_DATA

# --- Page config -----------------------------------------------------------------
st.set_page_config(
    page_title="KosFind Semarang - Cari Kos Pintar",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Global CSS (Tampilan Premium, Rapi & Navigasi Bersih) -----------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --primary:      #0F2419;
    --secondary:    #1A5C38;
    --accent:       #3DB87A;
    --accent-dim:   #2D8A5B;
    --light:        #A8DDBE;
    --bg:           #F8F9FA;
    --white:        #FFFFFF;
    --text:         #1E293B;
    --muted:        #64748B;
    --border:       #E2E8F0;
    --card-shadow:  0 4px 20px rgba(15, 36, 25, 0.05);
}

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: var(--text);
    background: var(--bg);
}
.main .block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1000px;
}

/* --- Sidebar Styling Eksklusif --- */
[data-testid="stSidebar"] {
    background-color: var(--primary) !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
}
[data-testid="stSidebar"] * { color: #E2F5E9 !important; }
[data-testid="stSidebarNavItems"] { display: none; }

.sidebar-brand {
    padding: 2.5rem 1.5rem 1.5rem;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 1.5rem;
}
.sidebar-brand .brand-mark {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--accent) !important;
    margin-bottom: 0.5rem;
}
.sidebar-brand .brand-name {
    font-size: 1.8rem;
    font-weight: 800;
    color: #FFFFFF !important;
    letter-spacing: -1px;
    line-height: 1;
}
.sidebar-brand .brand-city {
    font-size: 0.8rem;
    font-weight: 400;
    color: var(--light) !important;
    opacity: 0.8;
    margin-top: 4px;
}

.sidebar-nav-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: rgba(168,221,190,0.4) !important;
    padding: 0 1.5rem 0.75rem;
}

/* Sidebar Custom Buttons */
[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    border: none !important;
    color: rgba(226, 245, 233, 0.7) !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    text-align: left !important;
    padding: 12px 24px !important;
    border-radius: 8px !important;
    margin: 4px 12px !important;
    width: calc(100% - 24px) !important;
    transition: all 0.2s ease !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(61,184,122,0.08) !important;
    color: #FFFFFF !important;
    padding-left: 28px !important;
}

/* Active Nav State */
.nav-active > button {
    background: rgba(61,184,122,0.15) !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    border-left: 4px solid var(--accent) !important;
    border-radius: 0 8px 8px 0 !important;
    margin-left: 0 !important;
    padding-left: 24px !important;
}

.sidebar-tips {
    position: absolute;
    bottom: 2rem;
    left: 0; right: 0;
    padding: 0 1.5rem;
}
.sidebar-tips-inner {
    border-top: 1px solid rgba(255,255,255,0.08);
    padding-top: 1.25rem;
    font-size: 0.75rem;
    color: rgba(168,221,190,0.6) !important;
    line-height: 1.6;
}

/* --- Chatbot Layout & Bubbles --- */
.chat-wrapper {
    max-width: 800px;
    margin: 0 auto;
}
.chat-topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 1.25rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.5rem;
}
.state-pill {
    background: #E6F7ED;
    border: 1px solid #BCE7CD;
    color: var(--secondary);
    font-size: 0.7rem;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
    padding: 6px 14px;
    border-radius: 30px;
}

.chat-window {
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.5rem;
    min-height: 400px;
    max-height: 480px;
    overflow-y: auto;
    box-shadow: var(--card-shadow);
}

/* Chat Message Bubbles */
.msg-user { display: flex; justify-content: flex-end; margin-bottom: 1.25rem; }
.msg-user-bubble {
    background: var(--secondary);
    color: white;
    padding: 12px 18px;
    border-radius: 18px 18px 4px 18px;
    font-size: 0.9rem;
    line-height: 1.5;
    max-width: 75%;
}

.msg-bot { display: flex; justify-content: flex-start; margin-bottom: 1.25rem; }
.msg-bot-bubble {
    background: #F1F5F9;
    color: var(--text);
    padding: 12px 18px;
    border-radius: 18px 18px 18px 4px;
    font-size: 0.9rem;
    line-height: 1.6;
    max-width: 75%;
    white-space: pre-wrap;
}

/* --- Button Hubungi Pemilik (CTA WA) --- */
.wa-link-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background-color: #25D366;
    color: white !important;
    text-decoration: none !important;
    padding: 10px 20px;
    font-weight: 700;
    font-size: 0.85rem;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(37, 211, 102, 0.3);
    transition: all 0.2s ease;
}
.wa-link-btn:hover {
    background-color: #20BA56;
    transform: translateY(-1px);
    box-shadow: 0 6px 16px rgba(37, 211, 102, 0.4);
}

/* Quick Picks Panel */
.quick-panel {
    background: #FFFFFF;
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.25rem;
    margin-top: 1rem;
    box-shadow: var(--card-shadow);
}

#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# --- Session state init ---------------------------------------------------------
def init_session():
    if "page" not in st.session_state:
        st.session_state.page = "Beranda"
    if "fsm" not in st.session_state:
        st.session_state.fsm = KosFindFSM()
        st.session_state.chat_history = [
            {"role": "bot", "content": st.session_state.fsm.get_response()}
        ]
        st.session_state.quick_page = 0
        st.session_state.show_quick_buttons = True
        st.session_state.session_count = 1

init_session()

QUICK_COMMANDS = [
    "Saya ingin mencari kos berdasarkan lokasi",
    "Saya ingin mencari kos berdasarkan budget",
    "Saya ingin mencari kos berdasarkan kategori",
    "Saya ingin mencari kos berdasarkan fasilitas",
    "Saya ingin mencari kos berdasarkan kondisi kos",
    "Saya ingin mencari kos berdasarkan aturan kos",
]

NAV_ITEMS = ["Beranda", "Chatbot", "Rekomendasi Kos"]

# --- Sidebar (Tampilan Navigasi Rapi) --------------------------------------------
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="brand-mark">AI ASSISTANT SYSTEM</div>
        <div class="brand-name">KosFind</div>
        <div class="brand-city">Semarang City</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-nav-label">Menu Navigasi</div>', unsafe_allow_html=True)

    for label in NAV_ITEMS:
        active = "nav-active" if st.session_state.page == label else ""
        st.markdown(f'<div class="{active}">', unsafe_allow_html=True)
        if st.button(label, key=f"nav_{label}", use_container_width=True):
            st.session_state.page = label
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="sidebar-tips">
        <div class="sidebar-tips-inner">
            <b>PANDUAN PINTAR</b><br>
            • Ketik <b>reset</b> untuk mengulang chat<br>
            • Ketik <b>bantuan</b> untuk opsi perintah<br>
            • Klik tombol WA untuk hubungi pemilik
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- Helper functions -----------------------------------------------------------
def fmt_harga(h):
    return f"Rp {h:,.0f}".replace(",", ".")

def check_kos_context(bot_response):
    """
    Mendeteksi secara cerdas nama kos yang terkandung di dalam respon bot.
    """
    bot_response_lower = str(bot_response).lower()
    for kos in KOS_DATA:
        if kos["nama"].lower() in bot_response_lower:
            return kos
    return None

def get_state_string_safe():
    """
    SOLUSI UTAMA ERROR: Mengubah objek Enum State menjadi representasi string teks 
    secara aman tanpa memanggil properti .name yang memicu AttributeError.
    """
    fsm_obj = st.session_state.fsm
    if hasattr(fsm_obj, 'state'):
        # Mengonversi objek State.GREETING menjadi string "State.GREETING" lalu mengambil ujungnya
        state_str = str(fsm_obj.state)
        if "." in state_str:
            return state_str.split(".")[-1]
        return state_str
    return "UNKNOWN"

def _start_new_session():
    st.session_state.chat_history.append({
        "role": "system",
        "content": f"Sesi #{st.session_state.session_count + 1}"
    })
    st.session_state.fsm = KosFindFSM()
    st.session_state.chat_history.append({"role": "bot", "content": st.session_state.fsm.get_response()})
    st.session_state.quick_page = 0
    st.session_state.show_quick_buttons = True
    st.session_state.session_count += 1

# --- PAGE: BERANDA ---------------------------------------------------------------
def page_beranda():
    st.markdown("""
    <div class="beranda-hero" style="background: var(--primary); border-radius: 16px; padding: 3rem 2.5rem; margin-bottom: 2rem; color: white;">
        <div class="hero-tag" style="font-family:'JetBrains Mono'; color:var(--accent); font-size:0.7rem; letter-spacing:0.15em; margin-bottom:1rem;">INTELLIGENT KOS FINDER</div>
        <h1 style="font-size: 2.5rem; font-weight: 800; margin-bottom: 1rem; letter-spacing: -1px; line-height:1.2;">Cari Hunian Terbaik di<br>Semarang Tanpa Ribet.</h1>
        <p style="color: #A8DDBE; max-width: 600px; font-size: 0.95rem; line-height: 1.6;">
            Konsultasikan kriteria kos impian Anda dengan AI Finder kami yang berbasis Finite State Automata. Dapatkan rekomendasi presisi dari lokasi, budget, hingga aturan kos secara real-time.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="section-head">
        <span class="sh-title" style="font-weight:700; color:var(--primary); font-size:1.1rem;">Keunggulan KosFind Chatbot</span>
    </div>
    <div class="section-sub" style="margin-bottom: 1.5rem;">Kemudahan pencarian data yang terintegrasi secara interaktif</div>
    """, unsafe_allow_html=True)

    features = [
        ("Filter Lokasi", "Pencarian spesifik berbasis kecamatan & area kampus."),
        ("Akurasi Budget", "Sesuaikan rentang harga tanpa over-budget."),
        ("Direct Booking", "Hubungi langsung pemilik lewat WhatsApp sekali klik."),
        ("Fasilitas Detil", "Cek ketersediaan AC, Kamar Mandi Dalam, Wifi dll."),
        ("Kondisi Lapangan", "Informasi transparan mengenai bebas banjir & keamanan."),
        ("Update Kamar", "Pantau sisa kuota kamar kosong secara live.")
    ]

    cols = st.columns(3)
    for i, (title, desc) in enumerate(features):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="feat-card" style="background:white; border:1px solid var(--border); padding:1.25rem; border-radius:12px; margin-bottom:1rem;">
                <div style="color:var(--accent); font-family:'JetBrains Mono'; font-size:0.75rem; font-weight:700; margin-bottom:0.5rem;">0{i+1}</div>
                <h4 style="margin:0 0 0.5rem 0; font-size:1rem; font-weight:700; color:var(--primary);">{title}</h4>
                <p style="margin:0; font-size:0.8rem; color:var(--muted); line-height:1.5;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

# --- PAGE: CHATBOT (Interaktif & Pro) -------------------------------------------
def page_chatbot():
    state_string = get_state_string_safe()
    fsm_display_state = state_string.replace("_", " ").title()

    st.markdown(f"""
    <div class="chat-wrapper">
        <div class="chat-topbar">
            <div>
                <h1 style="font-size: 1.5rem; font-weight: 800; color: var(--primary); margin:0;">Asisten AI KosFind</h1>
                <p style="font-size: 0.8rem; color: var(--muted); margin: 4px 0 0 0;">Cari kos impian & langsung terhubung ke pemilik via WA</p>
            </div>
            <div class="state-pill">Status FSM: {fsm_display_state}</div>
        </div>
    """, unsafe_allow_html=True)

    # Chat Windows
    st.markdown('<div class="chat-window">', unsafe_allow_html=True)
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="msg-user">
                <div class="msg-user-bubble">{msg["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
        elif msg["role"] == "bot":
            matched_kos = check_kos_context(msg["content"])
            
            st.markdown(f"""
            <div class="msg-bot">
                <div class="msg-bot-bubble">
                    <div>{msg["content"]}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # FITUR DIRECT-CTA REDIRECT WA OTOMATIS SAAT USER MEMILIH/BERTANYA KOS
            if matched_kos and matched_kos.get("whatsapp"):
                wa_url = f"https://wa.me/{matched_kos['whatsapp']}?text=Halo,%20saya%20tertarik%20dengan%20{matched_kos['nama']}%20di%20KosFind."
                st.markdown(f"""
                <div style="display:flex; justify-content:flex-start; margin:-10px 0 20px 0; padding-left: 5px;">
                    <a href="{wa_url}" target="_blank" class="wa-link-btn">
                        📲 Hubungi Pemilik ({matched_kos['nama']}) via WA
                    </a>
                </div>
                """, unsafe_allow_html=True)
                
        elif msg["role"] == "system":
            st.markdown(f'<div class="session-sep" style="text-align:center; margin:15px 0; color:var(--muted); font-size:0.75rem;">--- {msg["content"]} ---</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Quick Picks Panel
    if st.session_state.show_quick_buttons and state_string != "EXIT":
        st.markdown('<div class="quick-panel">', unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.7rem; font-family:\'JetBrains Mono\'; color:var(--muted); margin-bottom:10px; font-weight:600; letter-spacing:0.05em;">KLIK UNTUK MEMULAI OPSI CEPAT:</div>', unsafe_allow_html=True)

        start_idx = st.session_state.quick_page * 3
        display_cmds = QUICK_COMMANDS[start_idx:start_idx + 3]

        cols = st.columns(3)
        for i, cmd in enumerate(display_cmds):
            with cols[i]:
                if st.button(cmd, key=f"quick_{start_idx + i}", use_container_width=True):
                    st.session_state.chat_history.append({"role": "user", "content": cmd})
                    st.session_state.fsm.step(cmd)
                    st.session_state.chat_history.append({"role": "bot", "content": st.session_state.fsm.get_response()})
                    st.session_state.show_quick_buttons = False
                    st.rerun()

        # Toggle Page Pilihan Cepat
        st.markdown('<div style="text-align:center; margin-top:10px;">', unsafe_allow_html=True)
        if st.button("🔄 Lihat Pilihan Perintah Lain", key="ganti_btn_baru"):
            st.session_state.quick_page = 1 - st.session_state.quick_page
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Sesi Baru Button
    if state_string == "EXIT":
        st.markdown('<div style="text-align:center; margin: 20px 0;">', unsafe_allow_html=True)
        if st.button("🔄 Mulai Sesi Baru / Kosultasi Lagi", key="new_session_btn", use_container_width=True):
            _start_new_session()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Chat Input Area
    user_input = st.chat_input("Ketik di sini (Contoh: cari kos putri di tembalang budget 1jt)...")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.session_state.fsm.step(user_input)
        st.session_state.chat_history.append({"role": "bot", "content": st.session_state.fsm.get_response()})
        if st.session_state.show_quick_buttons:
            st.session_state.show_quick_buttons = False
        st.rerun()

    st.markdown('<div style="text-align:center; font-size:0.75rem; color:var(--muted); margin-top:10px; font-family:\'JetBrains Mono\'">Ketik <b>"reset"</b> kapan saja untuk menyegarkan sistem chatbot</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- PAGE: REKOMENDASI KOS -------------------------------------------------------
def page_rekomendasi():
    st.markdown("""
    <div style="padding-bottom:1rem; margin-bottom:1.5rem; border-bottom:1px solid var(--border);">
        <h1 style="font-size:1.5rem; font-weight:800; color:var(--primary); margin:0;">Eksplorasi Katalog Kos</h1>
        <p style="font-size:0.8rem; color:var(--muted); margin:4px 0 0 0;">Gunakan filter dinamis untuk mempersempit pencarian hunian Anda</p>
    </div>
    """, unsafe_allow_html=True)

    filter_col, list_col = st.columns([1, 2.2])

    with filter_col:
        st.markdown("<div style='background:white; border:1px solid var(--border); padding:1.25rem; border-radius:12px;'>", unsafe_allow_html=True)
        st.markdown("<b style='color:var(--primary); font-size:0.95rem;'>Filter Pencarian</b>", unsafe_allow_html=True)
        st.markdown("<div style='margin-bottom:10px;'></div>", unsafe_allow_html=True)

        lokasi_options = ["Semua Lokasi"] + sorted(set(k["kecamatan"] for k in KOS_DATA))
        f_lokasi = st.selectbox("Kecamatan", lokasi_options)

        jenis_options = ["Semua Jenis", "putri", "putra", "campur"]
        f_jenis = st.selectbox("Jenis Penghuni", jenis_options)

        f_budget_max = st.slider("Budget Maksimal / Bulan", 300_000, 2_000_000, 2_000_000, step=100_000, format="Rp %d")

        f_tersedia = st.checkbox("Hanya Tampilkan Kamar Tersedia", value=False)
        sort_by = st.selectbox("Urutan Berdasarkan", ["Rating Tertinggi", "Harga Terendah", "Harga Tertinggi", "Kamar Tersedia"])

        st.markdown(f"<div style='margin-top:1.5rem; font-size:0.75rem; color:var(--muted); font-family:JetBrains Mono;'>Total Database: {len(KOS_DATA)} unit</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with list_col:
        results = KOS_DATA[:]
        if f_lokasi != "Semua Lokasi":
            results = [k for k in results if k["kecamatan"] == f_lokasi]
        if f_jenis != "Semua Jenis":
            results = [k for k in results if k["jenis"] == f_jenis]
        results = [k for k in results if k["harga"] <= f_budget_max]
        if f_tersedia:
            results = [k for k in results if k["kamar_kosong"] > 0]

        # Sorting logic
        if sort_by == "Rating Tertinggi": results.sort(key=lambda x: -x["rating"])
        elif sort_by == "Harga Terendah": results.sort(key=lambda x: x["harga"])
        elif sort_by == "Harga Tertinggi": results.sort(key=lambda x: -x["harga"])
        elif sort_by == "Kamar Tersedia": results.sort(key=lambda x: -x["kamar_kosong"])

        st.markdown(f"<div style='margin-bottom:1rem; font-size:0.85rem; color:var(--muted);'>Ditemukan <b>{len(results)}</b> kos yang cocok:</div>", unsafe_allow_html=True)

        if not results:
            st.info("Tidak ada kos yang memenuhi seluruh kriteria filter Anda. Sila sesuaikan kembali budget atau lokasi.")
            return

        for kos in results:
            badge_cls = f"badge-{kos['jenis']}"
            status_txt = f"🟢 {kos['kamar_kosong']} Kamar Tersedia" if kos["kamar_kosong"] > 0 else "🔴 Kamar Penuh"
            status_cls = "status-available" if kos["kamar_kosong"] > 0 else "status-full"
            fas_tags = "".join(f'<span class="fas-tag">{f}</span>' for f in kos["fasilitas"][:3])
            more = f'<span class="fas-tag">+{len(kos["fasilitas"]) - 3}</span>' if len(kos["fasilitas"]) > 3 else ""

            st.markdown(f"""
            <div class="kos-card">
                <div class="kos-card-header">
                    <div class="kos-card-name">{kos['nama']}</div>
                    <span class="kos-badge {badge_cls}">{kos['jenis'].upper()}</span>
                </div>
                <div class="kos-meta">📍 Kecamatan {kos['kecamatan']} &nbsp;|&nbsp; ⭐ {kos['rating']}/5 ({kos['ulasan']} Ulasan)</div>
                <div class="kos-price">{fmt_harga(kos['harga'])} <span style='font-size:0.75rem; font-weight:normal; color:var(--muted);'>/ bulan</span></div>
                <div class="kos-fasilitas">{fas_tags}{more}</div>
                <div class="{status_cls}" style="margin-top:5px; font-size:0.8rem; font-weight:600;">{status_txt}</div>
            </div>
            """, unsafe_allow_html=True)

            with st.expander("🔎 Lihat Detail Spesifikasi & Kontak"):
                st.markdown(f"**Alamat Lengkap:** {kos['alamat']}")
                st.markdown(f"**Aturan Kos:** {kos['aturan']}")
                st.markdown(f"**Semua Fasilitas:** {', '.join(kos['fasilitas'])}")
                
                kondisi = kos.get("kondisi", {})
                if kondisi:
                    st.markdown("**Analisis Kondisi Lingkungan:**")
                    st.markdown(f"- Keamanan Wilayah: {kondisi.get('keamanan', '-')}")
                    st.markdown(f"- Tingkat Kebersihan: {kondisi.get('kebersihan', '-')}")
                    st.markdown(f"- Risiko Banjir Semarang: {kondisi.get('keterangan_banjir', '-')}")
                
                if kos.get("whatsapp"):
                    wa_direct_url = f"https://wa.me/{kos['whatsapp']}?text=Halo,%20saya%20mendapatkan%20info%20dari%20KosFind%20dan%20tertarik%20untuk%20booking%20{kos['nama']}."
                    st.markdown(f"""
                    <div style="margin-top: 15px;">
                        <a href="{wa_direct_url}" target="_blank" class="wa-link-btn" style="width: 100%; box-sizing: border-box;">
                            💬 Hubungi & Pesan via WhatsApp Sekarang
                        </a>
                    </div>
                    """, unsafe_allow_html=True)

# --- Router --------------------------------------------------------------------
page = st.session_state.page
if page == "Beranda":
    page_beranda()
elif page == "Chatbot":
    page_chatbot()
elif page == "Rekomendasi Kos":
    page_rekomendasi()
