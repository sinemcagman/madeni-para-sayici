"""ayarlar.py - Algoritmanın sabitleri (bağımlılık zincirinin EN ALTI).

Bu modül hiçbir şeyi import etmez. Diğer modüller buraya
`from . import ayarlar` ile bağlanır ve değerleri `ayarlar.AD` diye okur;
böylece çalışma sırasında bir sabit değiştirilirse herkes güncel değeri görür.
"""

# Gürültüyü bastırmak için kullanılan küçük Gauss bulanıklığı (piksel).
SIGMA_GURULTU = 1.5

# Arka plan ışığını tahmin etmek için kullanılan büyük Gauss bulanıklığı.
# Görüntüden bu çıkarılınca eşit olmayan aydınlatma düzelir.
SIGMA_ARKAPLAN = 40

# Morfolojik açma (opening) için disk yarıçapı (piksel). Paraları kenardaki
# gürültüye bağlayan ince köprüleri koparır. 0 verilirse açma yapılmaz.
ACMA_YARICAPI = 4

# Işık düzeltilmiş görüntünün standart sapması bunun altındaysa görüntüde
# nesne yok sayılır. (Otsu her görüntüyü zorla ikiye böler; boş bir
# görüntüde bile sahte "para" uydurmasını bu kontrol engeller.)
MIN_KONTRAST = 0.02

# Bundan küçük alanlı (piksel) bölgeler para değil, gürültü sayılır.
MIN_ALAN = 400

# Çıktıların yazılacağı varsayılan klasör.
CIKTI_KLASORU = "cikti"
