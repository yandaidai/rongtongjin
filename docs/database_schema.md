# 融通金 数据库设计

## 用户表 (users)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT (PK) | 主键 |
| phone | VARCHAR(20) | 手机号，唯一 |
| nickname | VARCHAR(50) | 用户昵称 |
| avatar | VARCHAR(255) | 用户头像URL |
| hashed_password | VARCHAR(255) | 密码哈希（可为空） |
| status | BOOLEAN | 状态：1-正常 0-禁用 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

## 贵金属品种表 (metal_product)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT (PK) | 主键 |
| code | VARCHAR(50) | 品种代码，如 Au99.99 |
| name | VARCHAR(100) | 品种名称，如黄金99.99 |
| unit | VARCHAR(20) | 计价单位，默认元/克 |
| status | BOOLEAN | 状态：1-启用 0-禁用 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

## 默认点差配置表 (metal_global_config)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT (PK) | 主键 |
| product_id | INT (FK) | 贵金属品种ID |
| sell_add_price | FLOAT | 销售价加点（元/克），默认3.0 |
| buy_back_sub_price | FLOAT | 回购价减点（元/克），默认2.0 |
| status | BOOLEAN | 状态：1-启用 0-禁用 |
| create_time | DATETIME | 创建时间 |
| update_time | DATETIME | 更新时间 |

## 用户自定义点差配置表 (metal_user_config)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT (PK) | 主键 |
| user_id | INT (FK) | 用户ID |
| product_id | INT (FK) | 贵金属品种ID |
| sell_add_price | FLOAT | 用户自定义销售价加点（元/克） |
| buy_back_sub_price | FLOAT | 用户自定义回购价减点（元/克） |
| status | BOOLEAN | 状态：1-启用 0-禁用 |
| create_time | DATETIME | 创建时间 |
| update_time | DATETIME | 更新时间 |

## 实时行情表 (metal_quote)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT (PK) | 主键 |
| product_id | INT (FK) | 贵金属品种ID |
| price | FLOAT | 大盘价（元/克） |
| open | FLOAT | 开盘价 |
| high | FLOAT | 最高价 |
| low | FLOAT | 最低价 |
| rise | FLOAT | 涨跌额 |
| rise_rate | FLOAT | 涨跌幅% |
| quote_time | DATETIME | 行情时间 |
| update_time | DATETIME | 更新时间 |

## K线数据表 (metal_kline)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT (PK) | 主键 |
| product_id | INT (FK) | 贵金属品种ID |
| k_type | VARCHAR(20) | K线类型：minute/two_day/day/week/month |
| open_price | FLOAT | 开盘价 |
| high_price | FLOAT | 最高价 |
| low_price | FLOAT | 最低价 |
| close_price | FLOAT | 收盘价 |
| volume | FLOAT | 成交量 |
| k_time | DATETIME | K线时间 |
| create_time | DATETIME | 创建时间 |

## 用户价格预警表 (metal_warn)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT (PK) | 主键 |
| user_id | INT (FK) | 用户ID |
| product_id | INT (FK) | 贵金属品种ID |
| upper_limit | FLOAT | 最高阀值 |
| lower_limit | FLOAT | 最低阀值 |
| warn_enable | BOOLEAN | 是否启用预警 |
| upper_trigger | BOOLEAN | 最高阀值是否已触发 |
| lower_trigger | BOOLEAN | 最低阀值是否已触发 |
| create_time | DATETIME | 创建时间 |
| update_time | DATETIME | 更新时间 |
