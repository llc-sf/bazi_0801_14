"""
数据模型定义
基于8Char-Uni-App-master的数据结构设计
"""

from pydantic import BaseModel, Field, conint
from typing import Optional, List, Dict, Any, Union
from datetime import datetime

class BaziRequest(BaseModel):
    """原有的八字请求模型（兼容性）"""
    name: str
    city: str
    gender: Optional[str] = "男"
    year: conint(ge=1900, le=2100)
    month: conint(ge=1, le=12)
    day: conint(ge=1, le=31)
    hour: conint(ge=0, le=23)
    minute: conint(ge=0, le=59) = 0

class BaziResponse(BaseModel):
    """八字响应模型"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

# 四柱数据结构
class PillarData(BaseModel):
    """四柱数据"""
    year: str = ""
    month: str = ""
    day: str = ""
    time: str = ""

class DateTimeInfo(BaseModel):
    """日期时间信息"""
    solar: str = ""
    lunar: str = ""

class FestivalInfo(BaseModel):
    """节气信息"""
    label: str = ""
    time: str = ""

class PillarFestival(BaseModel):
    """四柱节气"""
    pre: FestivalInfo
    next: FestivalInfo

class ElementInfo(BaseModel):
    """五行信息"""
    relation: List[str] = []
    pro_decl: List[str] = Field(default_factory=lambda: [""] * 5)
    include: List[str] = []
    ninclude: List[str] = []

class TbRelation(BaseModel):
    """天干地支关系"""
    top: List[str] = []
    bottom: List[str] = []

class StartTend(BaseModel):
    """起运信息"""
    main: PillarData
    assiste: PillarData

class WeighBone(BaseModel):
    """称骨算命"""
    poetry: Optional[str] = None
    title: Optional[str] = None
    explain: Optional[str] = None
    total: Optional[str] = None

class BookInfo(BaseModel):
    """古籍信息"""
    weigh_bone: WeighBone
    books: List[Dict[str, Any]] = []

# 大运流年数据结构
class DayunItem(BaseModel):
    """大运项"""
    startYear: int
    startAge: int
    pillar: str
    shishen: str

class YearItem(BaseModel):
    """流年项"""
    year: int
    pillar: str
    age: int
    shishen: str

class MonthItem(BaseModel):
    """流月项"""
    year: int
    jieqi: str
    date: str
    nextJieqiDate: str
    pillar: str
    shishen: str

class DayItem(BaseModel):
    """流日项"""
    date: str
    nongli: str
    top: str
    bottom: str
    pillar: str
    shishen: str

class TimeItem(BaseModel):
    """流时项"""
    top: str
    bottom: str
    pillar: str
    time: str
    shishen: str

class TendData(BaseModel):
    """大运数据"""
    dayunList: List[DayunItem] = []
    yearList: List[YearItem] = []
    monthList: List[MonthItem] = []
    dayList: List[DayItem] = []
    timeList: List[TimeItem] = []
    currentIndex: int = 0
    yearIndex: int = 0
    monthIndex: int = 0
    dayIndex: int = 0
    timeIndex: int = 0

class BaziInfoResponse(BaseModel):
    """八字信息完整响应"""
    realname: str
    gender: int
    timestamp: int
    sect: int
    datetime: DateTimeInfo
    festival: PillarFestival
    constellation: str
    zodiac: str
    top: PillarData        # 天干
    bottom: PillarData     # 地支
    bottom_hide: Dict[str, List[str]]  # 藏干
    empty: PillarData      # 空亡
    start: StartTend       # 起运
    trend: PillarData      # 星运
    nayin: PillarData      # 纳音
    element: ElementInfo   # 五行
    selfsit: PillarData    # 自坐
    embryo: List[List[List[str]]]  # 胎元
    tb_relation: TbRelation        # 天干地支关系
    gods: List[str]        # 神煞
    start_tend: PillarData # 起运时间

# 常量定义（从前端移植）
class Constants:
    """常量定义"""
    
    # 十神映射（对应前端的SHI_SHEN_ZHI）
    SHI_SHEN_ZHI = {
        "甲子":"正印","甲丑":"正财","甲寅":"比肩","甲卯":"劫财","甲辰":"偏财","甲巳":"食神",
        "甲午":"伤官","甲未":"正财","甲申":"七杀","甲酉":"正官","甲戌":"偏财","甲亥":"偏印",
        "乙子":"偏印","乙丑":"偏财","乙寅":"劫财","乙卯":"比肩","乙辰":"正财","乙巳":"伤官",
        "乙午":"食神","乙未":"偏财","乙申":"正官","乙酉":"七杀","乙戌":"正财","乙亥":"正印",
        "丙子":"正官","丙丑":"伤官","丙寅":"偏印","丙卯":"正印","丙辰":"食神","丙巳":"比肩",
        "丙午":"劫财","丙未":"伤官","丙申":"偏财","丙酉":"正财","丙戌":"食神","丙亥":"七杀",
        "丁子":"七杀","丁丑":"食神","丁寅":"正印","丁卯":"偏印","丁辰":"伤官","丁巳":"劫财",
        "丁午":"比肩","丁未":"食神","丁申":"正财","丁酉":"偏财","丁戌":"伤官","丁亥":"正官",
        "戊子":"正财","戊丑":"劫财","戊寅":"七杀","戊卯":"正官","戊辰":"比肩","戊巳":"偏印",
        "戊午":"正印","戊未":"劫财","戊申":"食神","戊酉":"伤官","戊戌":"比肩","戊亥":"偏财",
        "己子":"偏财","己丑":"比肩","己寅":"正官","己卯":"七杀","己辰":"劫财","己巳":"正印",
        "己午":"偏印","己未":"比肩","己申":"伤官","己酉":"食神","己戌":"劫财","己亥":"正财",
        "庚子":"伤官","庚丑":"正印","庚寅":"偏财","庚卯":"正财","庚辰":"偏印","庚巳":"七杀",
        "庚午":"正官","庚未":"正印","庚申":"比肩","庚酉":"劫财","庚戌":"偏印","庚亥":"食神",
        "辛子":"食神","辛丑":"偏印","辛寅":"正财","辛卯":"偏财","辛辰":"正印","辛巳":"正官",
        "辛午":"七杀","辛未":"偏印","辛申":"劫财","辛酉":"比肩","辛戌":"正印","辛亥":"伤官",
        "壬子":"劫财","壬丑":"正官","壬寅":"食神","壬卯":"伤官","壬辰":"七杀","壬巳":"偏财",
        "壬午":"正财","壬未":"正官","壬申":"偏印","壬酉":"正印","壬戌":"七杀","壬亥":"比肩",
        "癸子":"比肩","癸丑":"七杀","癸寅":"伤官","癸卯":"食神","癸辰":"正官","癸巳":"正财",
        "癸午":"偏财","癸未":"七杀","癸申":"正印","癸酉":"偏印","癸戌":"正官","癸亥":"劫财"
    }
    
    # 十神简化（对应前端的SHI_SHEN_SIMPLIFIE）
    SHI_SHEN_SIMPLIFIE = {
        "正印":"印","正官":"官","劫财":"劫","伤官":"伤","正财":"财",
        "七杀":"杀","偏印":"枭","比肩":"比","食神":"食","偏财":"才"
    }
    
    # 长生偏移（对应前端的CHANG_SHENG_OFFSET）
    CHANG_SHENG_OFFSET = {
        "甲":1,"丙":10,"戊":10,"庚":7,"壬":4,
        "乙":6,"丁":9,"己":9,"辛":0,"癸":3
    }
    
    # 太岁关系（对应前端的TAISUI_RELATION）
    TAISUI_RELATION = {
        "子子":"值太岁","丑丑":"值太岁","寅寅":"值太岁","卯卯":"值太岁","巳巳":"值太岁",
        "未未":"值太岁","申申":"值太岁","戌戌":"值太岁","子卯":"刑太岁","丑戌":"刑太岁(丑戌未三刑)",
        "辰辰":"刑太岁(值)","午午":"刑太岁(值)","酉酉":"刑太岁(值)","亥亥":"刑太岁(值)",
        "子午":"冲太岁","卯酉":"冲太岁","寅申":"冲太岁(寅巳申三刑)","巳亥":"冲太岁",
        "辰戌":"冲太岁","丑未":"冲太岁(丑戌未三刑)","子未":"害太岁","丑午":"害太岁",
        "寅巳":"害太岁(寅巳申三刑)","卯辰":"害太岁","申亥":"害太岁","酉戌":"害太岁",
        "子酉":"破太岁","卯午":"破太岁","辰丑":"破太岁","寅亥":"破太岁",
        "巳申":"破太岁(寅巳申三刑)","未戌":"破太岁(丑戌未三刑)"
    }
    
    # 五行信息
    ELEMENT = {
        "labels": ['金', '木', '水', '火', '土'],
        "types": ['warning', 'success', 'primary', 'error', 'steady'],
        "colors": ["#ff9900", "#19be6b", "#2979ff", "#fa3534", "#795548"]
    }
    
    # 四柱字段
    PILLAR_FIELD = ["year", "month", "day", "time"]
    
    # 天干地支
    TIAN_GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    DI_ZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]