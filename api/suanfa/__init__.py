"""
算法层（suanfa）：八字排盘与易经起卦的全部确定性推算。

只做计算，不依赖 Web 框架和大模型；命名统一用拼音，便于与命理术语对照：
    jichu    干支基础表（五行、藏干、十二长生、纳音、十神、合冲刑害）
    lifa     历法：四柱、节气、农历换算（唯一依赖 lunar_python / lunardate 的模块）
    jiben    基本推算：十神、十二长生、纳音、旬空、旺相休囚
    wangshuai 五行力量、日主旺衰、扶抑喜用
    guanxi   干支合冲刑害、三合三会
    yunshi   大运、流年
    mingpan  汇总成完整命盘
    qigua    铜钱起卦、本卦变卦
    quyong   动爻取用经文
"""
