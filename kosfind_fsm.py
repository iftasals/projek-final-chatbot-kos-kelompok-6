# kosfind_fsm.py — FSM untuk KosFind Semarang (Natural)

from enum import Enum, auto
import re
from typing import Dict, List, Optional, Any, Tuple
from data import KOS_DATA
from nlp_engine import KosFindNLP


class State(Enum):
    GREETING = auto()
    MENU = auto()
    INPUT_LOKASI = auto()
    INPUT_BUDGET = auto()
    INPUT_JENIS = auto()
    INPUT_FASILITAS = auto()
    HASIL_PENCARIAN = auto()
    DETAIL_KOS = auto()
    BANTUAN = auto()
    EXIT = auto()


class KosFindFSM:
    def __init__(self):
        self.state = State.GREETING
        self.nlp = KosFindNLP()
        
        self.search_criteria = {
            "lokasi": None,
            "kedekatan": None,
            "budget": None,
            "jenis": None,
            "budget_min": None,
            "budget_max": None,
            "fasilitas_query": None,
            "fasilitas_list": None
        }
        
        self.last_results: List[Dict] = []
        self.selected_kos: Optional[Dict] = None
        self.selected_kos_id: Optional[int] = None
        self.selected_kos_nomor: Optional[int] = None
        
        self.response = ""
        
        self._greeting()
    
    def _greeting(self):
        self.response = "Halo! Saya KosFind, asisten cari kos di Semarang. Ada yang bisa saya bantu?"
        self.state = State.MENU
        self.nlp.set_state("MENU")
    
    def get_response(self) -> str:
        return self.response
    
    def _reset_all(self):
        self.state = State.GREETING
        self.search_criteria = {
            "lokasi": None,
            "kedekatan": None,
            "budget": None,
            "jenis": None,
            "budget_min": None,
            "budget_max": None,
            "fasilitas_query": None,
            "fasilitas_list": None
        }
        self.last_results = []
        self.selected_kos = None
        self.selected_kos_id = None
        self.selected_kos_nomor = None
        self.nlp.set_state("GREETING")
        self._greeting()
    
    def _reset_search(self):
        self.search_criteria = {
            "lokasi": None,
            "kedekatan": None,
            "budget": None,
            "jenis": None,
            "budget_min": None,
            "budget_max": None,
            "fasilitas_query": None,
            "fasilitas_list": None
        }
    
    def _fmt_harga(self, harga: int) -> str:
        return f"Rp{harga:,.0f}".replace(",", ".")
    
    def _query_kos(self) -> List[Dict]:
        results = KOS_DATA[:]
        criteria = self.search_criteria
        
        if criteria["lokasi"]:
            results = [k for k in results if 
                      criteria["lokasi"].lower() in k["kecamatan"].lower() or
                      criteria["lokasi"].lower() in k["wilayah"].lower()]
        
        if criteria["kedekatan"]:
            results = [k for k in results if criteria["kedekatan"] in k.get("dekat", [])]
        
        if criteria.get("budget_min") is not None:
            results = [k for k in results if k["harga"] >= criteria["budget_min"]]
        if criteria.get("budget_max") is not None:
            results = [k for k in results if k["harga"] <= criteria["budget_max"]]
        elif criteria["budget"] is not None:
            results = [k for k in results if k["harga"] <= criteria["budget"]]
        
        if criteria["jenis"]:
            results = [k for k in results if k["jenis"] == criteria["jenis"]]
        
        if criteria.get("fasilitas_query") and criteria.get("fasilitas_list"):
            results = [k for k in results if any(f.lower() in [fas.lower() for fas in k["fasilitas"]] for f in criteria["fasilitas_list"])]
        
        results.sort(key=lambda x: (-x["kamar_kosong"], -x["rating"]))
        return results
    
    def _build_kos_list(self, results: List[Dict]) -> str:
        if not results:
            return ""
        
        lines = [f"Saya temukan {len(results)} kos yang cocok:\n"]
        for i, kos in enumerate(results, 1):
            kamar_info = "Ada kamar" if kos['kamar_kosong'] > 0 else "Penuh"
            lines.append(
                f"{i}. {kos['nama']}\n"
                f"   {kos['kecamatan']} | {self._fmt_harga(kos['harga'])}/bln | "
                f"{kos['jenis'].capitalize()} | {kamar_info}\n"
            )
        
        return "\n".join(lines)
    
    def _build_fasilitas(self, kos: Dict) -> str:
        fasilitas_str = ", ".join(kos["fasilitas"])
        return f"Fasilitas {kos['nama']}:\n{fasilitas_str}"
    
    def _build_kondisi_banjir(self, kos: Dict) -> str:
        kondisi = kos.get("kondisi", {})
        return f"Kondisi banjir {kos['nama']}:\n{kondisi.get('keterangan_banjir', 'Informasi tidak tersedia')}"
    
    def _build_kondisi_keamanan(self, kos: Dict) -> str:
        kondisi = kos.get("kondisi", {})
        return f"Keamanan {kos['nama']}:\n{kondisi.get('keamanan', 'Informasi tidak tersedia')}"
    
    def _build_kondisi_kebersihan(self, kos: Dict) -> str:
        kondisi = kos.get("kondisi", {})
        return f"Kebersihan {kos['nama']}:\n{kondisi.get('kebersihan', 'Informasi tidak tersedia')}"
    
    def _build_kondisi_kebisingan(self, kos: Dict) -> str:
        kondisi = kos.get("kondisi", {})
        return f"Tingkat kebisingan {kos['nama']}:\n{kondisi.get('kebisingan', 'Informasi tidak tersedia')}"
    
    def _build_kondisi_akses_jalan(self, kos: Dict) -> str:
        kondisi = kos.get("kondisi", {})
        return f"Akses jalan {kos['nama']}:\n{kondisi.get('akses_jalan', 'Informasi tidak tersedia')}"
    
    def _build_kondisi_listrik(self, kos: Dict) -> str:
        kondisi = kos.get("kondisi", {})
        return f"Kondisi listrik {kos['nama']}:\n{kondisi.get('listrik', 'Informasi tidak tersedia')}"
    
    def _build_kondisi_air(self, kos: Dict) -> str:
        kondisi = kos.get("kondisi", {})
        return f"Kondisi air {kos['nama']}:\n{kondisi.get('air', 'Informasi tidak tersedia')}"
    
    def _build_kondisi_udara(self, kos: Dict) -> str:
        kondisi = kos.get("kondisi", {})
        return f"Sirkulasi udara {kos['nama']}:\n{kondisi.get('sirkulasi_udara', 'Informasi tidak tersedia')}"
    
    def _build_kondisi_pencahayaan(self, kos: Dict) -> str:
        kondisi = kos.get("kondisi", {})
        return f"Pencahayaan {kos['nama']}:\n{kondisi.get('pencahayaan', 'Informasi tidak tersedia')}"
    
    def _build_kondisi_lingkungan(self, kos: Dict) -> str:
        kondisi = kos.get("kondisi", {})
        return f"Lingkungan {kos['nama']}:\n{kondisi.get('lingkungan', 'Informasi tidak tersedia')}"
    
    def _build_kondisi_semua(self, kos: Dict) -> str:
        kondisi = kos.get("kondisi", {})
        return (
            f"Kondisi {kos['nama']}:\n\n"
            f"Banjir: {kondisi.get('keterangan_banjir', '-')}\n"
            f"Keamanan: {kondisi.get('keamanan', '-')}\n"
            f"Kebersihan: {kondisi.get('kebersihan', '-')}\n"
            f"Kebisingan: {kondisi.get('kebisingan', '-')}\n"
            f"Akses Jalan: {kondisi.get('akses_jalan', '-')}\n"
            f"Listrik: {kondisi.get('listrik', '-')}\n"
            f"Air: {kondisi.get('air', '-')}\n"
            f"Sirkulasi Udara: {kondisi.get('sirkulasi_udara', '-')}\n"
            f"Pencahayaan: {kondisi.get('pencahayaan', '-')}\n"
            f"Lingkungan: {kondisi.get('lingkungan', '-')}"
        )
    
    def _build_ketersediaan(self, kos: Dict) -> str:
        kamar = kos["kamar_kosong"]
        if kamar > 0:
            return f"{kos['nama']} masih ada {kamar} kamar kosong."
        else:
            return f"Maaf, {kos['nama']} sudah penuh."
    
    def _build_aturan(self, kos: Dict) -> str:
        return f"Aturan {kos['nama']}:\n{kos['aturan']}"
    
    def _build_detail_lengkap(self, kos: Dict) -> str:
        fasilitas_str = ", ".join(kos["fasilitas"])
        kamar_info = f"{kos['kamar_kosong']} kamar kosong" if kos['kamar_kosong'] > 0 else "Penuh"
        
        return (
            f"{kos['nama']}\n"
            f"Lokasi: {kos['kecamatan']}\n"
            f"Alamat: {kos['alamat']}\n"
            f"Harga: {self._fmt_harga(kos['harga'])}/bulan\n"
            f"Jenis: {kos['jenis'].capitalize()}\n\n"
            f"Fasilitas: {fasilitas_str}\n\n"
            f"Kondisi Banjir: {kos['kondisi']['keterangan_banjir']}\n"
            f"Keamanan: {kos['kondisi']['keamanan']}\n"
            f"Kebersihan: {kos['kondisi']['kebersihan']}\n\n"
            f"Aturan: {kos['aturan']}\n\n"
            f"Ketersediaan: {kamar_info}\n"
            f"Rating: {kos['rating']}/5 ({kos['ulasan']} ulasan)"
        )
    
    def _build_pemesanan(self, kos: Dict) -> str:
        wa_url = f"https://wa.me/{kos['whatsapp']}?text=Halo,%20saya%20tertarik%20dengan%20{kos['nama'].replace(' ', '%20')}"
        return (
            f"Pemesanan {kos['nama']}\n\n"
            f"Nama: {kos['nama']}\n"
            f"Alamat: {kos['alamat']}\n\n"
            f"Hubungi pemilik: {wa_url}\n\n"
            "Tips: Siapkan KTP dan uang muka saat survey."
        )
    
    def _extract_nomor_dari_teks(self, text: str) -> Optional[int]:
        text_lower = text.lower()
        
        patterns = [
            r'\b(kos|kost|kosan)\s+(\d+)\b',
            r'\b(kos|kost|kosan)\s+(nomor|no\.?)\s*(\d+)\b',
            r'\b(nomor|no\.?)\s*(\d+)\b',
            r'\byang\s+(\d+)\b',
            r'\bpilih\s+(\d+)\b',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                for group in match.groups()[::-1]:
                    if group and group.isdigit():
                        return int(group)
        
        numbers = re.findall(r'\b(\d+)\b', text_lower)
        for num in numbers:
            num_int = int(num)
            if 1 <= num_int <= 10:
                return num_int
        
        return None
    
    def _split_multi_question(self, text: str) -> List[str]:
        text_lower = text.lower()
        separators = [r'\s+dan\s+', r'\s*&\s*', r'\s*,\s*', r'\s+serta\s+', r'\s+lalu\s+', r'\s+terus\s+']
        
        for sep in separators:
            if re.search(sep, text_lower):
                parts = re.split(sep, text_lower)
                parts = [p.strip() for p in parts if p.strip()]
                if len(parts) >= 2:
                    return parts
        
        return [text_lower]
    
    def _detect_single_aksi(self, text: str) -> Tuple[Optional[str], Optional[int]]:
        text_lower = text.lower()
        nomor = self._extract_nomor_dari_teks(text)
        
        if re.search(r'kondisi\s+kos\s*nya\s+gimana', text_lower):
            return ("kondisi_semua", nomor)
        if re.search(r'kondisi\s+kos\s*nya\s+bagaimana', text_lower):
            return ("kondisi_semua", nomor)
        if re.search(r'kondisinya\s+gimana', text_lower):
            return ("kondisi_semua", nomor)
        if re.search(r'^kondisi$', text_lower):
            return ("kondisi_semua", nomor)
        
        if re.search(r'banjir|rawan\s*banjir', text_lower):
            return ("kondisi_banjir", nomor)
        if re.search(r'keamanan|aman\s*(nggak|tidak)?|satpam|cctv', text_lower):
            return ("kondisi_keamanan", nomor)
        if re.search(r'kebersihan|bersih\s*(nggak|tidak)?', text_lower):
            return ("kondisi_kebersihan", nomor)
        if re.search(r'bising|ramai|tenang', text_lower):
            return ("kondisi_kebisingan", nomor)
        if re.search(r'akses\s*jalan|jalan\s*(bagus|mulus)?', text_lower):
            return ("kondisi_akses_jalan", nomor)
        if re.search(r'listrik|mati\s*listrik|padam', text_lower):
            return ("kondisi_listrik", nomor)
        if re.search(r'air\s*(bersih|keruh)?|pam|sumur', text_lower):
            return ("kondisi_air", nomor)
        if re.search(r'udara|sirkulasi|pengap', text_lower):
            return ("kondisi_udara", nomor)
        if re.search(r'lampu|pencahayaan|penerangan|terang', text_lower):
            return ("kondisi_pencahayaan", nomor)
        if re.search(r'lingkungan|tetangga|nyaman', text_lower):
            return ("kondisi_lingkungan", nomor)
        
        if re.search(r'fasilitas|fasilitasnya|ada apa saja', text_lower):
            return ("fasilitas", nomor)
        
        if re.search(r'aturan|peraturan|jam malam', text_lower):
            return ("aturan", nomor)
        
        if re.search(r'(ada|masih ada|tersedia)\s*(kamar)?|kamar\s*kosong|lowongan', text_lower):
            return ("ketersediaan", nomor)
        
        if re.search(r'detail|info\s*lengkap|lihat|tentang|jelaskan', text_lower):
            return ("detail", nomor)
        
        pemesanan_patterns = [
            r'cara\s*(pesan|booking|sewa)',
            r'prosedur\s*sewa',
            r'bagaimana\s*cara\s*(pesan|sewa)',
            r'gimana\s*cara\s*(pesan|sewa)',
            r'pesan\s*sekarang',
            r'booking\s*kos',
            r'pemesanan',
            r'cara\s*pesan\s*ini',
            r'cara\s*sewa\s*kos\s*ini',
            r'mau\s*pesan\s*kos\s*ini',
            r'^pesan\s*kos\s*ini$',
            r'^sewa\s*kos\s*ini$',
        ]
        for pattern in pemesanan_patterns:
            if re.search(pattern, text_lower):
                return ("pemesanan", nomor)
        
        if re.search(r'kontak|wa|whatsapp|nomor\s*wa|hubungi', text_lower):
            return ("kontak", nomor)
        
        if re.search(r'lokasi|maps|alamat|di\s*mana', text_lower):
            return ("lokasi", nomor)
        
        return (None, nomor)
    
    def _get_kos_from_nomor(self, nomor: Optional[int]) -> Optional[Dict]:
        if nomor and self.last_results and 1 <= nomor <= len(self.last_results):
            kos = self.last_results[nomor - 1]
            self.selected_kos = kos
            self.selected_kos_id = kos["id"]
            self.selected_kos_nomor = nomor
            return kos
        elif self.selected_kos:
            return self.selected_kos
        return None
    
    def _execute_aksi(self, aksi: str, kos: Dict) -> str:
        if aksi == "fasilitas":
            return self._build_fasilitas(kos)
        elif aksi == "aturan":
            return self._build_aturan(kos)
        elif aksi == "ketersediaan":
            return self._build_ketersediaan(kos)
        elif aksi == "kondisi_banjir":
            return self._build_kondisi_banjir(kos)
        elif aksi == "kondisi_keamanan":
            return self._build_kondisi_keamanan(kos)
        elif aksi == "kondisi_kebersihan":
            return self._build_kondisi_kebersihan(kos)
        elif aksi == "kondisi_kebisingan":
            return self._build_kondisi_kebisingan(kos)
        elif aksi == "kondisi_akses_jalan":
            return self._build_kondisi_akses_jalan(kos)
        elif aksi == "kondisi_listrik":
            return self._build_kondisi_listrik(kos)
        elif aksi == "kondisi_air":
            return self._build_kondisi_air(kos)
        elif aksi == "kondisi_udara":
            return self._build_kondisi_udara(kos)
        elif aksi == "kondisi_pencahayaan":
            return self._build_kondisi_pencahayaan(kos)
        elif aksi == "kondisi_lingkungan":
            return self._build_kondisi_lingkungan(kos)
        elif aksi == "kondisi_semua":
            return self._build_kondisi_semua(kos)
        elif aksi == "detail":
            return self._build_detail_lengkap(kos)
        elif aksi == "pemesanan":
            return self._build_pemesanan(kos)
        elif aksi == "kontak":
            wa_url = f"https://wa.me/{kos['whatsapp']}?text=Halo,%20saya%20tertarik%20dengan%20{kos['nama'].replace(' ', '%20')}"
            return f"Hubungi pemilik {kos['nama']}: {wa_url}"
        elif aksi == "lokasi":
            maps_url = f"https://maps.google.com/?q={kos['latitude']},{kos['longitude']}"
            return f"Alamat {kos['nama']}: {kos['alamat']}\n\nGoogle Maps: {maps_url}"
        else:
            return ""
    
    def _handle_multi_question(self, text: str) -> bool:
        questions = self._split_multi_question(text)
        if len(questions) <= 1:
            return False
        
        nomor_global = self._extract_nomor_dari_teks(text)
        kos = self._get_kos_from_nomor(nomor_global)
        
        if not kos:
            return False
        
        responses = []
        for q in questions:
            aksi, nomor = self._detect_single_aksi(q)
            if nomor and nomor != nomor_global:
                kos_pertanyaan = self._get_kos_from_nomor(nomor)
                if kos_pertanyaan:
                    res = self._execute_aksi(aksi, kos_pertanyaan)
                    if res:
                        responses.append(res)
                continue
            res = self._execute_aksi(aksi, kos)
            if res:
                responses.append(res)
        
        if responses:
            self.response = "\n\n---\n\n".join(responses)
            self.state = State.DETAIL_KOS
            self.nlp.set_state("DETAIL_KOS")
            return True
        
        return False
    
    def _handle_single_question(self, text: str) -> bool:
        aksi, nomor = self._detect_single_aksi(text)
        if aksi is None:
            return False
        
        kos = self._get_kos_from_nomor(nomor)
        if not kos:
            if self.last_results:
                self.response = f"Kos nomor berapa yang mau ditanyakan? (1-{len(self.last_results)})"
            else:
                self.response = "Belum ada hasil pencarian. Silakan cari kos dulu."
            return True
        
        response = self._execute_aksi(aksi, kos)
        if response:
            self.response = response
            self.state = State.DETAIL_KOS
            self.nlp.set_state("DETAIL_KOS")
            return True
        
        return False
    
    def _handle_aksi(self, user_input: str) -> bool:
        if not self.last_results:
            return False
        
        if self._handle_multi_question(user_input):
            return True
        
        if self._handle_single_question(user_input):
            return True
        
        return False
    
    def _process_search_query(self, user_input: str, entities: Dict) -> bool:
        lokasi = entities.get("lokasi")
        kedekatan = entities.get("kedekatan")
        jenis = entities.get("jenis_kos")
        budget = entities.get("budget")
        budget_min = entities.get("budget_min")
        budget_max = entities.get("budget_max")
        
        has_criteria = lokasi or kedekatan or budget or budget_min or budget_max or jenis
        
        if has_criteria:
            self.search_criteria["lokasi"] = lokasi
            self.search_criteria["kedekatan"] = kedekatan
            self.search_criteria["jenis"] = jenis
            self.search_criteria["budget_min"] = budget_min
            self.search_criteria["budget_max"] = budget_max
            self.search_criteria["budget"] = budget if budget_max is None else None
            self._show_search_results()
            return True
        
        return False
    
    def _show_search_results(self):
        self.last_results = self._query_kos()
        
        if not self.last_results:
            criteria_parts = []
            if self.search_criteria["lokasi"]:
                criteria_parts.append(f"lokasi {self.search_criteria['lokasi']}")
            elif self.search_criteria["kedekatan"]:
                criteria_parts.append(f"dekat {self.search_criteria['kedekatan']}")
            
            if self.search_criteria.get("budget_min") is not None:
                criteria_parts.append(f"budget minimal {self._fmt_harga(self.search_criteria['budget_min'])}")
            if self.search_criteria.get("budget_max") is not None:
                criteria_parts.append(f"budget maksimal {self._fmt_harga(self.search_criteria['budget_max'])}")
            elif self.search_criteria["budget"] is not None:
                criteria_parts.append(f"budget maksimal {self._fmt_harga(self.search_criteria['budget'])}")
            
            if self.search_criteria["jenis"]:
                criteria_parts.append(f"jenis {self.search_criteria['jenis']}")
            
            self.response = f"Maaf, tidak ada kos yang cocok dengan kriteria tersebut. Coba dengan lokasi atau budget lain ya."
            self.state = State.MENU
            self.nlp.set_state("MENU")
            return
        
        self.selected_kos = None
        self.selected_kos_id = None
        self.selected_kos_nomor = None
        
        self.response = self._build_kos_list(self.last_results)
        self.state = State.HASIL_PENCARIAN
        self.nlp.set_state("HASIL_PENCARIAN")
    
    def _extract_fasilitas_from_text(self, text: str) -> List[str]:
        fasilitas_list = []
        fasilitas_keywords = ["wifi", "ac", "kipas", "kamar mandi dalam", "kamar mandi luar", 
                              "parkir motor", "parkir mobil", "dapur", "lemari", "kasur", 
                              "meja", "laundry", "air panas", "tv", "kulkas", "dispenser"]
        
        for fas in fasilitas_keywords:
            if fas in text.lower():
                fasilitas_list.append(fas)
        
        return fasilitas_list
    
    def step(self, user_input: str):
        if not user_input.strip():
            return
        
        # QUICK BUTTON HANDLER - Pencarian berdasarkan kriteria spesifik
        if "Saya ingin mencari kos berdasarkan" in user_input:
            if "lokasi" in user_input:
                self.state = State.INPUT_LOKASI
                self.response = "Tentu! Mau cari kos di daerah mana? Contoh: Tembalang, Banyumanik, Pedurungan"
                self.nlp.set_state("INPUT_LOKASI")
                return
            elif "budget" in user_input:
                self.state = State.INPUT_BUDGET
                self.response = "Baik. Budget per bulannya berapa? (Misal: 500rb, 1jt, atau tulis 'tidak ada batasan')"
                self.nlp.set_state("INPUT_BUDGET")
                return
            elif "kategori" in user_input:
                self.state = State.INPUT_JENIS
                self.response = "Jenis kos yang dicari? (Putra, Putri, atau Campur)"
                self.nlp.set_state("INPUT_JENIS")
                return
            elif "fasilitas" in user_input:
                self.response = "Silakan sebutkan fasilitas yang diinginkan. Contoh: AC, wifi, kamar mandi dalam, parkir motor. Nanti saya akan cari kos dengan fasilitas tersebut."
                self.state = State.INPUT_FASILITAS
                self.nlp.set_state("INPUT_FASILITAS")
                return
            elif "kondisi" in user_input:
                self.response = "Kondisi apa yang ingin Anda cari tahu? (Banjir, Keamanan, Kebersihan, Kebisingan, Akses Jalan, Listrik, Air, Udara, Pencahayaan, atau Lingkungan). Ketik 'semua kondisi' untuk melihat semuanya."
                self.state = State.MENU
                self.nlp.set_state("MENU")
                return
            elif "aturan" in user_input:
                self.response = "Untuk melihat aturan kos, silakan cari kos dulu dengan menyebutkan lokasi dan budget. Setelah daftar kos muncul, ketik 'aturan kos 1' untuk melihat aturan kos pertama."
                self.state = State.MENU
                self.nlp.set_state("MENU")
                return
        
        self.nlp.set_state(self.state.name)
        nlp_result = self.nlp.process(user_input)
        intent = nlp_result["intent"]
        confidence = nlp_result["confidence"]
        entities = nlp_result["entities"]
        cleaned = nlp_result["cleaned"]
        
        # RESET - masuk ke state EXIT
        if intent == "reset" and confidence > 0.5:
            self.state = State.EXIT
            self.response = "✅ Percakapan telah direset.\n\nTekan tombol **✨ Mulai Sesi Baru** di bawah untuk memulai percakapan baru."
            return
        
        # KELUAR - masuk ke state EXIT
        if intent == "keluar" and confidence > 0.5:
            self.state = State.EXIT
            self.response = "👋 Terima kasih sudah menggunakan KosFind!\n\nTekan tombol **✨ Mulai Sesi Baru** di bawah jika ingin memulai percakapan baru."
            return
        
        # BANTUAN
        if intent == "bantuan" and confidence > 0.5:
            self.state = State.BANTUAN
            self.response = (
                "Panduan KosFind:\n\n"
                "Cari kos:\n"
                "- Cari kos putri di Tembalang budget 800rb\n"
                "- Cari kos budget dibawah 1jt\n"
                "- Rekomendasi kos dekat kampus\n\n"
                "Setelah daftar kos muncul, tanyakan:\n"
                "- fasilitas kos 1\n"
                "- aturan kos 1\n"
                "- ada kamar kosong?\n"
                "- cek banjir kos 1\n"
                "- detail kos 1\n"
                "- kondisi kosnya gimana\n\n"
                "Reset/Keluar: ketik 'reset' atau 'keluar'\n"
                "Kembali ke menu: menu utama"
            )
            return
        
        # KEMBALI KE MENU
        if intent == "kembali_menu" and confidence > 0.5:
            self._reset_search()
            self.last_results = []
            self.selected_kos = None
            self.selected_kos_id = None
            self.selected_kos_nomor = None
            self.state = State.MENU
            self.response = "Baik, kembali ke menu utama. Ada yang bisa saya bantu?"
            self.nlp.set_state("MENU")
            return
        
        # KEMBALI KE HASIL
        if intent == "kembali_hasil" and self.last_results and confidence > 0.5:
            self.state = State.HASIL_PENCARIAN
            self.response = self._build_kos_list(self.last_results)
            self.nlp.set_state("HASIL_PENCARIAN")
            return
        
        # SAPAAN
        if self.state in [State.MENU, State.GREETING] and intent == "salam" and confidence > 0.5:
            self.response = "Halo! Ada yang bisa saya bantu? Silakan sebutkan kriteria kos yang dicari."
            self.state = State.MENU
            self.nlp.set_state("MENU")
            return
        
        # STATE: GREETING
        if self.state == State.GREETING:
            self.state = State.MENU
            self.nlp.set_state("MENU")
        
        # STATE: MENU
        if self.state == State.MENU:
            if self._process_search_query(user_input, entities):
                return
            
            if intent == "rekomendasi" and confidence > 0.5:
                kedekatan = entities.get("kedekatan")
                budget = entities.get("budget")
                budget_min = entities.get("budget_min")
                budget_max = entities.get("budget_max")
                jenis = entities.get("jenis_kos")
                
                results = KOS_DATA[:]
                if kedekatan:
                    results = [k for k in results if kedekatan in k.get("dekat", [])]
                if budget_max:
                    results = [k for k in results if k["harga"] <= budget_max]
                elif budget:
                    results = [k for k in results if k["harga"] <= budget]
                if budget_min:
                    results = [k for k in results if k["harga"] >= budget_min]
                if jenis:
                    results = [k for k in results if k["jenis"] == jenis]
                
                results.sort(key=lambda x: (-x["rating"], x["harga"]))
                results = results[:5]
                self.last_results = results
                
                if results:
                    self.response = self._build_kos_list(results)
                    self.state = State.HASIL_PENCARIAN
                    self.nlp.set_state("HASIL_PENCARIAN")
                else:
                    self.response = "Maaf, tidak ada rekomendasi yang cocok dengan kriteria tersebut."
                return
            
            if intent == "cari_kos" and confidence > 0.5:
                self.state = State.INPUT_LOKASI
                self.response = "Mau cari kos di daerah mana?"
                self.nlp.set_state("INPUT_LOKASI")
                return
            
            self.response = "Maaf, saya kurang paham. Silakan sebutkan kriteria kos yang dicari, atau ketik 'bantuan'."
            return
        
        # STATE: INPUT_LOKASI
        if self.state == State.INPUT_LOKASI:
            lokasi = entities.get("lokasi")
            kedekatan = entities.get("kedekatan")
            
            if lokasi or kedekatan:
                self.search_criteria["lokasi"] = lokasi
                self.search_criteria["kedekatan"] = kedekatan
                self.state = State.INPUT_BUDGET
                self.response = "Oke. Budget per bulannya berapa? (Misal: 500rb, 1jt, atau tulis 'tidak ada batasan')"
                self.nlp.set_state("INPUT_BUDGET")
                return
            
            self.response = "Maaf, lokasi tidak dikenal. Coba sebutkan kecamatan di Semarang ya. Contoh: Tembalang, Banyumanik"
            return
        
        # STATE: INPUT_BUDGET
        if self.state == State.INPUT_BUDGET:
            budget_result = self.nlp._extract_budget(cleaned)
            
            if budget_result:
                if budget_result.get("is_min"):
                    self.search_criteria["budget_min"] = budget_result["value"]
                    self.search_criteria["budget_max"] = None
                elif budget_result.get("is_max"):
                    self.search_criteria["budget_max"] = budget_result["value"]
                    self.search_criteria["budget_min"] = None
                else:
                    self.search_criteria["budget"] = budget_result["value"]
                    self.search_criteria["budget_min"] = None
                    self.search_criteria["budget_max"] = None
            elif "tidak ada" in cleaned or "bebas" in cleaned or "skip" in cleaned:
                self.search_criteria["budget"] = None
                self.search_criteria["budget_min"] = None
                self.search_criteria["budget_max"] = None
            
            self.state = State.INPUT_JENIS
            self.response = "Terima kasih. Jenis kos yang dicari? (Putra, Putri, atau Campur)"
            self.nlp.set_state("INPUT_JENIS")
            return
        
        # STATE: INPUT_JENIS
        if self.state == State.INPUT_JENIS:
            jenis = entities.get("jenis_kos")
            if not jenis or "semua" in cleaned:
                jenis = None
            
            self.search_criteria["jenis"] = jenis
            self._show_search_results()
            return
        
        # STATE: INPUT_FASILITAS
        if self.state == State.INPUT_FASILITAS:
            fasilitas_list = self._extract_fasilitas_from_text(cleaned)
            if fasilitas_list:
                self.search_criteria["fasilitas_query"] = True
                self.search_criteria["fasilitas_list"] = fasilitas_list
                self._show_search_results()
            else:
                self.response = "Maaf, saya tidak mengenali fasilitas yang Anda sebutkan. Contoh fasilitas: AC, wifi, kamar mandi dalam, parkir motor, dapur, lemari, kasur"
                return
            return
        
        # STATE: HASIL_PENCARIAN atau DETAIL_KOS
        if self.state in [State.HASIL_PENCARIAN, State.DETAIL_KOS]:
            if self._handle_aksi(user_input):
                return
        
        # STATE: HASIL_PENCARIAN (fallback)
        if self.state == State.HASIL_PENCARIAN:
            if intent == "cari_kos" and confidence > 0.5:
                self._reset_search()
                self.state = State.INPUT_LOKASI
                self.response = "Mau cari kos di daerah mana?"
                self.nlp.set_state("INPUT_LOKASI")
                return
            
            self.response = "Silakan pilih kos dengan menyebut nomornya. Misal: 'fasilitas kos 1'"
            return
        
        # STATE: DETAIL_KOS (fallback)
        if self.state == State.DETAIL_KOS:
            if intent == "kembali_hasil" and self.last_results:
                self.state = State.HASIL_PENCARIAN
                self.response = self._build_kos_list(self.last_results)
                self.nlp.set_state("HASIL_PENCARIAN")
                return
            
            if intent == "cari_kos":
                self._reset_search()
                self.state = State.INPUT_LOKASI
                self.response = "Mau cari kos di daerah mana?"
                self.nlp.set_state("INPUT_LOKASI")
                return
            
            self.response = "Ada yang bisa saya bantu dari kos ini? (fasilitas, aturan, ketersediaan, kondisi, dll)"
            return
        
        # STATE: BANTUAN
        if self.state == State.BANTUAN:
            self.state = State.MENU
            self.response = "Baik, kembali ke menu utama. Ada yang bisa saya bantu?"
            self.nlp.set_state("MENU")
            return
        
        # STATE: EXIT
        if self.state == State.EXIT:
            self.response = "Silakan tekan tombol **✨ Mulai Sesi Baru** di bawah untuk memulai percakapan baru."
            return
        
        # FALLBACK
        self.response = "Maaf, saya kurang paham. Silakan coba lagi atau ketik 'bantuan'."
