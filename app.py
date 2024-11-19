import streamlit as st
import requests

# Konfigurasi halaman
st.set_page_config(
    page_title="Interest Recommendation by Zartificial",
    page_icon="🎯",  # Mengubah ikon menjadi panah
    layout="wide",
    initial_sidebar_state="expanded",
)

# Fungsi untuk memanggil API Facebook
def get_interest_recommendations(access_token, search_term, limit=10, locale="en_US"):
    url = f"https://graph.facebook.com/v16.0/search"
    params = {
        "type": "adinterest",
        "q": search_term,
        "limit": limit,
        "locale": locale,
        "access_token": access_token,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json().get("data", [])
        return [item["name"] for item in data]  # Ambil hanya nama interest
    else:
        st.error(f"Error {response.status_code}: {response.json().get('error', {}).get('message', 'Tidak diketahui')}")
        return []

# Sidebar
with st.sidebar:
    st.header("🔧 Konfigurasi")
    st.write("Sesuaikan parameter untuk mencari rekomendasi interest.")
    access_token = st.text_input("🔑 Masukkan Access Token", type="password")
    search_term = st.text_input("🔍 Masukkan Kata Kunci", placeholder="Contoh: Technology")
    limit = st.slider("📊 Jumlah Rekomendasi", min_value=1, max_value=100, value=50)
    locale = st.selectbox("🌐 Pilih Bahasa/Region", options=["en_US", "id_ID", "es_ES"], index=0)
    submit_button = st.button("🚀 Cari Rekomendasi")

# Header
st.title("🎯 Interest Recommendation by Zartificial")
st.markdown(
    """
    **🔎 Dapatkan rekomendasi interest terbaik** untuk kampanye iklan Meta Ads Anda.  
    Masukkan kata kunci di sidebar untuk memulai pencarian.
    """
)

# Jika tombol ditekan, ambil data dari API
if submit_button:
    if not access_token:
        st.error("❌ Silakan masukkan Access Token terlebih dahulu.")
    elif not search_term:
        st.error("❌ Silakan masukkan kata kunci untuk pencarian.")
    else:
        with st.spinner("⏳ Mengambil data..."):
            interests = get_interest_recommendations(access_token, search_term, limit, locale)
        
        if interests:
            st.success(f"✅ Ditemukan {len(interests)} rekomendasi interest untuk '{search_term}'")

            # Tampilkan hasil dalam paragraf
            paragraph_result = ", ".join(interests)
            st.markdown("### 🔽 Hasil Rekomendasi:")
            st.write(
                f"<div style='padding: 15px; background-color: #f9f9f9; border-radius: 8px; border: 1px solid #e0e0e0; font-size: 16px;'>"
                f"{paragraph_result}</div>",
                unsafe_allow_html=True,
            )

            # # Menambahkan rekomendasi dalam daftar bernomor dengan gaya kartu
            # st.markdown("### 📋 Rekomendasi Individu:")
            # for idx, interest in enumerate(interests, start=1):
            #     st.markdown(
            #         f"""
            #         <div style='padding: 10px; margin-bottom: 8px; background-color: #ffffff; border-radius: 5px; 
            #                     border: 1px solid #ddd; box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);'>
            #             <strong>{idx}. {interest}</strong>
            #         </div>
            #         """,
            #         unsafe_allow_html=True,
            #     )
        else:
            st.warning("⚠️ Tidak ada hasil yang ditemukan. Coba gunakan kata kunci lain atau atur ulang filter.")

# Footer
st.markdown("---")
st.caption("Dikembangkan oleh Zartificial © 2024.")
