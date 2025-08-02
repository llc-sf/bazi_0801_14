#!/usr/bin/env python3
"""
快速测试修改后的八字计算功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
from app.bazi_calculator import BaziCalculator

def test_bazi_calculation():
    """测试八字计算功能"""
    print("🚀 开始测试修改后的八字计算...")
    
    try:
        # 创建计算器实例
        calculator = BaziCalculator()
        
        # 测试数据
        test_dt = datetime(1992, 9, 9, 9, 0)
        
        print(f"📅 测试时间: {test_dt}")
        
        # 执行计算
        result = calculator.calculate_bazi_info(
            dt=test_dt,
            gender=1,  # 男
            sect=1,    # 传统
            realname="测试用户"
        )
        
        print("✅ 计算成功！")
        print(f"📊 返回字段数量: {len(result)}")
        
        # 检查关键字段
        key_fields = [
            "姓名", "天干", "地支", "藏干", "空亡", "纳音",
            "五行", "十神", "十神详细", "专业大运", "专业流年", "professional"
        ]
        
        print("\n🔍 关键字段检查:")
        for field in key_fields:
            if field in result:
                value = result[field]
                if isinstance(value, list):
                    print(f"  ✅ {field}: 列表，长度={len(value)}")
                    if value:  # 如果列表不为空，显示第一个元素
                        print(f"      首项: {value[0]}")
                elif isinstance(value, dict):
                    print(f"  ✅ {field}: 字典，键数={len(value)}")
                    if value:  # 如果字典不为空，显示一些键
                        keys = list(value.keys())[:3]
                        print(f"      部分键: {keys}")
                else:
                    print(f"  ✅ {field}: {type(value).__name__} = {str(value)[:50]}...")
            else:
                print(f"  ❌ {field}: 缺失")
        
        # 检查专业数据
        if "professional" in result:
            prof = result["professional"]
            print(f"\n📈 专业数据:")
            print(f"  大运数量: {len(prof.get('dayun', []))}")
            print(f"  流年数量: {len(prof.get('liunian', []))}")
            
            if prof.get('dayun'):
                print(f"  首个大运: {prof['dayun'][0]}")
            if prof.get('liunian'):
                print(f"  首个流年: {prof['liunian'][0]}")
        
        # 检查五行分析
        if "五行" in result:
            wuxing = result["五行"]
            print(f"\n🌟 五行分析:")
            print(f"  专业解读: {wuxing.get('专业解读', [])}")
            print(f"  包含元素: {wuxing.get('包含', [])}")
            print(f"  缺失元素: {wuxing.get('缺失', [])}")
        
        # 检查十神详细分析
        if "十神详细" in result:
            shishen = result["十神详细"]
            print(f"\n🔮 十神详细分析:")
            print(f"  天干十神: {shishen.get('天干十神', {})}")
            
            zhi_shishen = shishen.get('地支藏干十神', {})
            for pillar, details in zhi_shishen.items():
                if details:
                    print(f"  {pillar}: {details}")
                else:
                    print(f"  {pillar}: 无藏干")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_bazi_calculation()
    if success:
        print("\n🎉 测试完成，数据已优化！")
    else:
        print("\n💥 测试失败，需要进一步调试。")