# Mini PC kasası — montaj ve malzeme listesi

Model: `build_case.py` (v4). Dış ölçü 178 × 206 × 265 mm (üst kapakla; ayaklar +12, arka GPU rafı
ve ek kulakları +10 mm), ~9.7 L. Gövde Z = 80 mm'den iki parça; en yüksek parça 178 mm.

## Parçalar

| Dosya | Ne | Yükseklik (baskı) |
|---|---|---|
| `govde_alt` | taban + alt giriş fanı, GPU açıklığı + braket rafı, B/R ve C/H standoff'ları, ayaklar, PSU ayakları, ön panel çerçevesi | 91 mm |
| `govde_ust` | I/O açıklığı, F/J standoff'ları, PSU vidaları/ızgarası/priz, MX anahtar yuvaları, CPU arkası ızgarası, isteğe bağlı ön fan deliği | 178 mm |
| `ust_kapak` | üst kapak, egzoz fanı ızgarası | 7 mm |
| `ayak` × 4 | Ø22 × 12 mm, tabana M3 ile | 12 mm |
| `on_panel_alt` (+ `_duz`, `_petek`) | ön alt panel 156 × 72: varsayılan 3.5" LCD penceresi 75 × 46 (modül 85 × 55 × 5 arkasında), düz, petek | 2.5 mm |
| `on_panel_ust` (+ `_petek`, `_ekran`) | **Steam Machine ön plakası** 156 × 126.1 × 6.5, 4 mıknatısla: varsayılan düz (ahşap kaplama/boya için), petek, ekran. Valve'ın ve üçüncü parti plakalar da takılır | 6.5 mm |
| `on_serit` (+ `_duz`) | kontrol şeridi 156 × 32, Steam plakasının üstünde: ortada MX güç, solda MX reset + USB-C, sağda 2 × USB-A (panel tipi uzatmalar) | 2.2 mm |
| `yan_alt`, `yan_ust` | sol yan kapaklar; alt kapak kapalı, iç yüzünde SSD yatağı (4 vida, 1.5 mm aralayıcı) | 2.5 mm |
| `deneme_parcasi` | arka-sağ köşe: I/O açıklığı, GPU açıklığı + rafı, iki standoff | 133 mm |

## Bağlantı elemanları

Hepsi M3, tek tip insert: Ø4.3 × 6 mm yuva, M3 × 5 × 4.5 pirinç heat-set.

| Nerede | Insert | Vida |
|---|---|---|
| Anakart (6) | 6 | M3 × 6 silindir başlı (DIN 7985) |
| GPU braketi (arka raf) | 2 | M3 × 6 silindir başlı |
| Gövde eki, ön (2): dıştan yatay, alt gövdedeki iç bloklara | 2 | M3 × 8 havşa (DIN 7991) |
| Gövde eki, arka (2): üst kulaktan dikey, alt kulağa | 2 | M3 × 12 havşa |
| Üst kapak (3) | 3 | M3 × 10 havşa |
| Yan kapaklar (alt 4, üst 4) | 8 | M3 × 8 havşa |
| Ayaklar (4), tabandan | 4 | M3 × 8 silindir başlı |
| SSD, alt yan kapaktan SSD'nin alt dişlerine (4) | — | M3 × 6 havşa |
| Paneller: ön alt 4, kontrol şeridi 4 | 8 | M3 × 8 havşa (pad ile plaka 3.25 mm) |
| Steam plakası | — | 8 × K&J SB443-OUT (6.35 × 6.35 × 4.76 blok; 4 kasada, 4 plakada, yapıştırma) |
| PSU (4) | — | 6-32 UNC × 6 (PSU ile gelir) |
| **Toplam** | **35 insert** | M3×6: 8 · M3×8 silindir: 4 · M3×8 havşa: 20 · M3×10 havşa: 3 · M3×12 havşa: 2 |

Diğer: güç ve reset için 2 adet Cherry MX tipi mekanik anahtar + keycap (kontrol şeridinde; 14 × 14 plaka
deliği, 1.5 mm plaka; anahtar bacaklarına lehimli 2 kablo F_PANEL PWR/RESET'e); panel tipi USB-C ve 2 × USB-A
uzatma (açıklıklar 9.6 × 3.9 ve 13.6 × 6.4; flanş vidaları ürüne göre delinir), anakartın USB başlıklarına. 120 × 25 mm Molex fan × 2
(tabanda giriş, üst kapakta egzoz: baca düzeni; fanın kendi vidalarıyla, Ø4.5 delikler, aralık 105).
Ön duvarda üstte isteğe bağlı 3. fan için aynı delik düzeni var. Molex olduğu için anakart başlığına gerek yok.

Duvar 2.2 mm (3 çevre), üst kapak 3 mm; toplam 763 cm³: Steam plakası hariç 635 cm³ ≈ 810 g PETG, plaka %20 dolguyla ≈ 80 g → hepsi 1 kg makaraya sığar (az payla).
Ahşap görünüm için düz plakanın önüne 0.6 mm ceviz kaplama yapıştırılabilir ya da plaka ahşap dolgulu PLA ile basılır.
PSU 150 × 86 × 140 (kullanıcının PSU'su 149.7 × 86.4 × 140); arka yüzde priz alt-ortada, anahtar solunda,
ızgara üstte; kablolar ön-alttan çıkar. Dış köşeler R5, alt/üst kenarlar 1.5 mm pah.

## Kendi panelini tasarlamak için

Üç panel de aynı kural: dış plaka 1.25 mm kalın, kasadaki 1.25 mm gömmeye oturur (dış yüzle hizalı);
ortadaki iç kademe 1.25 mm daha kalın ve duvardaki açıklığa girer; 4 köşede Ø3.4 delik + 90° havşa.
Boşluk: plaka ve kademe her kenarda 0.2 mm küçük. Plakayı istediğin kadar kalın ve dışa taşkın yapabilirsin.

| Panel | Plaka (dış) | Açıklık | Vida merkezleri (plaka köşesinden) |
|---|---|---|---|
| Ön alt | 156 × 72 | 128 × 52 | 6 × 5 mm içeride |
| Kontrol şeridi | 156 × 32 | 128 × 18 | 6 × 3.5 mm içeride |

**Ön üst = Steam Machine plakası** (Valve'ın resmi `steam_machine_3d.stp` dosyasından, CC BY-NC-SA):
156 × 126.1 mm, 6.5 mm kalın, düz ya da hafif dışbükey ön yüz; gömme yok, plaka ön duvarın dış yüzüne oturur.
Arka yüzünde plaka merkezinden (±67, ±52.5) mm'de 4 adet SB443-OUT mıknatıs, plakadan 4 mm dışarı çıkar
(0.8 mm sığ cebe yapıştırılır). Kasada aynı konumda 6.65 mm kare cepler: plakanın mıknatısı 4 mm girer,
arkasında kasanın mıknatısı (kutuplar birbirini çekecek şekilde yapıştır). Kasadaki açıklık 112 × 82 (mıknatıs ceplerinden 6 mm uzak).
Valve'ın stok plakası, Inkterface e-ink plakası ve üçüncü parti Steam Machine plakaları da takılır.

Arkasındaki boşluk: ön alt panelde 8 mm (GPU), Steam plakasının arkasında 50 mm (soğutucuya kadar), şeritte 40 mm.
Gövde ekinin ön vidaları Steam plakasının arkasında (Z 95): plakayı çekince erişilir, takılıyken görünmez.
Vidalı panellerde havşa başı için vida köşelerinde Ø8 × 2 mm pad var; kasada karşılığı Ø8.6 yuva.

## Birbirine geçen yerler (boşluk 0.4 mm, PETG)

- **Gövde eki (Z = 80):** alt gövdenin ön ve sağ iç yüzünde 6 mm yukarı çıkan 2 mm'lik etek, sol
  direklerin üstünde 4 mm'lik iki pim; üst gövde bunların üstüne oturur. Ön 2 + arka 2 vida.
- **Yan kapaklar** ön/arka duvar ile taban arasındaki yuvaya oturur, dış yüzleri kasayla hizalı;
  ikisi Z = 80'de düz birleşir, sıra fark etmez.
- **Üst yan kapağın** üst dili üst kapağın altındaki oluğa girer.
- **Üst kapağın** ön, sağ ve arka kenarındaki 4 mm etek duvarların içine oturur.
- **I/O kalkanı** açıklığın çevresindeki 1.2 mm'ye inceltilmiş duvara tırnaklarıyla takılır.

## Baskı

| Parça | Yön (STL bu yönde) | Not |
|---|---|---|
| `govde_alt` | dik, taban tablada | 215 mm derinlik: K1 tablasına 2.5 mm payla sığar, brim yerine köşelere mouse-ear |
| `govde_ust` | dik, ek yüzü (Z = 80 halkası) tablada | brim; 178 mm |
| `ust_kapak` | düz yüzü tablada | |
| `ayak` | düz yüzü tablada, 4 adet | |
| `on_panel*`, `ust_panel*` | dış yüzü tablada | gövdedeki panel açıklıklarının kaburgalarını kır |
| `yan_alt` | dış yüzü tablada | |
| `yan_ust` | iç yüzü tablada | dil ve bindirme tablaya oturur |
| `deneme_parcasi` | dik | **önce bunu bas** |

Ayar: PETG, 0.2 mm katman, 4 duvar, %20 gyroid, destek kapalı. I/O, GPU ve priz
açıklıklarındaki ince kırılabilir kaburgaları baskıdan sonra pense ile kır, kenarı zımparala.

## Montaj sırası

1. Insert'leri havyayla yerleştir (alt gövde 16, üst gövde 11).
2. Ayakları tabana 4 vidayla tak.
3. Alt yan kapak: SSD'yi iç yüzdeki yatağa 4 vidayla tak (konnektör öne bakar). Alt gövde: giriş fanını tabana tak (hava içeri).
4. Kontrol şeridi: MX anahtarları ve USB uzatmalarını tak, keycap'leri geçir. Üst gövde: PSU'yu içeri koy, arkadan 4 adet 6-32 vidayla bağla (PSU'nun altı ek düzlemiyle
   hizalı; alt gövdeye takınca PSU alt gövdedeki iki ayağa oturur).
5. Üst gövdeyi alt gövdeye oturt (etek + pimler); ön 2 yatay (Steam plakası takılmadan), arka 2 dikey vidayı sık.
6. I/O kalkanını içeriden tak; anakartı 6 vidayla bağla (üst gövde F/J, alt gövde B/R/C/H).
7. GPU'yu tak, braketini arka rafa 2 vidayla sabitle.
8. Kabloları bağla, güç düğmesini F_PANEL'e bağla. Egzoz fanını üst kapağın altına tak (hava yukarı); iki fanı PSU Molex'ine bağla.
9. Ön alt paneli ve kontrol şeridini 4'er vidayla tak, Steam plakasını mıknatısla oturt; yan kapaklar, sonra üst kapak.

## Doğrulanacaklar

- `GPU_TAB_H = 112.5`: anakart yüzeyinden GPU braket kulağının alt yüzüne (deneme parçasıyla).
- PCIEX16 hizası (`Z_C`): kılavuz görselinden; deneme parçasında GPU açıklığı ile denenir.
- PSU prizi/anahtarı: standart ATX çizimine göre; PSU arkası farklıysa açıklık taşınır.
