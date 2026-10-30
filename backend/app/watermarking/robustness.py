import os
import time
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
from app.watermarking.invisible_dct import embed_dct_watermark_image, extract_dct_watermark_image

def calculate_psnr(orig: Image.Image, modified: Image.Image) -> float:
    """Calculates Peak Signal-to-Noise Ratio (PSNR) in dB."""
    arr1 = np.array(orig.convert('RGB'), dtype=np.float32)
    arr2 = np.array(modified.convert('RGB'), dtype=np.float32)
    mse = np.mean((arr1 - arr2) ** 2)
    if mse == 0:
        return 100.0  # Perfect identity
    max_pixel = 255.0
    return float(20 * np.log10(max_pixel / np.sqrt(mse)))

def calculate_bit_error_rate(str1: str, str2: str) -> float:
    if not str2:
        return 1.0
    s1_bits = "".join(bin(ord(c))[2:].zfill(8) for c in str1)
    s2_bits = "".join(bin(ord(c))[2:].zfill(8) for c in str2)
    min_len = min(len(s1_bits), len(s2_bits))
    max_len = max(len(s1_bits), len(s2_bits))
    diff = sum(1 for a, b in zip(s1_bits[:min_len], s2_bits[:min_len])) + (max_len - min_len)
    return float(diff / max_len)

def run_single_experiment(
    carrier_image: Image.Image,
    payload_text: str,
    transformation_type: str,
    intensity: float
) -> dict:
    """
    Executes controlled robustness trial on watermarked image.
    Supports:
    - jpeg_compression (intensity = quality factor, e.g. 85, 70, 50)
    - resize (intensity = scale factor, e.g. 0.75, 0.5)
    - gaussian_noise (intensity = std dev of noise)
    - crop (intensity = percentage border cropped, e.g. 0.05)
    - contrast_adjust (intensity = contrast multiplier)
    """
    start_time = time.time()
    
    # 1. Embed watermark
    watermarked_img, _ = embed_dct_watermark_image(carrier_image, payload_text)
    
    # 2. Apply chosen transformation
    transformed_img = watermarked_img.copy()
    
    if transformation_type == "jpeg_compression":
        # Save to buffer with JPEG compression
        quality = int(np.clip(intensity, 10, 95))
        temp_path = f"/tmp/aq_exp_{os.getpid()}_{time.time()}.jpg"
        watermarked_img.save(temp_path, format="JPEG", quality=quality)
        transformed_img = Image.open(temp_path).convert("RGB")
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
    elif transformation_type == "resize":
        # Downscale and upscale back to original resolution
        orig_w, orig_h = watermarked_img.size
        scale = float(np.clip(intensity, 0.25, 0.95))
        new_w = max(64, int(orig_w * scale))
        new_h = max(64, int(orig_h * scale))
        down = watermarked_img.resize((new_w, new_h), Image.Resampling.BILINEAR)
        transformed_img = down.resize((orig_w, orig_h), Image.Resampling.BILINEAR)
        
    elif transformation_type == "gaussian_noise":
        arr = np.array(watermarked_img, dtype=np.float32)
        noise = np.random.normal(0, intensity, arr.shape)
        noisy_arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
        transformed_img = Image.fromarray(noisy_arr)
        
    elif transformation_type == "crop":
        crop_ratio = float(np.clip(intensity, 0.01, 0.20))
        orig_w, orig_h = watermarked_img.size
        left = int(orig_w * crop_ratio)
        top = int(orig_h * crop_ratio)
        right = orig_w - left
        bottom = orig_h - top
        cropped = watermarked_img.crop((left, top, right, bottom))
        transformed_img = cropped.resize((orig_w, orig_h), Image.Resampling.BILINEAR)
        
    elif transformation_type == "contrast_adjust":
        enhancer = ImageEnhance.Contrast(watermarked_img)
        transformed_img = enhancer.enhance(intensity)
        
    # 3. Attempt extraction
    extracted_payload, confidence = extract_dct_watermark_image(transformed_img)
    duration_ms = int((time.time() - start_time) * 1000)
    
    # 4. Measure metrics
    psnr = calculate_psnr(watermarked_img, transformed_img)
    recovered = (extracted_payload == payload_text) if extracted_payload else False
    ber = calculate_bit_error_rate(payload_text, extracted_payload or "")
    
    return {
        "transformation_type": transformation_type,
        "intensity": intensity,
        "psnr_db": round(psnr, 2),
        "detected": (extracted_payload is not None),
        "payload_recovered": recovered,
        "extracted_payload": extracted_payload,
        "bit_error_rate": round(ber, 4),
        "duration_ms": duration_ms
    }
