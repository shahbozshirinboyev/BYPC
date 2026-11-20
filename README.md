# BYPC — Build Your PC

Zamonaviy, sodda PC yig'ish kalkulyatori. Asl HTML fayli o'rniga to'liq Django ilovasi.

## UI kontseptsiyasi — BYPC Studio

Uchta namunaviy sayt tahlili asosida yaratilgan yangi interfeys:
- **cyborgpc.uz** — bosqichma-bosqich oqim, aqlli maslahatlar, tayyor profillar;
- **age.uz** — mahsulot kartochkalari va narxlar;
- **pcpartpicker.com** — ixcham yakuniy jadval.

Studio ularni birlashtiradi: chapda 12 bosqich, markazda faqat bitta bosqichning kartalari,
o'ngda vizual yig'ma ko'rinishi (slotlar bosqichga o'tkazadi) va jonli hisob.
Faqat bir-biriga mos qismlar ko'rsatiladi (ketma-ket tanlash); har bosqichda qismlar ichida qidiruv oynasi bor, filtr sababi qisqa izohda yoziladi.
Tayyor profillar (Ofis / O'yin / Kuchli), avto-yig'ish, saqlash, ulashish mavjud.

## Ishga tushirish

```bash
cd C:\Users\PC\Desktop\BYPC
pipenv shell
python manage.py migrate
python manage.py runserver
```

- Sayt: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/ — `admin` / `admin123` (o'zgartiring)
- Muhit: Python 3.11.0, Django 5.2.19, Pipenv, SQLite (`db.sqlite3`)

## Asosiy imkoniyatlar

- **Moslikka qarab dinamik filtrlar** — qism tanlansa, qolgan ro'yxatlar faqat mos variantlarga qisqaradi:
  - CPU → MB (soket), COOLER (soket + sovutish quvvati)
  - MB → RAM (DDR4/DDR5), SSD (M.2 slot bo'lmasa SATA), CASE (form-faktor)
  - GPU + CASE → o'zaro uzunlik tekshiruvi
  - COOLER + CASE → balandlik tekshiruvi
  - CPU + GPU → PSU minimal quvvati hisoblanadi va ro'yxat filtrlanadi
- **Avtomatik yig'ish** — barcha mos qismlarning eng arzon kombinatsiyasi
- **Namuna yig'ma**, **Tozalash**, **Ro'yxatni nusxalash**
- **Saqlash/Yuklash** — yig'malar brauzer `localStorage` da saqlanadi
- **Ulashish** — tanlov URL hash orqali havolaga kodlanadi
- **Valyuta** (USD / so'm), **ustama %**, **byudjet nazorati**
- **Bosqich indikatori** — 8 ta majburiy qismdan nechtasi tanlanganligi
- Har bir qator uchun mos variantlar soni va tushunarli izoh

## Admin panel

Modellar **aniq tartibda** chiqadi: CPU, MB, RAM, COOLER, GPU, SSD, HDD, PSU, CASE, MONITOR, KB&M, HEADSET.
Shuningdek **Users / Groups** (auth) va **SAVED BUILDS** (saqlangan yig'malar) ham ko'rinadi.

Har bir modelda `list_filter` (tur bo'yicha filtr) va `search_fields` mavjud:

| Jadval | Filtrlar |
|---|---|
| CPU | brend, soket, yadrolar |
| MB | brend, soket, RAM turi, form-faktor, M.2 slotlari |
| RAM | brend, RAM turi, hajm, tezlik |
| COOLER | brend, turi, sovutish quvvati, soketlar |
| GPU | brend, chipset, videoxotira |
| SSD | brend, interfeys, hajm |
| HDD | brend, form-faktor, hajm, aylanish tezligi |
| PSU | brend, sertifikat, quvvat, modullilik |
| CASE | brend, korpus turi, mos platalar |
| MONITOR | brend, matritsa, o'lcham, yangilanish |
| KB&M | brend, ulanish, tartib |
| HEADSET | brend, ulanish, surround |

## Ma'lumotlar

```bash
python manage.py seed_data          # asl HTML namunalarini yangilaydi
python manage.py seed_data --clear  # o'chirib, qayta kiritadi
python manage.py import_age         # AGE Computers Excel jadvalidan 976 ta qism yuklaydi
```

Manba: `Downloads/Telegram Desktop/Price of Age Computers.xlsx` (Export varag'i), tahlil natijasi `builder/data/age_products.json`. Jami katalog: **1025 ta qism**.

Ustama va dollar kursi endi **admin paneli → SETTINGS** dan sozlanadi (`markup_percent`, `usd_to_uzs`). Foydalanuvchi interfeysida ular ko'rsatilmaydi. Qismlar alohida jadvallarda saqlanadi (`builder_*`). Saqlangan yig'malar `builder_savedbuild` jadvalida, brauzer sessioniga bog'lanadi (`/api/builds/*`).

Moslik qoidalari: `builder/templates/builder/index.html` → `allowed()`, `issues()`, `autoBuild()`.
