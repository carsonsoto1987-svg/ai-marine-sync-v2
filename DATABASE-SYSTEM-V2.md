# 大规模海洋观赏生物数据库系统 v2.0

**日期：** 2026-03-25  
**规模目标：** 10,000+ 鱼类，5,000+ 珊瑚，2,000+ 无脊椎动物  
**更新频率：** 每日自动更新价格和库存状态

---

## 一、系统架构

### 整体架构
```
┌─────────────────────────────────────────────────────────────┐
│                    数据采集层                                │
├─────────────┬─────────────┬─────────────┬───────────────────┤
│  FishBase   │   WoRMS     │  价格爬虫   │    图片下载       │
│   API       │    API      │  (每日)     │    (批量)         │
└──────┬──────┴──────┬──────┴──────┬──────┴─────────┬─────────┘
       │             │             │                │
       └─────────────┴──────┬──────┴────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    数据处理层                                │
│  • 数据清洗    • 去重合并    • 格式标准化    • 质量检查      │
└────────────────────────┬────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    数据存储层                                │
├────────────────┬────────────────┬───────────────────────────┤
│  PostgreSQL    │   图片存储      │    缓存层 (Redis)        │
│  (主数据库)    │  (本地/云盘)   │    热点数据缓存           │
└────────────────┴────────────────┴───────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   本地查询    │ │  API 服务    │ │  同步服务    │
│   (OpenClaw)  │ │  (RESTful)   │ │ (到其他AI)   │
└──────────────┘ └──────────────┘ └──────────────┘
```

---

## 二、数据库设计（PostgreSQL）

### 优化后的表结构

#### 1. 鱼类主表 (fish_species)
```sql
CREATE TABLE fish_species (
    id SERIAL PRIMARY KEY,
    species_code VARCHAR(50) UNIQUE,        -- FishBase/WoRMS 代码
    scientific_name VARCHAR(255) NOT NULL,
    common_name VARCHAR(255),
    common_name_cn VARCHAR(255),            -- 中文名
    synonyms TEXT[],                        -- 异名数组
    
    -- 分类
    kingdom VARCHAR(50),
    phylum VARCHAR(50),
    class VARCHAR(50),
    order_name VARCHAR(50),
    family VARCHAR(100),
    genus VARCHAR(100),
    
    -- 分布与栖息地
    origin TEXT,                            -- 原产地（JSON格式）
    habitat TEXT,                           -- 栖息地描述
    depth_range_m VARCHAR(50),             -- 深度范围
    
    -- 体型与寿命
    max_size_cm DECIMAL(5,2),
    size_at_maturity_cm DECIMAL(5,2),
    lifespan_years INTEGER,
    
    -- 饲养参数
    care_level VARCHAR(20),                -- Easy/Medium/Difficult/Expert
    temperament VARCHAR(20),               -- Peaceful/Semi-aggressive/Aggressive
    reef_safe BOOLEAN,
    reef_safe_notes TEXT,
    
    -- 环境参数
    temp_min_c DECIMAL(4,1),
    temp_max_c DECIMAL(4,1),
    ph_min DECIMAL(3,1),
    ph_max DECIMAL(3,1),
    salinity_min DECIMAL(4,3),
    salinity_max DECIMAL(4,3),
    ammonia_ppm_max DECIMAL(4,2),
    nitrite_ppm_max DECIMAL(4,2),
    nitrate_ppm_max DECIMAL(4,2),
    
    -- 饲养要求
    min_tank_size_liters INTEGER,
    tank_type VARCHAR(50),                 -- FOWLR/Reef/Species only
    diet_type VARCHAR(50),                 -- Carnivore/Herbivore/Omnivore/Planktivore
    feeding_frequency VARCHAR(50),
    special_diet_needs TEXT,
    
    -- 社交行为
    schooling BOOLEAN,
    min_group_size INTEGER,
    compatible_with TEXT[],                -- 兼容物种数组
    incompatible_with TEXT[],              -- 不兼容物种数组
    
    -- 繁殖
    breeding_difficulty VARCHAR(20),
    breeding_method VARCHAR(100),          -- Egg scatterer/Mouthbrooder/etc
    sexual_dimorphism BOOLEAN,
    
    -- CITES与法规
    cites_appendix VARCHAR(10),           -- I/II/III/None
    cites_status_date DATE,
    iucn_status VARCHAR(20),              -- CR/EN/VU/NT/LC
    export_restrictions TEXT,
    
    -- 图片
    primary_image_path VARCHAR(500),
    image_gallery JSONB,                  -- [{path, caption, source}, ...]
    
    -- 价格（每日更新）
    price_retail_usd DECIMAL(8,2),
    price_wholesale_usd DECIMAL(8,2),
    price_currency VARCHAR(3) DEFAULT 'USD',
    price_date DATE,
    price_source VARCHAR(100),            -- 数据来源
    price_history JSONB,                  -- [{date, price, source}, ...]
    
    -- 可获得性
    availability_status VARCHAR(50),      -- Common/Seasonal/Rare/Very Rare
    availability_notes TEXT,
    seasonal_availability VARCHAR(100),   -- 特定季节可获得
    
    -- 数据来源与元数据
    source_databases TEXT[],              -- ['FishBase', 'WoRMS', 'ReefBuilder']
    external_links JSONB,                 -- {fishbase_url, worms_url, ...}
    date_added DATE DEFAULT CURRENT_DATE,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_count INTEGER DEFAULT 0,
    data_quality_score INTEGER,           -- 1-10 数据质量评分
    
    -- 搜索优化
    search_vector tsvector,               -- PostgreSQL全文搜索
    tags TEXT[],                          -- 标签数组
    
    -- 备注
    notes TEXT,
    care_notes TEXT,
    common_issues TEXT
);

-- 创建索引
CREATE INDEX idx_fish_family ON fish_species(family);
CREATE INDEX idx_fish_care_level ON fish_species(care_level);
CREATE INDEX idx_fish_reef_safe ON fish_species(reef_safe);
CREATE INDEX idx_fish_price ON fish_species(price_retail_usd);
CREATE INDEX idx_fish_availability ON fish_species(availability_status);
CREATE INDEX idx_fish_search ON fish_species USING GIN(search_vector);
CREATE INDEX idx_fish_tags ON fish_species USING GIN(tags);
```

#### 2. 珊瑚主表 (coral_species)
```sql
CREATE TABLE coral_species (
    id SERIAL PRIMARY KEY,
    aphia_id INTEGER UNIQUE,              -- WoRMS Aphia ID
    scientific_name VARCHAR(255) NOT NULL,
    common_name VARCHAR(255),
    common_name_cn VARCHAR(255),
    
    -- 分类
    type VARCHAR(50),                     -- SPS/LPS/Soft/Leather/Polyps
    family VARCHAR(100),
    genus VARCHAR(100),
    
    -- 形态特征
    growth_form VARCHAR(100),             -- Branching/Encrusting/Massive/Tabling
    colors TEXT[],                        -- 常见颜色数组
    polyp_size_mm DECIMAL(5,2),          -- 触手大小
    
    -- 饲养参数
    care_level VARCHAR(20),
    lighting VARCHAR(50),                -- Low/Medium/High/Very High
    water_flow VARCHAR(50),              -- Low/Medium/High
    feeding_requirement VARCHAR(50),     -- Photosynthetic/Filter feeder/Both
    
    -- 环境参数
    temp_min_c DECIMAL(4,1),
    temp_max_c DECIMAL(4,1),
    ph_min DECIMAL(3,1),
    ph_max DECIMAL(3,1),
    salinity_min DECIMAL(4,3),
    salinity_max DECIMAL(4,3),
    
    -- 化学参数
    calcium_ppm_min INTEGER,
    calcium_ppm_max INTEGER,
    alkalinity_dkh_min DECIMAL(4,1),
    alkalinity_dkh_max DECIMAL(4,1),
    magnesium_ppm_min INTEGER,
    magnesium_ppm_max INTEGER,
    strontium_ppm_min DECIMAL(5,2),
    strontium_ppm_max DECIMAL(5,2),
    
    -- 生长与繁殖
    growth_rate VARCHAR(20),             -- Slow/Medium/Fast
    aggression VARCHAR(20),              -- Peaceful/Moderate/Aggressive
    sweeper_tentacles BOOLEAN,
    sweeper_tentacle_length_cm INTEGER,
    
    fraggable BOOLEAN,
    fragging_difficulty VARCHAR(20),
    fragging_notes TEXT,
    propagation_methods TEXT[],
    
    -- 疾病与害虫
    common_diseases TEXT[],
    disease_susceptibility TEXT,
    pest_susceptibility TEXT[],
    
    -- CITES与法规
    cites_appendix VARCHAR(10),
    iucn_status VARCHAR(20),
    collection_restrictions TEXT,
    mariculture_only BOOLEAN,            -- 是否只能人工繁殖
    
    -- 图片
    primary_image_path VARCHAR(500),
    image_gallery JSONB,
    fragging_images JSONB,
    
    -- 价格（每日更新）
    price_small_usd DECIMAL(8,2),        -- 小规格价格
    price_medium_usd DECIMAL(8,2),
    price_large_usd DECIMAL(8,2),
    price_per_polyp_usd DECIMAL(6,2),    -- 单头价格（如Zoanthids）
    price_date DATE,
    price_source VARCHAR(100),
    price_history JSONB,
    
    -- 可获得性
    availability_status VARCHAR(50),
    wild_collected_available BOOLEAN,
    aquacultured_available BOOLEAN,
    aquaculture_sources TEXT[],          -- 人工繁殖来源
    
    source_databases TEXT[],
    external_links JSONB,
    date_added DATE DEFAULT CURRENT_DATE,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    search_vector tsvector,
    tags TEXT[],
    notes TEXT
);

CREATE INDEX idx_coral_type ON coral_species(type);
CREATE INDEX idx_coral_family ON coral_species(family);
CREATE INDEX idx_coral_care ON coral_species(care_level);
CREATE INDEX idx_coral_lighting ON coral_species(lighting);
CREATE INDEX idx_coral_search ON coral_species USING GIN(search_vector);
```

#### 3. 价格历史表 (price_history)
```sql
CREATE TABLE price_history (
    id SERIAL PRIMARY KEY,
    species_type VARCHAR(20) NOT NULL,     -- 'fish'/'coral'/'invertebrate'
    species_id INTEGER NOT NULL,
    price_usd DECIMAL(8,2) NOT NULL,
    price_type VARCHAR(20),               -- retail/wholesale
    size_category VARCHAR(20),            -- small/medium/large
    currency VARCHAR(3) DEFAULT 'USD',
    source VARCHAR(100),                  -- 数据来源
    source_url VARCHAR(500),
    recorded_date DATE NOT NULL,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    region VARCHAR(100),                  -- 价格地区
    notes TEXT
);

CREATE INDEX idx_price_species ON price_history(species_type, species_id);
CREATE INDEX idx_price_date ON price_history(recorded_date);
CREATE INDEX idx_price_source ON price_history(source);
```

#### 4. 图片存储表 (species_images)
```sql
CREATE TABLE species_images (
    id SERIAL PRIMARY KEY,
    species_type VARCHAR(20) NOT NULL,
    species_id INTEGER NOT NULL,
    image_path VARCHAR(500) NOT NULL,     -- 本地路径或URL
    image_url VARCHAR(500),               -- 原始URL
    thumbnail_path VARCHAR(500),
    caption TEXT,
    photographer VARCHAR(255),
    source VARCHAR(100),
    license VARCHAR(100),                 -- 版权信息
    is_primary BOOLEAN DEFAULT FALSE,
    image_type VARCHAR(50),               -- full_body/close_up/habitat/disease
    file_size_kb INTEGER,
    dimensions VARCHAR(50),               -- 1920x1080
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_images_species ON species_images(species_type, species_id);
CREATE INDEX idx_images_primary ON species_images(is_primary) WHERE is_primary = TRUE;
```

---

## 三、数据采集系统

### 1. 物种数据采集

#### FishBase 全量采集
```python
#!/usr/bin/env python3
# fishbase_collector.py

import requests
import psycopg2
import json
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

class FishBaseCollector:
    def __init__(self, db_config):
        self.base_url = "https://fishbase.ropensci.org"
        self.conn = psycopg2.connect(**db_config)
        self.cursor = self.conn.cursor()
        
    def get_all_species(self, limit=10000):
        """获取所有海水鱼物种"""
        offset = 0
        total_collected = 0
        
        marine_families = [
            "Pomacentridae", "Acanthuridae", "Pomacanthidae", "Labridae",
            "Chaetodontidae", "Serranidae", "Lutjanidae", "Chaetodontidae",
            "Apogonidae", "Blenniidae", "Gobiidae", "Callionymidae",
            "Siganidae", "Zanclidae", "Ephippidae", "Scatophagidae",
            # ... 添加更多海水鱼科
        ]
        
        for family in marine_families:
            print(f"Collecting family: {family}")
            offset = 0
            
            while True:
                try:
                    url = f"{self.base_url}/species?family={family}&limit=100&offset={offset}"
                    response = requests.get(url, timeout=30)
                    
                    if response.status_code != 200:
                        print(f"Error: {response.status_code}")
                        break
                    
                    data = response.json()
                    
                    if not data.get('data'):
                        break
                    
                    for species in data['data']:
                        self.save_species(species)
                    
                    self.conn.commit()
                    total_collected += len(data['data'])
                    offset += 100
                    
                    print(f"Collected: {total_collected} species")
                    time.sleep(0.5)  # 避免请求过快
                    
                except Exception as e:
                    print(f"Error collecting {family}: {e}")
                    break
        
        print(f"Total collected: {total_collected}")
    
    def save_species(self, species_data):
        """保存物种到数据库"""
        try:
            scientific_name = f"{species_data.get('Genus', '')} {species_data.get('Species', '')}".strip()
            
            self.cursor.execute("""
                INSERT INTO fish_species 
                (species_code, scientific_name, common_name, family, genus, 
                 source_databases, date_added, last_updated)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (species_code) DO UPDATE SET
                scientific_name = EXCLUDED.scientific_name,
                common_name = EXCLUDED.common_name,
                last_updated = EXCLUDED.last_updated
            """, (
                species_data.get('SpecCode'),
                scientific_name,
                species_data.get('FBname'),
                species_data.get('Family'),
                species_data.get('Genus'),
                ['FishBase'],
                datetime.now().date(),
                datetime.now()
            ))
        except Exception as e:
            print(f"Error saving species: {e}")

if __name__ == '__main__':
    db_config = {
        'dbname': 'marine_species',
        'user': 'postgres',
        'password': 'password',
        'host': 'localhost'
    }
    
    collector = FishBaseCollector(db_config)
    collector.get_all_species()
```

### 2. 价格数据采集（每日更新）

```python
#!/usr/bin/env python3
# price_collector.py

import requests
import psycopg2
from bs4 import BeautifulSoup
from datetime import datetime
import json

class PriceCollector:
    def __init__(self, db_config):
        self.conn = psycopg2.connect(**db_config)
        self.cursor = self.conn.cursor()
    
    def collect_from_liveaquaria(self):
        """从 LiveAquaria 采集价格"""
        # 注意：需要遵守网站的 robots.txt 和服务条款
        base_url = "https://www.liveaquaria.com/category/2/marine-fish"
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(base_url, headers=headers, timeout=30)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 解析价格数据（根据实际网页结构调整）
            products = soup.find_all('div', class_='product-item')
            
            for product in products:
                try:
                    name = product.find('h2', class_='product-title').text.strip()
                    price_text = product.find('span', class_='price').text.strip()
                    price = float(price_text.replace('$', '').replace(',', ''))
                    
                    # 匹配数据库中的物种
                    self.cursor.execute("""
                        SELECT id FROM fish_species 
                        WHERE common_name ILIKE %s OR scientific_name ILIKE %s
                        LIMIT 1
                    """, (f'%{name}%', f'%{name}%'))
                    
                    result = self.cursor.fetchone()
                    if result:
                        species_id = result[0]
                        self.save_price('fish', species_id, price, 'LiveAquaria')
                        
                except Exception as e:
                    continue
            
            self.conn.commit()
            print(f"Prices collected from LiveAquaria at {datetime.now()}")
            
        except Exception as e:
            print(f"Error collecting from LiveAquaria: {e}")
    
    def collect_from_saltwaterfish(self):
        """从 SaltwaterFish.com 采集"""
        # 类似实现...
        pass
    
    def save_price(self, species_type, species_id, price_usd, source):
        """保存价格到数据库"""
        today = datetime.now().date()
        
        # 更新主表当前价格
        if species_type == 'fish':
            self.cursor.execute("""
                UPDATE fish_species 
                SET price_retail_usd = %s, price_date = %s, price_source = %s,
                    price_history = COALESCE(price_history, '[]'::jsonb) || jsonb_build_array(
                        jsonb_build_object('date', %s, 'price', %s, 'source', %s)
                    ),
                    last_updated = %s
                WHERE id = %s
            """, (price_usd, today, source, today, price_usd, source, datetime.now(), species_id))
        
        # 插入历史记录表
        self.cursor.execute("""
            INSERT INTO price_history 
            (species_type, species_id, price_usd, price_type, source, recorded_date)
            VALUES (%s, %s, %s, 'retail', %s, %s)
        """, (species_type, species_id, price_usd, source, today))
    
    def run_daily_update(self):
        """每日价格更新"""
        print(f"Starting daily price update at {datetime.now()}")
        self.collect_from_liveaquaria()
        self.collect_from_saltwaterfish()
        # 添加更多数据源...
        print(f"Daily price update completed at {datetime.now()}")

if __name__ == '__main__':
    db_config = {
        'dbname': 'marine_species',
        'user': 'postgres',
        'password': 'password',
        'host': 'localhost'
    }
    
    collector = PriceCollector(db_config)
    collector.run_daily_update()
```

### 3. 图片下载系统

```python
#!/usr/bin/env python3
# image_downloader.py

import requests
import os
import psycopg2
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor
import hashlib

class ImageDownloader:
    def __init__(self, db_config, storage_path):
        self.conn = psycopg2.connect(**db_config)
        self.cursor = self.conn.cursor()
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)
        
        # 创建子目录
        for subdir in ['fish', 'coral', 'invertebrates']:
            os.makedirs(os.path.join(storage_path, subdir), exist_ok=True)
    
    def download_fishbase_images(self):
        """从 FishBase 下载图片"""
        self.cursor.execute("SELECT id, species_code, scientific_name FROM fish_species WHERE primary_image_path IS NULL LIMIT 100")
        species_list = self.cursor.fetchall()
        
        for species_id, spec_code, sci_name in species_list:
            try:
                # FishBase 图片 URL 格式
                image_url = f"https://www.fishbase.org/images/species/{sci_name.replace(' ', '_')}_u0.jpg"
                
                response = requests.get(image_url, timeout=30)
                if response.status_code == 200:
                    # 保存图片
                    filename = f"{sci_name.replace(' ', '_')}.jpg"
                    filepath = os.path.join(self.storage_path, 'fish', filename)
                    
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    
                    # 更新数据库
                    self.cursor.execute("""
                        UPDATE fish_species 
                        SET primary_image_path = %s, last_updated = %s
                        WHERE id = %s
                    """, (filepath, datetime.now(), species_id))
                    
                    # 记录到图片表
                    self.cursor.execute("""
                        INSERT INTO species_images 
                        (species_type, species_id, image_path, image_url, is_primary, source)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, ('fish', species_id, filepath, image_url, True, 'FishBase'))
                    
                    self.conn.commit()
                    print(f"Downloaded image for {sci_name}")
                    
            except Exception as e:
                print(f"Error downloading image for {sci_name}: {e}")
    
    def download_with_retry(self, url, max_retries=3):
        """带重试的下载"""
        for i in range(max_retries):
            try:
                response = requests.get(url, timeout=30)
                if response.status_code == 200:
                    return response.content
            except Exception as e:
                if i == max_retries - 1:
                    raise e
                time.sleep(2 ** i)  # 指数退避
        return None

if __name__ == '__main__':
    db_config = {
        'dbname': 'marine_species',
        'user': 'postgres',
        'password': 'password',
        'host': 'localhost'
    }
    
    storage_path = '/Users/carson/.openclaw/workspace/knowledge/images'
    
    downloader = ImageDownloader(db_config, storage_path)
    downloader.download_fishbase_images()
```

---

## 四、每日自动更新 Cron 配置

```bash
# crontab -e

# 每日凌晨 2:00 更新价格数据
0 2 * * * cd ~/.openclaw/workspace && python collectors/price_collector.py >> logs/price_update.log 2>&1

# 每日凌晨 3:00 下载新图片
0 3 * * * cd ~/.openclaw/workspace && python collectors/image_downloader.py >> logs/image_download.log 2>&1

# 每周日凌晨 4:00 全量数据同步
0 4 * * 0 cd ~/.openclaw/workspace && python collectors/full_sync.py >> logs/full_sync.log 2>&1

# 每日早上 8:00 生成数据报告
0 8 * * * cd ~/.openclaw/workspace && python collectors/generate_report.py >> logs/report.log 2>&1
```

---

## 五、系统部署清单

### 环境要求
```
- PostgreSQL 14+
- Python 3.9+
- Redis（可选，用于缓存）
- 存储空间：100GB+（图片）
```

### Python 依赖
```
psycopg2-binary
requests
beautifulsoup4
pandas
numpy
Pillow
schedule
```

### 安装步骤
```bash
# 1. 安装 PostgreSQL
brew install postgresql  # macOS
# 或 apt install postgresql  # Ubuntu

# 2. 创建数据库
createdb marine_species

# 3. 运行建表脚本
psql -d marine_species -f schema.sql

# 4. 安装 Python 依赖
pip install -r requirements.txt

# 5. 创建目录结构
mkdir -p collectors logs images/{fish,coral,invertebrates}

# 6. 配置 cron
crontab -e
# 添加上面的 cron 任务

# 7. 启动首次全量采集
python collectors/fishbase_collector.py
```

---

## 六、数据规模预估

| 数据类型 | 目标数量 | 存储空间 | 更新频率 |
|---------|---------|---------|---------|
| 鱼类物种 | 10,000+ | ~500MB | 月度新增 |
| 珊瑚物种 | 5,000+ | ~300MB | 月度新增 |
| 无脊椎动物 | 2,000+ | ~100MB | 月度新增 |
| 价格记录 | 1,000,000+/年 | ~2GB/年 | 每日 |
| 图片 | 20,000+ | ~50GB | 每周 |
| **总计** | **17,000+ 物种** | **~55GB** | **持续更新** |

---

*需要我开始部署这个系统吗？*
