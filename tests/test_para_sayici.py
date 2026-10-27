"""Testler. Proje kök klasöründen çalıştırın: python -m unittest -v"""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np
from skimage import data, util

from ornekler.uret import BEKLENEN, KLASOR as ORNEK_KLASORU
from para_sayici import ayarlar, goruntu, klasik
from para_sayici.rapor import json_yaz

KOK = Path(__file__).resolve().parent.parent


class OrnekGoruntuTesti(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sonuc = klasik.madeni_para_say()

    def test_24_para_bulur(self):
        self.assertEqual(self.sonuc.sayi, 24)

    def test_paralar_1den_numaralanir(self):
        self.assertEqual([p.no for p in self.sonuc.paralar], list(range(1, 25)))
        self.assertEqual(int(self.sonuc.etiket.max()), 24)

    def test_hepsi_min_alandan_buyuk(self):
        self.assertTrue(all(p.alan >= ayarlar.MIN_ALAN for p in self.sonuc.paralar))

    def test_farkli_sigmalarda_kararli(self):
        for sigma in (20, 30, 60):
            with self.subTest(sigma=sigma):
                self.assertEqual(klasik.madeni_para_say(sigma_arkaplan=sigma).sayi, 24)


class GoruntuFormatTesti(unittest.TestCase):
    def test_renkli_goruntu(self):
        rgb = np.dstack([data.coins()] * 3)
        self.assertEqual(klasik.madeni_para_say(goruntu.gri_yap(rgb)).sayi, 24)

    def test_ters_renkli_goruntu(self):
        ters = goruntu.gri_yap(util.invert(data.coins()))
        self.assertEqual(klasik.madeni_para_say(ters, ters=True).sayi, 24)

    def test_gurultulu_bos_goruntu(self):
        # Para yok, sadece hafif gürültü: Otsu sahte para uydurmamalı.
        rng = np.random.default_rng(0)
        bos = rng.normal(0.5, 0.03, (300, 300)).clip(0, 1)
        sonuc = klasik.madeni_para_say(bos)
        self.assertEqual(sonuc.sayi, 0)
        self.assertIsNone(sonuc.esik)

    def test_tek_renk_goruntu(self):
        self.assertEqual(klasik.madeni_para_say(np.full((100, 100), 0.3)).sayi, 0)

    def test_olmayan_dosya(self):
        with self.assertRaises(FileNotFoundError):
            goruntu.yukle("olmayan_dosya.png")


class OrnekKlasoruTesti(unittest.TestCase):
    """ornekler/ klasöründeki, para sayısı bilinen görüntüler."""

    def test_her_ornek_dogru_sayilir(self):
        for ad, (beklenen, ters) in BEKLENEN.items():
            with self.subTest(goruntu=ad):
                gri = goruntu.yukle(ORNEK_KLASORU / ad)
                self.assertEqual(klasik.madeni_para_say(gri, ters=ters).sayi, beklenen)


class RaporTesti(unittest.TestCase):
    def test_json_turkce_karakter_korunur(self):
        sonuc = klasik.madeni_para_say()
        with tempfile.TemporaryDirectory() as klasor:
            yol = json_yaz(sonuc, Path(klasor) / "r.json", kaynak="örnek görüntü")
            metin = yol.read_text(encoding="utf-8")
            self.assertIn("örnek görüntü", metin)
            self.assertNotIn("\\u00f6", metin)
            self.assertEqual(json.loads(metin)["madeni_para_sayisi"], 24)


class ModulKorumaTesti(unittest.TestCase):
    def test_import_main_sessizdir(self):
        """B6.2: 'import main' hiçbir şey basmamalı, dosya yazmamalı."""
        cikti = subprocess.run(
            [sys.executable, "-c", "import main"],
            cwd=KOK, capture_output=True, text=True, check=True,
        )
        self.assertEqual(cikti.stdout, "")


if __name__ == "__main__":
    unittest.main()
