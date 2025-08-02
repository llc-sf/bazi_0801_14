"""
十神计算器
基于8Char-Uni-App-master的十神计算逻辑
"""

from typing import Dict, List
from .data_models import Constants

class ShishenCalculator:
    """
    十神计算器
    """
    
    def __init__(self):
        self.shi_shen_zhi = Constants.SHI_SHEN_ZHI
        self.shi_shen_gan = self._generate_shi_shen_gan()
        self.shi_shen_simplifie = Constants.SHI_SHEN_SIMPLIFIE
    
    def _generate_shi_shen_gan(self) -> Dict[str, str]:
        """
        生成天干十神映射
        基于传统命理学十神理论
        """
        shi_shen_gan = {}
        tian_gan = Constants.TIAN_GAN
        
        # 五行属性
        wu_xing = {
            "甲": "木", "乙": "木", "丙": "火", "丁": "火", "戊": "土",
            "己": "土", "庚": "金", "辛": "金", "壬": "水", "癸": "水"
        }
        
        # 阴阳属性
        yin_yang = {
            "甲": "阳", "乙": "阴", "丙": "阳", "丁": "阴", "戊": "阳",
            "己": "阴", "庚": "阳", "辛": "阴", "壬": "阳", "癸": "阴"
        }
        
        # 五行生克关系
        sheng = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}
        ke = {"木": "土", "火": "金", "土": "水", "金": "木", "水": "火"}
        
        for day_gan in tian_gan:
            day_wu_xing = wu_xing[day_gan]
            day_yin_yang = yin_yang[day_gan]
            
            for gan in tian_gan:
                key = day_gan + gan
                gan_wu_xing = wu_xing[gan]
                gan_yin_yang = yin_yang[gan]
                
                if day_gan == gan:
                    shi_shen_gan[key] = "比肩"
                elif day_wu_xing == gan_wu_xing:
                    # 同五行，阴阳不同
                    if day_yin_yang != gan_yin_yang:
                        shi_shen_gan[key] = "劫财"
                    else:
                        shi_shen_gan[key] = "比肩"
                elif sheng[day_wu_xing] == gan_wu_xing:
                    # 日干生目标干
                    if day_yin_yang == gan_yin_yang:
                        shi_shen_gan[key] = "食神"
                    else:
                        shi_shen_gan[key] = "伤官"
                elif sheng[gan_wu_xing] == day_wu_xing:
                    # 目标干生日干
                    if day_yin_yang == gan_yin_yang:
                        shi_shen_gan[key] = "正印"
                    else:
                        shi_shen_gan[key] = "偏印"
                elif ke[day_wu_xing] == gan_wu_xing:
                    # 日干克目标干
                    if day_yin_yang == gan_yin_yang:
                        shi_shen_gan[key] = "偏财"
                    else:
                        shi_shen_gan[key] = "正财"
                elif ke[gan_wu_xing] == day_wu_xing:
                    # 目标干克日干
                    if day_yin_yang == gan_yin_yang:
                        shi_shen_gan[key] = "七杀"
                    else:
                        shi_shen_gan[key] = "正官"
                else:
                    shi_shen_gan[key] = "未知"
        
        return shi_shen_gan
    
    def get_relation(self, day_gan: str, target: str) -> str:
        """获取十神关系"""
        if target in Constants.TIAN_GAN:
            # 天干
            return self.shi_shen_gan.get(day_gan + target, "")
        elif target in Constants.DI_ZHI:
            # 地支
            return self.shi_shen_zhi.get(day_gan + target, "")
        return ""
    
    def get_relation_by_pillar(self, day_gan: str, pillar: str) -> str:
        """根据干支柱获取十神关系"""
        if pillar == "童限":
            return "童限"
        
        if len(pillar) >= 2:
            top_relation = self.get_relation(day_gan, pillar[0])
            bottom_relation = self.get_relation(day_gan, pillar[1])
            
            top_simple = self.shi_shen_simplifie.get(top_relation, "")
            bottom_simple = self.shi_shen_simplifie.get(bottom_relation, "")
            
            return top_simple + bottom_simple
        
        return ""
    
    def get_simplified_relation(self, relation: str) -> str:
        """获取简化的十神名称"""
        return self.shi_shen_simplifie.get(relation, relation)