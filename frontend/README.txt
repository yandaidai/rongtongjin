融通金 App - 前端项目说明
=============================
项目路径: frontend/
技术栈: React Native (Expo) + TypeScript


一、项目文件结构
-----------------

frontend/
├── App.tsx                              # 入口：AuthProvider + Navigation
├── app.json                             # Expo 配置
├── package.json                         # 依赖管理
├── tsconfig.json                        # TypeScript 配置
├── babel.config.js                      # Babel 配置
├── .gitignore                           # Git 忽略规则
│
└── src/
    ├── types/index.ts                   # 31 个 TS 接口，覆盖全部 API 响应
    │
    ├── api/client.ts                    # API 客户端，自动管理 JWT Token（AsyncStorage 持久化）
    │
    ├── store/AuthContext.tsx             # 全局认证状态 Context
    │
    ├── components/
    │   ├── ProductCard.tsx              # 产品报价卡片（大盘价 + 销售价 + 回购价）
    │   ├── QuoteCard.tsx                # 行情卡片（最新价 + 涨跌 + 开高低）
    │   ├── KlineChart.tsx               # K 线简易折线图组件
    │   └── Loading.tsx                  # 加载中组件
    │
    ├── screens/
    │   ├── LoginScreen.tsx              # 手机验证码登录
    │   ├── RegisterScreen.tsx           # 注册 + 同意协议 + 隐私政策
    │   ├── ProductsScreen.tsx           # 产品价格展示页
    │   ├── DomesticQuotesScreen.tsx     # 国内大盘行情页
    │   ├── InternationalQuotesScreen.tsx# 国际大盘行情页
    │   ├── KlineScreen.tsx              # K 线图页（分时/两日/日K/周K/月K）
    │   ├── ProfileScreen.tsx            # 个人中心（头像/昵称/密码/注销）
    │   ├── SpreadConfigScreen.tsx        # 销售价&回购价点差配置
    │   ├── WarnListScreen.tsx           # 预警列表 + 开关
    │   └── WarnCreateScreen.tsx         # 新建/编辑预警
    │
    └── navigation/
        └── AppNavigator.tsx             # 底部 Tab 导航（4 tab）+ Stack 导航


二、页面与需求对应关系
-----------------------

需求文档章节     | 页面                    | 功能说明
----------------|------------------------|-------------------------------------------
1. 产品价格显示   | ProductsScreen         | 显示所有品种大盘价、销售价、回购价、涨跌幅
2. 国内大盘行情   | DomesticQuotesScreen   | 黄金9999、黄金延期、白银延期、铂金9995
3. 国际大盘行情   | InternationalQuotesScreen | 现货黄金/白银/铂金、COMEX 等
4/5. 回购价/销售价K线图 | KlineScreen    | 分时/两日/日K/周K/月K 切换 + 价格记录列表 + 预警入口
6. 用户登录/注册  | LoginScreen + RegisterScreen | 手机验证码 + 同意协议
7. 用户个人中心   | ProfileScreen          | 修改昵称、设置密码、点差配置、预警管理、注销账号
8. 点差配置      | SpreadConfigScreen     | 选择品种自定义销售价加点/回购价减点
-              | WarnListScreen         | 查看/开关/删除价格预警
-              | WarnCreateScreen       | 新建/编辑价格预警（选择品种 + 阀值）


三、页面导航流
---------------

未登录:
  LoginScreen ←→ RegisterScreen

登录后:
  Tab 导航:
    ├── 首页 (ProductsScreen) ──点击产品──→ KlineScreen ──设置提醒──→ WarnCreateScreen
    ├── 国内 (DomesticQuotesScreen)
    ├── 国际 (InternationalQuotesScreen) ──点击产品──→ KlineScreen
    └── 我的 (ProfileScreen)
                  ├── 点差配置 ──→ SpreadConfigScreen
                  └── 价格预警 ──→ WarnListScreen ──添加/编辑──→ WarnCreateScreen


四、启动方式
---------------

1. 安装依赖:
   cd frontend
   npm install

2. 启动 Expo 开发服务器:
   npx expo start

3. 运行方式:
   - 按 i 打开 iOS 模拟器
   - 按 a 打开 Android 模拟器
   - 用手机扫码打开 Expo Go App
   - 按 w 在浏览器中运行

4. 前置条件:
   - 后端服务已启动（默认 http://localhost:8000）
   - 后端已运行 python seed.py 初始化品种数据


五、重要提示
---------------

1. API 地址配置:
   后端地址在 src/api/client.ts 第 5 行配置（BASE_URL）
   默认值: http://localhost:8000/api
   部署时需改为实际服务器地址

2. 验证码:
   开发环境固定验证码为 123456
   生产环境需接入真实短信服务（修改 src/screens/LoginScreen.tsx 和 RegisterScreen.tsx）

3. 依赖安装失败:
   如果 npm install 报错，尝试:
   npm install --legacy-peer-deps
   或使用 yarn:
   yarn install

4. 后端 API 端点列表（供前端调试参考）:
   POST   /api/auth/register       注册
   POST   /api/auth/login          登录
   GET    /api/auth/user/info      获取用户信息
   PATCH  /api/auth/user/avatar    修改头像
   PATCH  /api/auth/user/nickname  修改昵称
   POST   /api/auth/user/password  设置密码
   DELETE /api/auth/user/account   注销账号
   GET    /api/products/           获取品种列表
   GET    /api/quotes/             获取全部行情
   GET    /api/quotes/domestic     获取国内行情
   GET    /api/quotes/international 获取国际行情
   GET    /api/quotes/history      获取历史行情
   GET    /api/klines/             获取K线数据
   GET    /api/klines/latest       获取最新K线
   GET    /api/global/config/      获取全局点差配置
   PATCH  /api/global/config/{id}  更新全局点差
   GET    /api/user/config/        获取用户点差配置
   POST   /api/user/config/        创建/更新用户点差
   GET    /api/user/warn/          获取预警列表
   POST   /api/user/warn/          创建预警
   PATCH  /api/user/warn/{id}      更新预警
   DELETE /api/user/warn/{id}      删除预警

5. 配色说明:
   主色调: 金色 (#d4a84b) — 对应黄金交易主题
   涨: 红色 (#e74c3c)；跌: 绿色 (#2ecc71)
