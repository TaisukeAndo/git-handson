"""みんなのガチャ結果を集計して、チームのランクとランキングを表示します。

使い方:  python3 ranking.py
gacha.txt を読み、gacha.py の結果と合っているかも確認します。
結果やポイントが合っていない欄は、ポイントに数えません（うそはバレます）。
"""
import re
from pathlib import Path

from gacha import draw

TIERS = [(100, "プラチナ"), (60, "ゴールド"), (30, "シルバー"), (10, "ブロンズ"), (0, "ランクなし")]


def read_slots(text: str):
    slots = []
    parts = re.split(r"(?m)^== (\d+)番 ==\s*$", text)
    for number, body in zip(parts[1::2], parts[2::2]):
        field = lambda key: (re.search(rf"(?m)^{key}：(.*)$", body) or [None, ""])[1].strip()
        slots.append((int(number), field("名前"), field("ガチャの結果"), field("ポイント")))
    return slots


def main():
    slots = read_slots(Path(__file__).with_name("gacha.txt").read_text(encoding="utf-8"))
    valid, wrong, empty = [], [], 0
    for number, name, result, points in slots:
        if not (name or result or points):
            empty += 1
            continue
        rarity, item, pt, _ = draw(number)
        if result == f"{rarity} {item}" and points == str(pt) and name:
            valid.append((pt, number, name, result))
        else:
            wrong.append((number, name or "（名前なし）"))
    total = sum(v[0] for v in valid)
    tier = next(label for border, label in TIERS if total >= border)

    print("=== Git ガチャ大会 ===")
    print(f"参加：{len(valid) + len(wrong)}人 / 未記入の欄：{empty}")
    print(f"チームの合計：{total}ポイント → {tier}")
    nxt = [(b, l) for b, l in TIERS if b > total]
    if nxt:
        b, l = nxt[-1]
        print(f"次のランク（{l}）まで：あと{b - total}ポイント")
    print()
    print("--- ランキング（上位5人）---")
    for rank, (pt, number, name, result) in enumerate(sorted(valid, reverse=True)[:5], 1):
        print(f"{rank}位  {name}（{number:02d}番）  {result}  {pt}pt")
    if wrong:
        print()
        print("--- 確認が必要な欄（結果やポイントが gacha.py と合っていません）---")
        for number, name in wrong:
            print(f"{number:02d}番  {name}")


if __name__ == "__main__":
    main()
