import streamlit as st
import json

# Sayfa yapılandırması
st.set_page_config(page_title="Hanefi Fıkhı Rehberi", layout="wide")

# JSON Verisini Yükle
@st.cache_data
def veriyi_yukle():
    try:
        with open("fikihrehberi.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"JSON yükleme hatası: {e}")
        return None

data = veriyi_yukle()

if data:
    st.title(f"📖 {data.get('kitap_adi', 'Fıkıh Rehberi')}")
    st.caption(f"Yazar: {data.get('yazar')}")

    # --- YAN PANEL (SIDEBAR) ---
    st.sidebar.header("Bölümler")
    bolum_isimleri = [bolum["bolum"] for bolum in data["icerik"]]
    secilen_bolum_adi = st.sidebar.radio("Bir bölüm seçin:", bolum_isimleri)

    # --- ÜST ARAMA ÇUBUĞU ---
    arama_terimi = st.text_input("🔍 Fıkhi bir kavram veya hüküm arayın...", placeholder="Örn: Sehiv Secdesi, İmsak, Mehir...")

    # --- İÇERİK GÖSTERİMİ ---
    if arama_terimi:
        st.subheader(f"'{arama_terimi}' için arama sonuçları:")
        bulundu = False
        for bolum in data["icerik"]:
            for alt in bolum.get("alt_konular", []):
                # Başlıkta veya maddelerde ara
                terim = arama_terimi.lower()
                if terim in alt["baslik"].lower() or any(terim in m.lower() for m in alt["maddeler"]):
                    with st.expander(f"{bolum['bolum']} > {alt['baslik']}", expanded=True):
                        for madde in alt["maddeler"]:
                            if terim in madde.lower():
                                st.markdown(f"✅ **{madde}**")
                            else:
                                st.write(f"• {madde}")
                    bulundu = True
        if not bulundu:
            st.warning("Eşleşen bir sonuç bulunamadı.")
    
    else:
        # Normal Bölüm Gösterimi
        for bolum in data["icerik"]:
            if bolum["bolum"] == secilen_bolum_adi:
                st.header(bolum["bolum"])
                for alt in bolum.get("alt_konular", []):
                    with st.container():
                        st.subheader(alt["baslik"])
                        for madde in alt["maddeler"]:
                            st.write(f"🔹 {madde}")
                        st.divider()