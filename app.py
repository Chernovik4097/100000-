import streamlit as st
import pandas as pd
import json

# Налаштування сторінки
st.set_page_config(
    page_title="Crypto Marathon $100k",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 Crypto Marathon: Path to $100k")
st.caption("Покроковий трекер капіталу (160 підрівнів) • 30,000 ₴/міс пасиву")

# Ініціалізація даних у сесії
if 'usd_rate' not in st.session_state:
    st.session_state.usd_rate = 41.30

if 'exchanges' not in st.session_state:
    st.session_state.exchanges = {
        "Binance Acc 1": [
            {"coin": "USDT", "amount": 200.0, "apy": 6.0},
            {"coin": "USDC", "amount": 200.0, "apy": 6.0},
            {"coin": "USD1", "amount": 200.0, "apy": 6.0},
            {"coin": "U", "amount": 0.0, "apy": 5.0},
            {"coin": "RWUSD", "amount": 0.0, "apy": 5.0},
        ],
        "Binance Acc 2": [{"coin": "USDT", "amount": 0.0, "apy": 6.0}],
        "Binance Acc 3": [{"coin": "USDT", "amount": 0.0, "apy": 6.0}],
        "Binance Acc 4": [{"coin": "USDT", "amount": 0.0, "apy": 6.0}],
        "Bybit Acc 1": [{"coin": "USDT", "amount": 0.0, "apy": 6.0}],
        "Bybit Acc 2": [{"coin": "USDT", "amount": 0.0, "apy": 6.0}],
    }

if 'reit' not in st.session_state:
    st.session_state.reit = {"certs": 157, "price": 0.2821, "apy": 9.5}

# Бокова панель налаштувань
with st.sidebar:
    st.header("⚙️ Налаштування")
    st.session_state.usd_rate = st.number_input("Курс USD/UAH", value=st.session_state.usd_rate, step=0.1)
    
    st.markdown("---")
    st.subheader("➕ Додати новий акаунт/біржу")
    new_acc_name = st.text_input("Назва акаунту (напр. Gate.io)")
    if st.button("Створити акаунт") and new_acc_name:
        if new_acc_name not in st.session_state.exchanges:
            st.session_state.exchanges[new_acc_name] = [{"coin": "USDT", "amount": 0.0, "apy": 6.0}]
            st.success(f"Акаунт '{new_acc_name}' додано!")
            st.rerun()

# Обчислення загальних балансів та пасиву
total_exchanges_usd = 0.0
total_exchanges_passive_usd = 0.0

for acc, coins in st.session_state.exchanges.items():
    for c in coins:
        total_exchanges_usd += c['amount']
        total_exchanges_passive_usd += (c['amount'] * (c['apy'] / 100.0)) / 12.0

reit_total_usd = st.session_state.reit['certs'] * st.session_state.reit['price']
reit_passive_usd = (reit_total_usd * (st.session_state.reit['apy'] / 100.0)) / 12.0

total_capital_usd = total_exchanges_usd + reit_total_usd
total_passive_usd = total_exchanges_passive_usd + reit_passive_usd
total_passive_uah = total_passive_usd * st.session_state.usd_rate

# Метрики вгорі
col1, col2, col3, col4 = st.columns(4)
col1.metric("Загальний капітал", f"${total_capital_usd:,.2f}")
col2.metric("Капітал у UAH", f"₴{total_capital_usd * st.session_state.usd_rate:,.0f}")
col3.metric("Пасив / місяць", f"${total_passive_usd:,.2f}", f"₴{total_passive_uah:,.0f}/міс")
col4.metric("Ціль ($100k)", f"{(total_capital_usd / 100000.0)*100:.2f}%")

st.markdown("---")

# Таби для навігації
tab1, tab2, tab3 = st.tabs(["📊 Акаунти та Монети", "🏢 Inzhur REIT", "🎮 160 Підрівнів"])

with tab1:
    st.subheader("Управління акаунтами та монетами")
    
    for acc_name, coins_list in st.session_state.exchanges.items():
        with st.expander(f"🏦 {acc_name} — Всього: ${sum(c['amount'] for c in coins_list):,.2f}"):
            # Таблиця монет
            for idx, coin in enumerate(coins_list):
                c1, c2, c3, c4 = st.columns([2, 3, 3, 1])
                coin['coin'] = c1.text_input(f"Монета #{idx+1}", value=coin['coin'], key=f"{acc_name}_coin_{idx}")
                coin['amount'] = c2.number_input(f"Сума ($)", value=float(coin['amount']), key=f"{acc_name}_amt_{idx}")
                coin['apy'] = c3.number_input(f"APY (%)", value=float(coin['apy']), key=f"{acc_name}_apy_{idx}")
                if c4.button("❌", key=f"{acc_name}_del_{idx}"):
                    coins_list.pop(idx)
                    st.rerun()
            
            if st.button(f"➕ Додати монету у {acc_name}", key=f"add_{acc_name}"):
                coins_list.append({"coin": "USDT", "amount": 0.0, "apy": 6.0})
                st.rerun()

with tab2:
    st.subheader("Inzhur REIT (Нерухомість)")
    c1, c2, c3 = st.columns(3)
    st.session_state.reit['certs'] = c1.number_input("Кількість сертифікатів", value=int(st.session_state.reit['certs']))
    st.session_state.reit['price'] = c2.number_input("Ціна за сертифікат ($)", value=float(st.session_state.reit['price']), format="%.4f")
    st.session_state.reit['apy'] = c3.number_input("Дивідендна ставка APY (%)", value=float(st.session_state.reit['apy']))
    
    st.info(f"Загальна вартість REIT: **${reit_total_usd:,.2f}** (~{reit_total_usd * st.session_state.usd_rate:,.0f} ₴)")

with tab3:
    st.subheader("🎮 Система 160 підрівнів")
    # Простий розрахунок поточного підрівня
    sublevel = int(min(160, max(1, (total_capital_usd / 100000.0) * 160)))
    phase = ((sublevel - 1) // 40) + 1
    level = (((sublevel - 1) % 40) // 10) + 1
    micro = ((sublevel - 1) % 10) + 1
    
    st.success(f"Поточний статус: **Фаза {phase} ➔ Рівень {phase}.{level} ➔ Підрівень {phase}.{level}.{micro}** (всього {sublevel}/160)")
    st.progress(sublevel / 160)
