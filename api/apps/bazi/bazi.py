from lunar_python import Solar, Lunar
from datetime import datetime
from lunardate import LunarDate

def calculate_wuxing(bazi_list: list)->list:
    tiangan_wuxing = {
        '甲': '木', '乙': '木',  # 甲乙属木
        '丙': '火', '丁': '火',  # 丙丁属火
        '戊': '土', '己': '土',  # 戊己属土
        '庚': '金', '辛': '金',  # 庚辛属金
        '壬': '水', '癸': '水',  # 壬癸属水
    }
    dizhi_wuxing = {
        '子': '水', '亥': '水',  # 子亥属水
        '寅': '木', '卯': '木',  # 寅卯属木
        '巳': '火', '午': '火',  # 巳午属火
        '丑': '土', '辰': '土', '未': '土', '戌': '土',  # 丑辰未戌属土
        '申': '金', '酉': '金',  # 申酉属金
    }
    # 八字为4柱，每柱包含一个天干和一个地支
    elements = {'木': 0, '火': 0, '土': 0, '金': 0, '水': 0}
     
    for s in bazi_list:
        tangan = tiangan_wuxing[s[0]]
        dizhi= dizhi_wuxing[s[1]]
        elements[tangan] += 1
        elements[dizhi] += 1
        
    total = sum(elements.values())  # 8

    elements_percentage = {}  # 创建空字典
    for key, value in elements.items():
        elements_percentage[key] = (value / total) * 100  # 计算并赋值
        
    return elements_percentage
        
    
    
    print(bazi_str)

def calculate_shishen(bazi_list: list)->list:

    #计算口诀
    """
    生我正偏印（同正异偏）（同性为正印，异性为偏印）
    我生食伤（同食异伤）（同性为食神，异性为伤官）
    同我比劫（同比异劫）（同性为比肩，异性为劫财）
    我克正偏财（同正异偏）（同性为正财，异性为偏财）
    克我正官七杀（同正异杀）（同性为正官，异性为七杀）
    """
    # 天干五行和阴阳属性
    GAN_WUXING = {'甲': '木', '乙': '木', '丙': '火', '丁': '火', '戊': '土', '己': '土', '庚': '金', '辛': '金', '壬': '水', '癸': '水'}
    GAN_YINYANG = {'甲': '阳', '乙': '阴', '丙': '阳', '丁': '阴', '戊': '阳', '己': '阴', '庚': '阳', '辛': '阴', '壬': '阳', '癸': '阴'}


    # 十神关系表（基于五行生克关系和阴阳同异）
    SHISHEN_RELATION = {
        '水': {
            '水': {'同性': '比肩', '异性': '劫财'},  # 同我
            '金': {'同性': '偏印', '异性': '正印'},  # 生我
            '木': {'同性': '食神', '异性': '伤官'},  # 我生
            '火': {'同性': '偏财', '异性': '正财'},  # 我克
            '土': {'同性': '七杀', '异性': '正官'}   # 克我
        },
        '木': {
            '木': {'同性': '比肩', '异性': '劫财'},
            '水': {'同性': '偏印', '异性': '正印'},
            '火': {'同性': '食神', '异性': '伤官'},
            '土': {'同性': '偏财', '异性': '正财'},
            '金': {'同性': '七杀', '异性': '正官'}
        },
        '火': {
            '火': {'同性': '比肩', '异性': '劫财'},
            '木': {'同性': '偏印', '异性': '正印'},
            '土': {'同性': '食神', '异性': '伤官'},
            '金': {'同性': '偏财', '异性': '正财'},
            '水': {'同性': '七杀', '异性': '正官'}
        },
        '土': {
            '土': {'同性': '比肩', '异性': '劫财'},
            '火': {'同性': '偏印', '异性': '正印'},
            '金': {'同性': '食神', '异性': '伤官'},
            '水': {'同性': '偏财', '异性': '正财'},
            '木': {'同性': '七杀', '异性': '正官'}
        },
        '金': {
            '金': {'同性': '比肩', '异性': '劫财'},
            '土': {'同性': '偏印', '异性': '正印'},
            '水': {'同性': '食神', '异性': '伤官'},
            '木': {'同性': '偏财', '异性': '正财'},
            '火': {'同性': '七杀', '异性': '正官'}
        }
    }
    """
    根据八字字符串计算每个天干的十神关系
    :param bazi_str: 八字字符串，例如 '戊寅甲寅壬辰癸卯'
    :return: 每个天干的十神关系（字典格式）
    """
    def get_shishen(day_gan, gan):
        """
        获取某个天干相对于日主的十神关系
        :param day_gan: 日主天干
        :param gan: 需要计算的天干
        :return: 十神名称
        """
        # 获取日主和目标天干的五行属性
        day_wuxing = GAN_WUXING[day_gan]
        target_wuxing = GAN_WUXING[gan]
        
        # 根据五行生克关系查找十神
        return SHISHEN_RELATION[day_wuxing][target_wuxing]
    
    
    # 提取日主天干（日柱的第一个字符）
    day_gan = bazi_list[2][0]
    day_wuxing = GAN_WUXING[day_gan]
    day_yinyang = GAN_YINYANG[day_gan]
    
    # 计算每个天干的十神关系
    shishen_list = []
    for pillar in bazi_list:
        gan = pillar[0]
        gan_wuxing = GAN_WUXING[gan]
        gan_yinyang = GAN_YINYANG[gan]
        
        # 判断阴阳是同性还是异性
        yinyang_relation = '同性' if day_yinyang == gan_yinyang else '异性'
        
        # 根据五行生克关系和阴阳同异查找十神
        shishen = SHISHEN_RELATION[day_wuxing][gan_wuxing][yinyang_relation]
        shishen_list.append(shishen)
    
    return shishen_list


    
    # 遍历八字中的每个天干
    for idx, pillar in enumerate(bazi):
        gan = pillar[0]  # 每柱的第一个字符是天干
        shishen = get_shishen(day_gan, gan)
        shishen_result[f'第{idx+1}柱'] = (gan, shishen)
    
    return shishen_result


# 映射到时辰
def get_shichen(hour):
    if 23 <= hour or hour < 1:
        return "子时"
    elif 1 <= hour < 3:
        return "丑时"
    elif 3 <= hour < 5:
        return "寅时"
    elif 5 <= hour < 7:
        return "卯时"
    elif 7 <= hour < 9:
        return "辰时"
    elif 9 <= hour < 11:
        return "巳时"
    elif 11 <= hour < 13:
        return "午时"
    elif 13 <= hour < 15:
        return "未时"
    elif 15 <= hour < 17:
        return "申时"
    elif 17 <= hour < 19:
        return "酉时"
    elif 19 <= hour < 21:
        return "戌时"
    else:  # 21 <= hour < 23
        return "亥时"




def lunar_to_solar(date_str:str):
    """
    将给定的农历日期转换为对应的公历日期。
    
    参数:
    - lunar_year: 农历年份
    - lunar_month: 农历月份 (1-12)
    - lunar_day: 农历日 (1-30)
    - is_leap: 是否为闰月，默认值为False
    
    返回:
    - 对应的公历日期(datetime.date对象)
    """
    dt = datetime.strptime(date_str, "%Y%m%d %H")
    lunar_year, lunar_month, lunar_day, hour = dt.year, dt.month, dt.day, dt.hour
    run_month=LunarDate.leapMonthForYear(lunar_year)
    print(run_month)
    if run_month == lunar_month:
        is_leap = True
    else:
        is_leap = False
    
    # 创建LunarDate对象
    lunar_date = LunarDate(lunar_year, lunar_month, lunar_day, is_leap)
    # 转换为公历日期
    solar_date = lunar_date.toSolarDate()
    str_solar_date=solar_date.strftime("%Y%m%d")
    str=f"{str_solar_date} {hour}"
    return str

def calculate_bazi(date_str: str,is_lunar:bool=False) -> dict:
    if is_lunar:
        str_solar_date=lunar_to_solar(date_str)
        dt = datetime.strptime(str_solar_date, "%Y%m%d %H")
        year, month, day, hour = dt.year, dt.month, dt.day, dt.hour
    else:
        # 解析新历日期
        dt = datetime.strptime(date_str, "%Y%m%d %H")
        year, month, day, hour = dt.year, dt.month, dt.day, dt.hour

    shichen = get_shichen(hour)

    # 将新历转换为农历
    solar = Solar.fromYmdHms(year, month, day, hour, 0, 0)
    lunar = solar.getLunar()
    eight_char = lunar.getEightChar()

    # 获取八字
    year_gan_zhi = eight_char.getYear()   # 年柱
    month_gan_zhi = eight_char.getMonth() # 月柱
    day_gan_zhi = eight_char.getDay()     # 日柱
    hour_gan_zhi = eight_char.getTime()   # 时柱

    baizi_list=[]
    baizi_list.append(year_gan_zhi)
    baizi_list.append(month_gan_zhi)
    baizi_list.append(day_gan_zhi)
    baizi_list.append(hour_gan_zhi)

    bazi_str=f"{year_gan_zhi}{month_gan_zhi}{day_gan_zhi}{hour_gan_zhi}"

    shishen =calculate_shishen(baizi_list)
    wuxing =calculate_wuxing(baizi_list)

    # 返回结果
    return {
        "bazi": baizi_list,
        "shishen": shishen,
        "wuxing": wuxing,
        "xin_time": f"{year}年{month}月{day}日{hour}时",
        "nong_time": f"{lunar.getYearInChinese()}年 {lunar.getMonthInChinese()}月 {lunar.getDayInChinese()} {shichen}"
    }

# 测试
# if __name__ == "__main__":
#     result = calculate_shishen("戊寅甲寅壬辰癸卯")
#     print(result)





# 测试（异步函数需要用事件循环运行）
if __name__ == "__main__":
    import asyncio
    
    async def test():
        # result =  calculate_bazi("19980214 06",False)
        result =  calculate_bazi("19980118 06",True)
        # result = lunar_to_solar(1998, 1, 18)
        # result = lunar_to_solar("20230201 06")
        print(result)
    
    asyncio.run(test())