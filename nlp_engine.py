# nlp_engine.py — NLP Engine untuk KosFind Semarang

import re
from difflib import SequenceMatcher
from typing import Dict, List, Optional, Tuple, Any
from data import (
    INTENTS, SINONIM, LOKASI_VALID, LOKASI_KEDEKATAN,
    FASILITAS_VALID, KONDISI_TYPES
)


class KosFindNLP:
    def __init__(self):
        self.current_state = None
        self.typo_threshold = 0.7
        
        self.all_keywords = {}
        for intent, keywords in INTENTS.items():
            if intent == "fallback":
                continue
            for kw in keywords:
                if kw:
                    self.all_keywords[kw.lower()] = intent
        
        self.common_typos = {
            "cri": "cari", "crii": "cari", "carri": "cari",
            "kost": "kos", "indekos": "kos",
            "tmbaling": "tembalang", "bnyumanik": "banyumanik",
            "dket": "dekat", "deket": "dekat",
            "budged": "budget", "budjet": "budget",
            "fasilitas": "fasilitas", "detil": "detail",
            "makasih": "terima kasih", "thx": "terima kasih",
            "dibwah": "dibawah", "bawah": "dibawah",
            "diatas": "diatas", "atas": "diatas",
            "reset": "reset", "mulai": "mulai lagi",
            "clear": "reset", "bersihkan": "reset",
            "halo": "halo", "hai": "hai", "hi": "hi"
        }
    
    def set_state(self, state: str):
        self.current_state = state
    
    def _preprocess(self, text: str) -> Tuple[str, List[str]]:
        text = text.lower().strip()
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        
        for k, v in SINONIM.items():
            text = re.sub(r'\b' + re.escape(k) + r'\b', v, text)
        
        words = text.split()
        fixed_words = []
        for w in words:
            if w in self.common_typos:
                fixed_words.append(self.common_typos[w])
            elif len(w) >= 3:
                best_match = None
                best_score = 0
                for kw in self.all_keywords.keys():
                    if len(kw) >= 3:
                        score = SequenceMatcher(None, w, kw).ratio()
                        if score > best_score and score > self.typo_threshold:
                            best_score = score
                            best_match = kw
                fixed_words.append(best_match if best_match else w)
            else:
                fixed_words.append(w)
        
        return ' '.join(fixed_words), fixed_words
    
    def detect_intent(self, text: str) -> Dict[str, Any]:
        cleaned, tokens = self._preprocess(text)
        
        scores = {}
        
        # Deteksi sapaan (halo, hai, hi, dll) - prioritas sedang
        if re.search(r'\b(halo|hai|hi|hey|selamat|pagi|siang|malam|assalamualaikum)\b', cleaned):
            scores["salam"] = scores.get("salam", 0) + 6
        
        # Reset
        if re.search(r'\b(reset|mulai lagi|clear|bersihkan|awal lagi|start over|ulang)\b', cleaned):
            scores["reset"] = scores.get("reset", 0) + 10
        
        # Cari kos
        if re.search(r'\b(cari|nyari|butuh|mau|tolong)\s+(kos|kost)\b', cleaned):
            scores["cari_kos"] = scores.get("cari_kos", 0) + 8
        
        # Detail kos
        if re.search(r'\b(detail|info|lihat|tentang)\s+(kos|kost)\s+(\d+)\b', cleaned):
            scores["lihat_detail"] = scores.get("lihat_detail", 0) + 8
        
        # Pemesanan
        if re.search(r'\b(cara|prosedur|langkah)\s+(pesan|booking|sewa)\b', cleaned):
            scores["tanya_pemesanan"] = scores.get("tanya_pemesanan", 0) + 8
        
        for intent, keywords in INTENTS.items():
            if intent == "fallback":
                continue
            for kw in keywords:
                if kw and kw in cleaned:
                    weight = 3 if ' ' in kw else 2
                    scores[intent] = scores.get(intent, 0) + weight
        
        for kondisi_type, keywords in KONDISI_TYPES.items():
            for kw in keywords:
                if kw in cleaned:
                    scores[f"tanya_kondisi_{kondisi_type}"] = scores.get(f"tanya_kondisi_{kondisi_type}", 0) + 5
        
        if not scores:
            return {"intent": "fallback", "confidence": 0.0, "cleaned": cleaned}
        
        best_intent = max(scores, key=scores.get)
        best_score = scores[best_intent]
        confidence = min(best_score / 15.0, 1.0)
        
        return {
            "intent": best_intent,
            "confidence": confidence,
            "cleaned": cleaned,
            "tokens": tokens
        }
    
    def extract_entities(self, text: str) -> Dict[str, Any]:
        cleaned, _ = self._preprocess(text)
        entities = {}
        
        match = re.search(r'\b(kos|nomor|detail)\s+(\d+)\b', cleaned)
        if match:
            entities["nomor_pilihan"] = int(match.group(2))
        else:
            numbers = re.findall(r'\b(\d+)\b', cleaned)
            if numbers and 1 <= int(numbers[0]) <= 10:
                entities["nomor_pilihan"] = int(numbers[0])
        
        for lok in LOKASI_VALID:
            if lok in cleaned:
                entities["lokasi"] = lok
                break
        
        for phrase, value in LOKASI_KEDEKATAN.items():
            if phrase in cleaned:
                entities["kedekatan"] = value
                break
        
        budget_result = self._extract_budget(cleaned)
        if budget_result:
            entities["budget"] = budget_result["value"]
            if budget_result.get("is_min"):
                entities["budget_min"] = budget_result["value"]
            if budget_result.get("is_max"):
                entities["budget_max"] = budget_result["value"]
        
        for jenis in ["putri", "putra", "campur"]:
            if jenis in cleaned:
                entities["jenis_kos"] = jenis
                break
        
        return entities
    
    def _extract_budget(self, text: str) -> Optional[Dict]:
        result = {"value": None, "is_max": False, "is_min": False, "is_range": False}
        
        # Range budget
        range_patterns = [
            r'(\d+(?:[.,]\d+)?)\s*(jt|juta|rb|ribu|k)?\s*(-|sampai|sd|hingga|to)\s+(\d+(?:[.,]\d+)?)\s*(jt|juta|rb|ribu|k)?',
            r'dari\s+(\d+(?:[.,]\d+)?)\s*(jt|juta|rb|ribu|k)?\s+(-|sampai|hingga)\s+(\d+(?:[.,]\d+)?)\s*(jt|juta|rb|ribu|k)?',
        ]
        
        for pattern in range_patterns:
            match = re.search(pattern, text)
            if match:
                groups = match.groups()
                val1 = float(groups[0].replace(',', '.'))
                unit1 = groups[1] if groups[1] else ""
                if unit1 in ['jt', 'juta']:
                    budget_min = int(val1 * 1_000_000)
                elif unit1 in ['rb', 'ribu', 'k']:
                    budget_min = int(val1 * 1000)
                else:
                    budget_min = int(val1)
                
                for i, g in enumerate(groups):
                    if g and i > 0 and isinstance(g, str) and g.replace('.', '').replace(',', '').isdigit():
                        val2 = float(g.replace(',', '.'))
                        unit2 = groups[i+1] if i+1 < len(groups) and groups[i+1] else ""
                        break
                else:
                    val2 = float(groups[3].replace(',', '.')) if len(groups) > 3 else 0
                    unit2 = groups[4] if len(groups) > 4 else ""
                
                if unit2 in ['jt', 'juta']:
                    budget_max = int(val2 * 1_000_000)
                elif unit2 in ['rb', 'ribu', 'k']:
                    budget_max = int(val2 * 1000)
                else:
                    budget_max = int(val2)
                
                result["value"] = budget_max
                result["is_range"] = True
                result["min"] = budget_min
                result["max"] = budget_max
                return result
        
        is_min_budget = False
        if re.search(r'\b(diatas|di atas|lebih dari|minimal|min|>|>=)\b', text):
            is_min_budget = True
        
        is_max_budget = False
        if re.search(r'\b(dibawah|di bawah|kurang dari|bawah|maksimal|max|<|<=)\b', text):
            is_max_budget = True
        
        match = re.search(r'\b(dibawah|di bawah|bawah|kurang dari|maksimal|max|diatas|di atas|atas|lebih dari|minimal|min)\s+(\d+(?:[.,]\d+)?)\s*(jt|juta|rb|ribu|k)?', text)
        if match:
            keyword = match.group(1)
            amount = float(match.group(2).replace(',', '.'))
            unit = match.group(3) if match.group(3) else ""
            
            if unit in ['jt', 'juta']:
                budget = int(amount * 1_000_000)
            elif unit in ['rb', 'ribu', 'k']:
                budget = int(amount * 1000)
            else:
                budget = int(amount)
            
            if keyword in ['diatas', 'di atas', 'atas', 'lebih dari', 'minimal', 'min']:
                result["value"] = budget
                result["is_min"] = True
                return result
            elif keyword in ['dibawah', 'di bawah', 'bawah', 'kurang dari', 'maksimal', 'max']:
                result["value"] = budget - 1
                result["is_max"] = True
                return result
        
        match = re.search(r'(\d+(?:[.,]\d+)?)\s*(rb|ribu|k)', text)
        if match:
            amount = float(match.group(1).replace(',', '.'))
            budget = int(amount * 1000)
            if is_max_budget:
                result["value"] = budget - 1
                result["is_max"] = True
            elif is_min_budget:
                result["value"] = budget
                result["is_min"] = True
            else:
                result["value"] = budget
            return result
        
        match = re.search(r'(\d+(?:[.,]\d+)?)\s*(jt|juta)', text)
        if match:
            amount = float(match.group(1).replace(',', '.'))
            budget = int(amount * 1_000_000)
            if is_max_budget:
                result["value"] = budget - 1
                result["is_max"] = True
            elif is_min_budget:
                result["value"] = budget
                result["is_min"] = True
            else:
                result["value"] = budget
            return result
        
        match = re.search(r'\b(\d{5,7})\b', text)
        if match:
            budget = int(match.group(1))
            if is_max_budget:
                result["value"] = budget - 1
                result["is_max"] = True
            elif is_min_budget:
                result["value"] = budget
                result["is_min"] = True
            else:
                result["value"] = budget
            return result
        
        match = re.search(r'rp\s*(\d+(?:[.,]\d+)?)', text)
        if match:
            amount = float(match.group(1).replace(',', '.'))
            budget = int(amount)
            if is_max_budget:
                result["value"] = budget - 1
                result["is_max"] = True
            elif is_min_budget:
                result["value"] = budget
                result["is_min"] = True
            else:
                result["value"] = budget
            return result
        
        return None if result["value"] is None else result
    
    def process(self, text: str) -> Dict[str, Any]:
        intent_result = self.detect_intent(text)
        entities = self.extract_entities(text)
        
        return {
            "raw": text,
            "cleaned": intent_result["cleaned"],
            "intent": intent_result["intent"],
            "confidence": intent_result["confidence"],
            "entities": entities,
            "success": True
        }