"""main.py - Madeni para sayıcının komut satırı giriş noktası.

Kullanım:
    python main.py                       # hazır örnek görüntü (24 para)
    python main.py resim.jpg             # kendi görüntünüz
    python main.py resim.jpg --ters      # paralar arka plandan koyuysa
    python main.py --min-alan 600 --sigma-arkaplan 60
"""

import argparse
import sys
from pathlib import Path

from para_sayici import ayarlar
from para_sayici.gorsel import adimlari_kaydet
from para_sayici.goruntu import yukle
from para_sayici.klasik import madeni_para_say
from para_sayici.rapor import json_yaz


def argumanlari_oku(argv=None):
    ayrac = argparse.ArgumentParser(
        description="Klasik görüntü işleme ile madeni para sayar.")
    ayrac.add_argument("goruntu", nargs="?", default=None,
                       help="Görüntü dosyası (verilmezse hazır örnek kullanılır)")
    ayrac.add_argument("--min-alan", type=int, default=ayarlar.MIN_ALAN,
                       help=f"Para sayılacak en küçük alan, piksel (varsayılan {ayarlar.MIN_ALAN})")
    ayrac.add_argument("--sigma-arkaplan", type=float, default=ayarlar.SIGMA_ARKAPLAN,
                       help=f"Arka plan bulanıklığı (varsayılan {ayarlar.SIGMA_ARKAPLAN})")
    ayrac.add_argument("--ters", action="store_true",
                       help="Paralar arka plandan koyu ise kullanın")
    ayrac.add_argument("--cikti", default=ayarlar.CIKTI_KLASORU,
                       help=f"Çıktı klasörü (varsayılan '{ayarlar.CIKTI_KLASORU}')")
    return ayrac.parse_args(argv)


def calistir(argv=None):
    arg = argumanlari_oku(argv)

    try:
        gri = yukle(arg.goruntu)
    except (FileNotFoundError, ValueError, OSError) as hata:
        print(f"HATA: {hata}", file=sys.stderr)
        return 1

    sonuc = madeni_para_say(gri, sigma_arkaplan=arg.sigma_arkaplan,
                            min_alan=arg.min_alan, ters=arg.ters)

    kaynak = arg.goruntu or "ornek: skimage.data.coins()"
    cikti = Path(arg.cikti)
    json_yolu = json_yaz(sonuc, cikti / "sonuclar.json", kaynak)
    png_yolu = adimlari_kaydet(sonuc, cikti / "adimlar.png")

    print(f"Görüntü        : {kaynak}")
    print(f"Madeni para    : {sonuc.sayi}")
    print(f"Elenen gürültü : {sonuc.elenen}")
    print(f"Rapor          : {json_yolu}")
    print(f"Görsel         : {png_yolu}")
    return 0


if __name__ == "__main__":
    # Windows konsolunda Türkçe karakterler bozulmasın.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    sys.exit(calistir())
