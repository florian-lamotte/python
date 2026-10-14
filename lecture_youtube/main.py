from yt_dlp import YoutubeDL
import csv
import time
import random

channel_url_playlist = "https://www.youtube.com/playlist?list="

# entêtes du fichier csv et données de la vidéo à récupérer
csv_fields = ["Titres", "Albums", "Artistes", "Sorties", "Durées", "id"]
video_fields = ["title", "album", "artist", "release_date", "duration_string", "id"]

# mapping des colonnes csv avec les données vidéo
csv_map = dict(zip(csv_fields, video_fields))

prefix = ""

ydl_opts = {
    'quiet': True,
    'extract_flat': True,
}

with YoutubeDL(ydl_opts) as ydl:  
    channel_info = ydl.extract_info(channel_url_playlist, download=False)
    entries = [{"id": e.get('id'), "title": e.get('title')} for e in channel_info['entries'] if e and e.get('id')]

with open("videos.csv", "a", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_fields)
    writer.writeheader()

    for entry in entries[600:]:
        video_url = f"https://www.youtube.com/watch?v={entry['id']}"

        try:
            with YoutubeDL({'quiet': True}) as ydl:
                video_info = ydl.extract_info(video_url, download=False)
        except Exception:
            video_info = entry
        
        row = {csv_col: video_info.get(video_col) or "" for csv_col, video_col in csv_map.items()}
        
        if row["Artistes"].startswith(prefix):
            row["Artistes"] = row["Artistes"][len(prefix):].strip()
        
        # écrit ces informations dans le fichier CSV
        writer.writerow(row)
        
        time.sleep(random.uniform(2, 3))
