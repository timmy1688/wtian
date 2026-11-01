"""
历法层：四柱干支、节气时刻、立春换年、农历换算。

整个算法层中只有本模块依赖第三方历法库（lunar_python 负责干支与节气，lunardate 负责农历转公历），
更换历法实现时只需改这里。
"""
from datetime import date, datetime

from lunar_python import Solar
from lunardate import LunarDate

from .jichu import DIZHI


class ShengriCuowu(ValueError):
    """出生时间在历法上不存在，message 可直接展示给用户。"""


def _nongli(shike: datetime):
    return Solar.fromYmdHms(shike.year, shike.month, shike.day, shike.hour, shike.minute, 0).getLunar()


def _zhuan_datetime(solar) -> datetime:
    return datetime(solar.getYear(), solar.getMonth(), solar.getDay(),
                    solar.getHour(), solar.getMinute(), solar.getSecond())


def pai_sizhu(shike: datetime) -> list:
    """按节气换月、立春换年排出四柱：[年柱, 月柱, 日柱, 时柱]。"""
    bazi = _nongli(shike).getEightChar()
    return [bazi.getYear(), bazi.getMonth(), bazi.getDay(), bazi.getTime()]


def xianglin_jie(shike: datetime) -> tuple:
    """出生时刻前后最近的「节」（不含中气）：(上一节名, 时刻, 下一节名, 时刻)。"""
    nongli = _nongli(shike)
    shang = nongli.getPrevJie()
    xia = nongli.getNextJie()
    return (
        shang.getName(), _zhuan_datetime(shang.getSolar()),
        xia.getName(), _zhuan_datetime(xia.getSolar()),
    )


def lichun_nian_ganzhi(riqi: date) -> str:
    """以立春为界的年干支。"""
    return Solar.fromYmd(riqi.year, riqi.month, riqi.day).getLunar().getYearInGanZhiByLiChun()


def qiu_shichen(xiaoshi: int) -> str:
    """小时所属时辰：23-1 点为子时，每两小时一个时辰。"""
    return DIZHI[((xiaoshi + 1) // 2) % 12] + "时"


def nongli_miaoshu(shike: datetime) -> str:
    """农历中文描述，如「一九九〇年 四月 廿六 未时」。"""
    nongli = Solar.fromYmdHms(shike.year, shike.month, shike.day, shike.hour, 0, 0).getLunar()
    return (f"{nongli.getYearInChinese()}年 {nongli.getMonthInChinese()}月 "
            f"{nongli.getDayInChinese()} {qiu_shichen(shike.hour)}")


def nongli_zhuan_gongli(riqi_str: str, shi_runyue: bool = False) -> datetime:
    """
    农历 "YYYYMMDD HH" 转公历。
    :param shi_runyue: 是否闰月；仅当该年确有此闰月时生效
    """
    # Not strptime: lunar days such as 二月三十 are invalid Gregorian dates
    nian, yue, ri, shi = int(riqi_str[0:4]), int(riqi_str[4:6]), int(riqi_str[6:8]), int(riqi_str[9:11])
    if shi > 23:
        raise ShengriCuowu(f"出生时辰不合法：{shi} 时")
    runyue = shi_runyue and LunarDate.leapMonthForYear(nian) == yue
    try:
        gongli = LunarDate(nian, yue, ri, runyue).toSolarDate()
    except ValueError:
        biaoji = "闰" if runyue else ""
        raise ShengriCuowu(f"农历 {nian} 年 {biaoji}{yue} 月没有第 {ri} 天，请检查出生日期")
    return datetime(gongli.year, gongli.month, gongli.day, shi)


def jiexi_shengri(riqi_str: str, shi_nongli: bool = False, shi_runyue: bool = False) -> datetime:
    """解析 "YYYYMMDD HH" 出生时间，农历先转公历。"""
    if shi_nongli:
        return nongli_zhuan_gongli(riqi_str, shi_runyue)
    try:
        return datetime.strptime(riqi_str, "%Y%m%d %H")
    except ValueError:
        raise ShengriCuowu(f"公历日期不存在：{riqi_str[0:4]}-{riqi_str[4:6]}-{riqi_str[6:8]} {riqi_str[9:11]} 时")
