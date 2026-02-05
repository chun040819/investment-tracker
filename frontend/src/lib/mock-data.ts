
export const KPIData = {
  totalNetWorth: {
    value: 1250000,
    change: 12.5,
    changeType: "profit", // or 'loss'
  },
  dayChange: {
    value: 15000,
    change: 1.2,
    changeType: "profit",
  },
  totalProfitLoss: {
    value: 450000,
    change: 56.0,
    changeType: "profit",
  },
  cashBalance: {
    value: 50000,
    change: -2.3,
    changeType: "loss",
  },
};

export const NetWorthHistoryData = [
  { date: "Jan", value: 1000000 },
  { date: "Feb", value: 1050000 },
  { date: "Mar", value: 1020000 },
  { date: "Apr", value: 1100000 },
  { date: "May", value: 1150000 },
  { date: "Jun", value: 1120000 },
  { date: "Jul", value: 1200000 },
  { date: "Aug", value: 1250000 },
];

export const AllocationData = [
  { name: "Stocks", value: 60, color: "#10b981" }, // profit color (emerald-500 approx)
  { name: "ETFs", value: 30, color: "#3b82f6" }, // blue-500
  { name: "Cash", value: 10, color: "#f59e0b" }, // amber-500
];

export const RecentActivityData = [
  {
    id: 1,
    type: "Buy",
    asset: "AAPL",
    amount: 1500,
    date: "2023-10-25",
    status: "Completed",
  },
  {
    id: 2,
    type: "Dividend",
    asset: "VTI",
    amount: 450,
    date: "2023-10-24",
    status: "Completed",
  },
  {
    id: 3,
    type: "Deposit",
    asset: "USD",
    amount: 5000,
    date: "2023-10-22",
    status: "Completed",
  },
  {
    id: 4,
    type: "Sell",
    asset: "TSLA",
    amount: 2000,
    date: "2023-10-20",
    status: "Completed",
  },
  {
    id: 5,
    type: "Buy",
    asset: "MSFT",
    amount: 3200,
    date: "2023-10-18",
    status: "Completed",
  },
];

export const PortfolioData = [
  {
    symbol: "AAPL",
    name: "Apple Inc.",
    quantity: 150,
    avgCost: 145.50,
    currentPrice: 173.50,
  },
  {
    symbol: "MSFT",
    name: "Microsoft Corp.",
    quantity: 80,
    avgCost: 280.00,
    currentPrice: 330.20,
  },
  {
    symbol: "VTI",
    name: "Vanguard Total Stock Market",
    quantity: 200,
    avgCost: 205.10,
    currentPrice: 215.30,
  },
  {
    symbol: "TSLA",
    name: "Tesla Inc.",
    quantity: 50,
    avgCost: 250.00,
    currentPrice: 210.00, // Loss example
  },
  {
    symbol: "NVDA",
    name: "NVIDIA Corp.",
    quantity: 30,
    avgCost: 350.00,
    currentPrice: 450.00,
  },
  {
    symbol: "AMZN",
    name: "Amazon.com Inc.",
    quantity: 100,
    avgCost: 130.00,
    currentPrice: 128.50, // Small loss example
  },
  {
    symbol: "GOOGL",
    name: "Alphabet Inc.",
    quantity: 60,
    avgCost: 110.00,
    currentPrice: 135.00,
  },
];

export const AssetPriceHistory = [
  { date: "2023-01-01", price: 150 },
  { date: "2023-02-01", price: 155 },
  { date: "2023-03-01", price: 148 },
  { date: "2023-04-01", price: 160 },
  { date: "2023-05-01", price: 165 },
  { date: "2023-06-01", price: 170 },
  { date: "2023-07-01", price: 175 },
  { date: "2023-08-01", price: 172 },
  { date: "2023-09-01", price: 180 },
  { date: "2023-10-01", price: 178 },
  { date: "2023-11-01", price: 185 },
  { date: "2023-12-01", price: 190 },
];

export const AssetActivityData = [
  {
    id: 101,
    type: "Buy",
    asset: "AAPL",
    amount: 15000,
    price: 150.00,
    quantity: 100,
    date: "2023-01-15",
    status: "Completed",
  },
  {
    id: 102,
    type: "Buy",
    asset: "AAPL",
    amount: 7750,
    price: 155.00,
    quantity: 50,
    date: "2023-06-20",
    status: "Completed",
  },
  {
    id: 103,
    type: "Dividend",
    asset: "AAPL",
    amount: 25.50,
    price: 0,
    quantity: 0,
    date: "2023-08-10",
    status: "Completed",
  },
];

export const CashSummaryData = {
  totalBalance: 50000.00,
  ytdNetInflow: 12500.00,
  ytdDividends: 450.25,
};

export const CashTransactionsData = [
  {
    id: "c1",
    date: "2023-11-01",
    type: "Deposit",
    amount: 5000.00,
    currency: "USD",
    note: "Monthly savings",
  },
  {
    id: "c2",
    date: "2023-10-25",
    type: "Trade", // Buy AAPL
    amount: -1500.00,
    currency: "USD",
    note: "Buy 10 AAPL @ $150",
  },
  {
    id: "c3",
    date: "2023-10-24",
    type: "Dividend",
    amount: 45.25,
    currency: "USD",
    note: "VTI Q3 Dividend",
  },
  {
    id: "c4",
    date: "2023-10-15",
    type: "Withdrawal",
    amount: -2000.00,
    currency: "USD",
    note: "Emergency fund transfer",
  },
  {
    id: "c5",
    date: "2023-10-01",
    type: "Interest",
    amount: 12.50,
    currency: "USD",
    note: "High Yield Savings Interest",
  },
  {
    id: "c6",
    date: "2023-09-15",
    type: "Trade", // Sell TSLA
    amount: 4200.00,
    currency: "USD",
    note: "Sell 20 TSLA @ $210",
  }
];

export const DividendHistory = [
  { month: "Jan", amount: 45.00 },
  { month: "Feb", amount: 50.00 },
  { month: "Mar", amount: 55.00 },
  { month: "Apr", amount: 48.00 },
  { month: "May", amount: 60.00 },
  { month: "Jun", amount: 58.00 },
  { month: "Jul", amount: 65.00 },
  { month: "Aug", amount: 70.00 },
  { month: "Sep", amount: 72.00 },
  { month: "Oct", amount: 68.00 },
  { month: "Nov", amount: 75.00 },
  { month: "Dec", amount: 80.00 },
];

export const DividendByAsset = [
  { symbol: "VTI", amount: 350.00 },
  { symbol: "AAPL", amount: 150.00 },
  { symbol: "MSFT", amount: 120.00 },
  { symbol: "KO", amount: 80.00 },
  { symbol: "JNJ", amount: 65.00 },
];

export const PerformanceHistory = [
  { date: "2023-01", value: 45000, pnl: 0 },
  { date: "2023-02", value: 46000, pnl: 1000 },
  { date: "2023-03", value: 45500, pnl: 500 },
  { date: "2023-04", value: 47000, pnl: 2000 },
  { date: "2023-05", value: 48500, pnl: 3500 },
  { date: "2023-06", value: 49000, pnl: 4000 },
  { date: "2023-07", value: 50500, pnl: 5500 },
  { date: "2023-08", value: 50000, pnl: 5000 },
  { date: "2023-09", value: 51200, pnl: 6200 },
  { date: "2023-10", value: 51000, pnl: 6000 },
  { date: "2023-11", value: 52500, pnl: 7500 },
  { date: "2023-12", value: 53500, pnl: 8500 },
];

export const PerformanceMetricsData = {
  realizedPnL: 5400.00,
  unrealizedPnL: 8500.00,
  totalReturn: 13900.00,
  returnPercent: 12.5,
};

export const FeesDistribution = [
  { name: "Commissions", value: 120.00, color: "#f87171" }, // red-400
  { name: "Regulations", value: 45.00, color: "#fbbf24" }, // amber-400
  { name: "ADR Fees", value: 15.00, color: "#60a5fa" }, // blue-400
  { name: "Tax", value: 80.00, color: "#94a3b8" }, // slate-400
];

