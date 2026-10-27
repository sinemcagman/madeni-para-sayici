"""uret.py - Para sayısı bilinen örnek test görüntülerini üretir.

Kök klasörden çalıştırın:  python -m ornekler.uret
Dosya adındaki sayı, görüntüdeki gerçek para sayısıdır (ör. sentetik_12.png).
Sabit tohum (seed) kullanıldığı için her çalıştırmada aynı görüntüler oluşur.
"""

from pathlib import Path

import numpy as np
from skimage import data, draw, filters, io, util

KLASOR = Path(__file__).resolve().parent

# dosya adı -> (beklenen para sayısı, --ters gerekir mi)
BEKLENEN = {
    "coins_renkli.png": (24, False),
    "coins_ters.png": (24, True),
    "coins_golgeli.png": (24, False),
    "sentetik_12.png": (12, False),
    "sentetik_7_gurultulu.png": (7, False),
    "sentetik_9_koyu_para.png": (9, True),
    "bos_masa.png": (0, False),
}


def _kaydet(ad, goruntu):
    goruntu = np.clip(goruntu, 0, 1)
    io.imsave(KLASOR / ad, util.img_as_ubyte(goruntu), check_contrast=False)


def _isik_egimi(yukseklik, genislik, guc):
    """Sol üstten sağ alta doğru kararan eşit olmayan aydınlatma."""
    y, x = np.mgrid[0:yukseklik, 0:genislik]
    return 1 - guc * (x / genislik + y / yukseklik) / 2


def _para_yerlestir(rng, adet, boyut, yaricap_araligi, bosluk=12):
    """Birbirine ve kenarlara değmeyen rastgele daireler üretir."""
    yukseklik, genislik = boyut
    paralar = []
    while len(paralar) < adet:
        r = rng.integers(*yaricap_araligi)
        y = rng.integers(r + bosluk, yukseklik - r - bosluk)
        x = rng.integers(r + bosluk, genislik - r - bosluk)
        if all((y - py) ** 2 + (x - px) ** 2 > (r + pr + bosluk) ** 2
               for py, px, pr in paralar):
            paralar.append((y, x, r))
    return paralar


def _sentetik(rng, adet, zemin, para, gurultu, boyut=(400, 520), egim=0.35):
    """Dokulu zemin üzerinde kabartmalı paralar çizer."""
    yukseklik, genislik = boyut
    goruntu = zemin + filters.gaussian(rng.normal(0, 0.04, boyut), 3)
    for y, x, r in _para_yerlestir(rng, adet, boyut, (20, 36)):
        rr, cc = draw.disk((y, x), r, shape=boyut)
        goruntu[rr, cc] = para
        # kenar halkası ve iç kabartma deseni (gerçek para gibi koyu çizgiler)
        rr, cc = draw.circle_perimeter(y, x, r - 3, shape=boyut)
        goruntu[rr, cc] = para - 0.25 * np.sign(para - zemin)
        for _ in range(4):
            dy, dx = rng.integers(-r // 2, r // 2, 2)
            rr, cc = draw.disk((y + dy, x + dx), r // 6, shape=boyut)
            goruntu[rr, cc] -= 0.15 * np.sign(para - zemin)
    goruntu = filters.gaussian(goruntu, 1)
    goruntu = goruntu * _isik_egimi(yukseklik, genislik, egim)
    return goruntu + rng.normal(0, gurultu, boyut)


def uret():
    rng = np.random.default_rng(2026)
    coins = util.img_as_float(data.coins())

    # 1) Renkli (bakır tonlu) coins: RGB -> gri dönüşümünü dener
    _kaydet("coins_renkli.png", np.dstack([coins * 1.0, coins * 0.75, coins * 0.5]))

    # 2) Ters renkli coins: paralar koyu, zemin açık -> --ters gerekir
    _kaydet("coins_ters.png", 1 - coins)

    # 3) Güçlü yan ışık/gölge: arka plan çıkarma adımını zorlar
    _kaydet("coins_golgeli.png", coins * _isik_egimi(*coins.shape, 0.6) + 0.1)

    # 4) Sentetik, açık paralar, koyu masa
    _kaydet("sentetik_12.png", _sentetik(rng, 12, zemin=0.25, para=0.75, gurultu=0.02))

    # 5) Sentetik, yoğun gürültü (kötü kamera)
    _kaydet("sentetik_7_gurultulu.png",
            _sentetik(rng, 7, zemin=0.3, para=0.7, gurultu=0.08))

    # 6) Sentetik, koyu paralar açık masa -> --ters gerekir
    _kaydet("sentetik_9_koyu_para.png",
            _sentetik(rng, 9, zemin=0.8, para=0.3, gurultu=0.02))

    # 7) Boş masa: sadece doku ve gürültü, 0 para beklenir
    bos = 0.4 + filters.gaussian(rng.normal(0, 0.04, (400, 520)), 3)
    _kaydet("bos_masa.png", bos * _isik_egimi(400, 520, 0.1) + rng.normal(0, 0.02, (400, 520)))

    return list(BEKLENEN)


if __name__ == "__main__":
    for ad in uret():
        print("yazıldı:", KLASOR / ad)
