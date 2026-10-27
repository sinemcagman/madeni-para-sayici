"""para_sayici - Klasik görüntü işleme ile madeni para sayma paketi.

Yapay zekâ kullanılmaz; yalnızca Gauss bulanıklaştırma, Otsu eşikleme ve
bağlı bileşen etiketleme gibi matematiksel yöntemler kullanılır.
"""

from .klasik import Para, Sonuc, madeni_para_say

__all__ = ["Para", "Sonuc", "madeni_para_say"]
__version__ = "1.0.0"
