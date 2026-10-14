"""Draws the LempiraFlow app icon (green tile with a white spending ring) as PNGs, no dependencies."""
import math, struct, zlib, os

OUT = os.path.join(os.path.dirname(__file__), '..', 'icons')

def png(path, size, pixels):
    raw = b''.join(b'\x00' + bytes(pixels[y*size*4:(y+1)*size*4]) for y in range(size))
    def chunk(t, d): return struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
    data = b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', size, size, 8, 6, 0, 0, 0)) \
        + chunk(b'IDAT', zlib.compress(raw, 9)) + chunk(b'IEND', b'')
    with open(path, 'wb') as f: f.write(data)

def clamp(v): return max(0.0, min(1.0, v))

def draw(size, maskable=False):
    top, bot = (0x16, 0x9A, 0x67), (0x0C, 0x5E, 0x3F)
    px = bytearray(size * size * 4)
    c = size / 2
    scale = 0.78 if maskable else 1.0          # keep the ring inside the maskable safe zone
    R, w = size * 0.27 * scale, size * 0.085 * scale
    gap0, gap1 = math.radians(-90), math.radians(-90 + 70)   # missing slice at top-right
    split = math.radians(-90 + 200)                            # second shade starts here
    for y in range(size):
        t = y / (size - 1)
        bg = [top[i] + (bot[i] - top[i]) * t for i in range(3)]
        for x in range(size):
            dx, dy = x + .5 - c, y + .5 - c
            d = math.hypot(dx, dy)
            cov = clamp(w / 2 - abs(d - R) + .5)
            a = math.atan2(dy, dx)
            rel = (a - gap0) % (2 * math.pi)
            if rel < (gap1 - gap0): cov = 0
            col = bg
            if cov:
                ring = (255, 255, 255) if ((a - split) % (2 * math.pi)) > math.radians(160) else (0xBF, 0xEB, 0xD6)
                col = [bg[i] * (1 - cov) + ring[i] * cov for i in range(3)]
            # small "L" coin dot in the gap
            dd = math.hypot(dx - R * math.cos(math.radians(-55)), dy - R * math.sin(math.radians(-55)))
            dc = clamp(w * .62 - dd + .5)
            if dc: col = [col[i] * (1 - dc) + (0xF2, 0xC1, 0x4E)[i] * dc for i in range(3)]
            o = (y * size + x) * 4
            px[o:o+4] = bytes([int(col[0]), int(col[1]), int(col[2]), 255])
    return px

os.makedirs(OUT, exist_ok=True)
for name, size, mask in [('apple-touch-icon.png', 180, False), ('icon-192.png', 192, False),
                         ('icon-512.png', 512, False), ('icon-maskable-512.png', 512, True)]:
    png(os.path.join(OUT, name), size, draw(size, mask))
    print('wrote', name)
