export type DecimalString = string;

export type CostMethod = "AVG" | "FIFO";
export type AssetType = "STOCK" | "ETF" | "REIT" | "OTHER";
export type TradeSide = "BUY" | "SELL";
export type CashTxnType =
  | "DEPOSIT"
  | "WITHDRAW"
  | "DIVIDEND_CASH"
  | "DIVIDEND_STOCK"
  | "REWARD"
  | "INTEREST"
  | "FEE_REBATE"
  | "TAX_REFUND"
  | "TRADE_EXPENSE"
  | "OTHER";

export type Tag = {
  id: number;
  name: string;
  created_at: string;
  updated_at: string;
};

export type Portfolio = {
  id: number;
  name: string;
  base_currency: string;
  cost_method: CostMethod;
  created_at: string;
  updated_at: string;
};

export type PortfolioCreate = {
  name: string;
  base_currency?: string;
  cost_method?: CostMethod;
};

export type PortfolioUpdate = {
  name?: string;
  base_currency?: string;
  cost_method?: CostMethod;
};

export type Asset = {
  id: number;
  symbol: string;
  name: string;
  asset_type: AssetType;
  exchange: string | null;
  currency: string;
  tags: Tag[] | null;
  created_at: string;
  updated_at: string;
};

export type AssetCreate = {
  symbol: string;
  name: string;
  asset_type: AssetType;
  exchange?: string | null;
  currency?: string;
  tags?: string[] | null;
};

export type Trade = {
  id: number;
  portfolio_id: number;
  account_id: number;
  asset_id: number;
  trade_date: string;
  side: TradeSide;
  quantity: DecimalString;
  price: DecimalString;
  fee: DecimalString;
  tax: DecimalString;
  note: string | null;
  currency: string | null;
  asset_currency: string | null;
  settlement_currency: string | null;
  fx_rate: DecimalString | null;
  tags: Tag[] | null;
  created_at: string;
  updated_at: string;
};

export type TradeCreate = {
  portfolio_id: number;
  account_id: number;
  asset_id: number;
  trade_date: string;
  side: TradeSide;
  quantity: DecimalString | number;
  price: DecimalString | number;
  fee?: DecimalString | number;
  tax?: DecimalString | number;
  note?: string | null;
  currency?: string | null;
  asset_currency?: string | null;
  settlement_currency?: string | null;
  fx_rate?: DecimalString | number | null;
  tags?: string[] | null;
};

export type Position = {
  asset_id: number;
  symbol: string;
  name: string;
  currency: string;
  shares_held: DecimalString;
  avg_cost: DecimalString;
  cost_basis: DecimalString;
  last_price: DecimalString | null;
  market_value: DecimalString | null;
  unrealized_pnl: DecimalString | null;
  fx_rate_used: DecimalString | null;
  market_value_base: DecimalString | null;
  unrealized_pnl_base: DecimalString | null;
};

export type CashTransaction = {
  id: number;
  portfolio_id: number;
  account_id: number;
  asset_id: number | null;
  date: string;
  type: CashTxnType;
  amount: DecimalString;
  withholding_tax: DecimalString;
  shares: DecimalString | null;
  note: string | null;
  created_at: string;
  updated_at: string;
};

export type CashTransactionCreate = {
  portfolio_id: number;
  account_id: number;
  asset_id?: number | null;
  date: string;
  type: CashTxnType;
  amount: DecimalString | number;
  withholding_tax?: DecimalString | number;
  shares?: DecimalString | number | null;
  note?: string | null;
};

export type PnLSummary = {
  realized_pnl: DecimalString;
  income_total: DecimalString;
  income_dividend: DecimalString;
  income_reward: DecimalString;
  unrealized_pnl: DecimalString;
  price_return: DecimalString;
  total_return: DecimalString;
  invested_cashflow: DecimalString;
};

export type DashboardStats = {
  total_net_worth: number;
  day_change_amount: number;
  day_change_percent: number;
  total_pnl: number;
  cash_balance: number;
};
