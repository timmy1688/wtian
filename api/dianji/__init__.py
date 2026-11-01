"""
典籍层（dianji）：古籍原文数据及其加载、检索。

    zhouyi.json / zhouyi.py              《周易》卦辞、爻辞、大象、小象
    ditiansui.json / ditiansui.py        《滴天髓》原文与旧注
    qiongtong_baojian.json / qiongtong.py 《穷通宝鉴》十干十二月调候
    jiansuo.py                           按命盘特征确定性选取八字典籍原文
    goujian.py                           从维基文库重新生成两部八字典籍数据（维护用）
"""
import json
from pathlib import Path

MULU = Path(__file__).resolve().parent


def du_json(wenjianming: str) -> dict:
    with (MULU / wenjianming).open(encoding="utf-8") as fh:
        return json.load(fh)
