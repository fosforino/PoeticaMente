import numpy as np
import cv2
import os
import sys
import time
# La nuova sintassi per MoviePy 2.x
from moviepy import VideoFileClip, AudioFileClip

# === CONFIGURAZIONE ORIGINALE ===
ASSETS_DIR = "assets"
image_fronte_path = os.path.join(ASSETS_DIR, "Fronte_3d.png") 
image_retro_path = os.path.join(ASSETS_DIR, "Retro_3d.png")
audio_file = os.path.join(ASSETS_DIR, "musica_colossal.mp3")
output_video = os.path.join(ASSETS_DIR, "medaglia_v2.mp4")
temp_video_avi = "temp_render.avi"

width, height = 1920, 1080
fps = 30
duration = 20  # Video più rapido e dinamico
total_frames = fps * duration

if os.path.exists(output_video):
    os.remove(output_video)

def prepare_image(path):
    if not os.path.exists(path):
        print(f"❌ Errore: manca {path}")
        sys.exit()
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    # Se PNG ha canale alpha, lo fondiamo su nero per eliminare aloni
    if img is not None and img.shape[2] == 4:
        alpha = img[:,:,3] / 255.0
        for c in range(3):
            img[:,:,c] = (img[:,:,c] * alpha).astype(np.uint8)
        img = img[:,:,:3]
    
    h, w = img.shape[:2]
    target_h = int(height * 0.70)
    ratio = w / h
    target_w = int(target_h * ratio)
    return cv2.resize(img, (target_w, target_h), interpolation=cv2.INTER_LANCZOS4), target_w, target_h

img_fronte, t_w, t_h = prepare_image(image_fronte_path)
img_retro, _, _ = prepare_image(image_retro_path)

fourcc = cv2.VideoWriter_fourcc(*'MJPG')
video = cv2.VideoWriter(temp_video_avi, fourcc, fps, (width, height))

print(f"🚀 Renderizzazione Medaglione Poeticamente in corso...")

for i in range(total_frames):
    frame = np.zeros((height, width, 3), dtype=np.uint8)
    progress = i / total_frames
    angolo_rad = np.radians(progress * (2 * 360)) # 2 giri completi in 20 secondi
    
    cos_a = np.cos(angolo_rad)
    is_front = cos_a >= 0
    img_target = img_fronte if is_front else img_retro
    
   # === NUOVO CODICE 3D DEFINITIVE: Centratura & Profondità ===
    w_effettivo = t_w * abs(cos_a)
    
    # Ricalcoliamo x_offset per una centratura dinamica perfetta
    x_offset = (width - w_effettivo) / 2
    
    # Innalziamo dist_p per forzare l'illusione dello spessore
    dist_p = abs(np.sin(angolo_rad)) * 160 
    
    src_pts = np.float32([[0, 0], [t_w, 0], [t_w, t_h], [0, t_h]])
    
    # y_offset garantisce la centratura verticale nel frame 1080p
    y_offset = (height - t_h) / 2
    
    dst_pts = np.float32([
        [x_offset, y_offset + dist_p], 
        [x_offset + w_effettivo, y_offset - dist_p],
        [x_offset + w_effettivo, y_offset + t_h + dist_p], 
        [x_offset, y_offset + t_h - dist_p]
    ])

    matrix = cv2.getPerspectiveTransform(src_pts, dst_pts)
    warped = cv2.warpPerspective(img_target, matrix, (width, height), flags=cv2.INTER_LANCZOS4)

    # Riflesso dorato leggero
    lx = int((i % 60) / 60 * width * 1.5) - 300
    light_mask = np.zeros_like(frame)
    cv2.line(light_mask, (lx, 0), (lx + 150, height), (70, 60, 20), 40)
    cv2.GaussianBlur(light_mask, (81, 81), 0, light_mask)
    
    final_frame = cv2.addWeighted(warped, 1.0, light_mask, 0.4, 0)
    video.write(final_frame)

# IL RILASCIO DEVE STARE FUORI DAL CICLO FOR
video.release()

try:
    clip = VideoFileClip(temp_video_avi)
    if os.path.exists(audio_file):
        audio = AudioFileClip(audio_file).subclip(0, duration)
        clip = clip.set_audio(audio)
    clip.write_videofile(output_video, codec="libx264", bitrate="3000k")
    clip.close()
    if os.path.exists(temp_video_avi): 
        os.remove(temp_video_avi)
    print(f"✅ Video pronto: {output_video}")
except Exception as e:
    print(f"⚠️ Errore finale: {e}")