"""klasik.py - Klasik görüntü işleme: madeni para sayma (yapay zekâ YOK).

Adımlar:
  1. Işık düzeltme : küçük Gauss - büyük Gauss (arka plan çıkarma)
  2. Eşikleme      : Otsu yöntemi ile otomatik siyah/beyaz ayrımı
  3. Delik doldurma: para içindeki koyu desenleri kapatma
     + morfolojik açma: paraları gürültüye bağlayan ince köprüleri koparma
  4. Etiketleme    : birbirine bağlı beyaz bölgeleri numaralandırma
  5. Alan filtresi : MIN_ALAN'dan küçük gürültü lekelerini atma
"""

from dataclasses import dataclass, field

import numpy as np
from scipy import ndimage as ndi
from skimage import filters, measure, morphology

from . import ayarlar  # from ... import DEĞİL: ayarlar.X canlı okunur
from . import goruntu


@dataclass
class Para:
    """Bulunan tek bir madeni paranın bilgileri."""

    no: int
    merkez_y: float
    merkez_x: float
    alan: int
    yaricap: float  # alanı aynı olan dairenin yarıçapı

    def sozluk(self):
        return {
            "no": self.no,
            "merkez": [round(self.merkez_x, 1), round(self.merkez_y, 1)],
            "alan": self.alan,
            "yaricap": round(self.yaricap, 1),
        }


@dataclass
class Sonuc:
    """Sayma işleminin tüm çıktıları."""

    sayi: int
    esik: float
    paralar: list = field(default_factory=list)
    gri: np.ndarray = field(default=None, repr=False)
    duz: np.ndarray = field(default=None, repr=False)
    maske: np.ndarray = field(default=None, repr=False)
    etiket: np.ndarray = field(default=None, repr=False)
    elenen: int = 0  # alan filtresine takılan gürültü bölgesi sayısı


def isik_duzelt(gri, sigma_gurultu=None, sigma_arkaplan=None):
    """Görüntüden arka plan ışığını çıkarır (ve hafif gürültüyü bastırır)."""
    if sigma_gurultu is None:
        sigma_gurultu = ayarlar.SIGMA_GURULTU
    if sigma_arkaplan is None:
        sigma_arkaplan = ayarlar.SIGMA_ARKAPLAN
    return filters.gaussian(gri, sigma_gurultu) - filters.gaussian(gri, sigma_arkaplan)


def maske_olustur(duz, ters=False):
    """Otsu eşiği ile ikili (True/False) maske üretir; delikleri doldurur.

    ters=True: nesneler arka plandan KOYU ise kullanılır.
    """
    esik = filters.threshold_otsu(duz)
    maske = duz < esik if ters else duz > esik
    maske = ndi.binary_fill_holes(maske)
    if ayarlar.ACMA_YARICAPI > 0:
        # Açma = önce aşındır, sonra genişlet: ince köprüler kopar, paralar korunur.
        maske = ndi.binary_opening(maske, structure=morphology.disk(ayarlar.ACMA_YARICAPI))
    return maske, float(esik)


def madeni_para_say(gri=None, sigma_gurultu=None, sigma_arkaplan=None,
                    min_alan=None, ters=False):
    """Gri görüntüdeki madeni paraları sayar ve ayrıntılı Sonuc döndürür.

    gri verilmezse scikit-image'ın hazır 'coins' görüntüsü kullanılır.
    """
    if gri is None:
        gri = goruntu.yukle()
    if min_alan is None:
        min_alan = ayarlar.MIN_ALAN

    duz = isik_duzelt(gri, sigma_gurultu, sigma_arkaplan)
    maske, esik = maske_olustur(duz, ters)
    ham_etiket = measure.label(maske)

    # Küçük gürültü lekelerini at, kalan bölgeleri 1..n diye yeniden numarala.
    etiket = np.zeros_like(ham_etiket)
    paralar = []
    elenen = 0
    for bolge in measure.regionprops(ham_etiket):
        if bolge.area < min_alan:
            elenen += 1
            continue
        no = len(paralar) + 1
        etiket[ham_etiket == bolge.label] = no
        y, x = bolge.centroid
        paralar.append(Para(
            no=no,
            merkez_y=float(y),
            merkez_x=float(x),
            alan=int(bolge.area),
            yaricap=float(np.sqrt(bolge.area / np.pi)),
        ))

    return Sonuc(
        sayi=len(paralar), esik=esik, paralar=paralar,
        gri=gri, duz=duz, maske=maske, etiket=etiket, elenen=elenen,
    )


if __name__ == "__main__":
    # Sadece "python -m para_sayici.klasik" ile çalışınca basılır.
    sonuc = madeni_para_say()
    print(f"Bulunan madeni para: {sonuc.sayi} (elenen gürültü: {sonuc.elenen})")
