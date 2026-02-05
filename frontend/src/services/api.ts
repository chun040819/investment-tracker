import apiClient from "@/lib/api-client";
import type {
  Asset,
  CashTransaction,
  CashTransactionCreate,
  DashboardStats,
  PnLSummary,
  Portfolio,
  Position,
  Trade,
  TradeCreate,
} from "@/types/api";

const toNumber = (value: string | null | undefined): number => {
  if (value == null) {
    return 0;
  }
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : 0;
};

const sumMarketValue = (positions: Position[]): number =>
  positions.reduce((sum, position) => sum + toNumber(position.market_value), 0);

const formatDate = (date: Date): string => date.toISOString().slice(0, 10);

export async function getPortfolios(): Promise<Portfolio[]> {
  const { data } = await apiClient.get<Portfolio[]>("/portfolios");
  return data;
}

export async function getPortfolioPositions(portfolioId: number): Promise<Position[]> {
  const { data } = await apiClient.get<Position[]>("/reports/positions", {
    params: { portfolio_id: portfolioId },
  });
  return data;
}

export async function createTrade(payload: TradeCreate): Promise<Trade> {
  const { data } = await apiClient.post<Trade>("/trades", payload);
  return data;
}

export async function getCashTransactions(): Promise<CashTransaction[]> {
  const { data } = await apiClient.get<CashTransaction[]>("/cash-transactions");
  return data;
}

export async function createCashTransaction(
  payload: CashTransactionCreate
): Promise<CashTransaction> {
  const { data } = await apiClient.post<CashTransaction>("/cash-transactions", payload);
  return data;
}

export async function getAssets(symbol?: string): Promise<Asset[]> {
  const { data } = await apiClient.get<Asset[]>("/assets", {
    params: symbol ? { symbol } : undefined,
  });
  return data;
}

export async function getDashboardStats(): Promise<DashboardStats> {
  const portfolios = await getPortfolios();
  if (!portfolios.length) {
    return {
      total_net_worth: 0,
      day_change_amount: 0,
      day_change_percent: 0,
      total_pnl: 0,
      cash_balance: 0,
    };
  }

  const portfolioId = portfolios[0].id;
  const today = new Date();
  const yesterday = new Date(today);
  yesterday.setDate(today.getDate() - 1);

  const [positionsToday, positionsYesterday, cashTransactions, pnlSummaryResp] =
    await Promise.all([
      apiClient.get<Position[]>("/reports/positions", {
        params: { portfolio_id: portfolioId, as_of: formatDate(today) },
      }),
      apiClient.get<Position[]>("/reports/positions", {
        params: { portfolio_id: portfolioId, as_of: formatDate(yesterday) },
      }),
      apiClient.get<CashTransaction[]>("/cash-transactions", {
        params: { portfolio_id: portfolioId },
      }),
      apiClient.get<PnLSummary>("/reports/pnl/summary", {
        params: {
          portfolio_id: portfolioId,
          from: "1970-01-01",
          to: formatDate(today),
          as_of: formatDate(today),
        },
      }),
    ]);

  const marketValueToday = sumMarketValue(positionsToday.data);
  const marketValueYesterday = sumMarketValue(positionsYesterday.data);
  const cashBalance = cashTransactions.data.reduce(
    (sum, txn) => sum + toNumber(txn.amount),
    0
  );
  const dayChangeAmount = marketValueToday - marketValueYesterday;
  const dayChangePercent =
    marketValueYesterday === 0 ? 0 : (dayChangeAmount / marketValueYesterday) * 100;

  return {
    total_net_worth: marketValueToday + cashBalance,
    day_change_amount: dayChangeAmount,
    day_change_percent: dayChangePercent,
    total_pnl: toNumber(pnlSummaryResp.data.total_return),
    cash_balance: cashBalance,
  };
}
