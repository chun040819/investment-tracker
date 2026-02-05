
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
