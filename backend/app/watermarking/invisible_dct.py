import os
import numpy as np
from PIL import Image
import fitz  # PyMuPDF
from scipy.fftpack import dct, idct
from typing import Tuple, Optional, Dict, Any

# Discrete Cosine Transform Watermarking in Mid-Frequency Coefficients
# Mid-frequency coefficients balance perceptual transparency and compression robustness

BLOCK_SIZE = 8
# Selected mid-frequency coordinates in an 8x8 DCT matrix
MID_FREQ_COORDS = [(3, 2), (2, 3), (4, 1), (1, 4), (3, 3), (4, 2), (2, 4)]
EMBEDDING_STRENGTH = 18.0

def _dct2(block: np.ndarray) -> np.ndarray:
    return dct(dct(block.T, norm='ortho').T, norm='ortho')

def _idct2(block: np.ndarray) -> np.ndarray:
    return idct(idct(block.T, norm='ortho').T, norm='ortho')

def text_to_bit_array(text: str, max_bits: int = 128) -> np.ndarray:
    """Converts ASCII text to bit array with preamble sync marker [1, 0, 1, 0, 1, 1, 0, 0]."""
    sync_marker = [1, 0, 1, 0, 1, 1, 0, 0]
    char_bits = []
    for char in text:
        b = bin(ord(char))[2:].zfill(8)
        char_bits.extend([int(x) for x in b])
    
    total_bits = sync_marker + char_bits
    if len(total_bits) > max_bits:
        total_bits = total_bits[:max_bits]
    else:
        # Zero-pad
        total_bits.extend([0] * (max_bits - len(total_bits)))
    return np.array(total_bits, dtype=np.uint8)

def bit_array_to_text(bits: np.ndarray) -> Optional[str]:
    """Detects preamble sync marker and extracts text."""
    sync_marker = [1, 0, 1, 0, 1, 1, 0, 0]
    bits_list = list(bits)
    
    # Check sync marker
    sync_len = len(sync_marker)
    if bits_list[:sync_len] != sync_marker:
        # Check Hamming distance to allow 1 bit error in sync
        err = sum(1 for a, b in zip(bits_list[:sync_len], sync_marker) if a != b)
        if err > 1:
            return None
    
    payload_bits = bits_list[sync_len:]
    chars = []
    for i in range(0, len(payload_bits) - 7, 8):
        byte_chunk = payload_bits[i:i+8]
        char_code = int("".join(str(b) for b in byte_chunk), 2)
        if char_code == 0:
            break
        if 32 <= char_code <= 126:
            chars.append(chr(char_code))
        else:
            break
    return "".join(chars) if chars else None

def embed_dct_watermark_image(image: Image.Image, payload_text: str) -> Tuple[Image.Image, int]:
    """
    Embeds binary payload into the Luminance (Y) channel of an image using 8x8 DCT blocks.
    Returns the watermarked PIL Image and number of bits embedded.
    """
    img_ycrcb = image.convert('YCbCr')
    y, cb, cr = img_ycrcb.split()
    y_arr = np.array(y, dtype=np.float32)
    
    h, w = y_arr.shape
    blocks_h = h // BLOCK_SIZE
    blocks_w = w // BLOCK_SIZE
    total_blocks = blocks_h * blocks_w
    
    bits = text_to_bit_array(payload_text, max_bits=min(256, total_blocks))
    num_bits = len(bits)
    
    bit_idx = 0
    # Embedding: modify difference between two mid-frequency DCT coefficients
    u1, v1 = (3, 2)
    u2, v2 = (2, 3)
    
    for bh in range(blocks_h):
        for bw in range(blocks_w):
            if bit_idx >= num_bits:
                break
                
            row_start = bh * BLOCK_SIZE
            col_start = bw * BLOCK_SIZE
            block = y_arr[row_start:row_start+BLOCK_SIZE, col_start:col_start+BLOCK_SIZE]
            
            d_block = _dct2(block)
            bit = bits[bit_idx]
            
            # Enforce difference depending on bit value
            c1 = d_block[u1, v1]
            c2 = d_block[u2, v2]
            
            if bit == 1:
                if c1 - c2 < EMBEDDING_STRENGTH:
                    d_block[u1, v1] = (c1 + c2 + EMBEDDING_STRENGTH) / 2.0
                    d_block[u2, v2] = (c1 + c2 - EMBEDDING_STRENGTH) / 2.0
            else:
                if c2 - c1 < EMBEDDING_STRENGTH:
                    d_block[u1, v1] = (c1 + c2 - EMBEDDING_STRENGTH) / 2.0
                    d_block[u2, v2] = (c1 + c2 + EMBEDDING_STRENGTH) / 2.0
            
            y_arr[row_start:row_start+BLOCK_SIZE, col_start:col_start+BLOCK_SIZE] = _idct2(d_block)
            bit_idx += 1
            
        if bit_idx >= num_bits:
            break
            
    y_mod = Image.fromarray(np.clip(y_arr, 0, 255).astype(np.uint8), mode='L')
    res_img = Image.merge('YCbCr', (y_mod, cb, cr)).convert('RGB')
    return res_img, num_bits

def extract_dct_watermark_image(image: Image.Image, max_bits: int = 128) -> Tuple[Optional[str], float]:
    """
    Extracts embedded DCT payload from the Luminance (Y) channel.
    Returns (extracted_text, confidence_score).
    """
    img_ycrcb = image.convert('YCbCr')
    y, _, _ = img_ycrcb.split()
    y_arr = np.array(y, dtype=np.float32)
    
    h, w = y_arr.shape
    blocks_h = h // BLOCK_SIZE
    blocks_w = w // BLOCK_SIZE
    
    u1, v1 = (3, 2)
    u2, v2 = (2, 3)
    
    extracted_bits = []
    bit_count = 0
    
    for bh in range(blocks_h):
        for bw in range(blocks_w):
            if bit_count >= max_bits:
                break
                
            row_start = bh * BLOCK_SIZE
            col_start = bw * BLOCK_SIZE
            block = y_arr[row_start:row_start+BLOCK_SIZE, col_start:col_start+BLOCK_SIZE]
            d_block = _dct2(block)
            
            c1 = d_block[u1, v1]
            c2 = d_block[u2, v2]
            
            extracted_bits.append(1 if c1 >= c2 else 0)
            bit_count += 1
            
        if bit_count >= max_bits:
            break
            
    extracted_text = bit_array_to_text(np.array(extracted_bits, dtype=np.uint8))
    confidence = 1.0 if extracted_text is not None else 0.0
    return extracted_text, confidence

def apply_invisible_watermark_pdf(
    input_pdf_path: str,
    output_pdf_path: str,
    payload_text: str,
    dpi: int = 150
) -> Dict[str, Any]:
    """
    Renders PDF pages to high-resolution raster images, embeds DCT watermark into the
    first page (and documents with pages), then compiles back into a standardized PDF.
    """
    doc = fitz.open(input_pdf_path)
    output_doc = fitz.open()
    
    for page_idx in range(len(doc)):
        page = doc[page_idx]
        pix = page.get_pixmap(dpi=dpi)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        # Embed on first page (primary carrier)
        if page_idx == 0:
            watermarked_img, _ = embed_dct_watermark_image(img, payload_text)
        else:
            watermarked_img = img
            
        # Save temp image for fitz insert
        temp_img_path = f"{output_pdf_path}.p{page_idx}.png"
        watermarked_img.save(temp_img_path, format="PNG")
        
        # Create new PDF page with exact matching dimensions
        rect = page.rect
        new_page = output_doc.new_page(width=rect.width, height=rect.height)
        new_page.insert_image(rect, filename=temp_img_path)
        
        if os.path.exists(temp_img_path):
            os.remove(temp_img_path)
            
    output_doc.save(output_pdf_path, deflate=True)
    output_doc.close()
    doc.close()
    
    return {
        "status": "SUCCESS",
        "watermark_type": "invisible_dct_midfreq",
        "payload_text": payload_text,
        "algorithm": "DCT-SpreadSpectrum-v1"
    }

def detect_invisible_watermark_pdf(pdf_path: str, dpi: int = 150) -> Dict[str, Any]:
    """Inspects first page of candidate PDF for DCT watermark."""
    doc = fitz.open(pdf_path)
    if len(doc) == 0:
        return {"detected": False, "extracted_payload": None, "confidence": 0.0}
        
    page = doc[0]
    pix = page.get_pixmap(dpi=dpi)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    doc.close()
    
    payload, confidence = extract_dct_watermark_image(img)
    return {
        "detected": (payload is not None),
        "extracted_payload": payload,
        "confidence": confidence,
        "algorithm": "DCT-SpreadSpectrum-v1"
    }
