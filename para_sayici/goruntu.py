"""goruntu.py - Görüntüyü diskten (veya hazır örnekten) okuyup griye çevirir."""

from pathlib import Path

import numpy as np
from skimage import color, data, io, util


def ornek_goruntu():
    """scikit-image ile gelen hazır 'coins' görüntüsü (303x384, 24 para)."""
    return data.coins()


def gri_yap(goruntu):
    """Her türlü görüntüyü 0-1 aralığında float64 gri tonlamaya çevirir.

    - RGBA (4 kanal) -> önce RGB'ye, sonra griye
    - RGB  (3 kanal) -> griye
    - Gri  (2 boyut) -> olduğu gibi
    """
    goruntu = np.asarray(goruntu)
    if goruntu.ndim == 3:
        if goruntu.shape[2] == 4:
            goruntu = color.rgba2rgb(goruntu)
        goruntu = color.rgb2gray(goruntu)
    elif goruntu.ndim != 2:
        raise ValueError(f"Desteklenmeyen görüntü boyutu: {goruntu.shape}")
    return util.img_as_float(goruntu)


def yukle(yol=None):
    """Görüntüyü yükler; yol verilmezse hazır örnek görüntü kullanılır."""
    if yol is None:
        return gri_yap(ornek_goruntu())

    yol = Path(yol)
    if not yol.is_file():
        raise FileNotFoundError(f"Görüntü dosyası bulunamadı: {yol}")
    return gri_yap(io.imread(yol))
