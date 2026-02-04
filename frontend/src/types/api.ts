export type Portfolio = {
  id: number
  name: string
  cash_balance: number
}

export type Asset = {
  symbol: string
  name: string
  current_price: number
}

export type Position = {
  asset: Asset
  quantity: number
  average_cost: number
  current_value: number
  unrealized_pnl: number
}

export type Trade = {
  date: string
  type: string
  symbol: string
  quantity: number
  price: number
  fee: number
}
