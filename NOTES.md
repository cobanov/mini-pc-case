# Mini PC kasası — ölçü referansı

## Parçalar
- Anakart: ASUS PRIME H310M-K (doğrulanacak), mATX 226 (arka kenar) × 185 (derinlik) mm
- CPU: i3-8100 65 W; soğutucu PCCOOLER RC400, 53 mm, 90 mm fan
- GPU: ASUS Phoenix GTX 1050 Ti (PH-GTX1050TI-4G) 192 × 111 × 37 mm, 2 slot, ek güç yok
- PSU: standart ATX 150 × 86 × 140 mm, 400 W
- Yazıcı: Creality K1, tabla 220 × 220 × 250, PETG

## ATX 2.2 (atx2_2.pdf, Fig. 3–4) — inç, datum = delik A
X: arka kenar boyunca I/O'ya doğru (+), Y: arka kenardan öne (+). Kasada X = yukarı.
- Kart arka kenarı Y = -0.400; ATX kartın sol kenarı X = -0.650, sağ (üst) kenarı X = 11.350
- Delikler Ø0.156: A(0,0) B(3.1,0) C(4.9,0) F(11.1,0.9) G(0,6.1) H(4.9,6.1) J(11.1,6.1) K(0,8.95) L(4.9,8.95) M(11.1,8.95); mATX ek: R, S (Y=6.1, B yakını — kartta ölçülecek)
- H310M-K (226 mm): sol/alt kenar X = 11.35 - 8.90 = 2.45 → olası delikler B, C, F, H, J, R/S (derinlik 185 → ön kenar Y = 6.88)
- I/O açıklığı 6.250 × 1.750 (158.75 × 44.45 mm), X = 5.196 … 11.446; alt kenarı anakart üst yüzeyinin 3.81 mm altında; 2.5 mm keepout
- Arka panel datumdan Y = -0.483 (12.27 mm), panel kalınlığı I/O kalkanı için 0.94–1.32 mm
- Slot aralığı 0.800 (20.32 mm); AGP/x16 pin-1 ≈ X 5.0; H310M-K'da 3 slot (≈5.0, 4.2, 3.4) — x16'nın hangisi olduğu fotoğrafla doğrulanacak

## Yerleşim (v4, `build_case.py`)
Anakart dik, sağ duvara (X = W) bağlı; GPU doğrudan slotta, braketi arka duvarın dışındaki rafa.
PSU soğutucunun karşısında yan yatık, fanı sol yan kapaktaki ızgaraya bakar. SSD tabanda.
Dış ölçü 178 × 206 × 251 mm, ~9.2 L. Gövde Z = 80'den iki parça (GPU açıklığı ≤ 78.2 altta,
I/O ≥ 81.4 ve PSU üstte); etek + pim + 4 vida ile birleşir. En yüksek parça 164 mm.
Bağlantılar, vida listesi, baskı ve montaj: `MONTAJ.md`.
Kontroller (`build()` + `check_print()`): geçerli tek katı, referans parçalarla çakışma yok,
baskı yönünde 18 mm'den uzun desteksiz köprü yok.
