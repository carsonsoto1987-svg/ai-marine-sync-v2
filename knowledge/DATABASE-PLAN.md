# 海洋观赏生物数据库建设方案

**日期：** 2026-03-25  
**目标：** 建立完整的观赏鱼、珊瑚、无脊椎动物数据库  
**数据来源：** FishBase、WoRMS、水产名录网站

---

## 一、数据库架构设计

### 数据库类型选择
```
推荐：SQLite（本地）+ JSON（交换）+ Markdown（文档）
后期可迁移：PostgreSQL（大规模）
```

### 数据表结构

#### 1. 鱼类表 (fish_species)
```sql
CREATE TABLE fish_species (
    id INTEGER PRIMARY KEY,
    scientific_name VARCHAR(255) NOT NULL,  -- 学名
    common_name VARCHAR(255),                -- 英文名
    chinese_name VARCHAR(255),               -- 中文名
    family VARCHAR(100),                     -- 科
    genus VARCHAR(100),                      -- 属
    origin VARCHAR(255),                     -- 原产地
    habitat TEXT,                            -- 栖息地
    max_size_cm DECIMAL(5,2),               -- 最大尺寸
    temperament VARCHAR(50),                -- 性情（温和/凶猛）
    reef_safe BOOLEAN,                       -- 珊瑚兼容
    care_level VARCHAR(50),                 -- 饲养难度
    diet VARCHAR(100),                       -- 食性
    min_tank_size_liters INTEGER,           -- 最小缸容
    temperature_c_min DECIMAL(4,1),         -- 温度范围
    temperature_c_max DECIMAL(4,1),
    ph_min DECIMAL(3,1),                    -- pH范围
    ph_max DECIMAL(3,1),
    salinity_min DECIMAL(4,3),              -- 盐度范围
    salinity_max DECIMAL(4,3),
    lifespan_years INTEGER,                 -- 寿命
    price_range_usd VARCHAR(50),            -- 价格区间
    availability VARCHAR(50),               -- 可获得性
    image_url TEXT,                          -- 图片链接
    description TEXT,                        -- 描述
    special_notes TEXT,                      -- 特殊说明
    cites_status VARCHAR(50),               -- CITES状态
    source VARCHAR(100),                     -- 数据来源
    last_updated DATE                        -- 最后更新
);
```

#### 2. 珊瑚表 (coral_species)
```sql
CREATE TABLE coral_species (
    id INTEGER PRIMARY KEY,
    scientific_name VARCHAR(255) NOT NULL,
    common_name VARCHAR(255),
    chinese_name VARCHAR(255),
    type VARCHAR(50),                        -- SPS/LPS/软珊瑚
    family VARCHAR(100),
    origin VARCHAR(255),
    care_level VARCHAR(50),
    lighting VARCHAR(50),                    -- 光照需求
    water_flow VARCHAR(50),                  -- 水流需求
    growth_rate VARCHAR(50),                 -- 生长速度
    aggression VARCHAR(50),                  -- 攻击性
    difficulty VARCHAR(50),                  -- 饲养难度
    colors TEXT,                             -- 常见颜色
    fraggable BOOLEAN,                       -- 可切枝
    temperaturer_c_min DECIMAL(4,1),
    temperaturer_c_max DECIMAL(4,1),
    calcium_ppm_min INTEGER,
    calcium_ppm_max INTEGER,
    alkalinity_dkh_min DECIMAL(4,1),
    alkalinity_dkh_max DECIMAL(4,1),
    magnesium_ppm_min INTEGER,
    magnesium_ppm_max INTEGER,
    image_url TEXT,
    description TEXT,
    propagation_notes TEXT,                  -- 繁殖说明
    disease_susceptibility TEXT,             -- 易感疾病
    cites_status VARCHAR(50),
    source VARCHAR(100),
    last_updated DATE
);
```

#### 3. 无脊椎动物表 (invertebrates)
```sql
CREATE TABLE invertebrates (
    id INTEGER PRIMARY KEY,
    scientific_name VARCHAR(255) NOT NULL,
    common_name VARCHAR(255),
    chinese_name VARCHAR(255),
    category VARCHAR(50),                    -- 虾/蟹/贝/海星/海胆
    family VARCHAR(100),
    reef_safe BOOLEAN,
    fish_safe BOOLEAN,                       -- 对鱼安全
    coral_safe BOOLEAN,                      -- 对珊瑚安全
    care_level VARCHAR(50),
    diet VARCHAR(100),
    max_size_cm DECIMAL(5,2),
    temperaturer_c_min DECIMAL(4,1),
    temperaturer_c_max DECIMAL(4,1),
    special_requirements TEXT,               -- 特殊需求
    image_url TEXT,
    description TEXT,
    source VARCHAR(100),
    last_updated DATE
);
```

#### 4. 病虫害表 (diseases_pests)
```sql
CREATE TABLE diseases_pests (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    chinese_name VARCHAR(255),
    category VARCHAR(50),                    -- 寄生虫/细菌/真菌/害虫
    affected_species TEXT,                   -- 受影响物种
    symptoms TEXT,                           -- 症状
    causes TEXT,                             -- 病因
    treatment TEXT,                          -- 治疗方案
    prevention TEXT,                         -- 预防措施
    medication TEXT,                         -- 推荐药物
    severity VARCHAR(50),                    -- 严重程度
    contagious BOOLEAN,
    images TEXT,                             -- 症状图片链接
    source VARCHAR(100),
    last_updated DATE
);
```

---

## 二、数据源与爬取方案

### 主要数据源

| 数据库 | 网址 | 数据量 | 访问方式 |
|-------|------|--------|---------|
| **FishBase** | fishbase.org | 35,000+ 物种 | API + 网页 |
| **WoRMS** | marinespecies.org | 50,000+ 海洋物种 | API + 下载 |
| **Reef Builder** | reefbuilders.com | 珊瑚/海水鱼 | 网页 |
| **LiveAquaria** | liveaquaria.com | 观赏鱼珊瑚 | 网页 |
| **CORAL Magazine** | coralmagazine.com | 珊瑚专题 | 网页 |

### 爬取策略

#### A. FishBase API 获取
```python
import requests
import pandas as pd

# FishBase API 示例
base_url = "https://fishbase.ropensci.org"

# 获取物种列表
def get_fish_species_list():
    url = f"{base_url}/species"
    response = requests.get(url)
    return response.json()

# 获取详细信息
def get_fish_details(species_code):
    url = f"{base_url}/species/{species_code}"
    response = requests.get(url)
    return response.json()
```

#### B. WoRMS 数据下载
```python
# WoRMS 提供完整数据下载
# 网址：http://www.marinespecies.org/aphia.php?p=download

# 或者使用 API
import requests

def get_worms_species(name):
    url = f"https://www.marinespecies.org/rest/AphiaRecordsByName/{name}"
    response = requests.get(url)
    return response.json()
```

#### C. 网页爬虫（需要时使用 agent-browser）
```bash
# 使用 agent-browser 爬取网页
npx agent-browser open https://www.liveaquaria.com
cd ~/.openclaw/workspace
# 编写爬取脚本...
```

---

## 三、数据采集计划

### 第一阶段：基础数据（1-2周）

#### 目标：获取 500-1000 种常见观赏鱼
- [ ] 从 FishBase 获取海水观赏鱼列表
- [ ] 筛选常见贸易物种（约300种）
- [ ] 获取基础信息（学名、英文名、科属）
- [ ] 补充中文名（对照国内资料）

#### 目标：获取 200-300 种常见珊瑚
- [ ] 从 WoRMS 获取石珊瑚列表
- [ ] 筛选常见贸易珊瑚
- [ ] 分类：SPS / LPS / 软珊瑚

### 第二阶段：详细信息（2-4周）

#### 鱼类信息完善
- [ ] 原产地、栖息地
- [ ] 尺寸、性情、珊瑚兼容性
- [ ] 饲养难度、食性
- [ ] 水质参数要求
- [ ] 价格区间

#### 珊瑚信息完善
- [ ] 光照/水流需求
- [ ] 生长速度/攻击性
- [ ] 水质参数要求
- [ ] 繁殖方法

### 第三阶段：病虫害数据（1-2周）
- [ ] 整理已有病虫害知识
- [ ] 添加症状图片链接
- [ ] 建立治疗方案数据库

### 第四阶段：持续更新（长期）
- [ ] 每月更新价格数据
- [ ] 每季度添加新物种
- [ ] 持续修正错误信息

---

## 四、实施工具

### 推荐工具栈
```
数据采集：Python + requests + BeautifulSoup
数据存储：SQLite / PostgreSQL
数据导出：JSON / CSV / Markdown
版本控制：Git
自动化：Cron + Python脚本
```

### Python 脚本示例

#### 数据收集脚本
```python
# collect_fish_data.py
import requests
import sqlite3
import json
from datetime import datetime

def init_database():
    conn = sqlite3.connect('marine_species.db')
    cursor = conn.cursor()
    # 创建表...
    return conn

def collect_fishbase_data():
    """从 FishBase 收集数据"""
    base_url = "https://fishbase.ropensci.org"
    
    # 获取常见观赏鱼科
    families = [
        "Pomacentridae",  # 雀鲷科（小丑鱼）
        "Acanthuridae",   # 刺尾鱼科（吊类）
        "Pomacanthidae",  # 盖刺鱼科（神仙鱼）
        "Labridae",       # 隆头鱼科
        "Pomacentridae",  # 雀鲷科
        "Chaetodontidae", # 蝴蝶鱼科
    ]
    
    for family in families:
        url = f"{base_url}/species?family={family}"
        response = requests.get(url)
        data = response.json()
        
        # 存储到数据库
        save_to_database(data)

def save_to_database(data):
    conn = sqlite3.connect('marine_species.db')
    cursor = conn.cursor()
    
    for species in data['data']:
        cursor.execute('''
            INSERT OR REPLACE INTO fish_species 
            (scientific_name, common_name, family, genus, source, last_updated)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            species.get('Genus') + ' ' + species.get('Species'),
            species.get('FBname'),
            species.get('Family'),
            species.get('Genus'),
            'FishBase',
            datetime.now().date()
        ))
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_database()
    collect_fishbase_data()
```

#### 自动化任务
```bash
# 添加到 crontab，每周更新数据
0 2 * * 0 cd ~/.openclaw/workspace && python collect_fish_data.py >> logs/collection.log 2>&1
```

---

## 五、数据质量保证

### 验证流程
1. **自动验证** - 检查必填字段完整性
2. **交叉验证** - 多个数据源对比
3. **专家审核** - 定期请行业专家检查
4. **用户反馈** - 收集使用中的纠错

### 数据标准
- 学名使用拉丁文，遵循国际命名法规
- 中文名参考《中国鱼类志》等权威资料
- 水质参数单位统一（摄氏度、pH、ppm）
- 图片来源标注版权信息

---

## 六、应用场景

### 1. 智能查询系统
```
用户问："有什么适合 beginners 的海水鱼？"
→ 查询 care_level = 'Easy' 的 fish_species
→ 返回列表 + 基本信息
```

### 2. 兼容性检查
```
用户问："小丑鱼和蓝吊能一起养吗？"
→ 查询两种鱼的 temperament
→ 分析兼容性
→ 给出建议
```

### 3. 疾病诊断
```
用户发图："这是什么病？"
→ 图像识别（或描述匹配）
→ 查询 diseases_pests 表
→ 返回诊断 + 治疗方案
```

### 4. 库存管理
```
用户问："Acropora millepora 的库存情况？"
→ 查询内部库存系统（需对接）
→ 返回库存 + 价格 + 养护建议
```

---

## 七、实施时间表

| 阶段 | 时间 | 产出 |
|-----|------|------|
| **Week 1** | 数据库设计 + 基础架构 | SQLite 数据库 + 表结构 |
| **Week 2** | FishBase 数据采集 | 300种鱼类基础数据 |
| **Week 3** | WoRMS 珊瑚数据采集 | 200种珊瑚基础数据 |
| **Week 4** | 详细信息完善 | 完整参数数据 |
| **Week 5** | 病虫害数据整理 | 疾病数据库 |
| **Week 6** | 测试 + 优化 | 可用系统 v1.0 |
| **Ongoing** | 持续更新 | 月度数据更新 |

---

## 八、下一步行动

### 立即可做
1. **创建数据库** - 运行 SQL 创建表结构
2. **注册 API** - FishBase、WoRMS API 密钥
3. **测试爬取** - 小规模测试数据获取

### 本周完成
1. **完成 100 种鱼类数据** - 验证流程可行性
2. **建立自动化脚本** - 每日/每周自动更新
3. **对接知识库** - 将数据库与现有知识库整合

### 需要你的决策
- [ ] 数据库规模目标（1000种？5000种？）
- [ ] 是否包含价格数据（会变化，需频繁更新）
- [ ] 是否需要图片存储（占用空间大）
- [ ] 是否对接你的库存系统

---

*需要我开始创建数据库和爬取脚本吗？*
