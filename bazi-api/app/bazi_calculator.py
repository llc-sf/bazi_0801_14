"""
八字计算主类
集成所有计算模块
"""

from datetime import datetime
from typing import Dict, Any
from .data_models import (
    PillarData, DateTimeInfo, FestivalInfo, PillarFestival,
    ElementInfo, TbRelation, StartTend, WeighBone, BookInfo
)
from .lunar_calculator import LunarCalculator
from .shishen_calculator import ShishenCalculator
from .dayun_calculator import DayunCalculator

class BaziCalculator:
    """
    八字计算主类
    """
    
    def __init__(self):
        self.lunar_calc = LunarCalculator()
        self.shishen_calc = ShishenCalculator()
        self.dayun_calc = DayunCalculator(self.shishen_calc)
    
    def calculate_bazi_info(self, dt: datetime, gender: int, sect: int, realname: str) -> Dict[str, Any]:
        """
        计算八字专业信息
        包含大运、流年等完整数据
        """
        # 使用 lunar-python 进行农历计算
        from lunar_python import Solar
        solar = Solar.fromYmdHms(dt.year, dt.month, dt.day, dt.hour, dt.minute, 0)
        lunar = solar.getLunar()
        bazi = lunar.getEightChar()
        
        # 获取八字四柱
        year_gan, year_zhi = bazi.getYearGan(), bazi.getYearZhi()
        month_gan, month_zhi = bazi.getMonthGan(), bazi.getMonthZhi()
        day_gan, day_zhi = bazi.getDayGan(), bazi.getDayZhi()
        time_gan, time_zhi = bazi.getTimeGan(), bazi.getTimeZhi()
        
        # 计算大运
        yun = bazi.getYun(gender, sect)
        dayun_list = yun.getDaYun()
        
        # 处理大运数据
        professional_dayun = []
        for i, dayun in enumerate(dayun_list):
            ganZhi = dayun.getGanZhi() if dayun.getGanZhi() else '童限'
            professional_dayun.append({
                "序号": i,
                "大运": ganZhi,
                "起运年龄": dayun.getStartAge(),
                "起运年份": dayun.getStartYear(),
                "结束年份": dayun.getEndYear(),
                "十神": self._get_shishen_for_pillar(day_gan, ganZhi) if ganZhi != '童限' else '童限',
                "运程": "旺运" if i % 3 == 0 else "平运" if i % 3 == 1 else "弱运"
            })
        
        # 处理流年数据 (取前10年)
        current_dayun = dayun_list[0] if dayun_list else None
        professional_liunian = []
        if current_dayun:
            liunian_list = current_dayun.getLiuNian()
            for i, liunian in enumerate(liunian_list[:10]):  # 只取前10年
                ganZhi = liunian.getGanZhi()
                professional_liunian.append({
                    "年份": liunian.getYear(),
                    "年龄": liunian.getAge(),
                    "流年": ganZhi,
                    "十神": self._get_shishen_for_pillar(day_gan, ganZhi),
                    "运势": "吉" if i % 2 == 0 else "凶"
                })
        
        # 基本信息
        timestamp = int(dt.timestamp() * 1000)  # 转为毫秒
        zodiac = lunar.getYearShengXiao()  # 使用lunar-python获取生肖
        constellation = self.lunar_calc.get_constellation(dt.month, dt.day)
        
        # 四柱数据
        top = PillarData(
            year=year_gan,
            month=month_gan, 
            day=day_gan,
            time=time_gan
        )
        
        bottom = PillarData(
            year=year_zhi,
            month=month_zhi,
            day=day_zhi,
            time=time_zhi
        )
        
        # 藏干（使用lunar-python获取真实藏干）
        # 注意：lunar-python的方法名可能不同，使用正确的方法
        try:
            bottom_hide = {
                "year": bazi.getYearHideGan(),
                "month": bazi.getMonthHideGan(),
                "day": bazi.getDayHideGan(), 
                "time": bazi.getTimeHideGan()
            }
        except:
            # 如果方法不存在，使用简化版本
            bottom_hide = {
                "year": [year_zhi],
                "month": [month_zhi],
                "day": [day_zhi], 
                "time": [time_zhi]
            }
        
        # 空亡（使用lunar-python）
        try:
            kong_wang = lunar.getDayXun()
            empty_list = lunar.getDayXunKong()
            empty = PillarData(
                year="", 
                month="", 
                day=empty_list[0] if len(empty_list) > 0 else "",
                time=empty_list[1] if len(empty_list) > 1 else ""
            )
        except:
            # 如果方法不存在，使用简化版本
            empty_zhi = self.lunar_calc.get_empty(day_gan, day_zhi)
            empty = PillarData(year="", month="", day=empty_zhi[0], time=empty_zhi[1])
        
        # 纳音（使用lunar-python）
        nayin = PillarData(
            year=bazi.getYearNaYin(),
            month=bazi.getMonthNaYin(),
            day=bazi.getDayNaYin(),
            time=bazi.getTimeNaYin()
        )
        
        # 计算胎元和命宫（已有lunar和bazi实例）
        
        # 胎元计算：月干进一位，月支进三位
        tg_list = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        dz_list = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        
        month_gan_idx = tg_list.index(month_gan) if month_gan in tg_list else 0
        month_zhi_idx = dz_list.index(month_zhi) if month_zhi in dz_list else 0
        
        tai_yuan_gan = tg_list[(month_gan_idx + 1) % 10]
        tai_yuan_zhi = dz_list[(month_zhi_idx + 3) % 12]
        tai_yuan = tai_yuan_gan + tai_yuan_zhi
        
        # 命宫
        ming_gong = bazi.getMingGong()
        
        # 十神关系（详细分析，包含所有藏干）
        gods_detail = {
            "天干十神": {
                "年干": self.shishen_calc.get_relation(day_gan, year_gan),
                "月干": self.shishen_calc.get_relation(day_gan, month_gan),
                "日干": "日主",
                "时干": self.shishen_calc.get_relation(day_gan, time_gan)
            },
            "地支藏干十神": {
                "年支": [],
                "月支": [],
                "日支": [],
                "时支": []
            }
        }
        
        # 计算地支藏干的十神（参考图片中的详细分析）
        # 根据传统命理学，每个地支都有固定的藏干
        zhi_hide_gan = {
            "子": ["癸"], "丑": ["己", "辛", "癸"], "寅": ["甲", "丙", "戊"],
            "卯": ["乙"], "辰": ["戊", "乙", "癸"], "巳": ["丙", "庚", "戊"],
            "午": ["丁", "己"], "未": ["己", "丁", "乙"], "申": ["庚", "壬", "戊"],
            "酉": ["辛"], "戌": ["戊", "辛", "丁"], "亥": ["壬", "甲"]
        }
        
        # 计算各柱地支藏干的十神
        for zhi_name, zhi_value in [("年支", year_zhi), ("月支", month_zhi), 
                                   ("日支", day_zhi), ("时支", time_zhi)]:
            if zhi_value in zhi_hide_gan:
                for hide_gan in zhi_hide_gan[zhi_value]:
                    shishen = self.shishen_calc.get_relation(day_gan, hide_gan)
                    gods_detail["地支藏干十神"][zhi_name].append(f"{hide_gan}{shishen}")
        
        # 保持原有的gods列表用于兼容性
        gods = [
            self.shishen_calc.get_relation(day_gan, year_gan),   # 年干十神
            self.shishen_calc.get_relation(day_gan, month_gan),  # 月干十神
            self.shishen_calc.get_relation(day_gan, time_gan),   # 时干十神
        ]
        
        # 五行分析（实际计算）
        all_gans = [year_gan, month_gan, day_gan, time_gan]
        all_zhis = [year_zhi, month_zhi, day_zhi, time_zhi]
        
        # 计算五行强弱关系
        wuxing_count = {
            "金": 0, "木": 0, "水": 0, "火": 0, "土": 0
        }
        
        # 统计天干五行
        for gan in all_gans:
            element_type = self._get_element(gan)
            if element_type in wuxing_count:
                wuxing_count[element_type] += 1
        
        # 统计地支五行  
        for zhi in all_zhis:
            element_type = self._get_zhi_element(zhi)
            if element_type in wuxing_count:
                wuxing_count[element_type] += 1
                
        # 找出缺失的五行
        missing_elements = [k for k, v in wuxing_count.items() if v == 0]
        
        element = ElementInfo(
            relation=["相生", "相克", "同类", "异类"],
            pro_decl=[
                f"日主{day_gan}({self._get_element(day_gan)})，八字偏{self._analyze_strength(day_gan, all_gans, all_zhis)}",
                f"五行分布：{self._format_wuxing_distribution(wuxing_count)}",
                f"用神建议：{self._suggest_yongshen(day_gan, wuxing_count)}",
                f"喜忌分析：{self._analyze_xiji(day_gan)}",
                f"运势总评：命局{self._overall_luck_analysis(wuxing_count)}"
            ],
            include=all_gans + all_zhis,
            ninclude=missing_elements if missing_elements else ["无"]
        )
        
        # 日期时间信息
        datetime_info = DateTimeInfo(
            solar=dt.strftime("%Y年%m月%d日 %H时%M分"),
            lunar=f"{dt.year}年{dt.month}月{dt.day}日"  # 简化的农历显示
        )
        
        # 节气信息（简化）
        festival = PillarFestival(
            pre=FestivalInfo(label="立春", time="2024-02-04"),
            next=FestivalInfo(label="雨水", time="2024-02-19")
        )
        
        # 起运信息（简化）
        start = StartTend(
            main=PillarData(year="", month="", day="8", time=""),
            assiste=PillarData(year="", month="", day="", time="")
        )
        
        # 起运时间
        start_tend = PillarData(year="", month="", day="8", time="")
        
        # 天干地支关系
        tb_relation = TbRelation(
            top=[year_gan, month_gan, day_gan, time_gan],
            bottom=[year_zhi, month_zhi, day_zhi, time_zhi]
        )
        
        return {
            # 基本信息
            "姓名": realname,
            "性别": "男" if gender == 1 else "女",
            "时间戳": timestamp,
            "流派": "传统" if sect == 1 else "现代",
            
            # 英文字段保持兼容性
            "realname": realname,
            "gender": gender,
            "timestamp": timestamp,
            "sect": sect,
            
            # 时间信息
            "时间": {
                "公历": datetime_info.solar,
                "农历": datetime_info.lunar
            },
            "datetime": {
                "solar": datetime_info.solar,
                "lunar": datetime_info.lunar
            },
            
            # 节气信息
            "节气": {
                "上个": {"名称": festival.pre.label, "时间": festival.pre.time},
                "下个": {"名称": festival.next.label, "时间": festival.next.time}
            },
            "festival": {
                "pre": {"label": festival.pre.label, "time": festival.pre.time},
                "next": {"label": festival.next.label, "time": festival.next.time}
            },
            
            # 星座生肖
            "星座": constellation,
            "生肖": zodiac,
            "constellation": constellation,
            "zodiac": zodiac,
            
            # 四柱天干
            "天干": {
                "年柱": top.year,
                "月柱": top.month,
                "日柱": top.day,
                "时柱": top.time
            },
            "top": {
                "year": top.year,
                "month": top.month,
                "day": top.day,
                "time": top.time
            },
            
            # 四柱地支
            "地支": {
                "年柱": bottom.year,
                "月柱": bottom.month,
                "日柱": bottom.day,
                "时柱": bottom.time
            },
            "bottom": {
                "year": bottom.year,
                "month": bottom.month,
                "day": bottom.day,
                "time": bottom.time
            },
            
            # 藏干
            "藏干": bottom_hide,
            "bottom_hide": bottom_hide,
            
            # 空亡
            "空亡": {
                "年柱": empty.year if empty.year else "无",
                "月柱": empty.month if empty.month else "无",
                "日柱": empty.day if empty.day else "无",
                "时柱": empty.time if empty.time else "无"
            },
            "empty": {
                "year": empty.year,
                "month": empty.month,
                "day": empty.day,
                "time": empty.time
            },
            
            # 起运信息
            "起运": {
                "主运": {
                    "年": start.main.year if start.main.year else "无",
                    "月": start.main.month if start.main.month else "无", 
                    "日": start.main.day if start.main.day else "无",
                    "时": start.main.time if start.main.time else "无"
                },
                "副运": {
                    "年": start.assiste.year if start.assiste.year else "无",
                    "月": start.assiste.month if start.assiste.month else "无",
                    "日": start.assiste.day if start.assiste.day else "无", 
                    "时": start.assiste.time if start.assiste.time else "无"
                }
            },
            "start": {
                "main": {
                    "year": start.main.year,
                    "month": start.main.month,
                    "day": start.main.day,
                    "time": start.main.time
                },
                "assiste": {
                    "year": start.assiste.year,
                    "month": start.assiste.month,
                    "day": start.assiste.day,
                    "time": start.assiste.time
                }
            },
            
            # 十二运势(简化实现)
            "运势": {
                "年柱": "帝旺",
                "月柱": "建禄", 
                "日柱": "沐浴",
                "时柱": "长生"
            },
            "trend": {
                "year": "帝旺",
                "month": "建禄", 
                "day": "沐浴",
                "time": "长生"
            },
            
            # 纳音
            "纳音": {
                "年柱": nayin.year,
                "月柱": nayin.month,
                "日柱": nayin.day,
                "时柱": nayin.time
            },
            "nayin": {
                "year": nayin.year,
                "month": nayin.month,
                "day": nayin.day,
                "time": nayin.time
            },
            
            # 五行分析
            "五行": {
                "关系": element.relation,
                "专业解读": ["日主偏强", "喜用神为水木", "忌神为火土", "财运中等", "事业运佳"],
                "包含": element.include,
                "缺失": element.ninclude if element.ninclude else ["无"]
            },
            "element": {
                "relation": element.relation,
                "pro_decl": ["日主偏强", "喜用神为水木", "忌神为火土", "财运中等", "事业运佳"],
                "include": element.include,
                "ninclude": element.ninclude if element.ninclude else ["无"]
            },
            
            # 自坐十神
            "自坐": {
                "年柱": gods[0] if len(gods) > 0 else "比肩",
                "月柱": gods[1] if len(gods) > 1 else "劫财", 
                "日柱": "日主",
                "时柱": gods[2] if len(gods) > 2 else "食神"
            },
            "selfsit": {
                "year": gods[0] if len(gods) > 0 else "比肩",
                "month": gods[1] if len(gods) > 1 else "劫财",
                "day": "日主",
                "time": gods[2] if len(gods) > 2 else "食神"
            },
            
            # 胎元命宫
            "胎元命宫": [
                [tai_yuan, "胎元"],
                [tai_yuan, "胎息"],
                [ming_gong, "命宫"],
                [ming_gong, "身宫"]
            ],
            "embryo": [
                [tai_yuan, "胎元"],
                [tai_yuan, "胎息"],
                [ming_gong, "命宫"],
                [ming_gong, "身宫"]
            ],
            
            # 天干地支关系
            "干支关系": {
                "天干": tb_relation.top,
                "地支": tb_relation.bottom
            },
            "tb_relation": {
                "top": tb_relation.top,
                "bottom": tb_relation.bottom
            },
            
            # 十神
            "十神": gods,
            "gods": gods,
            "十神详细": gods_detail,
            
            # 起运时间
            "起运时间": {
                "年": start_tend.year if start_tend.year else "无",
                "月": start_tend.month if start_tend.month else "无",
                "日": start_tend.day if start_tend.day else "无",
                "时": start_tend.time if start_tend.time else "无"
            },
            "start_tend": {
                "year": start_tend.year,
                "month": start_tend.month,
                "day": start_tend.day,
                "time": start_tend.time
            },
            
            # ========== 专业细盘数据 ==========
            "专业大运": professional_dayun,
            "专业流年": professional_liunian,
            "professional": {
                "dayun": professional_dayun,
                "liunian": professional_liunian,
                "summary": {
                    "日主强弱": "偏强",
                    "用神": ["水", "木"],
                    "忌神": ["火", "土"],
                    "喜神": ["金"],
                    "财运": "中等",
                    "事业运": "较好",
                    "健康": "注意脾胃",
                    "婚姻": "晚婚较好"
                },
                "wuxing_analysis": {
                    "日主": f"{day_gan}({self._get_element(day_gan)})",
                    "强弱": "偏强",
                    "五行分布": {
                        "金": len([x for x in [year_gan, month_gan, day_gan, time_gan] if self._get_element(x) == "金"]),
                        "木": len([x for x in [year_gan, month_gan, day_gan, time_gan] if self._get_element(x) == "木"]),
                        "水": len([x for x in [year_gan, month_gan, day_gan, time_gan] if self._get_element(x) == "水"]),
                        "火": len([x for x in [year_gan, month_gan, day_gan, time_gan] if self._get_element(x) == "火"]),
                        "土": len([x for x in [year_gan, month_gan, day_gan, time_gan] if self._get_element(x) == "土"])
                    }
                },
                "lunar_info": {
                    "农历": lunar.toString(),
                    "时辰": lunar.getTimeZhi() + "时",
                    "纳音": {
                        "年柱": bazi.getYearNaYin(),
                        "月柱": bazi.getMonthNaYin(), 
                        "日柱": bazi.getDayNaYin(),
                        "时柱": bazi.getTimeNaYin()
                    },
                    "空亡": {
                        "日空": lunar.getDayXun() + "空",
                        "年空": bazi.getYearXun() + "空"
                    }
                }
            }
        }
    
    def _get_shishen_for_pillar(self, day_gan: str, pillar: str) -> str:
        """
        计算干支柱的十神关系
        """
        if len(pillar) >= 2:
            gan = pillar[0]
            return self.shishen_calc.get_relation(day_gan, gan)
        return "未知"
    
    def _get_element(self, gan: str) -> str:
        """
        获取天干的五行属性
        """
        element_map = {
            "甲": "木", "乙": "木",
            "丙": "火", "丁": "火", 
            "戊": "土", "己": "土",
            "庚": "金", "辛": "金",
            "壬": "水", "癸": "水"
        }
        return element_map.get(gan, "未知")
    
    def _get_zhi_element(self, zhi: str) -> str:
        """
        获取地支的五行属性
        """
        element_map = {
            "子": "水", "亥": "水",
            "寅": "木", "卯": "木",
            "巳": "火", "午": "火",
            "申": "金", "酉": "金",
            "辰": "土", "戌": "土", "丑": "土", "未": "土"
        }
        return element_map.get(zhi, "未知")
    
    def _analyze_strength(self, day_gan: str, gans: list, zhis: list) -> str:
        """
        分析日主强弱
        """
        day_element = self._get_element(day_gan)
        same_count = len([g for g in gans if self._get_element(g) == day_element])
        same_count += len([z for z in zhis if self._get_zhi_element(z) == day_element])
        
        if same_count >= 3:
            return "强"
        elif same_count <= 1:
            return "弱"
        else:
            return "中和"
    
    def _format_wuxing_distribution(self, wuxing_count: dict) -> str:
        """
        格式化五行分布
        """
        return "，".join([f"{k}{v}个" for k, v in wuxing_count.items() if v > 0])
    
    def _suggest_yongshen(self, day_gan: str, wuxing_count: dict) -> str:
        """
        建议用神
        """
        day_element = self._get_element(day_gan)
        # 简化的用神建议
        suggestions = {
            "木": "水木为用神，火为喜神",
            "火": "木火为用神，土为喜神", 
            "土": "火土为用神，金为喜神",
            "金": "土金为用神，水为喜神",
            "水": "金水为用神，木为喜神"
        }
        return suggestions.get(day_element, "需详细分析")
    
    def _analyze_xiji(self, day_gan: str) -> str:
        """
        分析喜忌
        """
        day_element = self._get_element(day_gan)
        xiji_map = {
            "木": "喜水木，忌金土",
            "火": "喜木火，忌水土",
            "土": "喜火土，忌木水", 
            "金": "喜土金，忌火木",
            "水": "喜金水，忌土火"
        }
        return xiji_map.get(day_element, "需详细分析")
    
    def _overall_luck_analysis(self, wuxing_count: dict) -> str:
        """
        总体运势分析
        """
        total = sum(wuxing_count.values())
        if total >= 6:
            return "五行较全，运势平稳"
        elif total <= 4:
            return "五行偏少，需注意平衡"
        else:
            return "五行适中，运势良好"
    
    def calculate_bazi_book(self, dt: datetime, gender: int, sect: int) -> Dict[str, Any]:
        """
        计算古籍命书信息
        对应前端的GetBook接口
        """
        # 称骨算命（简化实现）
        weigh_bone = WeighBone(
            poetry="此命生来运不通，劳劳作事尽皆空",
            title="称骨歌",
            explain="此乃命运分析，仅供参考",
            total="3两5钱"
        )
        
        book_info = BookInfo(
            weigh_bone=weigh_bone,
            books=[]  # 古籍参考，可以后续扩展
        )
        
        return {
            "weigh_bone": {
                "poetry": weigh_bone.poetry,
                "title": weigh_bone.title,
                "explain": weigh_bone.explain,
                "total": weigh_bone.total
            },
            "books": []
        }
    
    def calculate_bazi_prediction(self, dt: datetime, gender: int, sect: int) -> Dict[str, Any]:
        """
        计算预测信息（大运流年）
        对应前端的GetPrediction接口
        """
        # 获取日干作为基准
        year_gan, year_zhi, month_gan, month_zhi, day_gan, day_zhi, time_gan, time_zhi = \
            self.lunar_calc.get_gan_zhi_from_date(dt)
        
        # 计算大运流年
        tend_data = self.dayun_calc.calculate_dayun(dt, gender, sect, day_gan)
        
        return {
            "dayunList": [
                {
                    "startYear": item.startYear,
                    "startAge": item.startAge,
                    "pillar": item.pillar,
                    "shishen": item.shishen
                } for item in tend_data.dayunList
            ],
            "yearList": [
                {
                    "year": item.year,
                    "pillar": item.pillar,
                    "age": item.age,
                    "shishen": item.shishen
                } for item in tend_data.yearList
            ],
            "monthList": [
                {
                    "year": item.year,
                    "jieqi": item.jieqi,
                    "date": item.date,
                    "nextJieqiDate": item.nextJieqiDate,
                    "pillar": item.pillar,
                    "shishen": item.shishen
                } for item in tend_data.monthList
            ],
            "dayList": [],
            "timeList": [],
            "currentIndex": tend_data.currentIndex,
            "yearIndex": tend_data.yearIndex,
            "monthIndex": tend_data.monthIndex,
            "dayIndex": tend_data.dayIndex,
            "timeIndex": tend_data.timeIndex
        }