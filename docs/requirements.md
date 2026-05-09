# 融通金 App 需求文档

## 核心业务功能

### 1. 产品价格显示模块
- 实时获取国内黄金、白银、铂金等商品大盘价格（元/克）
- 根据国内黄金、白银、铂金大盘价格，获取商品的回购价以及销售价
- 商品回购价 = 当日大盘价 - 回购价点差
- 商品销售价 = 当日大盘价 + 销售价点差
- 回购价点差默认为2，可在配置页面配置
- 销售价点差默认为3，同样可在配置页面配置
- 价格更新频率：每分钟通过akshare模块刷新商品大盘价格从而刷新商品的回购价以及销售价

### 2. 国内大盘行情显示模块
- 实时获取国内黄金9999、黄金延期、白银延期、铂金9995的大盘价格
- 显示黄金9999、黄金延期、白银延期、铂金9995当日的最新价、涨跌、涨跌幅

### 3. 国际大盘行情显示模块
- 实时获取国际现货黄金、现货白银、现货铂金、美黄金、美白银、美铂金的大盘价格
- 显示国际现货黄金、现货白银、现货铂金、美黄金、美白银、美铂金的最新价、涨跌、涨跌幅

### 4. 商品回购价k图模块
- 从产品价格显示页面、国内行情页面、国际行情页面点击商品回购价后，进入商品回购价k图页面
- 页面实时显示该商品回购价，显示当前价格与前一次价格的差以及涨跌幅百分比
- 页面显示当日最高价格、最低价格，当日开盘时价格，昨日收盘时价格
- 按照分时、两日、日k、周k、月k、分钟这几种模式，构建k图
- 显示最新的10条价格记录，包括时间节点与价格
- 点击提醒功能，可以设置最高/最低阀值，超过阀值会提醒用户

### 5. 商品销售价k图
- 从产品价格显示页面、国内行情页面、国际行情页面点击商品销售价后，进入商品销售价k图页面
- 页面实时显示该商品销售价，显示当前价格与前一次价格的差以及涨跌幅百分比
- 页面显示当日销售价的最高价格、最低价格，当日开盘时价格，昨日收盘时价格
- 按照分时、两日、日k、周k、月k、分钟这几种模式，构建k图
- 显示最新的10条价格记录，包括时间节点与价格
- 点击提醒功能，可以设置最高/最低阀值，超过阀值会提醒用户

### 6. 用户登录/注册模块
- 用户使用手机验证码方式注册、登录，注册后即为登录成功
- 需要同意用户使用协议和隐私政策才能点击登录
- 点击用户使用协议弹窗显示查看用户使用协议
- 点击隐私政策弹窗显示查看隐私政策

### 7. 用户个人中心模块
- 显示基本资料：用户头像、用户昵称、用户ID
- 显示用户绑定的手机号码
- 点击设置密码按钮可以进行密码设置
- 点击注销账号按钮可以进行账号注销

### 8. 销售价&回购价点差配置模块
- 用户登录后可在用户个人中心中找到点差配置页面，然后选择贵金属进行销售价&回购价点差配置

## 数据实体

### 用户表 (users)
- id, phone, nickname, avatar, status, created_at, updated_at

### 贵金属品种表 (metal_product)
- id, code, name, unit, status, created_at, updated_at

### 默认贵金属销售价&回购价点差 (metal_global_config)
- id, product_id, sell_add_price, buy_back_sub_price, status, create_time, update_time

### 用户自定义贵金属销售价&回购价点差 (metal_user_config)
- id, user_id, product_id, sell_add_price, buy_back_sub_price, status, create_time, update_time

### 实时行情表 (metal_quote)
- id, product_id, price, open, high, low, rise, rise_rate, quote_time, update_time

### K 线数据表 (metal_kline)
- id, product_id, k_type, open_price, high_price, low_price, close_price, volume, k_time, create_time

### 用户价格预警表 (metal_warn)
- id, user_id, product_id, upper_limit, lower_limit, warn_enable, upper_trigger, lower_trigger, create_time, update_time

## 接口需求

### 后端 API（FastAPI）

| 端点 | 方法 | 功能 |
|------|------|------|
| /api/auth/login | POST | 手机号登录 |
| /api/auth/user/info | GET | 获取用户信息 |
| /api/auth/user/avatar | PATCH | 设置用户头像 |
| /api/auth/user/nickname | PATCH | 设置用户昵称 |
| /api/global/config | GET | 获取默认销售价&回购价点差 |
| /api/products | GET | 获取贵金属 |
| /api/quotes | GET | 获取实时行情（销售价、回购价、点差） |
| /api/klines | GET | 获取K线数据 |
| /api/user/config | GET | 获取用户销售价&回购价点差 |
| /api/user/warn | GET | 获取用户预警信息 |
| /api/user/warn | PATCH | 设置用户预警信息 |
| /api/user/warn | DELETE | 删除用户预警信息 |

## 非功能需求
- 响应时间 < 500ms
- 需考虑并发估价请求
- 核心功能覆盖率 >= 95%