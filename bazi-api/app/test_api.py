"""
测试重构后的八字API
"""

import json
from datetime import datetime
from .bazi_calculator import BaziCalculator

def test_bazi_calculation():
    """测试八字计算功能"""
    
    calculator = BaziCalculator()
    
    # 测试时间：2023年5月15日 10:30
    test_dt = datetime(2023, 5, 15, 10, 30)
    
    print("="*50)
    print("八字计算测试")
    print("="*50)
    
    # 测试基本信息计算
    try:
        info_result = calculator.calculate_bazi_info(
            dt=test_dt,
            gender=1,  # 男
            sect=1,    # 晚子时日柱算明天
            realname="测试用户"
        )
        
        print("✅ 基本信息计算成功")
        print(f"姓名: {info_result['realname']}")
        print(f"性别: {'男' if info_result['gender'] == 1 else '女'}")
        print(f"生肖: {info_result['zodiac']}")
        print(f"星座: {info_result['constellation']}")
        print(f"四柱: {info_result['top']['year']}{info_result['bottom']['year']} "
              f"{info_result['top']['month']}{info_result['bottom']['month']} "
              f"{info_result['top']['day']}{info_result['bottom']['day']} "
              f"{info_result['top']['time']}{info_result['bottom']['time']}")
        print(f"纳音: 年({info_result['nayin']['year']}) 月({info_result['nayin']['month']}) "
              f"日({info_result['nayin']['day']}) 时({info_result['nayin']['time']})")
        print(f"十神: {info_result['gods']}")
        
    except Exception as e:
        print(f"❌ 基本信息计算失败: {e}")
    
    print("\n" + "-"*30 + "\n")
    
    # 测试古籍信息计算
    try:
        book_result = calculator.calculate_bazi_book(
            dt=test_dt,
            gender=1,
            sect=1
        )
        
        print("✅ 古籍信息计算成功")
        print(f"称骨: {book_result['weigh_bone']['total']}")
        print(f"诗句: {book_result['weigh_bone']['poetry']}")
        
    except Exception as e:
        print(f"❌ 古籍信息计算失败: {e}")
    
    print("\n" + "-"*30 + "\n")
    
    # 测试大运预测计算
    try:
        prediction_result = calculator.calculate_bazi_prediction(
            dt=test_dt,
            gender=1,
            sect=1
        )
        
        print("✅ 大运预测计算成功")
        print(f"大运数量: {len(prediction_result['dayunList'])}")
        print(f"流年数量: {len(prediction_result['yearList'])}")
        print(f"流月数量: {len(prediction_result['monthList'])}")
        
        # 显示前3个大运
        print("\n前3个大运:")
        for i, dayun in enumerate(prediction_result['dayunList'][:3]):
            print(f"  {i+1}. {dayun['pillar']} ({dayun['shishen']}) - "
                  f"{dayun['startYear']}年起({dayun['startAge']}岁)")
        
        # 显示前5个流年
        print("\n前5个流年:")
        for i, year in enumerate(prediction_result['yearList'][:5]):
            print(f"  {i+1}. {year['year']}年 {year['pillar']} ({year['shishen']}) - {year['age']}岁")
        
    except Exception as e:
        print(f"❌ 大运预测计算失败: {e}")
    
    print("\n" + "="*50)

def test_shishen_calculation():
    """测试十神计算"""
    
    print("十神计算测试")
    print("="*50)
    
    from .shishen_calculator import ShishenCalculator
    
    shishen_calc = ShishenCalculator()
    
    # 测试天干十神
    day_gan = "甲"  # 日干为甲
    test_gans = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    
    print(f"以{day_gan}为日干的十神关系:")
    for gan in test_gans:
        relation = shishen_calc.get_relation(day_gan, gan)
        simplified = shishen_calc.get_simplified_relation(relation)
        print(f"  {day_gan} -> {gan}: {relation} ({simplified})")
    
    print("\n地支十神关系示例:")
    test_zhis = ["子", "丑", "寅", "卯", "辰", "巳"]
    for zhi in test_zhis:
        relation = shishen_calc.get_relation(day_gan, zhi)
        simplified = shishen_calc.get_simplified_relation(relation)
        print(f"  {day_gan} -> {zhi}: {relation} ({simplified})")

if __name__ == "__main__":
    # 运行测试
    test_bazi_calculation()
    print("\n")
    test_shishen_calculation()