# 融通金 API 接口文档

Base URL: `http://localhost:8000/api`

## 认证接口

### 用户注册（手机验证码）
- **POST** `/api/auth/register`
- Body: `{ phone, code, agree_protocol }`
- Response: `{ access_token, token_type, user }`

### 用户登录（手机验证码）
- **POST** `/api/auth/login`
- Body: `{ phone, code }`
- Response: `{ access_token, token_type, user }`

### 获取用户信息
- **GET** `/api/auth/user/info`
- Header: `Authorization: Bearer <token>`
- Response: `{ id, phone, nickname, avatar, status, created_at }`

### 设置用户头像
- **PATCH** `/api/auth/user/avatar`
- Header: `Authorization: Bearer <token>`
- Body: `{ avatar }`

### 设置用户昵称
- **PATCH** `/api/auth/user/nickname`
- Header: `Authorization: Bearer <token>`
- Body: `{ nickname }`

### 设置密码
- **POST** `/api/auth/user/password`
- Header: `Authorization: Bearer <token>`
- Body: `{ password }`

### 注销账号
- **DELETE** `/api/auth/user/account`
- Header: `Authorization: Bearer <token>`

## 贵金属品种

### 获取所有品种
- **GET** `/api/products/`
- Response: `[{ id, code, name, unit, status, created_at }]`

## 实时行情

### 获取所有产品报价（含销售价、回购价、点差）
- **GET** `/api/quotes/`
- Header: `Authorization: Bearer <token>` (可选，登录后使用用户自定义点差)
- Response: `[{ product_id, product_code, product_name, market_price, sell_price, buy_back_price, sell_add_price, buy_back_sub_price, rise, rise_rate, quote_time }]`

### 获取历史行情
- **GET** `/api/quotes/history?product_id=1&limit=10`
- Response: `[{ id, product_id, price, open, high, low, rise, rise_rate, quote_time }]`

## K线数据

### 获取K线数据
- **GET** `/api/klines/?product_id=1&k_type=day&limit=100`
- k_type: minute-分钟, two_day-两日, day-日K, week-周K, month-月K
- Response: `[{ id, product_id, k_type, open_price, high_price, low_price, close_price, volume, k_time }]`

### 获取最新K线记录
- **GET** `/api/klines/latest?product_id=1&k_type=minute&limit=10`

## 全局点差配置

### 获取所有默认点差配置
- **GET** `/api/global/config/`
- Response: `[{ id, product_id, sell_add_price, buy_back_sub_price, status, create_time }]`

### 获取指定品种默认点差
- **GET** `/api/global/config/{product_id}`

### 更新指定品种默认点差
- **PATCH** `/api/global/config/{product_id}`
- Body: `{ sell_add_price?, buy_back_sub_price? }`

## 用户自定义点差配置

### 获取用户所有自定义点差
- **GET** `/api/user/config/`
- Header: `Authorization: Bearer <token>`

### 创建/更新用户自定义点差
- **POST** `/api/user/config/`
- Header: `Authorization: Bearer <token>`
- Body: `{ product_id, sell_add_price?, buy_back_sub_price? }`

## 价格预警

### 获取用户所有预警
- **GET** `/api/user/warn/`
- Header: `Authorization: Bearer <token>`

### 获取单个预警
- **GET** `/api/user/warn/{warn_id}`
- Header: `Authorization: Bearer <token>`

### 创建预警
- **POST** `/api/user/warn/`
- Header: `Authorization: Bearer <token>`
- Body: `{ product_id, upper_limit?, lower_limit?, warn_enable }`

### 更新预警
- **PATCH** `/api/user/warn/{warn_id}`
- Header: `Authorization: Bearer <token>`
- Body: `{ upper_limit?, lower_limit?, warn_enable? }`

### 删除预警
- **DELETE** `/api/user/warn/{warn_id}`
- Header: `Authorization: Bearer <token>`
