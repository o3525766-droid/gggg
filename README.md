# Manga Bot - Telegram Group Moderator

Bu bot Telegram grupalarda o'zbek tilidagi xabarlarni moderatsiya qiladi.

## Xususiyatlar

- O'zbek tilidagi xabarlarni avtomatik tarzda o'chiradi
- Foydalanuvchilarga ogohlantirish beradi
- 3 marta ogohlantirilgandan so'ng foydalanuvchini gruhdan chqaradi
- Adminlar uchun ogohlantirishlarni qayta tiklash imkoniyati

## O'rnatish

1. Python o'rnating (agar yo'q bo'lsa)
2. Kerakli kutubxonalarni o'rnating:
```bash
pip install -r requirements.txt
```

## Ishga tushirish

```bash
python manga_bot.py
```

## Bot Buyruqlari

- `/start` - Botni ishga tushirish
- `/help` - Yordam olish
- `/reset` - Foydalanuvchining ogohlantirishlarini qayta tiklash (adminlar uchun)

## Qanday ishlaydi

1. Botni gruhga qo'shing va admin huquqini bering
2. Bot har qanday o'zbek tilidagi xabarni aniqlaydi
3. Xabar o'chiriladi va foydalanuvchiga ogohlantirish yuboriladi
4. 3 marta ogohlantirilgandan so'ng, foydalanuvchi gruhdan chqariladi

## Eslatma

Bot o'zbek tilini quyidagilar orqali aniqlaydi:
- O'zbek alifbosidagi maxsus harflar (ʻ, ', ʼ, g', o', G', O', Q')
- Umumiy o'zbek so'zlari ro'yxati

Bot faqat grupalarda ishlaydi, shaxsiy suhbatlarda emas.
