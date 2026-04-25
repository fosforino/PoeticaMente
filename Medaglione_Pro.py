import numpy as np
import cv2
import os
import sys

from moviepy import VideoFileClip, AudioFileClip

# === CONFIGURAZIONE ===
ASSETS_DIR = "assets"
image_fronte_path = os.path.join(ASSETS_DIR, "Fronte.png")
image_retro_path  = os.path.join(ASSETS_DIR, "Retro.png")
audio_file        = os.path.join(ASSETS_DIR, "musica_colossal.mp3")
output_video      = os.path.join(ASSETS_DIR, "Medaglia_v2.mp4")
temp_video_avi    = "temp_render.avi"

width, height = 1920, 1080
fps           = 30
duration      = 20
total_frames  = fps * duration

if os.path.exists(output_video):
    os.remove(output_video)


# ─────────────────────────────────────────
# RIMOZIONE SFONDO
# ─────────────────────────────────────────
def remove_background(img_bgra, is_transparent_bg=False):
    """
    - is_transparent_bg=True  → PNG già trasparente (Retro): non toccare l'alpha
    - is_transparent_bg=False → sfondo nero (Fronte): crea alpha dalla luminosità
    """
    if is_transparent_bg:
        # Il Retro ha già l'alpha corretto — non fare nulla
        return img_bgra
    else:
        # Fronte: sfondo nero → crea alpha dalla luminosità
        if img_bgra.shape[2] == 3:
            img_bgra = cv2.cvtColor(img_bgra, cv2.COLOR_BGR2BGRA)

        gray = cv2.cvtColor(img_bgra, cv2.COLOR_BGRA2GRAY)
        _, alpha = cv2.threshold(gray, 15, 255, cv2.THRESH_BINARY)

        h, w = gray.shape
        mask = np.zeros((h + 2, w + 2), np.uint8)
        alpha_fill = alpha.copy()
        cv2.floodFill(alpha_fill, mask, (0, 0),     0, loDiff=200, upDiff=200)
        cv2.floodFill(alpha_fill, mask, (w-1, 0),   0, loDiff=200, upDiff=200)
        cv2.floodFill(alpha_fill, mask, (0, h-1),   0, loDiff=200, upDiff=200)
        cv2.floodFill(alpha_fill, mask, (w-1, h-1), 0, loDiff=200, upDiff=200)

        alpha_fill = cv2.GaussianBlur(alpha_fill, (3, 3), 0)
        img_bgra[:, :, 3] = alpha_fill
        return img_bgra


# ─────────────────────────────────────────
# CARICAMENTO E PREPARAZIONE IMMAGINI
# ─────────────────────────────────────────
def prepare_image(path, is_transparent_bg=False):
    if not os.path.exists(path):
        print(f"❌ Errore: manca {path}")
        sys.exit()

    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print(f"❌ Impossibile leggere {path}")
        sys.exit()

    # Assicura 4 canali
    if img.ndim == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGRA)
    elif img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

    img = remove_background(img, is_transparent_bg=is_transparent_bg)

    h, w     = img.shape[:2]
    target_h = int(height * 0.78)
    ratio    = w / h
    target_w = int(target_h * ratio)
    img      = cv2.resize(img, (target_w, target_h), interpolation=cv2.INTER_LANCZOS4)
    return img, target_w, target_h


print("📂 Caricamento immagini...")
img_fronte, t_w, t_h = prepare_image(image_fronte_path, is_transparent_bg=False)
img_retro,  _,   _   = prepare_image(image_retro_path,  is_transparent_bg=True)

# ─────────────────────────────────────────
# FIX: flip orizzontale del retro
# Compensa lo specchiamento della prospettiva
# ─────────────────────────────────────────
img_retro = cv2.flip(img_retro, 1)

print(f"✅ Fronte caricato: alpha max={img_fronte[:,:,3].max()}")
print(f"✅ Retro  caricato: alpha max={img_retro[:,:,3].max()}")


# ─────────────────────────────────────────
# COMPOSITING
# ─────────────────────────────────────────
def composite(frame, warped_bgra):
    bgr   = warped_bgra[:, :, :3].astype(np.float32)
    alpha = warped_bgra[:, :, 3:4].astype(np.float32) / 255.0
    frame = frame.astype(np.float32)
    frame = bgr * alpha + frame * (1 - alpha)
    return frame.astype(np.uint8)


# ─────────────────────────────────────────
# RENDER
# ─────────────────────────────────────────
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
video  = cv2.VideoWriter(temp_video_avi, fourcc, fps, (width, height))

print("🚀 Renderizzazione in corso...")

for i in range(total_frames):
    frame      = np.zeros((height, width, 3), dtype=np.uint8)
    progress   = i / total_frames
    angolo_rad = np.radians(progress * (2 * 360))   # 2 giri in 20 sec

    cos_a    = np.cos(angolo_rad)
    is_front = cos_a >= 0
    img_src  = img_fronte if is_front else img_retro

    w_effettivo = max(int(t_w * abs(cos_a)), 1)
    x_offset    = (width  - w_effettivo) / 2
    y_offset    = (height - t_h)         / 2
    dist_p      = abs(np.sin(angolo_rad)) * 140

    src_pts = np.float32([[0,   0  ], [t_w, 0  ], [t_w, t_h], [0,   t_h]])
    dst_pts = np.float32([
        [x_offset,               y_offset           + dist_p],
        [x_offset + w_effettivo, y_offset           - dist_p],
        [x_offset + w_effettivo, y_offset + t_h     + dist_p],
        [x_offset,               y_offset + t_h     - dist_p],
    ])

    matrix = cv2.getPerspectiveTransform(src_pts, dst_pts)
    warped = cv2.warpPerspective(img_src, matrix, (width, height),
                                 flags=cv2.INTER_LANCZOS4)

    frame = composite(frame, warped)

    # Riflesso dorato leggero
    lx         = int((i % 60) / 60 * width * 1.5) - 300
    light_mask = np.zeros((height, width, 3), dtype=np.uint8)
    cv2.line(light_mask, (lx, 0), (lx + 150, height), (70, 60, 20), 40)
    cv2.GaussianBlur(light_mask, (81, 81), 0, light_mask)
    frame = cv2.addWeighted(frame, 1.0, light_mask, 0.35, 0)

    video.write(frame)

    if i % fps == 0:
        print(f"  ⏳ {i // fps}/{duration} sec")

video.release()
print("✅ Frame renderizzati!")

# ─────────────────────────────────────────
# AUDIO + EXPORT FINALE
# ─────────────────────────────────────────
try:
    clip = VideoFileClip(temp_video_avi)
    if os.path.exists(audio_file):
        audio = AudioFileClip(audio_file).subclipped(0, duration)
        clip  = clip.with_audio(audio)
        print("🎵 Audio aggiunto!")
    else:
        print("⚠️  Nessun file audio trovato, video senza musica.")

    clip.write_videofile(output_video, codec="libx264", bitrate="3000k", logger=None)
    clip.close()

    if os.path.exists(temp_video_avi):
        os.remove(temp_video_avi)

    print(f"🎬 Video pronto: {output_video}")

except Exception as e:
    print(f"⚠️ Errore finale: {e}")