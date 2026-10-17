"""Git ガチャ：自分の番号を渡すと、その番号のガチャ結果を表示します。

使い方:  python3 gacha.py 7
同じ番号なら、いつ・誰が実行しても同じ結果になります。
だから、隣の人のPRをレビューするときは、その人の番号で実行して
結果が合っているか確認できます。
"""
import random
import sys

# (レア度, 名前, ポイント, 出やすさ)
ITEMS = [
    ("★1", "スライム", 1, 30),
    ("★1", "どんぐり", 1, 30),
    ("★2", "ミニゴーレム", 3, 20),
    ("★2", "ふしぎなキノコ", 3, 20),
    ("★3", "ひかるつるぎ", 5, 12),
    ("★3", "まほうのたまご", 5, 12),
    ("★4", "ドラゴン", 10, 5),
    ("★4", "ふしぎな王冠", 10, 5),
    ("★5", "でんせつのGit", 30, 1),
]


def draw(number: int):
    rng = random.Random(f"git-handson-gacha-{number}")
    return rng.choices(ITEMS, weights=[w for *_, w in ITEMS], k=1)[0]


def main():
    if len(sys.argv) != 2 or not sys.argv[1].isdigit() or not 1 <= int(sys.argv[1]) <= 30:
        print("使い方: python3 gacha.py 番号（1〜30）")
        sys.exit(1)
    number = int(sys.argv[1])
    rarity, name, points, _ = draw(number)
    print(f"{number:02d}番のガチャ結果")
    print(f"ガチャの結果：{rarity} {name}")
    print(f"ポイント：{points}")


if __name__ == "__main__":
    main()
