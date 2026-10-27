"""gorsel.py - Algoritmanın adımlarını tek bir PNG'de gösterir."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # pencere açmadan dosyaya çizim (sunucu/terminal dostu)
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from skimage import color


def adimlari_kaydet(sonuc, yol):
    """4 panelli görsel: orijinal, ışık düzeltilmiş, maske, sonuç."""
    yol = Path(yol)
    yol.parent.mkdir(parents=True, exist_ok=True)

    fig, eksenler = plt.subplots(2, 2, figsize=(11, 9))
    a, b, c, d = eksenler.ravel()

    a.imshow(sonuc.gri, cmap="gray")
    a.set_title("1) Orijinal (gri)")

    b.imshow(sonuc.duz, cmap="gray")
    b.set_title("2) Işık düzeltilmiş")

    c.imshow(sonuc.maske, cmap="gray")
    if sonuc.esik is None:
        c.set_title("3) Maske (kontrast yetersiz, nesne yok)")
    else:
        c.set_title(f"3) Otsu maskesi (eşik = {sonuc.esik:.3f})")

    d.imshow(color.label2rgb(sonuc.etiket, image=sonuc.gri, bg_label=0, alpha=0.35))
    for p in sonuc.paralar:
        d.add_patch(Circle((p.merkez_x, p.merkez_y), p.yaricap,
                           fill=False, edgecolor="yellow", linewidth=1.5))
        d.text(p.merkez_x, p.merkez_y, str(p.no), color="white",
               ha="center", va="center", fontsize=8, fontweight="bold")
    d.set_title(f"4) Sonuç: {sonuc.sayi} madeni para")

    for eksen in eksenler.ravel():
        eksen.axis("off")
    fig.tight_layout()
    fig.savefig(yol, dpi=120)
    plt.close(fig)
    return yol
