import streamlit as st
import yt_dlp
import os
import shutil

st.set_page_config(page_title="Devoin-Play", page_icon="📥", layout="centered")

st.title("📥 Devoin-Play - Downloader")
st.markdown("Download video panjang, film, atau audio dari **YouTube, TikTok, Instagram, dll** tanpa batasan durasi!")

url = st.text_input("🔗 Masukkan Link URL Media Sosial:", placeholder="https://...")
format_pilihan = st.selectbox("Pilih Format Output:", ["MP4 (Video Full HD/4K)", "MP3 (Audio Kualitas Tinggi)"])

if st.button("Proses dan Download", type="primary"):
    if not url.strip():
        st.warning("⚠️ Masukkan URL terlebih dahulu!")
    else:
    
        output_dir = "downloads_temp"
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        os.makedirs(output_dir, exist_ok=True)

        status_text = st.empty()
        status_text.text("⏳ Sedang memproses media ukuran penuh, mohon tunggu...")

        ydl_opts = {
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
            'noplaylist': True,
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

            status_text.text("✅ Berhasil! Menyiapkan tombol unduh...")
            
            if os.path.exists(filename):
                file_size_mb = os.path.getsize(filename) / (1024 * 1024)
                st.success(f"🎉 File siap! Ukuran file: **{file_size_mb:.2f} MB**")

                with open(filename, "rb") as f:
                    st.download_button(
                        label="💾 Klik di Sini untuk Menyimpan File ke Perangkat",
                        data=f,
                        file_name=os.path.basename(filename),
                        mime="audio/mpeg" if "MP3" in format_pilihan else "video/mp4"
                    )
            else:
                st.error("❌ Gagal menemukan file hasil download.")

        except Exception as e:
            st.error(f"❌ Terjadi kesalahan: {e}")