import streamlit as st
from kosfind_fsm import KosFindFSM
from data import KOS_DATA

# --- Page config -----------------------------------------------------------------
st.set_page_config(
    page_title="KosFind Semarang",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Global CSS ------------------------------------------------------------------
st.markdown("""
<style>
/* --- Google Fonts ------------------------------------------------- */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* --- Root vars --------------------------------------------------- */
:root {
    --primary:     #1B4332;
    --secondary:   #2D6A4F;
    --accent:      #52B788;
    --light:       #95D5B2;
    --bg:          #F8F7F2;
    --white:       #FFFFFF;
    --text:        #1E1E1E;
    --muted:       #6B7280;
    --border:      #E5E7EB;
    --card-shadow: 0 2px 8px rgba(27,67,50,0.10);
}

/* --- Base -------------------------------------------------------- */
html, body, [class*="css"] {
    font-family: 'Inter', 'Segoe UI', sans-serif;
    color: var(--text);
}
.main .block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
    max-width: 900px;
}

/* --- Sidebar ----------------------------------------------------- */
[data-testid="stSidebar"] {
    background: var(--primary) !important;
    min-width: 200px !important;
    max-width: 220px !important;
}
[data-testid="stSidebar"] * { color: #E8F5E9 !important; }
[data-testid="stSidebarNavItems"] { display: none; }

.sidebar-logo {
    text-align: center;
    padding: 1.5rem 1rem 1rem;
    border-bottom: 1px solid rgba(255,255,255,0.15);
    margin-bottom: 0.5rem;
}
.sidebar-logo .logo-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #FFFFFF !important;
    letter-spacing: -0.3px;
    margin-top: 0.5rem;
}
.sidebar-logo .logo-sub {
    font-size: 0.7rem;
    color: var(--light) !important;
    opacity: 0.9;
}

[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    color: #C8E6C9 !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    text-align: left !important;
    padding: 10px 16px !important;
    border-radius: 8px !important;
    margin: 3px 10px !important;
    width: calc(100% - 20px) !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255,255,255,0.15) !important;
    color: #FFFFFF !important;
}

/* --- Chatbot Page ------------------------------------------------ */
.chat-container{
    max-width:850px;
    margin:auto;
}

.chat-header{
    text-align:center;
    margin-bottom:12px;
    padding-bottom:12px;
    border-bottom:1px solid var(--border);
}

.chat-header h1{
    font-size:2rem;
    margin:0;
    color:var(--primary);
}

.chat-header p{
    margin-top:4px;
    font-size:.9rem;
    color:var(--muted);
}

.state-chip{
    display:inline-flex;
    align-items:center;
    gap:6px;
    background:#E8F5E9;
    color:var(--secondary);
    padding:6px 14px;
    border-radius:999px;
    font-size:.75rem;
    font-weight:600;
    margin-bottom:12px;
}



.message-user,
.message-bot{
    margin-bottom:14px;
}

.message-user{
    text-align:right;
    margin-bottom:14px;
}

.message-user-label{
    font-size:.7rem;
    color:var(--muted);
    margin-bottom:3px;
}

.message-user-content{
    display:inline-block;

    background:var(--secondary);
    color:white;

    padding:10px 16px;
    border-radius:18px 18px 4px 18px;

    max-width:70%;
    text-align:left;

    white-space:normal;
    overflow-wrap:break-word;
}

.message-bot-content{
    background:#F1F5F9;
    color:var(--text);
    padding:10px 16px;
    border-radius:18px 18px 18px 4px;
    max-width:70%;
    font-size:.85rem;
}

.message-user-label,
.message-bot-label{
    font-size:.7rem;
    margin-bottom:3px;
    color:var(--muted);
}

.quick-panel{
    margin-top:12px;
    padding:12px;
    background:#fff;
    border:1px solid var(--border);
    border-radius:14px;
}

.quick-title{
    font-size:.75rem;
    font-weight:700;
    color:var(--muted);
    margin-bottom:10px;
}

.chat-footer{
    margin-top:8px;
    text-align:center;
    font-size:.7rem;
    color:var(--muted);
}

.new-session-container {
    text-align: center;
    margin: 0.75rem 0;
}
.new-session-container button {
    background: var(--secondary) !important;
    border: none !important;
    border-radius: 30px !important;
    padding: 6px 20px !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    color: white !important;
}

/* Beranda Page */
.sys-desc-card {
    background: var(--white);
    border: 1px solid var(--border);
    border-left: 4px solid var(--secondary);
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1.5rem;
}
.sys-desc-card .sys-title {
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--primary);
    margin: 0;
}
.sys-desc-card .sys-subtitle {
    font-size: 0.8rem;
    font-weight: 500;
    color: var(--secondary);
    margin: 0.25rem 0 0.75rem;
}
.sys-desc-card .sys-body {
    font-size: 0.85rem;
    color: var(--text);
    line-height: 1.6;
}

.section-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--primary);
    margin: 1rem 0 0;
}
.section-sub {
    font-size: 0.75rem;
    color: var(--muted);
    margin-bottom: 1rem;
}

.feat-card {
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 0.75rem;
    margin-bottom: 0.5rem;
}
.feat-card h4 {
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--primary);
    margin: 0 0 4px;
}
.feat-card p {
    font-size: 0.7rem;
    color: var(--muted);
    margin: 0;
}

/* Kos Cards */
.kos-card {
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 0.75rem;
    margin-bottom: 0.75rem;
}
.kos-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
}
.kos-card-name {
    font-size: 0.9rem;
    font-weight: 700;
    color: var(--primary);
}
.kos-badge {
    font-size: 0.6rem;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 20px;
}
.badge-putri { background: #FCE4EC; color: #C2185B; }
.badge-putra { background: #E3F2FD; color: #1565C0; }
.badge-campur { background: #FFF8E1; color: #F57F17; }
.kos-meta {
    font-size: 0.65rem;
    color: var(--muted);
    margin-bottom: 0.5rem;
}
.kos-price {
    font-size: 0.9rem;
    font-weight: 700;
    color: var(--secondary);
    margin-bottom: 0.5rem;
}
.kos-fasilitas {
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
    margin-bottom: 0.5rem;
}
.fas-tag {
    background: #F0FDF4;
    color: var(--secondary);
    font-size: 0.6rem;
    padding: 2px 6px;
    border-radius: 20px;
}
            
.quick-action-card{
    background:#FFFFFF;
    border:1px solid var(--border);
    border-radius:16px;
    overflow:hidden;
    margin-top:12px;
}

.quick-action-title{
    padding:16px;
    font-size:0.9rem;
    font-weight:600;
    color:var(--text);
    border-bottom:1px solid var(--border);
}

.quick-action-item{
    padding:14px 16px;
    border-bottom:1px solid var(--border);
    color:#2563EB;
    font-size:0.9rem;
}

.quick-action-footer{
    text-align:center;
    padding:12px;
}

.status-available { color: #16A34A; font-size: 0.7rem; }
.status-full { color: #DC2626; font-size: 0.7rem; }

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


# --- Sidebar --------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="logo-title">KosFind</div>
        <div class="logo-sub">Semarang</div>
    </div>
    """, unsafe_allow_html=True)

    for label in NAV_ITEMS:
        if st.button(label, key=f"nav_{label}", use_container_width=True):
            st.session_state.page = label
            st.rerun()

    st.markdown("<hr style='border-color:rgba(255,255,255,0.12); margin:1rem 0'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='padding:0 12px; font-size:0.65rem; color:#95D5B2; line-height:1.6;'>
        Tips:<br>
        - Ketik "reset" untuk mengakhiri sesi<br>
        - Ketik "bantuan" untuk panduan<br>
        - Pilih topik dari menu cepat
    </div>
    """, unsafe_allow_html=True)


# --- Helper functions -----------------------------------------------------------
def fmt_harga(h):
    return f"Rp{h:,.0f}".replace(",", ".")

def _start_new_session():
    st.session_state.chat_history.append({
        "role": "system",
        "content": f"Sesi Baru #{st.session_state.session_count + 1}"
    })
    st.session_state.fsm = KosFindFSM()
    st.session_state.chat_history.append({"role": "bot", "content": st.session_state.fsm.get_response()})
    st.session_state.quick_page = 0
    st.session_state.show_quick_buttons = True
    st.session_state.session_count += 1

def _hard_reset():
    st.session_state.fsm = KosFindFSM()
    st.session_state.chat_history = [{"role": "bot", "content": st.session_state.fsm.get_response()}]
    st.session_state.quick_page = 0
    st.session_state.show_quick_buttons = True
    st.session_state.session_count = 1


# -------------------------------------------------------------------------------
# PAGE: BERANDA
# -------------------------------------------------------------------------------
def page_beranda():
    st.markdown("""
    <div class="sys-desc-card">
        <div class="sys-title">KosFind Semarang</div>
        <div class="sys-subtitle">
            Sistem Chatbot Konsultasi Kos Berbasis NLP dan FSA
        </div>
        <p class="sys-body">
            KosFind Semarang adalah chatbot yang membantu Anda mencari informasi kos 
            di Kota Semarang melalui percakapan interaktif. Sistem ini menggunakan 
            Natural Language Processing (NLP) untuk memahami berbagai variasi pertanyaan 
            dan Finite State Automata (FSA) untuk mengelola alur percakapan.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Fitur Chatbot</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Informasi kos yang dapat diakses melalui percakapan</div>', unsafe_allow_html=True)

    features = [
        ("Lokasi", "Mencari kos berdasarkan kecamatan di Semarang"),
        ("Budget", "Mencari kos berdasarkan harga sewa"),
        ("Kategori", "Kos Putra, Putri, atau Campur"),
        ("Fasilitas", "AC, WiFi, Kamar Mandi Dalam, Parkir, dll"),
        ("Aturan", "Jam malam, aturan tamu, dll"),
        ("Kondisi", "Banjir, keamanan, kebersihan, akses jalan"),
        ("Ketersediaan", "Cek kamar kosong atau penuh"),
        ("Detail Kos", "Informasi lengkap kos"),
        ("Kontak", "Nomor WhatsApp pemilik kos"),
    ]

    for i in range(0, len(features), 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            if i + j < len(features):
                title, desc = features[i + j]
                with col:
                    st.markdown(f"""
                    <div class="feat-card">
                        <h4>{title}</h4>
                        <p>{desc}</p>
                    </div>
                    """, unsafe_allow_html=True)


# -------------------------------------------------------------------------------
# PAGE: CHATBOT
# -------------------------------------------------------------------------------
def page_chatbot():
    st.markdown("""
    <div class="chat-header">
        <h1>KosFind Semarang</h1>
        <p>Temukan kos terbaik di Semarang melalui percakapan interaktif</p>
    </div>
    """, unsafe_allow_html=True)

    fsm_state = st.session_state.fsm.state.name.replace("_", " ").title()
    st.markdown(
        f'<div class="state-chip">Status: {fsm_state}</div>',
        unsafe_allow_html=True
    )

    # Tampilkan riwayat chat tanpa kotak besar
    for msg in st.session_state.chat_history:

        if msg["role"] == "user":
            st.markdown(f"""
            <div class="message-user">
                <div>
                    <div class="message-user-label">Anda</div>
                    <div class="message-user-content">{msg["content"]}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        elif msg["role"] == "bot":
            st.markdown(f"""
            <div class="message-bot">
                <div>
                    <div class="message-bot-label">KosFind Assistant</div>
                    <div class="message-bot-content">{msg["content"]}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        elif msg["role"] == "system":
            st.markdown(
                f'<div class="session-separator"><span>{msg["content"]}</span></div>',
                unsafe_allow_html=True
            )

# Quick Action
    if (
        st.session_state.show_quick_buttons
        and st.session_state.fsm.state.name != "EXIT"
    ):

        st.markdown("""
        <div class="quick-action-card">
            <div class="quick-action-title">
                Silakan pilih topik yang ingin ditanyakan:
            </div>
        </div>
        """, unsafe_allow_html=True)

        start_idx = st.session_state.quick_page * 3
        display_cmds = QUICK_COMMANDS[start_idx:start_idx + 4]

        for i, cmd in enumerate(display_cmds):

            if st.button(
                cmd,
                key=f"quick_{i}",
                use_container_width=True
            ):
                st.session_state.chat_history.append({
                    "role": "user",
                    "content": cmd
                })

                st.session_state.fsm.step(cmd)

                st.session_state.chat_history.append({
                    "role": "bot",
                    "content": st.session_state.fsm.get_response()
                })

                st.session_state.show_quick_buttons = False
                st.rerun()

        if st.button(
            "↻ Ganti Pertanyaan",
            key="change_question",
            use_container_width=True
        ):
            st.session_state.quick_page = (
                st.session_state.quick_page + 1
            ) % 2
            st.rerun()


    # Tombol sesi baru
    if st.session_state.fsm.state.name == "EXIT":
        if st.button(
            "Mulai Sesi Baru",
            key="new_session_btn",
            use_container_width=True
        ):
            _start_new_session()
            st.rerun()

    # Input chat
    user_input = st.chat_input("Ketik pesan Anda di sini...")

    if user_input:
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input
        })

        st.session_state.fsm.step(user_input)

        st.session_state.chat_history.append({
            "role": "bot",
            "content": st.session_state.fsm.get_response()
        })

        st.session_state.show_quick_buttons = False
        st.rerun()

    st.markdown(
        '<div class="chat-footer">Contoh: Cari kos putri di Tembalang budget 800rb</div>',
        unsafe_allow_html=True
    )


# -------------------------------------------------------------------------------
# PAGE: REKOMENDASI KOS
# -------------------------------------------------------------------------------
def page_rekomendasi():
    st.markdown("""
    <div class="chat-header">
        <h1>Rekomendasi Kos</h1>
        <p>Jelajahi seluruh data kos di Semarang</p>
    </div>
    """, unsafe_allow_html=True)

    filter_col, list_col = st.columns([1, 2])

    with filter_col:
        st.markdown("### Filter Pencarian")
        
        lokasi_options = ["Semua Lokasi"] + sorted(set(k["kecamatan"] for k in KOS_DATA))
        f_lokasi = st.selectbox("Kecamatan", lokasi_options)
        
        jenis_options = ["Semua Jenis", "putri", "putra", "campur"]
        f_jenis = st.selectbox("Jenis Kos", jenis_options)
        
        f_budget_max = st.slider("Budget Maksimal (Rp)", 300_000, 2_000_000, 2_000_000, step=100_000, format="Rp%d")
        
        f_tersedia = st.checkbox("Hanya yang tersedia", value=False)
        sort_by = st.selectbox("Urutkan berdasarkan", ["Rating Tertinggi", "Harga Terendah", "Harga Tertinggi", "Kamar Tersedia"])
        
        st.markdown(f"<div style='margin-top:1rem; font-size:0.7rem; color:var(--muted);'>Total kos: {len(KOS_DATA)}</div>", unsafe_allow_html=True)

    with list_col:
        results = KOS_DATA[:]
        if f_lokasi != "Semua Lokasi":
            results = [k for k in results if k["kecamatan"] == f_lokasi]
        if f_jenis != "Semua Jenis":
            results = [k for k in results if k["jenis"] == f_jenis]
        results = [k for k in results if k["harga"] <= f_budget_max]
        if f_tersedia:
            results = [k for k in results if k["kamar_kosong"] > 0]

        if sort_by == "Rating Tertinggi":
            results.sort(key=lambda x: -x["rating"])
        elif sort_by == "Harga Terendah":
            results.sort(key=lambda x: x["harga"])
        elif sort_by == "Harga Tertinggi":
            results.sort(key=lambda x: -x["harga"])
        elif sort_by == "Kamar Tersedia":
            results.sort(key=lambda x: -x["kamar_kosong"])

        st.markdown(f"<div style='margin-bottom:0.75rem; font-size:0.8rem; color:var(--muted);'>Menampilkan <strong>{len(results)}</strong> kos</div>", unsafe_allow_html=True)

        if not results:
            st.info("Tidak ada kos yang sesuai dengan filter yang dipilih.")
            return

        for kos in results:
            badge_cls = f"badge-{kos['jenis']}"
            status_txt = f"{kos['kamar_kosong']} kamar tersedia" if kos["kamar_kosong"] > 0 else "Kamar penuh"
            status_cls = "status-available" if kos["kamar_kosong"] > 0 else "status-full"
            fas_tags = "".join(f'<span class="fas-tag">{f}</span>' for f in kos["fasilitas"][:3])
            more = f'<span class="fas-tag">+{len(kos["fasilitas"]) - 3} lagi</span>' if len(kos["fasilitas"]) > 3 else ""

            st.markdown(f"""
            <div class="kos-card">
                <div class="kos-card-header">
                    <div class="kos-card-name">{kos['nama']}</div>
                    <span class="kos-badge {badge_cls}">{kos['jenis']}</span>
                </div>
                <div class="kos-meta">
                    {kos['kecamatan']} | Rating: {kos['rating']}/5 ({kos['ulasan']} ulasan)
                </div>
                <div class="kos-price">{fmt_harga(kos['harga'])} / bulan</div>
                <div class="kos-fasilitas">{fas_tags}{more}</div>
                <div class="{status_cls}">{status_txt}</div>
            </div>
            """, unsafe_allow_html=True)

            with st.expander("Lihat Detail Lengkap"):
                st.markdown(f"**Alamat:** {kos['alamat']}")
                st.markdown(f"**Aturan:** {kos['aturan']}")
                st.markdown(f"**Fasilitas lengkap:** {', '.join(kos['fasilitas'])}")
                kondisi = kos.get("kondisi", {})
                if kondisi:
                    st.markdown("**Kondisi Kos:**")
                    st.markdown(f"- Keamanan: {kondisi.get('keamanan', '-')}")
                    st.markdown(f"- Kebersihan: {kondisi.get('kebersihan', '-')}")
                    st.markdown(f"- Banjir: {kondisi.get('keterangan_banjir', '-')}")
                if kos.get("whatsapp"):
                    st.markdown(f"**Hubungi:** [Chat via WhatsApp](https://wa.me/{kos['whatsapp']})")


# --- Router --------------------------------------------------------------------
page = st.session_state.page
if page == "Beranda":
    page_beranda()
elif page == "Chatbot":
    page_chatbot()
elif page == "Rekomendasi Kos":
    page_rekomendasi()
