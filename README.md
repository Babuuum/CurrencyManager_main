# 💰 Crypto Asset Manager

**Умный Telegram-бот и FastAPI-сервис для мониторинга криптоактивов.**

---

## 🚀 Возможности:

- Отслеживание вручную введённых активов (BTC, ETH и др.)
- Расчёт стоимости по CoinGecko
- Уведомления в Telegram с полной аналитикой (день, месяц)
- Сохраняет историю в БД и вычисляет изменение стоимости

---

## 📦 Стек:

- FastAPI, SQLAlchemy, Alembic
- Aiogram 3 (Telegram-бот)
- PostgreSQL, Docker, CoinGecko API

---

## 🔧 Установка (локально)

```bash
git clone https://github.com/Babuuum/CurrencyManager_main
cd CurrencyManager_main
pip install -r requirements.txt
uvicorn app.main:app --reload
