from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, conint
from typing import Optional, Dict, Any
from datetime import datetime
from .bazi_calculator_new import BaziCalculator

app = FastAPI(title="精准八字 API", version="2.0.0")

class BaziRequest(BaseModel):
    datetime: str  # 格式: YYYY-MM-DD HH:MM:SS
    gender: int = 1  # 1: 男, 2: 女
    sect: int = 1    # 1: 晚子时日柱算明天, 2: 晚子时日柱算当天
    realname: Optional[str] = ""

class LegacyBaziRequest(BaseModel):
    name: str
    city: str
    gender: str  # "男" 或 "女"
    year: int
    month: int
    day: int
    hour: int
    minute: int

class BaziInfoRequest(BaseModel):
    datetime: str
    gender: int = 1
    sect: int = 1
    realname: Optional[str] = ""

class BaziPredictionRequest(BaseModel):
    datetime: str
    gender: int = 1
    sect: int = 1

# 初始化计算器
bazi_calc = BaziCalculator()

@app.post("/8char/get-info")
def get_bazi_info(req: BaziInfoRequest):
    """获取八字基本信息"""
    try:
        dt = datetime.strptime(req.datetime, "%Y-%m-%d %H:%M:%S")
        result = bazi_calc.calculate_bazi_info(dt, req.gender, req.sect, req.realname or "")
        return {"data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/8char/get-prediction")
def get_bazi_prediction(req: BaziPredictionRequest):
    """获取大运流年预测"""
    try:
        dt = datetime.strptime(req.datetime, "%Y-%m-%d %H:%M:%S")
        result = bazi_calc.calculate_bazi_prediction(dt, req.gender, req.sect)
        return {"data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/8char/get-tips")
def get_tips():
    """获取提示信息"""
    return {
        "data": [
            "本排盘系统采用真太阳时校正，排盘结果更加精准",
            "晚子时（23:00-24:00）的日柱归属可选择流派",
            "大运起始年龄计算考虑了节令因素"
        ]
    }

@app.get("/8char/get-version")
def get_version():
    """获取版本信息"""
    return {
        "data": {
            "version": "2.0.0",
            "author": "重构版",
            "description": "基于 8Char-Uni-App-master 逻辑重构的专业八字排盘 API"
        }
    }

# 保持兼容性接口
@app.post("/bazi")
def get_bazi_legacy(req: LegacyBaziRequest):
    """兼容性接口"""
    try:
        # 构造datetime字符串
        dt_str = f"{req.year:04d}-{req.month:02d}-{req.day:02d} {req.hour:02d}:{req.minute:02d}:00"
        dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
        
        # 转换性别格式
        gender = 1 if req.gender == "男" else 2
        
        result = bazi_calc.calculate_bazi_info(dt, gender, 1, req.name)
        
        # 转换为兼容格式
        return {
            "基本信息": {
                "姓名": req.name,
                "性别": req.gender,
                "出生地": req.city,
                "公历时间": dt.strftime("%Y-%m-%d %H:%M"),
                "农历": result["datetime"]["lunar"]
            },
            "八字": {
                "年柱": result["top"]["year"] + result["bottom"]["year"],
                "月柱": result["top"]["month"] + result["bottom"]["month"],
                "日柱": result["top"]["day"] + result["bottom"]["day"],
                "时柱": result["top"]["time"] + result["bottom"]["time"]
            },
            "十神": {
                "年干": result["gods"][0] if len(result["gods"]) > 0 else "",
                "月干": result["gods"][1] if len(result["gods"]) > 1 else "",
                "日干": result["gods"][2] if len(result["gods"]) > 2 else "",
                "时干": result["gods"][3] if len(result["gods"]) > 3 else ""
            },
            "大运": {
                "description": f"起运年龄：{result.get('startAge', '8')}岁",
                "dayun_list": result.get("dayunList", [])
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
