def build_arbitrage_message(opportunities: dict) -> str:
    if not opportunities:
        return "Нет выгодных арбитражных возможностей за текущий цикл."

    max_pair, max_info = max(opportunities.items(), key=lambda item: item[1]["spread_percent"])
    lines = [
        f"💰 *Самое выгодное предложение*: {max_pair} — спред: {max_info['spread_percent']:.3f}%\n",
        "*Выгодные пары:*"
    ]
    for pair, info in sorted(opportunities.items(), key=lambda item: -item[1]["spread_percent"]):
        lines.append(f"• {pair}: {info['spread_percent']:.3f}% (Купить: {info['buy_exchange']}, Продать: {info['sell_exchange']})")
    return "\n".join(lines)
