"""
八字计算主类 - 完全按照 8Char-Uni-App-master 逻辑重构
只输出八字、十神、大运，先转阴历再输出
"""

from datetime import datetime
from typing import Dict, Any, List
import lunar_python

class BaziCalculator:
    """
    八字计算主类 - 完全按照前端逻辑重构
    """
    
    def __init__(self):
        # 前端配置映射
        self.SHI_SHEN_SIMPLIFIE = {
            "比肩": "比", "劫财": "劫", "食神": "食", "伤官": "伤", 
            "偏财": "才", "正财": "财", "七杀": "杀", "正官": "官",
            "偏印": "枭", "正印": "印"
        }
    
    def calculate_bazi_info(self, dt: datetime, gender: int, sect: int, realname: str) -> Dict[str, Any]:
        """
        计算八字基本信息 - 完全按照前端逻辑
        """
        # 1. 使用 lunar-javascript 逻辑进行农历计算
        solar = lunar_python.Solar.fromYmdHms(dt.year, dt.month, dt.day, dt.hour, dt.minute, 0)
        lunar = solar.getLunar()
        bazi = lunar.getEightChar()
        
        # 2. 获取八字四柱（先转阴历再输出）
        year_gan = bazi.getYearGan()
        year_zhi = bazi.getYearZhi()
        month_gan = bazi.getMonthGan()
        month_zhi = bazi.getMonthZhi()
        day_gan = bazi.getDayGan()
        day_zhi = bazi.getDayZhi()
        time_gan = bazi.getTimeGan()
        time_zhi = bazi.getTimeZhi()
        
        # 3. 获取十神关系
        gods = self._get_gods_list(day_gan, year_gan, month_gan, time_gan, year_zhi, month_zhi, day_zhi, time_zhi)
        
        # 4. 获取农历信息
        lunar_info = {
            "year": lunar.getYear(),
            "month": lunar.getMonth(),
            "day": lunar.getDay(),
            "isLeap": False,  # 简化处理
            "lunar_str": f"{lunar.getYear()}年{lunar.getMonthInChinese()}月{lunar.getDayInChinese()}日"
        }
        
        # 5. 计算大运信息
        yun = bazi.getYun(gender, sect)
        dayun_list = yun.getDaYun()
        
        # 处理大运数据
        dayun_result = []
        start_age = 8  # 默认起运年龄
        for item in dayun_list:
            pillar = item.getGanZhi() or '童限'
            if item.getStartAge() > 0:
                start_age = item.getStartAge()
            dayun_result.append({
                "startYear": item.getStartYear(),
                "startAge": item.getStartAge(),
                "pillar": pillar,
                "shishen": self._get_shishen_by_pillar(day_gan, pillar)
            })
        
        # 6. 构造返回数据 - 完全按照前端格式
        result = {
            # 基本信息
            "realname": realname,
            "gender": gender,
            "timestamp": int(dt.timestamp() * 1000),
            "sect": sect,
            
            # 时间信息
            "datetime": {
                "solar": dt.strftime("%Y年%m月%d日 %H时%M分"),
                "lunar": lunar_info["lunar_str"]
            },
            
            # 星座生肖
            "constellation": self._get_constellation(dt.month, dt.day),
            "zodiac": lunar.getYearShengXiao(),
            
            # 八字四柱
            "top": {
                "year": year_gan,
                "month": month_gan,
                "day": day_gan,
                "time": time_gan
            },
            "bottom": {
                "year": year_zhi,
                "month": month_zhi,
                "day": day_zhi,
                "time": time_zhi
            },
            
            # 纳音
            "nayin": {
                "year": bazi.getYearNaYin(),
                "month": bazi.getMonthNaYin(),
                "day": bazi.getDayNaYin(),
                "time": bazi.getTimeNaYin()
            },
            
            # 十神
            "gods": gods,
            
            # 藏干
            "bottom_hide": {
                "year": self._get_hide_gan(year_zhi),
                "month": self._get_hide_gan(month_zhi),
                "day": self._get_hide_gan(day_zhi),
                "time": self._get_hide_gan(time_zhi)
            },
            
            # 空亡
            "empty": {
                "year": "",
                "month": "",
                "day": lunar.getDayXunKong()[0] if lunar.getDayXunKong() else "",
                "time": lunar.getDayXunKong()[1] if len(lunar.getDayXunKong()) > 1 else ""
            },
            
            # 大运信息
            "startAge": start_age,
            "dayunList": dayun_result
        }
        
        return result
    
    def calculate_bazi_prediction(self, dt: datetime, gender: int, sect: int) -> Dict[str, Any]:
        """
        计算大运流年预测 - 完全按照前端逻辑
        """
        # 1. 使用 lunar-javascript 逻辑进行农历计算
        solar = lunar_python.Solar.fromDate(dt)
        lunar = solar.getLunar()
        bazi = lunar.getEightChar()
        
        # 2. 获取日干作为十神计算基准
        day_gan = bazi.getDayGan()
        
        # 3. 计算大运
        yun = bazi.getYun(gender, sect)
        dayun_list = yun.getDaYun()
        
        # 4. 处理大运数据
        dayun_result = []
        for item in dayun_list:
            pillar = item.getGanZhi() or '童限'
            dayun_result.append({
                "startYear": item.getStartYear(),
                "startAge": item.getStartAge(),
                "pillar": pillar,
                "shishen": self._get_shishen_by_pillar(day_gan, pillar)
            })
        
        # 5. 处理流年数据（取第一个大运的流年）
        year_result = []
        if dayun_list:
            first_dayun = dayun_list[0]
            liunian_list = first_dayun.getLiuNian()
            for item in liunian_list[:20]:  # 取前20年
                pillar = item.getGanZhi()
                year_result.append({
                    "year": item.getYear(),
                    "pillar": pillar,
                    "age": item.getAge(),
                    "shishen": self._get_shishen_by_pillar(day_gan, pillar)
                })
        
        return {
            "dayunList": dayun_result,
            "yearList": year_result,
            "monthList": [],
            "dayList": [],
            "timeList": [],
            "currentIndex": 0,
            "yearIndex": 0,
            "monthIndex": 0,
            "dayIndex": 0,
            "timeIndex": 0
        }
    
    def _get_gods_list(self, day_gan: str, year_gan: str, month_gan: str, time_gan: str,
                      year_zhi: str, month_zhi: str, day_zhi: str, time_zhi: str) -> List[str]:
        """
        获取十神列表 - 完全按照前端逻辑
        """
        gods = []
        
        # 年干十神
        year_gan_shishen = self._get_shishen_gan(day_gan, year_gan)
        gods.append(year_gan_shishen)
        
        # 月干十神
        month_gan_shishen = self._get_shishen_gan(day_gan, month_gan)
        gods.append(month_gan_shishen)
        
        # 日干十神（日干对自己是比肩）
        day_gan_shishen = "比肩"
        gods.append(day_gan_shishen)
        
        # 时干十神
        time_gan_shishen = self._get_shishen_gan(day_gan, time_gan)
        gods.append(time_gan_shishen)
        
        return gods
    
    def _get_shishen_gan(self, day_gan: str, target_gan: str) -> str:
        """
        获取天干十神 - 完全按照前端逻辑
        """
        # 前端使用 LunarUtil.SHI_SHEN_GAN 映射
        shishen_map = {
            # 甲日干
            "甲甲": "比肩", "甲乙": "劫财", "甲丙": "食神", "甲丁": "伤官",
            "甲戊": "偏财", "甲己": "正财", "甲庚": "七杀", "甲辛": "正官",
            "甲壬": "偏印", "甲癸": "正印",
            
            # 乙日干
            "乙甲": "劫财", "乙乙": "比肩", "乙丙": "伤官", "乙丁": "食神",
            "乙戊": "正财", "乙己": "偏财", "乙庚": "正官", "乙辛": "七杀",
            "乙壬": "正印", "乙癸": "偏印",
            
            # 丙日干
            "丙甲": "偏印", "丙乙": "正印", "丙丙": "比肩", "丙丁": "劫财",
            "丙戊": "食神", "丙己": "伤官", "丙庚": "偏财", "丙辛": "正财",
            "丙壬": "七杀", "丙癸": "正官",
            
            # 丁日干
            "丁甲": "正印", "丁乙": "偏印", "丁丙": "劫财", "丁丁": "比肩",
            "丁戊": "伤官", "丁己": "食神", "丁庚": "正财", "丁辛": "偏财",
            "丁壬": "正官", "丁癸": "七杀",
            
            # 戊日干
            "戊甲": "七杀", "戊乙": "正官", "戊丙": "偏印", "戊丁": "正印",
            "戊戊": "比肩", "戊己": "劫财", "戊庚": "食神", "戊辛": "伤官",
            "戊壬": "偏财", "戊癸": "正财",
            
            # 己日干
            "己甲": "正官", "己乙": "七杀", "己丙": "正印", "己丁": "偏印",
            "己戊": "劫财", "己己": "比肩", "己庚": "伤官", "己辛": "食神",
            "己壬": "正财", "己癸": "偏财",
            
            # 庚日干
            "庚甲": "偏财", "庚乙": "正财", "庚丙": "七杀", "庚丁": "正官",
            "庚戊": "偏印", "庚己": "正印", "庚庚": "比肩", "庚辛": "劫财",
            "庚壬": "食神", "庚癸": "伤官",
            
            # 辛日干
            "辛甲": "正财", "辛乙": "偏财", "辛丙": "正官", "辛丁": "七杀",
            "辛戊": "正印", "辛己": "偏印", "辛庚": "劫财", "辛辛": "比肩",
            "辛壬": "伤官", "辛癸": "食神",
            
            # 壬日干
            "壬甲": "食神", "壬乙": "伤官", "壬丙": "偏财", "壬丁": "正财",
            "壬戊": "七杀", "壬己": "正官", "壬庚": "偏印", "壬辛": "正印",
            "壬壬": "比肩", "壬癸": "劫财",
            
            # 癸日干
            "癸甲": "伤官", "癸乙": "食神", "癸丙": "正财", "癸丁": "偏财",
            "癸戊": "正官", "癸己": "七杀", "癸庚": "正印", "癸辛": "偏印",
            "癸壬": "劫财", "癸癸": "比肩"
        }
        
        key = day_gan + target_gan
        return shishen_map.get(key, "未知")
    
    def _get_shishen_by_pillar(self, day_gan: str, pillar: str) -> str:
        """
        根据干支柱获取十神 - 完全按照前端逻辑
        """
        if pillar == '童限':
            return '童限'
        
        if len(pillar) >= 2:
            gan = pillar[0]
            zhi = pillar[1]
            
            # 获取天干十神
            gan_shishen = self._get_shishen_gan(day_gan, gan)
            
            # 获取地支十神
            zhi_shishen = self._get_shishen_zhi(day_gan, zhi)
            
            # 组合十神
            gan_simplified = self.SHI_SHEN_SIMPLIFIE.get(gan_shishen, gan_shishen)
            zhi_simplified = self.SHI_SHEN_SIMPLIFIE.get(zhi_shishen, zhi_shishen)
            
            return gan_simplified + zhi_simplified
        
        return "未知"
    
    def _get_shishen_zhi(self, day_gan: str, zhi: str) -> str:
        """
        获取地支十神 - 完全按照前端逻辑
        """
        # 地支藏干十神映射
        zhi_hide_gan = {
            "子": ["癸"], "丑": ["己", "辛", "癸"], "寅": ["甲", "丙", "戊"],
            "卯": ["乙"], "辰": ["戊", "乙", "癸"], "巳": ["丙", "庚", "戊"],
            "午": ["丁", "己"], "未": ["己", "丁", "乙"], "申": ["庚", "壬", "戊"],
            "酉": ["辛"], "戌": ["戊", "辛", "丁"], "亥": ["壬", "甲"]
        }
        
        if zhi in zhi_hide_gan:
            # 取地支的本气天干
            main_gan = zhi_hide_gan[zhi][0]
            return self._get_shishen_gan(day_gan, main_gan)
        
        return "未知"
    
    def _get_hide_gan(self, zhi: str) -> List[str]:
        """
        获取地支藏干 - 完全按照前端逻辑
        """
        zhi_hide_gan = {
            "子": ["癸"], "丑": ["己", "辛", "癸"], "寅": ["甲", "丙", "戊"],
            "卯": ["乙"], "辰": ["戊", "乙", "癸"], "巳": ["丙", "庚", "戊"],
            "午": ["丁", "己"], "未": ["己", "丁", "乙"], "申": ["庚", "壬", "戊"],
            "酉": ["辛"], "戌": ["戊", "辛", "丁"], "亥": ["壬", "甲"]
        }
        
        return zhi_hide_gan.get(zhi, [])
    
    def _get_constellation(self, month: int, day: int) -> str:
        """
        获取星座
        """
        if (month == 3 and day >= 21) or (month == 4 and day <= 19):
            return "白羊座"
        elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
            return "金牛座"
        elif (month == 5 and day >= 21) or (month == 6 and day <= 21):
            return "双子座"
        elif (month == 6 and day >= 22) or (month == 7 and day <= 22):
            return "巨蟹座"
        elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
            return "狮子座"
        elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
            return "处女座"
        elif (month == 9 and day >= 23) or (month == 10 and day <= 23):
            return "天秤座"
        elif (month == 10 and day >= 24) or (month == 11 and day <= 22):
            return "天蝎座"
        elif (month == 11 and day >= 23) or (month == 12 and day <= 21):
            return "射手座"
        elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
            return "摩羯座"
        elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
            return "水瓶座"
        elif (month == 2 and day >= 19) or (month == 3 and day <= 20):
            return "双鱼座"
        else:
            return "未知"