import yt_dlp
import json

playlist_url = "https://www.youtube.com/playlist?list=PLXki4Tcp9MSqQNvBOAiEDZMplSv07vcyY"
video_list = []

ydl_opts = {
    'quiet': True,
    'extract_flat': True,
    'skip_download': True,
    'force_generic_extractor': True
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(playlist_url, download=False)
    entries = info.get('entries', [])
    
    for index, entry in enumerate(entries, start=1):
        video_info = {
            "title": f"{index}. {entry.get('title')}",
            "link": f"https://www.youtube.com/watch?v={entry.get('id')}",
            "description": ""  # Nếu cần mô tả thì cần chạy lại với extract_flat=False
        }
        video_list.append(video_info)

with open("playlist_videos.json", "w", encoding="utf-8") as f:
    json.dump(video_list, f, indent=2, ensure_ascii=False)

print("✅ Đã lưu xong playlist_videos.json")
