"""rapor.py - Sayma sonucunu okunur bir JSON dosyasına yazar."""

import json
from datetime import datetime
from pathlib import Path


def rapor_sozlugu(sonuc, kaynak):
    """Sonuc nesnesini JSON'a yazılabilir sade bir sözlüğe çevirir."""
    return {
        "kaynak": kaynak,
        "tarih": datetime.now().isoformat(timespec="seconds"),
        "madeni_para_sayisi": sonuc.sayi,
        "elenen_gurultu": sonuc.elenen,
        "otsu_esigi": None if sonuc.esik is None else round(sonuc.esik, 5),
        "paralar": [p.sozluk() for p in sonuc.paralar],
    }


def json_yaz(sonuc, yol, kaynak="ornek: skimage.data.coins()"):
    """Raporu yazar. ensure_ascii=False -> Türkçe harfler \\uXXXX olmaz."""
    yol = Path(yol)
    yol.parent.mkdir(parents=True, exist_ok=True)
    metin = json.dumps(rapor_sozlugu(sonuc, kaynak), ensure_ascii=False, indent=2)
    yol.write_text(metin, encoding="utf-8")
    return yol
