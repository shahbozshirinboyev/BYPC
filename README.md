# BYPC — Build Your PC

Zamonaviy, sodda PC yig'ish kalkulyatori va qismlar katalogi. Asl HTML fayli o'rniga to'liq Django ilovasi.

## Loyiha tuzilishi

- **`products/`** — faqat katalog mahsulotlari: CPU, AIO, MB, RAM, COOLER, GPU, SSD, HDD, PSU, CASE, MONITOR, PRINTER, KB&M, HEADSET.
- **`assembly/`** — PC va AIO uchun yig'ish sozlamalari hamda hisob-kitob tarixi (`PC ASSEMBLY SETTINGS`, `PC CALCULATIONS`, `AIO ASSEMBLY SETTINGS`, `AIO CALCULATIONS`).
- **`builder/`** — buyurtmalar, profillar, saqlangan yig'malar, umumiy sozlamalar va sayt sahifalari.

Mahsulot jadvallari eski `builder_*` nomlarida qoldirilgan, shuning uchun mavjud mahsulotlar va ID'lar migratsiyadan keyin ham saqlanadi.

## Interfeys kontseptsiyasi

Uchta namunaviy sayt tahlili asosida yaratilgan:

- **cyborgpc.uz** — bosqichma-bosqich oqim, aqlli maslahatlar, tayyor profillar;
- **age.uz** — mahsulot kartochkalari va narxlar;
- **pcpartpicker.com** — ixcham yakuniy jadval.

Chapda bosqichlar, markazda faqat bitta bosqichning kartalari, o'ngda vizual yig'ma (slotlar bosqichga o'tkazadi) va jonli hisob. Faqat bir-biriga mos qismlar ko'rsatiladi; har bosqichda qidiruv va tushunarli filtr izohi bor.

## Ishga tushirish

```bash
cd C:\Users\PC\Desktop\BYPC
pipenv shell
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

- Kirish sahifasi: http://127.0.0.1:8000/
- To'liq kalkulyator: http://127.0.0.1:8000/pc-assembly/ — 12 bosqich
- AIO hisobi: http://127.0.0.1:8000/aio-assembly/ — 5 bosqich (AIO → CPU → RAM → SSD → KB&M)
- Monitorlar katalogi: http://127.0.0.1:8000/monitors/
- Printerlar katalogi: http://127.0.0.1:8000/printers/
- Kirish / ro'yxatdan o'tish: `/login/`, `/register/`
- Profil: `/profile/`; savat: `/cart/`; buyurtmalar: `/orders/` (eski `/seller/` va `/seller/orders/` ham ishlaydi)
- Buyurtma tafsiloti: `/orders/<pk>/`; tahrirlash: `/orders/<pk>/edit/`; holat: `POST /orders/<pk>/status/`; eksport: `/orders/export/`
- Admin: http://127.0.0.1:8000/admin/ — `admin` / `admin123` (o'zgartiring)
- Muhit: Python 3.11.0, Django 5.2.19, Pipenv, SQLite (`db.sqlite3`)

Eski `_assembly` URL'lari (`/pc_assembly/`, `/aio_assembly/`) ham ishlaydi.

## Menyu

Barcha sahifalarda bitta umumiy navbar ishlatiladi (`builder/templates/builder/_navbar.html`):

`Bosh sahifa` · `PC` · `AIO` · `Monitors` · `Printers`

O'ng tomonda kunduzgi/tungi rejim tugmasi, kirish/profil va (admin uchun) **Admin** tugmasi joylashgan. Mobil ekranda menyu burger tugmasi bilan ochiladi.

## Rollar

| Rol | Imkoniyatlar |
|---|---|
| **Admin** | Katalog va narxlarni tahrirlash, foydalanuvchi rollarini belgilash, sozlamalar, barcha buyurtmalar va yig'malar, admin paneli |
| **Sotuvchi** | PC / AIO / monitor / printerlardan savat tuzib, klient uchun buyurtma yaratish. Admin paneliga kira olmaydi |
| **Mehmon** | Yig'malarni hisoblash, saqlash, ulashish. Buyurtma va admin paneli mavjud emas |

Rol foydalanuvchining `Profile.role` maydonida saqlanadi va admin paneli → **PROFIL** bo'limida o'zgartiriladi. Yangi foydalanuvchilarga profil avtomatik yaratiladi (`builder/signals.py`).

## Qismlar bog'liqligi

Moslik qoidalari kalkulyatorning pastidagi **"Qismlar bog'liqligi"** bo'limida yozilgan. Asosiylari:

- **AIO → CPU** — chipset soketni belgilaydi: `H61→LGA1155`, `H81→LGA1150`, `H410/H510→LGA1200`, `H610→LGA1700`;
- **AIO → RAM** — AIO ning `ram_type` maydoni (**DDR3 / DDR4 / DDR5**) faqat shu turdagi xotirani qoldiradi;
- **AIO → SSD** — `m2_slots > 0` bo'lsa NVMe ham, bo'lmasa faqat SATA SSD;
- **CPU → MB** — soket mos bo'lishi shart;
- **MB → RAM** — plata `ram_type` ga mos xotira;
- **MB → SSD** — `m2_slots = 0` bo'lsa NVMe ishlamaydi;
- **CPU + GPU → PSU** — hisoblangan quvvatdan kuchli blok;
- **MB + GPU + COOLER → CASE** — form-faktor, uzunlik va balandlik.

AIO yozuvi admin paneldan kiritilganda **RAM turi** va **M.2 slotlari soni** saqlanadi va tanlov paytida RAM/SSD ro'yxatini filtrlaydi.

## Asosiy imkoniyatlar

- Dinamik moslik filtrlari va har bosqichda tushunarli izoh;
- Avtomatik yig'ish, namuna yig'ma, tozalash, ro'yxatni nusxalash;
- Saqlash/yuklash — yig'malar serverda (`SavedBuild`), login qilingan foydalanuvchiga bog'lanadi; mehmonlar uchun brauzer sessioniga bog'liq;
- Ulashish — tanlov URL hash orqali kodlanadi;
- Valyuta (USD / so'm), ustama %, byudjet nazorati;
- Bosqich indikatori va har qator uchun mos variantlar soni;
- Kunduzgi/tungi tema (`localStorage` da saqlanadi).

## Katalog sahifalari

`/monitors/` va `/printers/` — mustaqil kataloglar: qidiruv, tur bo'yicha filtr va narx bo'yicha saralash. Sotuvchi/admin kartochkadagi “Savatga qo'shish” tugmasi orqali mahsulotni `/cart/` ga qo'shadi.

## Buyurtma boshqarish

Oqim yetkazish turiga bog'liq: `DELIVERY`/`POST` uchun `NEW → AGREED → QUEUED → IN_PROGRESS → READY → SHIPPING → DELIVERED`, `PICKUP` uchun `SHIPPING` bosqichi yo'q. Holat nomlari ham turga qarab o'zgaradi (`Olib ketildi`, `Qabul qilib oldi`). Har qanday bosqichdan `ON_HOLD` / `CANCELLED` qo'yish mumkin; holat **faqat oldinga** o'zgaradi. `AGREED → QUEUED` faqat to'lov holati `UNPAID` bo'lmaganda ruxsat etiladi. `DELIVERED` da `delivered_at` to'ldiriladi. To'lov holati: `UNPAID / ON_DELIVERY / ON_PICKUP / PARTIAL / PAID`; to'lov turi: `CASH / CARD / TRANSFER / CASH_CARD` (aralash summalar yig'indisi tekshiriladi). **“Yakunlangan”** = `DELIVERED + PAID`.

Mexanizmlar:

- **Serverda jami hisoblash** — savatdagi narx sessiondan emas, katalogdan qayta o'linadi; `OrderItem` qatorlari va `order_number = ORDER#<pk>` yaratiladi (`_create_order`, `transaction.atomic`);
- **Ruxsatlar** — sotuvchi faqat o'z buyurtmalarini ko'radi, `NEW/AGREED/QUEUED/CANCELLED` holatlarini belgilay oladi; admin hamma holatni qo'yadi, hammasini ko'radi va o'chiradi;
- **Ro'yxat** — `/orders/` da holat tablari (soni bilan, `DELIVERED` va `Yakunlangan` takrorlanmaydi), telefon qidiruvi (9/12 xonalik), sana oralig'i, admin uchun sotuvchi filtri, 20 tadan sahifalash, kun bo'yicha guruhlash;
- **Savat** — `/cart/` alohida sahifa. Narx sessionda emas, buyurtma yaratilayotganda bazadan qayta hisoblanadi; jami USD va so'm serverda belgilanadi.
- **Savatga qo'shish** — PC/AIO yig'masi tayyor bo'lgach builder'dagi “Savatga qo'shish” tugmasi orqali, monitor/printer esa katalog kartochkasidagi tugma orqali `/cart/` ga qo'shiladi.
- **Tahrirlash** — `orders/<pk>/edit/`: klient, yetkazish, manzil (`region/district/city/landmark`), vaqt va to'lov ma'lumotlari; jami qatorlar bo'yicha qayta hisoblanadi;
- **Tafsilot** — `orders/<pk>/`, yetkazish turiga mos holat oqimi, to'lov qoldigi, XHR orqali holat yangilash (`POST .../status/`);
- **Eksport** — `orders/export/?tab=...&date_from=...&date_to=...` (CSV, BOM bilan, telefon formatlangan, faol filtrlar hisobga olinadi);

Savat hali ham server sessionida saqlanadi (mijoz tomonidagi `localStorage` emas).

## Admin panel

Admin panel uchta bo'limga ajratilgan:

- **PRODUCTS** — faqat mahsulotlar: CPUs, AIOs, MB, RAM, COOLER, GPU, SSD, HDD, PSU, CASE, MONITOR, PRINTER, KB&M, HEADSET;
- **YIG'ISH SOZLAMALARI** — PC va AIO sozlamalari hamda hisob tarixi: `PC ASSEMBLY SETTINGS`, `PC CALCULATIONS`, `AIO ASSEMBLY SETTINGS`, `AIO CALCULATIONS`;
- **BUYURTMALAR VA SOZLAMALAR** — BUYURTMALAR (ichida BUYURTMA QATORLARI), PROFILLAR, SAVED BUILDS, SETTINGS.

Admin paneliga faqat **Admin** roli yoki superuser kira oladi. Har bir modelda `list_filter` va `search_fields` mavjud. Ustama % va ish haqi PC/AIO sozlamalaridan, dollar kursi esa **SETTINGS** dan olinadi. Kalkulyatorda **Saqlash** bosilganda hisob tarixiga ham yozuv qo'shiladi.

## Ma'lumotlar

```bash
python manage.py seed_data          # namunaviy qismlarni yangilaydi
python manage.py seed_data --clear  # o'chirib, qayta kiritadi
python manage.py import_age         # AGE Computers Excel jadvalidan qismlar yuklaydi
```

Manba: `Downloads/Telegram Desktop/Price of Age Computers.xlsx` (Export varag'i), tahlil natijasi `builder/data/age_products.json`.

Moslik qoidalari kodi: `builder/templates/builder/index.html` → `allowed()`, `issues()`, `autoBuild()`.
