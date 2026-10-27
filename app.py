import streamlit as st
import yt_dlp
import os
import shutil

st.set_page_config(
    page_title="OmniGrab - Modern Media Downloader", 
    page_icon="⚡", 
    layout="centered"
)

st.markdown("""
    <style>
    /* Mengatur latar belakang dan font utama */
    .main {
        background-color: #0f172a;
        color: #f8fafc;
    }
    
    /* Judul Utama */
    h1 {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        background: linear-gradient(90deg, #3b82f6, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding-bottom: 10px;
    }
    
    /* Subtitle */
    .subtext {
        text-align: center;
        color: #94a3b8;
        font-size: 1.1rem;
        margin-bottom: 30px;
    }

    /* Kotak Input dan Selectbox */
    .stTextInput input, .stSelectbox select {
        background-color: #1e293b !important;
        color: white !important;
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
        padding: 12px !important;
    }
    
    /* Tombol Utama */
    .stButton button {
        width: 100%;
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        font-weight: 600;
        border-radius: 12px;
        padding: 12px;
        border: none;
        box-shadow: 0 4px 14px rgba(59, 130, 246, 0.4);
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.6);
        transform: translateY(-1px);
    }

    /* Tombol Download Hasil */
    .stDownloadButton button {
        width: 100%;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        font-weight: 700;
        border-radius: 12px;
        padding: 14px;
        border: none;
        box-shadow: 0 4px 14px rgba(16, 185, 129, 0.4);
    }
    
    /* Kartu / Kotak Informasi */
    .success-box {
        background-color: #1e293b;
        border: 1px solid #334155;
        padding: 20px;
        border-radius: 16px;
        text-align: center;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>OmniGrab Cloud</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtext'>Platform download video & audio universal berkecepatan tinggi tanpa batas durasi.</p>", unsafe_allow_html=True)

with st.container():
    url = st.text_input("🔗 Link Media Sosial", placeholder="Tempel link YouTube, TikTok, IG, dll di sini...")
    format_pilihan = st.selectbox("🎯 Pilih Format Output", ["MP4 (Video Full HD/4K)", "MP3 (Audio Kualitas Tinggi)"])

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🚀 Proses & Ambil File", type="primary"):
        if not url.strip():
            st.warning("⚠️ Masukkan URL terlebih dahulu!")
        else:
            output_dir = "downloads_temp"
            if os.path.exists(output_dir):
                shutil.rmtree(output_dir)
            os.makedirs(output_dir, exist_ok=True)

            status_text = st.empty()
            status_text.info("⏳ Menghubungkan ke server media, mohon tunggu...")

            ydl_opts = {
                'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
                'noplaylist': True,
                'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
                'geo_bypass': True,
            }

            if "MP3" in format_pilihan:
                ydl_opts.update({
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                })
            else:
                ydl_opts.update({
                    'format': 'bestvideo+bestaudio/best',
                    'merge_output_format': 'mp4',
                })

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)
                    
                    if "MP3" in format_pilihan:
                        filename = os.path.splitext(filename)[0] + ".mp3"
                    else:
                        filename = os.path.splitext(filename)[0] + ".mp4"

                status_text.empty()
                
                if os.path.exists(filename):
                    file_size_mb = os.path.getsize(filename) / (1024 * 1024)
                    
                    st.markdown(f"""
                        <div class="success-box">
                            <h3 style="color: #34d399; margin-bottom: 5px;">✨ Berhasil Diproses!</h3>
                            <p style="color: #94a3b8; font-size: 0.95rem;">Ukuran File: <b>{file_size_mb:.2f} MB</b></p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)

                    with open(filename, "rb") as f:
                        st.download_button(
                            label="📥 DOWNLOAD FILE SEKARANG",
                            data=f,
                            file_name=os.path.basename(filename),
                            mime="audio/mpeg" if "MP3" in format_pilihan else "video/mp4"
                        )
                else:
                    st.error("❌ Gagal menemukan file hasil download.")

            except Exception as e:
                status_text.empty()
                st.error(f"❌ Terjadi kesalahan: {e}")
