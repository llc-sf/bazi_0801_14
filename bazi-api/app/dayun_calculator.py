"""
大运计算器
基于8Char-Uni-App-master的大运流年计算逻辑
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any
from .data_models import (
    Constants, TendData, DayunItem, YearItem, MonthItem, 
    DayItem, TimeItem
)
from .shishen_calculator import ShishenCalculator

class DayunCalculator:
    """
    大运计算器
    """
    
    def __init__(self, shishen_calc: ShishenCalculator):
        self.shishen_calc = shishen_calc
        self.tian_gan = Constants.TIAN_GAN
        self.di_zhi = Constants.DI_ZHI
        
        # 节气映射
        self.jieqi_map = [
            '立春', '惊蛰', '清明', '立夏', '芒种', '小暑', 
            '立秋', '白露', '寒露', '立冬', '大雪', '小寒'
        ]
    
    def calculate_dayun(self, birth_dt: datetime, gender: int, sect: int, day_gan: str) -> TendData:
        """
        计算大运流年
        gender: 1=男, 2=女
        sect: 1=晚子时日柱算明天, 2=晚子时日柱算当天
        """
        # 获取月柱作为起始大运
        year_offset = birth_dt.year - 1984
        month_offset = year_offset * 12 + birth_dt.month - 1
        month_gan = self.tian_gan[month_offset % 10]
        month_zhi = self.di_zhi[month_offset % 12]
        
        # 判断阳年阴年
        year_gan = self.tian_gan[year_offset % 10]
        year_gan_index = self.tian_gan.index(year_gan)
        is_yang_year = year_gan_index % 2 == 0
        
        # 确定大运排列方向
        if (is_yang_year and gender == 1) or (not is_yang_year and gender == 2):
            direction = 1  # 顺排
        else:
            direction = -1  # 逆排
        
        # 生成大运列表
        dayun_list = self._generate_dayun_list(
            birth_dt, month_gan, month_zhi, direction, day_gan
        )
        
        # 计算流年（基于第一个大运）
        year_list = self._generate_year_list(dayun_list, day_gan)
        
        # 计算流月（基于第一个流年）
        month_list = self._generate_month_list(year_list, day_gan) if year_list else []
        
        return TendData(
            dayunList=dayun_list,
            yearList=year_list,
            monthList=month_list,
            dayList=[],    # 流日计算较复杂，暂时留空  
            timeList=[],   # 流时计算较复杂，暂时留空
            currentIndex=0,
            yearIndex=0,
            monthIndex=0,
            dayIndex=0,
            timeIndex=0
        )
    
    def _generate_dayun_list(self, birth_dt: datetime, month_gan: str, month_zhi: str, 
                           direction: int, day_gan: str) -> List[DayunItem]:
        """生成大运列表"""
        dayun_list = []
        current_gan_index = self.tian_gan.index(month_gan)
        current_zhi_index = self.di_zhi.index(month_zhi)
        
        # 计算起运年龄（简化为8岁起运）
        start_age = 8
        
        for i in range(8):  # 生成8步大运
            start_year = birth_dt.year + start_age + i * 10
            
            if i == 0 and start_age < 8:
                pillar = "童限"
                shishen = "童限"
            else:
                gan = self.tian_gan[current_gan_index]
                zhi = self.di_zhi[current_zhi_index]
                pillar = gan + zhi
                shishen = self.shishen_calc.get_relation_by_pillar(day_gan, pillar)
            
            dayun_list.append(DayunItem(
                startYear=start_year,
                startAge=start_age + i * 10,
                pillar=pillar,
                shishen=shishen
            ))
            
            # 移动到下一个大运
            current_gan_index = (current_gan_index + direction) % 10
            current_zhi_index = (current_zhi_index + direction) % 12
        
        return dayun_list
    
    def _generate_year_list(self, dayun_list: List[DayunItem], day_gan: str) -> List[YearItem]:
        """生成流年列表"""
        year_list = []
        
        if not dayun_list:
            return year_list
        
        first_dayun = dayun_list[0]
        
        for year_offset in range(10):  # 每个大运包含10年
            current_year = first_dayun.startYear + year_offset
            year_gan_idx = (current_year - 1984) % 10
            year_zhi_idx = (current_year - 1984) % 12
            
            year_gan = self.tian_gan[year_gan_idx]
            year_zhi = self.di_zhi[year_zhi_idx]
            pillar = year_gan + year_zhi
            shishen = self.shishen_calc.get_relation_by_pillar(day_gan, pillar)
            
            year_list.append(YearItem(
                year=current_year,
                pillar=pillar,
                age=first_dayun.startAge + year_offset,
                shishen=shishen
            ))
        
        return year_list
    
    def _generate_month_list(self, year_list: List[YearItem], day_gan: str) -> List[MonthItem]:
        """生成流月列表"""
        month_list = []
        
        if not year_list:
            return month_list
        
        first_year = year_list[0]
        
        # 生成12个月的流月
        for month_idx in range(12):
            # 简化的月干支计算
            month_gan_idx = (first_year.year * 12 + month_idx) % 10
            month_zhi_idx = month_idx % 12
            
            month_gan = self.tian_gan[month_gan_idx]
            month_zhi = self.di_zhi[month_zhi_idx]
            pillar = month_gan + month_zhi
            shishen = self.shishen_calc.get_relation_by_pillar(day_gan, pillar)
            
            # 节气信息（简化）
            jieqi = self.jieqi_map[month_idx] if month_idx < len(self.jieqi_map) else "未知"
            
            month_list.append(MonthItem(
                year=first_year.year,
                jieqi=jieqi,
                date=f"{month_idx + 1}/1",  # 简化的日期
                nextJieqiDate=f"{(month_idx + 1) % 12 + 1}/1",  # 简化的下个节气日期
                pillar=pillar,
                shishen=shishen
            ))
        
        return month_list
    
    def skip_to_current_time(self, tend_data: TendData, current_dt: datetime, day_gan: str) -> TendData:
        """
        跳转到当前时间对应的大运流年
        对应前端的SkipCurrentTime方法
        """
        current_year = current_dt.year
        
        # 查找当前年份对应的大运
        for i, dayun in enumerate(tend_data.dayunList):
            if dayun.startYear <= current_year < dayun.startYear + 10:
                tend_data.currentIndex = i
                
                # 重新生成对应的流年
                year_list = []
                for year_offset in range(10):
                    year = dayun.startYear + year_offset
                    year_gan_idx = (year - 1984) % 10
                    year_zhi_idx = (year - 1984) % 12
                    
                    year_gan = self.tian_gan[year_gan_idx]
                    year_zhi = self.di_zhi[year_zhi_idx]
                    pillar = year_gan + year_zhi
                    shishen = self.shishen_calc.get_relation_by_pillar(day_gan, pillar)
                    
                    year_list.append(YearItem(
                        year=year,
                        pillar=pillar,
                        age=dayun.startAge + year_offset,
                        shishen=shishen
                    ))
                
                tend_data.yearList = year_list
                
                # 找到当前年份在流年中的位置
                for j, year_item in enumerate(year_list):
                    if year_item.year == current_year:
                        tend_data.yearIndex = j
                        break
                
                break
        
        return tend_data