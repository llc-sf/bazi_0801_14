# -*- encoding:utf-8 -*- 

import sxtwl, json
from datetime import datetime, timedelta
from math import radians, sin, cos
import math
from collections import OrderedDict
from bidict import bidict
from lunar_python import Solar, Lunar

# 基础表
TG  = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
DZ  = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
ELE = dict(zip(TG, ["木", "木", "火", "火", "土", "土", "金", "金", "水", "水"]))

# 地支五行属性
DZ_ELE = dict(zip(DZ, ["水", "土", "木", "木", "土", "火", "火", "土", "金", "金", "土", "水"]))

# 地支藏干（主气、中气、余气）
DZ_CANG_GAN = {
    "子": OrderedDict({"癸": 8}),
    "丑": OrderedDict({"己": 5, "癸": 2, "辛": 1}),
    "寅": OrderedDict({"甲": 5, "丙": 2, "戊": 1}),
    "卯": OrderedDict({"乙": 8}),
    "辰": OrderedDict({"戊": 5, "乙": 2, "癸": 1}),
    "巳": OrderedDict({"丙": 5, "戊": 2, "庚": 1}),
    "午": OrderedDict({"丁": 5, "己": 3}),
    "未": OrderedDict({"己": 5, "丁": 2, "乙": 1}),
    "申": OrderedDict({"庚": 5, "壬": 2, "戊": 1}),
    "酉": OrderedDict({"辛": 8}),
    "戌": OrderedDict({"戊": 5, "辛": 2, "丁": 1}),
    "亥": OrderedDict({"壬": 5, "甲": 3})
}

# 十神名称
SHEN = ["比肩", "劫财", "食神", "伤官", "偏财", "正财", "七杀", "正官", "偏印", "正印"]

# 完整的十神映射关系（基于传统命理学）
TEN_DEITIES = {
    '甲': bidict({
        '甲': '比', '乙': '劫', '丙': '食', '丁': '伤', '戊': '才',
        '己': '财', '庚': '杀', '辛': '官', '壬': '枭', '癸': '印',
        '子': '沐', '丑': '冠', '寅': '建', '卯': '帝', '辰': '衰',
        '巳': '病', '午': '死', '未': '墓', '申': '绝', '酉': '胎',
        '戌': '养', '亥': '长', '库': '未_', '本': '木', '克': '土',
        '被克': '金', '生我': '水', '生': '火', '合': '己', '冲': '庚'
    }),
    '乙': bidict({
        '甲': '劫', '乙': '比', '丙': '伤', '丁': '食', '戊': '财',
        '己': '才', '庚': '官', '辛': '杀', '壬': '印', '癸': '枭',
        '子': '病', '丑': '衰', '寅': '帝', '卯': '建', '辰': '冠',
        '巳': '沐', '午': '长', '未': '养', '申': '胎', '酉': '绝',
        '戌': '墓', '亥': '死', '库': '未_', '本': '木', '克': '土',
        '被克': '金', '生我': '水', '生': '火', '合': '庚', '冲': '辛'
    }),
    '丙': bidict({
        '丙': '比', '丁': '劫', '戊': '食', '己': '伤', '庚': '才',
        '辛': '财', '壬': '杀', '癸': '官', '甲': '枭', '乙': '印',
        '子': '胎', '丑': '养', '寅': '长', '卯': '沐', '辰': '冠',
        '巳': '建', '午': '帝', '未': '衰', '申': '病', '酉': '死',
        '戌': '墓', '亥': '绝', '库': '戌_', '本': '火', '克': '金',
        '被克': '水', '生我': '木', '生': '土', '合': '辛', '冲': '壬'
    }),
    '丁': bidict({
        '丙': '劫', '丁': '比', '戊': '伤', '己': '食', '庚': '财',
        '辛': '才', '壬': '官', '癸': '杀', '甲': '印', '乙': '枭',
        '子': '绝', '丑': '墓', '寅': '死', '卯': '病', '辰': '衰',
        '巳': '帝', '午': '建', '未': '冠', '申': '沐', '酉': '长',
        '戌': '养', '亥': '胎', '库': '戌_', '本': '火', '克': '金',
        '被克': '水', '生我': '木', '生': '土', '合': '壬', '冲': '癸'
    }),
    '戊': bidict({
        '戊': '比', '己': '劫', '庚': '食', '辛': '伤', '壬': '才',
        '癸': '财', '甲': '杀', '乙': '官', '丙': '枭', '丁': '印',
        '子': '胎', '丑': '养', '寅': '长', '卯': '沐', '辰': '冠',
        '巳': '建', '午': '帝', '未': '衰', '申': '病', '酉': '死',
        '戌': '墓', '亥': '绝', '库': '辰_', '本': '土', '克': '水',
        '被克': '木', '生我': '火', '生': '金', '合': '癸', '冲': ''
    }),
    '己': bidict({
        '戊': '劫', '己': '比', '庚': '伤', '辛': '食', '壬': '财',
        '癸': '才', '甲': '官', '乙': '杀', '丙': '印', '丁': '枭',
        '子': '绝', '丑': '墓', '寅': '死', '卯': '病', '辰': '衰',
        '巳': '帝', '午': '建', '未': '冠', '申': '沐', '酉': '长',
        '戌': '养', '亥': '胎', '库': '辰_', '本': '土', '克': '水',
        '被克': '木', '生我': '火', '生': '金', '合': '甲', '冲': ''
    }),
    '庚': bidict({
        '庚': '比', '辛': '劫', '壬': '食', '癸': '伤', '甲': '才',
        '乙': '财', '丙': '杀', '丁': '官', '戊': '枭', '己': '印',
        '子': '死', '丑': '墓', '寅': '绝', '卯': '胎', '辰': '养',
        '巳': '长', '午': '沐', '未': '冠', '申': '建', '酉': '帝',
        '戌': '衰', '亥': '病', '库': '丑_', '本': '金', '克': '木',
        '被克': '火', '生我': '土', '生': '水', '合': '乙', '冲': '甲'
    }),
    '辛': bidict({
        '庚': '劫', '辛': '比', '壬': '伤', '癸': '食', '甲': '财',
        '乙': '才', '丙': '官', '丁': '杀', '戊': '印', '己': '枭',
        '子': '长', '丑': '养', '寅': '胎', '卯': '绝', '辰': '墓',
        '巳': '死', '午': '病', '未': '衰', '申': '帝', '酉': '建',
        '戌': '冠', '亥': '沐', '库': '丑_', '本': '金', '克': '木',
        '被克': '火', '生我': '土', '生': '水', '合': '丙', '冲': '乙'
    }),
    '壬': bidict({
        '壬': '比', '癸': '劫', '甲': '食', '乙': '伤', '丙': '才',
        '丁': '财', '戊': '杀', '己': '官', '庚': '枭', '辛': '印',
        '子': '帝', '丑': '衰', '寅': '病', '卯': '死', '辰': '墓',
        '巳': '绝', '午': '胎', '未': '养', '申': '长', '酉': '沐',
        '戌': '冠', '亥': '建', '库': '辰_', '本': '水', '克': '火',
        '被克': '土', '生我': '金', '生': '木', '合': '丁', '冲': '丙'
    }),
    '癸': bidict({
        '壬': '劫', '癸': '比', '甲': '伤', '乙': '食', '丙': '财',
        '丁': '才', '戊': '官', '己': '杀', '庚': '印', '辛': '枭',
        '子': '建', '丑': '冠', '寅': '沐', '卯': '长', '辰': '养',
        '巳': '胎', '午': '绝', '未': '墓', '申': '死', '酉': '病',
        '戌': '衰', '亥': '帝', '库': '辰_', '本': '水', '克': '火',
        '被克': '土', '生我': '金', '生': '木', '合': '戊', '冲': '丁'
    })
}

# 天干阴阳属性
YIN_YANG = dict(zip(TG, [True, False, True, False, True, False, True, False, True, False]))

# 地支阴阳属性
DZ_YIN_YANG = dict(zip(DZ, [True, False, True, False, True, False, True, False, True, False, True, False]))

# 五行生克关系
WU_XING_SHENG = {
    "木": "火", "火": "土", "土": "金", "金": "水", "水": "木"
}

WU_XING_KE = {
    "木": "土", "火": "金", "土": "水", "金": "木", "水": "火"
}

# 纳音五行
NAYINS = {
    ('甲', '子'): '海中金', ('乙', '丑'): '海中金', ('壬', '寅'): '金泊金', ('癸', '卯'): '金泊金',
    ('庚', '辰'): '白蜡金', ('辛', '巳'): '白蜡金', ('甲', '午'): '砂中金', ('乙', '未'): '砂中金',
    ('壬', '申'): '剑锋金', ('癸', '酉'): '剑锋金', ('庚', '戌'): '钗钏金', ('辛', '亥'): '钗钏金',
    ('戊', '子'): '霹雳火', ('己', '丑'): '霹雳火', ('丙', '寅'): '炉中火', ('丁', '卯'): '炉中火',
    ('甲', '辰'): '覆灯火', ('乙', '巳'): '覆灯火', ('戊', '午'): '天上火', ('己', '未'): '天上火',
    ('丙', '申'): '山下火', ('丁', '酉'): '山下火', ('甲', '戌'): '山头火', ('乙', '亥'): '山头火',
    ('壬', '子'): '桑柘木', ('癸', '丑'): '桑柘木', ('庚', '寅'): '松柏木', ('辛', '卯'): '松柏木',
    ('戊', '辰'): '大林木', ('己', '巳'): '大林木', ('壬', '午'): '杨柳木', ('癸', '未'): '杨柳木',
    ('庚', '申'): '石榴木', ('辛', '酉'): '石榴木', ('戊', '戌'): '平地木', ('己', '亥'): '平地木',
    ('庚', '子'): '壁上土', ('辛', '丑'): '壁上土', ('戊', '寅'): '城头土', ('己', '卯'): '城头土',
    ('丙', '辰'): '砂中土', ('丁', '巳'): '砂中土', ('庚', '午'): '路旁土', ('辛', '未'): '路旁土',
    ('戊', '申'): '大驿土', ('己', '酉'): '大驿土', ('丙', '戌'): '屋上土', ('丁', '亥'): '屋上土',
    ('丙', '子'): '涧下水', ('丁', '丑'): '涧下水', ('甲', '寅'): '大溪水', ('乙', '卯'): '大溪水',
    ('壬', '辰'): '长流水', ('癸', '巳'): '长流水', ('丙', '午'): '天河水', ('丁', '未'): '天河水',
    ('甲', '申'): '井泉水', ('乙', '酉'): '井泉水', ('壬', '戌'): '大海水', ('癸', '亥'): '大海水'
}

# 空亡计算
EMPTIES = {
    ('甲', '子'): ('戌', '亥'), ('乙', '丑'): ('戌', '亥'), 
    ('丙', '寅'): ('戌', '亥'), ('丁', '卯'): ('戌', '亥'), 
    ('戊', '辰'): ('戌', '亥'), ('己', '巳'): ('戌', '亥'),
    ('庚', '午'): ('戌', '亥'), ('辛', '未'): ('戌', '亥'),
    ('壬', '申'): ('戌', '亥'), ('癸', '酉'): ('戌', '亥'),

    ('甲', '戌'): ('申', '酉'), ('乙', '亥'): ('申', '酉'),
    ('丙', '子'): ('申', '酉'), ('丁', '丑'): ('申', '酉'),
    ('戊', '寅'): ('申', '酉'), ('己', '卯'): ('申', '酉'),
    ('庚', '辰'): ('申', '酉'), ('辛', '巳'): ('申', '酉'),
    ('壬', '午'): ('申', '酉'), ('癸', '未'): ('申', '酉'),

    ('甲', '申'): ('午', '未'), ('乙', '酉'): ('午', '未'),
    ('丙', '戌'): ('午', '未'), ('丁', '亥'): ('午', '未'),
    ('戊', '子'): ('午', '未'), ('己', '丑'): ('午', '未'), 
    ('庚', '寅'): ('午', '未'), ('辛', '卯'): ('午', '未'),
    ('壬', '辰'): ('午', '未'), ('癸', '巳'): ('午', '未'),

    ('甲', '午'): ('辰', '巳'), ('乙', '未'): ('辰', '巳'),
    ('丙', '申'): ('辰', '巳'), ('丁', '酉'): ('辰', '巳'),
    ('戊', '戌'): ('辰', '巳'), ('己', '亥'): ('辰', '巳'),
    ('庚', '子'): ('辰', '巳'), ('辛', '丑'): ('辰', '巳'),
    ('壬', '寅'): ('辰', '巳'), ('癸', '卯'): ('辰', '巳'),

    ('甲', '辰'): ('寅', '卯'), ('乙', '巳'): ('寅', '卯'),
    ('丙', '午'): ('寅', '卯'), ('丁', '未'): ('寅', '卯'),
    ('戊', '申'): ('寅', '卯'), ('己', '酉'): ('寅', '卯'),
    ('庚', '戌'): ('寅', '卯'), ('辛', '亥'): ('寅', '卯'),
    ('壬', '子'): ('寅', '卯'), ('癸', '丑'): ('寅', '卯'), 

    ('甲', '寅'): ('子', '丑'), ('乙', '卯'): ('子', '丑'),     
    ('丙', '辰'): ('子', '丑'), ('丁', '巳'): ('子', '丑'), 
    ('戊', '午'): ('子', '丑'), ('己', '未'): ('子', '丑'),
    ('庚', '申'): ('子', '丑'), ('辛', '酉'): ('子', '丑'), 
    ('壬', '戌'): ('子', '丑'), ('癸', '亥'): ('子', '丑'),    
}

# 地支关系
ZHI_ATTS = {
    "子": {"冲": "午", "刑": "卯", "被刑": "卯", "合": ("申", "辰"), "会": ("亥", "丑"), '害': '未', '破': '酉'},
    "丑": {"冲": "未", "刑": "戌", "被刑": "未", "合": ("巳", "酉"), "会": ("子", "亥"), '害': '午', '破': '辰'},
    "寅": {"冲": "申", "刑": "巳", "被刑": "申", "合": ("午", "戌"), "会": ("卯", "辰"), '害': '巳', '破': '亥'},
    "卯": {"冲": "酉", "刑": "子", "被刑": "子", "合": ("未", "亥"), "会": ("寅", "辰"), '害': '辰', '破': '午'},
    "辰": {"冲": "戌", "刑": "辰", "被刑": "辰", "合": ("子", "申"), "会": ("寅", "卯"), '害': '卯', '破': '丑'},
    "巳": {"冲": "亥", "刑": "申", "被刑": "寅", "合": ("酉", "丑"), "会": ("午", "未"), '害': '寅', '破': '申'},
    "午": {"冲": "子", "刑": "午", "被刑": "午", "合": ("寅", "戌"), "会": ("巳", "未"), '害': '丑', '破': '卯'},
    "未": {"冲": "丑", "刑": "丑", "被刑": "戌", "合": ("卯", "亥"), "会": ("巳", "午"), '害': '子', '破': '戌'},
    "申": {"冲": "寅", "刑": "寅", "被刑": "巳", "合": ("子", "辰"), "会": ("酉", "戌"), '害': '亥', '破': '巳'},
    "酉": {"冲": "卯", "刑": "酉", "被刑": "酉", "合": ("巳", "丑"), "会": ("申", "戌"), '害': '戌', '破': '子'},
    "戌": {"冲": "辰", "刑": "未", "被刑": "丑", "合": ("午", "寅"), "会": ("申", "酉"), '害': '酉', '破': '未'},
    "亥": {"冲": "巳", "刑": "亥", "被刑": "亥", "合": ("卯", "未"), "会": ("子", "丑"), '害': '申', '破': '寅'},
}

# 地支三合
ZHI_3HES = {"申子辰": "水", "巳酉丑": "金", "寅午戌": "火", "亥卯未": "木"}

# 地支六合
ZHI_6HES = {
    "子丑": "土", "寅亥": "木", "卯戌": "火", 
    "酉辰": "金", "申巳": "水", "未午": "土"
}

# 天干五合
GAN_HES = {
    ("甲", "己"): "土", ("乙", "庚"): "金", ("丙", "辛"): "水",
    ("丁", "壬"): "木", ("戊", "癸"): "火"
}

# 神煞数据
SHENSHA_DATA = {
    '天乙': {"甲": '未丑', "乙": "申子", "丙": "酉亥", "丁": "酉亥", "戊": '未丑', "己": "申子", 
             "庚": "未丑", "辛": "寅午", "壬": "卯巳", "癸": "卯巳"},
    '文昌': {"甲": '巳', "乙": "午", "丙": "申", "丁": "酉", "戊": "申", "己": "酉", 
             "庚": "亥", "辛": "子", "壬": "寅", "癸": "丑"},
    '将星': {"子": "子", "丑": "酉", "寅": "午", "卯": "卯", "辰": "子", "巳": "酉", 
             "午": "午", "未": "卯", "申": "子", "酉": "酉", "戌": "午", "亥": "卯"},
    '华盖': {"子": "辰", "丑": "丑", "寅": "戌", "卯": "未", "辰": "辰", "巳": "丑", 
             "午": "戌", "未": "未", "申": "辰", "酉": "丑", "戌": "戌", "亥": "未"},
    '驿马': {"子": "寅", "丑": "亥", "寅": "申", "卯": "巳", "辰": "寅", "巳": "亥", 
             "午": "申", "未": "巳", "申": "寅", "酉": "亥", "戌": "申", "亥": "巳"},
    '桃花': {"子": "酉", "丑": "午", "寅": "卯", "卯": "子", "辰": "酉", "巳": "午", 
             "午": "卯", "未": "子", "申": "酉", "酉": "午", "戌": "卯", "亥": "子"},
}

# 胎元、命宫计算相关
YUAN_GONG = {
    "子": "午", "丑": "未", "寅": "申", "卯": "酉", "辰": "戌", "巳": "亥",
    "午": "子", "未": "丑", "申": "寅", "酉": "卯", "戌": "辰", "亥": "巳"
}

# 城市经纬度数据
def parse_city_coordinates(file_path: str) -> dict:
    """从文件解析城市经纬度数据"""
    city_coordinates = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) < 4:
                    continue
                
                code = parts[0]
                name = parts[1]
                try:
                    lng = float(parts[2])
                    lat = float(parts[3])
                except ValueError:
                    continue
                
                city_coordinates[name] = (lng, lat)
                
                # 添加简化名称支持
                simplified_name = name
                for suffix in ['市', '省', '自治区', '特别行政区', '县', '区']:
                    if simplified_name.endswith(suffix):
                        simplified_name = simplified_name[:-len(suffix)]
                        city_coordinates[simplified_name] = (lng, lat)
                        break
    except FileNotFoundError:
        # 如果文件不存在，使用默认数据
        city_coordinates = {
            "北京": (116.40, 39.90), "上海": (121.47, 31.23),
            "广州": (113.23, 23.16), "深圳": (114.05, 22.52),
            "杭州": (120.19, 30.26), "南京": (118.78, 32.04),
            "武汉": (114.31, 30.52), "成都": (104.06, 30.67),
            "西安": (108.95, 34.27), "重庆": (106.54, 29.59)
        }
    
    return city_coordinates

# 计算真太阳时
def calculate_eot(date: datetime) -> float:
    """计算时差修正值(EoT) - 单位：分钟"""
    n = date.timetuple().tm_yday
    b = math.radians((n - 81) * 360 / 365.242)
    eot = 9.87 * math.sin(2*b) - 7.53 * math.cos(b) - 1.5 * math.sin(b)
    return eot

def true_solar_time(city_name: str, local_dt: datetime) -> datetime:
    """计算真太阳时"""
    city_coordinates = parse_city_coordinates("/app/app/data.txt")
    
    # 尝试精确匹配
    coordinates = city_coordinates.get(city_name)
    
    if not coordinates:
        # 尝试模糊匹配
        for city, coord in city_coordinates.items():
            if city_name in city or city in city_name:
                coordinates = coord
                break
    
    if not coordinates:
        # 使用北京作为默认
        coordinates = (116.40, 39.90)
    
    lon, lat = coordinates
    
    # 计算经度时差
    lon_diff = (120 - lon) * 4
    
    # 计算时差修正值
    eot = calculate_eot(local_dt)
    
    # 计算真太阳时
    total_correction = timedelta(minutes=(lon_diff + eot))
    return local_dt + total_correction

# 计算十神关系
def ten_shen(day_gan, target_gan):
    """使用完整的十神映射关系计算十神"""
    if day_gan not in TEN_DEITIES:
        return "未知"
    
    deities_map = TEN_DEITIES[day_gan]
    if target_gan in deities_map:
        return deities_map[target_gan]
    
    return "未知"

def ten_shen_dz(day_gan, target_dz):
    """根据地支藏干计算十神关系"""
    if target_dz not in DZ_CANG_GAN:
        return "未知"
    
    # 获取地支藏干主气
    target_gan = max(DZ_CANG_GAN[target_dz].items(), key=lambda x: x[1])[0]
    
    return ten_shen(day_gan, target_gan)

# 计算五行强弱
def calculate_wu_xing_strength(gans, zhis, day_gan):
    """计算五行强弱"""
    scores = {"金": 0, "木": 0, "水": 0, "火": 0, "土": 0}
    
    # 天干得分
    for gan in gans:
        scores[ELE[gan]] += 5
    
    # 地支得分（根据地支藏干）
    for zhi in zhis:
        for gan, weight in DZ_CANG_GAN[zhi].items():
            scores[ELE[gan]] += weight
    
    # 计算日主强弱
    day_ele = ELE[day_gan]
    day_score = scores[day_ele]
    
    # 判断强弱
    total_score = sum(scores.values())
    strength_ratio = day_score / total_score if total_score > 0 else 0
    
    if strength_ratio > 0.25:
        strength_level = "强"
    elif strength_ratio > 0.18:
        strength_level = "中等"
    else:
        strength_level = "弱"
    
    return {
        "五行得分": scores,
        "日主五行": day_ele,
        "日主得分": day_score,
        "强度等级": strength_level,
        "强度比例": f"{strength_ratio:.2%}"
    }

# 计算神煞
def calculate_shensha(gans, zhis, day_gan):
    """计算神煞"""
    shensha_list = []
    
    # 天乙贵人
    if day_gan in SHENSHA_DATA['天乙']:
        tianyi_positions = SHENSHA_DATA['天乙'][day_gan]
        for zhi in zhis:
            if zhi in tianyi_positions:
                shensha_list.append("天乙贵人")
    
    # 文昌贵人
    if day_gan in SHENSHA_DATA['文昌']:
        wenchang_position = SHENSHA_DATA['文昌'][day_gan]
        if wenchang_position in zhis:
            shensha_list.append("文昌贵人")
    
    # 将星
    jiangxing_position = SHENSHA_DATA['将星'].get(zhis[0])  # 年支
    if jiangxing_position in zhis:
        shensha_list.append("将星")
    
    # 华盖
    huagai_position = SHENSHA_DATA['华盖'].get(zhis[0])  # 年支
    if huagai_position in zhis:
        shensha_list.append("华盖")
    
    # 驿马
    yima_position = SHENSHA_DATA['驿马'].get(zhis[0])  # 年支
    if yima_position in zhis:
        shensha_list.append("驿马")
    
    # 桃花
    taohua_position = SHENSHA_DATA['桃花'].get(zhis[0])  # 年支
    if taohua_position in zhis:
        shensha_list.append("桃花")
    
    return list(set(shensha_list))  # 去重

# 计算地支关系
def calculate_zhi_relations(zhis):
    """计算地支之间的关系"""
    relations = []
    
    for i, zhi1 in enumerate(zhis):
        for j, zhi2 in enumerate(zhis):
            if i >= j:
                continue
            
            # 六合
            if zhi1 + zhi2 in ZHI_6HES:
                relations.append(f"{zhi1}{zhi2}六合({ZHI_6HES[zhi1+zhi2]})")
            elif zhi2 + zhi1 in ZHI_6HES:
                relations.append(f"{zhi1}{zhi2}六合({ZHI_6HES[zhi2+zhi1]})")
            
            # 相冲
            if ZHI_ATTS[zhi1].get("冲") == zhi2:
                relations.append(f"{zhi1}{zhi2}相冲")
            
            # 相刑
            if ZHI_ATTS[zhi1].get("刑") == zhi2:
                relations.append(f"{zhi1}{zhi2}相刑")
            
            # 相害
            if ZHI_ATTS[zhi1].get("害") == zhi2:
                relations.append(f"{zhi1}{zhi2}相害")
            
            # 相破
            if ZHI_ATTS[zhi1].get("破") == zhi2:
                relations.append(f"{zhi1}{zhi2}相破")
    
    # 检查三合
    for sanhe, element in ZHI_3HES.items():
        if all(zhi in zhis for zhi in sanhe):
            relations.append(f"{sanhe}三合{element}")
    
    return relations

# 计算纳音五行
def calculate_nayin(gan_zhi):
    """计算纳音五行"""
    gan, zhi = gan_zhi
    return NAYINS.get((gan, zhi), "未知")

# 计算空亡
def calculate_empty(gan_zhi):
    """计算空亡"""
    if gan_zhi in EMPTIES:
        return EMPTIES[gan_zhi]
    return []

# 计算大运
def get_next_gan_zhi(gan_zhi, direction=1):
    """获取下一个干支组合"""
    gan = gan_zhi[0]
    zhi = gan_zhi[1]
    
    gan_idx = TG.index(gan)
    zhi_idx = DZ.index(zhi)
    
    next_gan_idx = (gan_idx + direction) % 10
    next_zhi_idx = (zhi_idx + direction) % 12
    
    return TG[next_gan_idx] + DZ[next_zhi_idx]

def calc_da_yun(birth_year, month_gan_zhi, day_gan, gender):
    """计算大运"""
    # 判断年干阴阳
    year_gan = TG[(birth_year - 4) % 10]
    is_yang_year = YIN_YANG[year_gan]
    
    # 确定排运方向
    if (is_yang_year and gender == "男") or (not is_yang_year and gender == "女"):
        direction = 1  # 顺排
    else:
        direction = -1  # 逆排
    
    # 简化起运年龄计算
    start_age = 8
    
    # 计算10步大运
    da_yun = []
    current_gan_zhi = month_gan_zhi
    
    for i in range(10):
        if i == 0:
            current_gan_zhi = get_next_gan_zhi(month_gan_zhi, direction)
        else:
            current_gan_zhi = get_next_gan_zhi(current_gan_zhi, direction)
        
        start_year = start_age + i * 10
        end_year = start_year + 9
        
        da_yun.append({
            "干支": current_gan_zhi,
            "起止年龄": f"{start_year}-{end_year}岁",
            "十神干": ten_shen(day_gan, current_gan_zhi[0]),
            "十神支": ten_shen_dz(day_gan, current_gan_zhi[1])
        })
    
    return {
        "排运方式": "顺排" if direction == 1 else "逆排",
        "起运年龄": f"{start_age}岁",
        "大运": da_yun
    }

# 主计算函数
def calc_bazi(name, city, gender, year, month, day, hour, minute=0):
    """计算八字"""
    # 1. 北京时 -> 当地标准时
    local_dt = datetime(year, month, day, hour, minute)
    
    # 2. 当地标准时 -> 真太阳时
    true_dt = true_solar_time(city, local_dt)
    
    # 3. 计算八字
    day_obj = sxtwl.fromSolar(year, month, day)
    
    # 农历日期
    lunar_year = day_obj.getLunarYear()
    lunar_month = day_obj.getLunarMonth()
    lunar_day = day_obj.getLunarDay()
    is_leap = bool(day_obj.isLunarLeap())
    
    # 获取干支
    yg, mg, dg, hg = (
        TG[day_obj.getYearGZ().tg] + DZ[day_obj.getYearGZ().dz],
        TG[day_obj.getMonthGZ().tg] + DZ[day_obj.getMonthGZ().dz],
        TG[day_obj.getDayGZ().tg] + DZ[day_obj.getDayGZ().dz],
        TG[day_obj.getHourGZ(hour).tg] + DZ[day_obj.getHourGZ(hour).dz]
    )
    
    # 提取四柱
    gans = [yg[0], mg[0], dg[0], hg[0]]
    zhis = [yg[1], mg[1], dg[1], hg[1]]
    
    # 计算胎元和命宫
    tai_yuan = TG[(TG.index(mg[0]) + 1) % 10] + DZ[(DZ.index(mg[1]) + 3) % 12]
    
    # 使用lunar_python计算命宫
    solar = Solar.fromYmdHms(year, month, day, hour, minute, 0)
    lunar = solar.getLunar()
    ba = lunar.getEightChar()
    ming_gong = ba.getMingGong()
    
    # 计算各项命理信息
    wu_xing_strength = calculate_wu_xing_strength(gans, zhis, dg[0])
    shensha = calculate_shensha(gans, zhis, dg[0])
    zhi_relations = calculate_zhi_relations(zhis)
    
    # 计算纳音五行
    nayins = {
        "年柱": calculate_nayin(yg),
        "月柱": calculate_nayin(mg),
        "日柱": calculate_nayin(dg),
        "时柱": calculate_nayin(hg)
    }
    
    # 计算空亡
    empties_info = {
        "年柱": calculate_empty(yg),
        "月柱": calculate_empty(mg),
        "日柱": calculate_empty(dg),
        "时柱": calculate_empty(hg)
    }
    
    # 计算大运
    da_yun_info = calc_da_yun(year, mg, dg[0], gender)
    
    # 构建返回结果
    result = {
        "基本信息": {
            "姓名": name,
            "性别": gender,
            "出生地": city,
            "公历时间": local_dt.strftime("%Y-%m-%d %H:%M"),
            "真太阳时": true_dt.strftime("%Y-%m-%d %H:%M"),
            "农历": f"{lunar_year}年{'闰' if is_leap else ''}{lunar_month}月{lunar_day}日"
        },
        "八字": {
            "年柱": yg,
            "月柱": mg,
            "日柱": dg,
            "时柱": hg
        },
        "五行分析": {
            "天干五行": " ".join([f"{g}({ELE[g]})" for g in gans]),
            "地支五行": " ".join([f"{z}({DZ_ELE[z]})" for z in zhis]),
            "纳音五行": nayins,
            "五行强弱": wu_xing_strength
        },
        "十神分析": {
            "年干": ten_shen(dg[0], yg[0]),
            "年支": ten_shen_dz(dg[0], yg[1]),
            "月干": ten_shen(dg[0], mg[0]),
            "月支": ten_shen_dz(dg[0], mg[1]),
            "日干": "日主",
            "日支": ten_shen_dz(dg[0], dg[1]),
            "时干": ten_shen(dg[0], hg[0]),
            "时支": ten_shen_dz(dg[0], hg[1])
        },
        "地支关系": zhi_relations,
        "神煞": shensha,
        "空亡": empties_info,
        "特殊信息": {
            "胎元": tai_yuan,
            "命宫": ming_gong
        },
        "大运": da_yun_info
    }
    
    return result

# API接口函数
def solar_to_bazi(name: str, city: str, gender: str, year: int, month: int, day: int, hour: int, minute: int = 0):
    """API接口函数"""
    json_data = {}
    try:
        json_data = calc_bazi(name, city, gender, year, month, day, hour, minute)
    except Exception as e:
        print(f"计算错误: {e}")
        json_data = {"error": str(e)}
    
    return json.dumps(json_data, ensure_ascii=False, indent=2)