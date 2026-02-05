
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
