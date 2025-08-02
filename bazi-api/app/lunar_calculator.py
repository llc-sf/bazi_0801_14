"""
农历计算器 - 简化版lunar-javascript逻辑
"""

from datetime import datetime, timedelta
from typing import Tuple, Dict, List
from .data_models import Constants

class LunarCalculator:
    """
    农历计算器 - 简化版lunar-javascript逻辑
    """
    
    def __init__(self):
        # 天干地支
        self.tian_gan = Constants.TIAN_GAN
        self.di_zhi = Constants.DI_ZHI
        
        # 生肖
        self.zodiac_names = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]
        
        # 星座
        self.constellation_names = [
            "水瓶座", "双鱼座", "白羊座", "金牛座", "双子座", "巨蟹座",
            "狮子座", "处女座", "天秤座", "天蝎座", "射手座", "摩羯座"
        ]
        
        # 纳音
        self.nayin_map = {
            ("甲", "子"): "海中金", ("乙", "丑"): "海中金", ("丙", "寅"): "炉中火", ("丁", "卯"): "炉中火",
            ("戊", "辰"): "大林木", ("己", "巳"): "大林木", ("庚", "午"): "路旁土", ("辛", "未"): "路旁土",
            ("壬", "申"): "剑锋金", ("癸", "酉"): "剑锋金", ("甲", "戌"): "山头火", ("乙", "亥"): "山头火",
            ("丙", "子"): "涧下水", ("丁", "丑"): "涧下水", ("戊", "寅"): "城头土", ("己", "卯"): "城头土",
            ("庚", "辰"): "白蜡金", ("辛", "巳"): "白蜡金", ("壬", "午"): "杨柳木", ("癸", "未"): "杨柳木",
            ("甲", "申"): "井泉水", ("乙", "酉"): "井泉水", ("丙", "戌"): "屋上土", ("丁", "亥"): "屋上土",
            ("戊", "子"): "霹雳火", ("己", "丑"): "霹雳火", ("庚", "寅"): "松柏木", ("辛", "卯"): "松柏木",
            ("壬", "辰"): "长流水", ("癸", "巳"): "长流水", ("甲", "午"): "砂中金", ("乙", "未"): "砂中金",
            ("丙", "申"): "山下火", ("丁", "酉"): "山下火", ("戊", "戌"): "平地木", ("己", "亥"): "平地木",
            ("庚", "子"): "壁上土", ("辛", "丑"): "壁上土", ("壬", "寅"): "金泊金", ("癸", "卯"): "金泊金",
            ("甲", "辰"): "覆灯火", ("乙", "巳"): "覆灯火", ("丙", "午"): "天河水", ("丁", "未"): "天河水",
            ("戊", "申"): "大驿土", ("己", "酉"): "大驿土", ("庚", "戌"): "钗钏金", ("辛", "亥"): "钗钏金",
            ("壬", "子"): "桑柘木", ("癸", "丑"): "桑柘木"
        }
        
        # 空亡 - 甲子旬的计算
        self.empty_map = {
            0: ("戌", "亥"), 10: ("申", "酉"), 20: ("午", "未"),
            30: ("辰", "巳"), 40: ("寅", "卯"), 50: ("子", "丑")
        }
        
    def get_gan_zhi_from_date(self, dt: datetime) -> Tuple[str, str, str, str, str, str, str, str]:
        """
        从日期计算八字（年月日时的天干地支）
        简化实现，实际应使用专业的万年历算法
        """
        # 简化的八字计算 - 实际应该使用精确的万年历
        year_offset = dt.year - 1984  # 1984年是甲子年
        year_gan = self.tian_gan[year_offset % 10]
        year_zhi = self.di_zhi[year_offset % 12]
        
        # 月干支计算（简化）
        month_offset = (dt.year - 1984) * 12 + dt.month - 1
        month_gan = self.tian_gan[month_offset % 10]
        month_zhi = self.di_zhi[month_offset % 12]
        
        # 日干支计算（简化 - 应使用儒略日）
        day_offset = (dt - datetime(1984, 1, 1)).days
        day_gan = self.tian_gan[day_offset % 10]
        day_zhi = self.di_zhi[day_offset % 12]
        
        # 时干支计算
        hour_index = (dt.hour + 1) // 2 % 12
        time_zhi = self.di_zhi[hour_index]
        # 时干根据日干推算
        day_gan_index = self.tian_gan.index(day_gan)
        time_gan_index = (day_gan_index * 2 + hour_index) % 10
        time_gan = self.tian_gan[time_gan_index]
        
        return year_gan, year_zhi, month_gan, month_zhi, day_gan, day_zhi, time_gan, time_zhi
    
    def get_zodiac(self, year: int) -> str:
        """获取生肖"""
        return self.zodiac_names[(year - 4) % 12]
    
    def get_constellation(self, month: int, day: int) -> str:
        """获取星座"""
        dates = [
            (1, 20), (2, 19), (3, 21), (4, 20), (5, 21), (6, 21),
            (7, 23), (8, 23), (9, 23), (10, 23), (11, 22), (12, 22)
        ]
        
        for i, (m, d) in enumerate(dates):
            if month < m or (month == m and day < d):
                return self.constellation_names[(i - 1) % 12]
        
        return self.constellation_names[11]
    
    def get_nayin(self, gan: str, zhi: str) -> str:
        """获取纳音"""
        return self.nayin_map.get((gan, zhi), "未知")
    
    def get_empty(self, day_gan: str, day_zhi: str) -> Tuple[str, str]:
        """计算空亡"""
        # 简化的空亡计算
        day_gan_index = self.tian_gan.index(day_gan)
        day_zhi_index = self.di_zhi.index(day_zhi)
        
        # 找到对应的旬
        xun_index = (day_gan_index * 6 + day_zhi_index) % 60
        xun_start = (xun_index // 10) * 10
        
        return self.empty_map.get(xun_start, ("", ""))