# 八字排盘 API (重构版)

基于 8Char-Uni-App-master 的 lunar-javascript 逻辑重构的专业八字排盘 API。

## 🚀 特性

- **完整八字计算**: 年月日时四柱排盘
- **十神关系**: 基于传统命理学的十神计算
- **大运流年**: 完整的大运流年推算
- **古籍参考**: 称骨算命等传统命理参考
- **多接口支持**: 兼容前端项目的多个接口需求

## 📋 API 接口

### 1. 获取八字基本信息
```http
POST /8char/get-info
Content-Type: application/json

{
  "datetime": "2023-05-15 10:30:00",
  "gender": 1,
  "sect": 1,
  "realname": "张三"
}
```

**响应示例:**
```json
{
  "data": {
    "realname": "张三",
    "gender": 1,
    "zodiac": "兔",
    "constellation": "金牛座",
    "top": {
      "year": "癸",
      "month": "丁",
      "day": "甲",
      "time": "己"
    },
    "bottom": {
      "year": "卯",
      "month": "巳",
      "day": "午",
      "time": "巳"
    },
    "nayin": {
      "year": "金泊金",
      "month": "砂中土",
      "day": "砂中金",
      "time": "大林木"
    },
    "gods": ["正印", "伤官", "食神"]
  }
}
```

### 2. 获取古籍命书信息
```http
POST /8char/get-book
Content-Type: application/json

{
  "datetime": "2023-05-15 10:30:00",
  "gender": 1,
  "sect": 1
}
```

### 3. 获取大运流年预测
```http
POST /8char/get-prediction
Content-Type: application/json

{
  "datetime": "2023-05-15 10:30:00",
  "gender": 1,
  "sect": 1
}
```

**响应示例:**
```json
{
  "data": {
    "dayunList": [
      {
        "startYear": 2031,
        "startAge": 8,
        "pillar": "戊午",
        "shishen": "才官"
      }
    ],
    "yearList": [
      {
        "year": 2031,
        "pillar": "辛亥",
        "age": 8,
        "shishen": "官印"
      }
    ]
  }
}
```

### 4. 获取提示信息
```http
GET /8char/get-tips
```

### 5. 获取版本信息
```http
GET /8char/get-version
```

## 🛠️ 技术架构

### 核心模块

1. **LunarCalculator** (`lunar_calculator.py`)
   - 农历公历转换
   - 八字四柱计算
   - 纳音、空亡计算

2. **ShishenCalculator** (`shishen_calculator.py`)
   - 十神关系计算
   - 基于五行生克理论
   - 支持天干地支十神

3. **DayunCalculator** (`dayun_calculator.py`)
   - 大运排盘计算
   - 流年推算
   - 流月计算

4. **BaziCalculator** (`bazi_calculator.py`)
   - 主计算类
   - 集成所有功能模块

### 数据模型

所有数据结构定义在 `data_models.py` 中，包括：
- 请求/响应模型
- 四柱数据结构
- 大运流年数据结构
- 常量定义

## 🔧 安装与运行

### 安装依赖
```bash
pip install -r requirements.txt
```

### 启动服务
```bash
# 开发模式
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 生产模式
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Docker 部署
```bash
# 构建镜像
docker build -t bazi-api .

# 运行容器
docker run -p 8000:8000 bazi-api
```

## 🧪 测试

运行测试脚本：
```bash
cd app
python test_api.py
```

## 📊 参数说明

### 性别参数
- `1`: 男
- `2`: 女

### 流派参数
- `1`: 晚子时日柱算明天
- `2`: 晚子时日柱算当天

### 时间格式
- 格式: `YYYY-MM-DD HH:MM:SS`
- 示例: `2023-05-15 10:30:00`

## 🔄 与前端的对应关系

| 前端接口 | 后端接口 | 说明 |
|---------|----------|------|
| `GetInfo` | `/8char/get-info` | 获取八字基本信息 |
| `GetBook` | `/8char/get-book` | 获取古籍命书信息 |
| `GetPrediction` | `/8char/get-prediction` | 获取大运流年预测 |
| `GetTips` | `/8char/get-tips` | 获取提示信息 |
| `GetVersion` | `/8char/get-version` | 获取版本信息 |

## 📈 版本历史

### v2.0.0 (当前版本)
- 基于 8Char-Uni-App-master 逻辑重构
- 支持完整的八字、十神、大运计算
- 新增多个专用接口
- 改进数据结构和响应格式

### v1.0.0 (原版本)
- 基础八字计算功能
- 单一 `/bazi` 接口

## 🤝 兼容性

- 保留原有 `/bazi` 接口以确保向后兼容
- 新接口格式与前端项目完全对应
- 支持前端项目的所有计算需求

## 📝 许可证

本项目遵循原项目的开源协议，仅供学习研究使用。