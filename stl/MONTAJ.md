# Mini PC kasası — montaj ve malzeme listesi

Model: `build_case.py` (v4). Dış ölçü 178 × 206 × 251 mm (üst kapakla; arka GPU rafı ve ek
kulakları +10 mm), ~9.2 L. Gövde Z = 80 mm'den iki parça; en yüksek parça 164 mm.

## Parçalar

| Dosya | Ne | Yükseklik (baskı) |
|---|---|---|
| `govde_alt` | taban, GPU açıklığı + braket rafı, B/R ve C/H standoff'ları, SSD, ayaklar, PSU ayakları | 91 mm |
| `govde_ust` | I/O açıklığı, F/J standoff'ları, PSU vidaları/ızgarası/priz, güç düğmesi, CPU arkası ızgarası | 164 mm |
| `ust_kapak` | üst kapak | 8 mm |
| `yan_alt`, `yan_ust` | sol yan kapaklar (bindirme eki Z = 80'de, gövde ekiyle aynı hizada) | 3 mm |
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
| SSD, tabandan SSD'nin kendi dişine (4) | — | M3 × 8 havşa |
| PSU (4) | — | 6-32 UNC × 6 (PSU ile gelir) |
| **Toplam** | **23 insert** | M3×6: 8 · M3×8 havşa: 14 · M3×10 havşa: 3 · M3×12 havşa: 2 |

Diğer: 16 mm basınca çalışan metal güç düğmesi (F_PANEL PWR), Ø12 × 6 mm yapışkanlı lastik
ayak × 4 (tabanda 1 mm yuva).

## Birbirine geçen yerler (boşluk 0.4 mm, PETG)

- **Gövde eki (Z = 80):** alt gövdenin ön ve sağ iç yüzünde 6 mm yukarı çıkan 2 mm'lik etek, sol
  direklerin üstünde 4 mm'lik iki pim; üst gövde bunların üstüne oturur. Ön 2 + arka 2 vida.
- **Yan kapaklar** ön/arka duvar ile taban arasındaki yuvaya oturur, dış yüzleri kasayla hizalı.
  İki yan kapak arasında 12 mm bindirme: önce üst yan kapak, sonra alt.
- **Üst yan kapağın** üst dili üst kapağın altındaki oluğa girer.
- **Üst kapağın** ön, sağ ve arka kenarındaki 4 mm etek duvarların içine oturur.
- **I/O kalkanı** açıklığın çevresindeki 1.2 mm'ye inceltilmiş duvara tırnaklarıyla takılır.

## Baskı

| Parça | Yön (STL bu yönde) | Not |
|---|---|---|
| `govde_alt` | dik, taban tablada | brim |
| `govde_ust` | dik, ek yüzü (Z = 80 halkası) tablada | brim; 164 mm |
| `ust_kapak` | düz yüzü tablada | |
| `yan_alt` | dış yüzü tablada | |
| `yan_ust` | iç yüzü tablada | dil ve bindirme tablaya oturur |
| `deneme_parcasi` | dik | **önce bunu bas** |

Ayar: PETG, 0.2 mm katman, 4 duvar, %20 gyroid, destek kapalı. I/O, GPU ve priz
açıklıklarındaki ince kırılabilir kaburgaları baskıdan sonra pense ile kır, kenarı zımparala.

## Montaj sırası

1. Insert'leri havyayla yerleştir (alt gövde 12, üst gövde 11).
2. Alt gövde: SSD'yi tabandan 4 vidayla tak.
3. Üst gövde: PSU'yu içeri koy, arkadan 4 adet 6-32 vidayla bağla (PSU'nun altı ek düzlemiyle
   hizalı; alt gövdeye takınca PSU alt gövdedeki iki ayağa oturur).
4. Üst gövdeyi alt gövdeye oturt (etek + pimler); ön 2 yatay, arka 2 dikey vidayı sık.
5. I/O kalkanını içeriden tak; anakartı 6 vidayla bağla (üst gövde F/J, alt gövde B/R/C/H).
6. GPU'yu tak, braketini arka rafa 2 vidayla sabitle.
7. Kabloları bağla, güç düğmesini F_PANEL'e bağla.
8. Üst yan kapak → alt yan kapak → üst kapak.

## Doğrulanacaklar

- `GPU_TAB_H = 112.5`: anakart yüzeyinden GPU braket kulağının alt yüzüne (deneme parçasıyla).
- PCIEX16 hizası (`Z_C`): kılavuz görselinden; deneme parçasında GPU açıklığı ile denenir.
- PSU prizi/anahtarı: standart ATX çizimine göre; PSU arkası farklıysa açıklık taşınır.
