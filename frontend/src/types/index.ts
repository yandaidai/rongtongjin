// 用户相关
export interface User {
  id: number;
  phone: string;
  nickname: string | null;
  avatar: string | null;
  status: boolean;
  created_at: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface UserRegister {
  phone: string;
  code: string;
  agree_protocol: boolean;
}

export interface UserLogin {
  phone: string;
  code: string;
}

export interface UserAvatarUpdate {
  avatar: string;
}

export interface UserNicknameUpdate {
  nickname: string;
}

export interface UserPasswordUpdate {
  password: string;
}

// 品种
export interface MetalProduct {
  id: number;
  code: string;
  name: string;
  unit: string;
  status: boolean;
  created_at: string;
}

// 行情
export interface MetalQuote {
  id: number;
  product_id: number;
  price: number;
  open: number | null;
  high: number | null;
  low: number | null;
  rise: number;
  rise_rate: number;
  quote_time: string;
}

export interface MetalProductQuote {
  product_id: number;
  product_code: string;
  product_name: string;
  market_price: number;
  sell_price: number;
  buy_back_price: number;
  sell_add_price: number;
  buy_back_sub_price: number;
  rise: number;
  rise_rate: number;
  quote_time: string;
}

export interface QuoteListResponse {
  items: MetalQuote[];
  total: number;
}

// K 线
export interface MetalKline {
  id: number;
  product_id: number;
  k_type: string;
  open_price: number;
  high_price: number;
  low_price: number;
  close_price: number;
  volume: number;
  k_time: string;
}

export interface KlineListResponse {
  items: MetalKline[];
  total: number;
}

// 点差配置
export interface GlobalConfig {
  id: number;
  product_id: number;
  sell_add_price: number;
  buy_back_sub_price: number;
  status: boolean;
  create_time: string;
}

export interface GlobalConfigUpdate {
  sell_add_price?: number;
  buy_back_sub_price?: number;
}

export interface UserConfig {
  id: number;
  user_id: number;
  product_id: number;
  sell_add_price: number;
  buy_back_sub_price: number;
  status: boolean;
  create_time: string;
}

export interface UserConfigUpdate {
  product_id: number;
  sell_add_price?: number;
  buy_back_sub_price?: number;
}

// 预警
export interface MetalWarn {
  id: number;
  user_id: number;
  product_id: number;
  upper_limit: number | null;
  lower_limit: number | null;
  warn_enable: boolean;
  upper_trigger: boolean;
  lower_trigger: boolean;
  create_time: string;
}

export interface WarnCreate {
  product_id: number;
  upper_limit?: number | null;
  lower_limit?: number | null;
  warn_enable: boolean;
}

export interface WarnUpdate {
  upper_limit?: number | null;
  lower_limit?: number | null;
  warn_enable?: boolean;
}

// API 通用
export interface ApiError {
  detail: string;
}
