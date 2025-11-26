import requests
import os
import sys
from urllib.parse import quote
from colorama import init, Fore, Style
import json

init(autoreset=True)

def banner():
    print(Fore.CYAN + """
    ╔══════════════════════════════════════╗
    ║      TIKTOK DOWNLOADER NO WATERMARK  ║
    ║           by @kyoasli / 2025         ║
    ╚══════════════════════════════════════╝
    """)

def download_tiktok(url):
    # Encode URL agar aman
    encoded_url = quote(url, safe='')
    api = f"https://tikwm.com/api/?url={encoded_url}&hd=1"
    
    try:
        response = requests.get(api, timeout=15)
        if response.status_code != 200:
            print(Fore.RED + f"[-] API Error: {response.status_code}")
            return
        
        data = response.json()
        
        if data.get("code") != 0:
            print(Fore.RED + f"[-] {data.get('msg', 'Unknown error')}")
            return
            
        info = data["data"]
        
        title = info["title"] or "tiktok_video"
        author = info["author"]["unique_id"]
        duration = info["duration"]
        
        # Bersihkan nama file
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            title = title.replace(char, "")
        filename = f"{title[:100]}.mp4".strip()
        
        # Pilihan download
        print(Fore.GREEN + f"\n[+] Judul    : {title}")
        print(Fore.GREEN + f"[+] Author   : @{author}")
        print(Fore.GREEN + f"[+] Durasi   : {duration} detik\n")
        
        print(Fore.YELLOW + "[1] Download Tanpa Watermark (HD)")
        print(Fore.YELLOW + "[2] Download Dengan Watermark")
        print(Fore.YELLOW + "[3] Download Musik/MP3")
        if info.get("images"):  # slideshow
            print(Fore.YELLOW + "[4] Download Semua Foto (Slideshow)")
        
        choice = input(Fore.CYAN + "\nPilih nomor (1/2/3/4): ").strip()
        
        os.makedirs("downloads", exist_ok=True)
        
        if choice == "1":
            video_url = info["hdplay"] if info.get("hdplay") else info["play"]
            download_file(video_url, f"downloads/{filename}")
            print(Fore.GREEN + f"\n✓ Berhasil disimpan: downloads/{filename}")
            
        elif choice == "2":
            video_url = info["wmplay"]
            download_file(video_url, f"downloads/[WITH_WM]_{filename}")
            print(Fore.GREEN + f"\n✓ Berhasil disimpan (with watermark)")
            
        elif choice == "3":
            music_url = info["music_info"]["play"] or info["music"]
            music_title = info["music_info"]["title"] or "tiktok_music"
            for char in invalid_chars:
                music_title = music_title.replace(char, "")
            download_file(music_url, f"downloads/{music_title[:100]}.mp3")
            print(Fore.GREEN + f"\n✓ Musik berhasil disimpan!")
            
        elif choice == "4" and info.get("images"):
            print(Fore.YELLOW + f"\nMengunduh {len(info['images'])} foto...")
            for i, img_url in enumerate(info["images"], 1):
                ext = img_url.split("?")[0].split(".")[-1]
                img_name = f"downloads/{title[:80]}_slide_{i}.{ext}"
                download_file(img_url, img_name, show_progress=False)
                print(Fore.GREEN + f"   Foto {i} saved")
            print(Fore.GREEN + "\n✓ Semua foto slideshow berhasil diunduh!")
            
    except Exception as e:
        print(Fore.RED + f"[-] Error: {str(e)}")

def download_file(url, filepath, show_progress=True):
    try:
        r = requests.get(url, stream=True, timeout=30)
        r.raise_for_status()
        total = int(r.headers.get('content-length', 0))
        
        with open(filepath, "wb") as f:
            downloaded = 0
            chunk_size = 1024 * 1024  # 1MB
            for chunk in r.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if show_progress and total > 0:
                        percent = (downloaded / total) * 100
                        print(Fore.MAGENTA + f"\r   Downloading... {percent:.1f}%", end="", flush=True)
        if show_progress:
            print()  # new line setelah progress
    except Exception as e:
        print(Fore.RED + f"\nGagal download: {str(e)}")
        if os.path.exists(filepath):
            os.remove(filepath)

if __name__ == "__main__":
    banner()
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input(Fore.CYAN + "Masukkan link TikTok: ").strip()
    
    if not url.startswith("http"):
        print(Fore.RED + "Link tidak valid!")
        sys.exit()
        
    download_tiktok(url)
