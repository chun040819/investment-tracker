# Investment Tracker Backend API

以下整理所有 API 的功能、用法、作用與範例。範例以 `http://localhost:8000` 作為示意 Base URL。

## 基本約定
- Content-Type：`application/json`
- 日期：`YYYY-MM-DD`
- 時間：ISO 8601（例如 `2025-01-15T00:00:00Z`）
- Decimal 欄位在回應中會以字串表示（例如 `"180.50"`）

## 系統狀態

### GET /health
- 功能：健康檢查
- 用法：無參數
- 作用：回傳服務狀態字串
- 範例：
```bash
curl -s http://localhost:8000/health
```
```json
{"status":"ok"}
```

## Portfolios

### 資料模型（Portfolio）
- name: string
- base_currency: string（預設 `TWD`）
- cost_method: `AVG` | `FIFO`

### GET /portfolios
- 功能：列出所有投資組合
- 用法：無參數
- 作用：讀取資料
- 範例：
```bash
curl -s http://localhost:8000/portfolios
```
```json
[
  {
    "id": 1,
    "name": "Long Term",
    "base_currency": "TWD",
    "cost_method": "AVG",
    "created_at": "2025-01-01T00:00:00Z",
    "updated_at": "2025-01-01T00:00:00Z"
  }
]
```

### POST /portfolios
- 功能：建立投資組合
- 用法：Body 為 PortfolioCreate
- 作用：新增一筆 Portfolio；若名稱重複會回 409
- 範例：
```bash
curl -s -X POST http://localhost:8000/portfolios \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Long Term",
    "base_currency": "TWD",
    "cost_method": "AVG"
  }'
```

### GET /portfolios/{portfolio_id}
- 功能：取得單一投資組合
- 用法：Path 參數 `portfolio_id`
- 作用：讀取單筆資料
- 範例：
```bash
curl -s http://localhost:8000/portfolios/1
```

### PUT /portfolios/{portfolio_id}
- 功能：更新投資組合
- 用法：Path 參數 `portfolio_id`，Body 為 PortfolioUpdate
- 作用：更新指定 Portfolio
- 範例：
```bash
curl -s -X PUT http://localhost:8000/portfolios/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Long Term (TWD)",
    "cost_method": "FIFO"
  }'
```

### DELETE /portfolios/{portfolio_id}
- 功能：刪除投資組合
- 用法：Path 參數 `portfolio_id`
- 作用：刪除指定 Portfolio（若不存在回 404）
- 範例：
```bash
curl -s -X DELETE http://localhost:8000/portfolios/1
```

## Accounts

### 資料模型（Account）
- name: string
- currency: string
- note: string | null
- portfolio_id: int（建立時必填）

### GET /accounts
- 功能：列出帳戶
- 用法：Query `portfolio_id`（可選）
- 作用：可依 portfolio 過濾
- 範例：
```bash
curl -s "http://localhost:8000/accounts?portfolio_id=1"
```

### POST /accounts
- 功能：建立帳戶
- 用法：Body 為 AccountCreate
- 作用：新增一筆 Account
- 範例：
```bash
curl -s -X POST http://localhost:8000/accounts \
  -H "Content-Type: application/json" \
  -d '{
    "portfolio_id": 1,
    "name": "Broker A",
    "currency": "USD",
    "note": "Main"
  }'
```

### GET /accounts/{account_id}
- 功能：取得單一帳戶
- 用法：Path 參數 `account_id`
- 作用：讀取單筆資料
- 範例：
```bash
curl -s http://localhost:8000/accounts/10
```

### PUT /accounts/{account_id}
- 功能：更新帳戶
- 用法：Path 參數 `account_id`，Body 為 AccountUpdate
- 作用：更新指定 Account
- 範例：
```bash
curl -s -X PUT http://localhost:8000/accounts/10 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Broker A (USD)",
    "note": "Primary broker"
  }'
```

### DELETE /accounts/{account_id}
- 功能：刪除帳戶
- 用法：Path 參數 `account_id`
- 作用：刪除指定 Account
- 範例：
```bash
curl -s -X DELETE http://localhost:8000/accounts/10
```

## Assets

### 資料模型（Asset）
- symbol: string
- name: string
- asset_type: `STOCK` | `ETF` | `REIT` | `OTHER`
- exchange: string | null
- currency: string（預設 `USD`）
- tags: string[] | null（僅建立時可傳入，會自動建立不存在的 Tag）

### GET /assets
- 功能：列出資產
- 用法：Query `symbol`（可選）
- 作用：可依 symbol 過濾
- 範例：
```bash
curl -s "http://localhost:8000/assets?symbol=AAPL"
```

### POST /assets
- 功能：建立資產
- 用法：Body 為 AssetCreate
- 作用：新增 Asset；(symbol, exchange) 唯一
- 範例：
```bash
curl -s -X POST http://localhost:8000/assets \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "AAPL",
    "name": "Apple Inc.",
    "asset_type": "STOCK",
    "exchange": "NASDAQ",
    "currency": "USD",
    "tags": ["tech", "us"]
  }'
```

### GET /assets/{asset_id}
- 功能：取得單一資產
- 用法：Path 參數 `asset_id`
- 作用：讀取單筆資料
- 範例：
```bash
curl -s http://localhost:8000/assets/100
```

### PUT /assets/{asset_id}
- 功能：更新資產
- 用法：Path 參數 `asset_id`，Body 為 AssetUpdate
- 作用：更新資產基本資料（Update schema 不包含 tags）
- 範例：
```bash
curl -s -X PUT http://localhost:8000/assets/100 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Apple Inc. (US)",
    "exchange": "NASDAQ"
  }'
```

### DELETE /assets/{asset_id}
- 功能：刪除資產
- 用法：Path 參數 `asset_id`
- 作用：刪除指定 Asset
- 範例：
```bash
curl -s -X DELETE http://localhost:8000/assets/100
```

## Tags

### 資料模型（Tag）
- name: string

### GET /tags
- 功能：列出標籤
- 用法：無參數
- 作用：依名稱排序
- 範例：
```bash
curl -s http://localhost:8000/tags
```

### POST /tags
- 功能：建立標籤
- 用法：Body 為 TagCreate
- 作用：新增 Tag；若重複會回 409
- 範例：
```bash
curl -s -X POST http://localhost:8000/tags \
  -H "Content-Type: application/json" \
  -d '{
    "name": "tech"
  }'
```

### GET /tags/{tag_id}
- 功能：取得單一標籤
- 用法：Path 參數 `tag_id`
- 作用：讀取單筆資料
- 範例：
```bash
curl -s http://localhost:8000/tags/5
```

### PUT /tags/{tag_id}
- 功能：更新標籤
- 用法：Path 參數 `tag_id`，Body 為 TagUpdate
- 作用：更新標籤名稱
- 範例：
```bash
curl -s -X PUT http://localhost:8000/tags/5 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "tech-us"
  }'
```

### DELETE /tags/{tag_id}
- 功能：刪除標籤
- 用法：Path 參數 `tag_id`
- 作用：刪除指定 Tag
- 範例：
```bash
curl -s -X DELETE http://localhost:8000/tags/5
```

## Trades

### 資料模型（Trade）
- portfolio_id: int
- account_id: int
- asset_id: int
- trade_date: date
- side: `BUY` | `SELL`
- quantity: decimal
- price: decimal
- fee: decimal（預設 0）
- tax: decimal（預設 0）
- note: string | null
- currency: string | null
- asset_currency: string | null
- settlement_currency: string | null
- fx_rate: decimal | null
- tags: string[] | null（僅建立時可傳入，會自動建立不存在的 Tag）

### GET /trades
- 功能：列出交易
- 用法：Query `portfolio_id`、`asset_id`、`account_id`、`from`、`to`（皆可選）
- 作用：可依條件與日期區間查詢
- 範例：
```bash
curl -s "http://localhost:8000/trades?portfolio_id=1&from=2025-01-01&to=2025-01-31"
```

### POST /trades
- 功能：建立交易
- 用法：Body 為 TradeCreate
- 作用：
  - SELL 不可超過可用股數
  - BUY 會檢查帳戶現金是否足夠
  - 若結算幣別與資產幣別不同且未提供 `fx_rate`，會嘗試用 FXRate 補齊，找不到則回 400
  - 若提供 `settlement_currency`，必須與 Account 幣別一致
- 範例：
```bash
curl -s -X POST http://localhost:8000/trades \
  -H "Content-Type: application/json" \
  -d '{
    "portfolio_id": 1,
    "account_id": 10,
    "asset_id": 100,
    "trade_date": "2025-01-15",
    "side": "BUY",
    "quantity": "10",
    "price": "180.50",
    "fee": "1.00",
    "tax": "0",
    "currency": "USD",
    "tags": ["core", "long-term"]
  }'
```

### PUT /trades/{trade_id}
- 功能：更新交易
- 用法：Path 參數 `trade_id`，Body 為 TradeUpdate
- 作用：
  - 若更新影響幣別或日期，會重新正規化幣別與 FX
  - SELL 仍會檢查可用股數
- 範例：
```bash
curl -s -X PUT http://localhost:8000/trades/1000 \
  -H "Content-Type: application/json" \
  -d '{
    "price": "182.00",
    "fee": "0.80"
  }'
```

### DELETE /trades/{trade_id}
- 功能：刪除交易
- 用法：Path 參數 `trade_id`
- 作用：刪除後會重建稅務批次
- 範例：
```bash
curl -s -X DELETE http://localhost:8000/trades/1000
```

## Cash Transactions

### 資料模型（CashTransaction）
- portfolio_id: int
- account_id: int
- asset_id: int | null
- date: date
- type: `DEPOSIT` | `WITHDRAW` | `DIVIDEND_CASH` | `DIVIDEND_STOCK` | `REWARD` | `INTEREST` | `FEE_REBATE` | `TAX_REFUND` | `TRADE_EXPENSE` | `OTHER`
- amount: decimal
- withholding_tax: decimal（預設 0）
- shares: decimal | null
- note: string | null

### GET /cash-transactions
- 功能：列出現金交易
- 用法：Query `portfolio_id`、`type`、`asset_id`、`from`、`to`（皆可選）
- 作用：可依條件與日期區間查詢
- 範例：
```bash
curl -s "http://localhost:8000/cash-transactions?portfolio_id=1&from=2025-01-01&to=2025-01-31"
```

### POST /cash-transactions
- 功能：建立現金交易
- 用法：Body 為 CashTransactionCreate
- 作用：會自動正規化 `amount` 正負號（DEPOSIT 為正、WITHDRAW/TRADE_EXPENSE 為負）
- 範例：
```bash
curl -s -X POST http://localhost:8000/cash-transactions \
  -H "Content-Type: application/json" \
  -d '{
    "portfolio_id": 1,
    "account_id": 10,
    "date": "2025-01-05",
    "type": "DEPOSIT",
    "amount": "10000",
    "note": "Initial funding"
  }'
```

### PUT /cash-transactions/{txn_id}
- 功能：更新現金交易
- 用法：Path 參數 `txn_id`，Body 為 CashTransactionUpdate
- 作用：若變更 `type` 或 `amount`，會重新正規化正負號
- 範例：
```bash
curl -s -X PUT http://localhost:8000/cash-transactions/2000 \
  -H "Content-Type: application/json" \
  -d '{
    "amount": "9500",
    "note": "Adjusted funding"
  }'
```

### DELETE /cash-transactions/{txn_id}
- 功能：刪除現金交易
- 用法：Path 參數 `txn_id`
- 作用：刪除指定 CashTransaction
- 範例：
```bash
curl -s -X DELETE http://localhost:8000/cash-transactions/2000
```

## Prices

### POST /prices/update
- 功能：更新價格資料
- 用法：Query `asset_id`、`start`、`end`（必填）
- 作用：抓取指定日期區間的日收盤價並 upsert
- 範例：
```bash
curl -s -X POST "http://localhost:8000/prices/update?asset_id=100&start=2025-01-01&end=2025-01-31"
```
```json
{"inserted":21,"updated":0}
```

### GET /prices/latest
- 功能：取得最新價格
- 用法：Query `asset_id`（必填）
- 作用：回傳該資產最後一筆價格
- 範例：
```bash
curl -s "http://localhost:8000/prices/latest?asset_id=100"
```
```json
{"date":"2025-01-31","close":"190.12"}
```

## FX Rates

### 資料模型（FXRate）
- date: date
- from_currency: string
- to_currency: string
- rate: decimal

### GET /fx-rates
- 功能：列出匯率
- 用法：Query `from_currency`、`to_currency`（可選）
- 作用：依日期倒序回傳
- 範例：
```bash
curl -s "http://localhost:8000/fx-rates?from_currency=USD&to_currency=TWD"
```

### POST /fx-rates
- 功能：建立匯率
- 用法：Body 為 FXRateCreate
- 作用：新增一筆 FXRate
- 範例：
```bash
curl -s -X POST http://localhost:8000/fx-rates \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2025-01-15",
    "from_currency": "USD",
    "to_currency": "TWD",
    "rate": "32.5000"
  }'
```

### GET /fx-rates/{fx_id}
- 功能：取得單一匯率
- 用法：Path 參數 `fx_id`
- 作用：讀取單筆資料
- 範例：
```bash
curl -s http://localhost:8000/fx-rates/3000
```

### PUT /fx-rates/{fx_id}
- 功能：更新匯率
- 用法：Path 參數 `fx_id`，Body 為 FXRateUpdate
- 作用：更新匯率資料
- 範例：
```bash
curl -s -X PUT http://localhost:8000/fx-rates/3000 \
  -H "Content-Type: application/json" \
  -d '{
    "rate": "32.4000"
  }'
```

### DELETE /fx-rates/{fx_id}
- 功能：刪除匯率
- 用法：Path 參數 `fx_id`
- 作用：刪除指定 FXRate
- 範例：
```bash
curl -s -X DELETE http://localhost:8000/fx-rates/3000
```

## Corporate Actions

### 資料模型（CorporateAction）
- asset_id: int
- date: date
- type: `SPLIT` | `REVERSE_SPLIT` | `MERGE` | `DRIP`
- numerator: int（正整數）
- denominator: int（正整數）

### GET /corporate-actions
- 功能：列出公司行動
- 用法：Query `asset_id`（可選）
- 作用：依日期排序
- 範例：
```bash
curl -s "http://localhost:8000/corporate-actions?asset_id=100"
```

### POST /corporate-actions
- 功能：建立公司行動
- 用法：Body 為 CorporateActionCreate
- 作用：新增公司行動；`MERGE` 會視為 `REVERSE_SPLIT`
- 範例：
```bash
curl -s -X POST http://localhost:8000/corporate-actions \
  -H "Content-Type: application/json" \
  -d '{
    "asset_id": 100,
    "date": "2025-02-01",
    "type": "SPLIT",
    "numerator": 2,
    "denominator": 1
  }'
```

### GET /corporate-actions/{action_id}
- 功能：取得單一公司行動
- 用法：Path 參數 `action_id`
- 作用：讀取單筆資料
- 範例：
```bash
curl -s http://localhost:8000/corporate-actions/4000
```

### PUT /corporate-actions/{action_id}
- 功能：更新公司行動
- 用法：Path 參數 `action_id`，Body 為 CorporateActionUpdate
- 作用：更新公司行動內容
- 範例：
```bash
curl -s -X PUT http://localhost:8000/corporate-actions/4000 \
  -H "Content-Type: application/json" \
  -d '{
    "numerator": 3,
    "denominator": 2
  }'
```

### DELETE /corporate-actions/{action_id}
- 功能：刪除公司行動
- 用法：Path 參數 `action_id`
- 作用：刪除指定 CorporateAction
- 範例：
```bash
curl -s -X DELETE http://localhost:8000/corporate-actions/4000
```

## Reports

### GET /reports/positions
- 功能：持倉報表
- 用法：Query `portfolio_id`（必填），`as_of`（可選），`in_base_currency`（可選，預設 `false`）
- 作用：回傳持倉與估值，若 `in_base_currency=true` 會嘗試換算為投資組合基準幣別
- 範例：
```bash
curl -s "http://localhost:8000/reports/positions?portfolio_id=1&as_of=2025-01-31&in_base_currency=true"
```
```json
[
  {
    "asset_id": 100,
    "symbol": "AAPL",
    "name": "Apple Inc.",
    "currency": "USD",
    "shares_held": "10",
    "avg_cost": "180.50",
    "cost_basis": "1805.00",
    "last_price": "190.12",
    "market_value": "1901.20",
    "unrealized_pnl": "96.20",
    "fx_rate_used": "32.5000",
    "market_value_base": "61889.00",
    "unrealized_pnl_base": "3126.50"
  }
]
```

### GET /reports/pnl/summary
- 功能：損益摘要報表
- 用法：Query `portfolio_id`、`from`、`to`（必填），`as_of`（可選）
- 作用：回傳損益彙總；若 `from` 大於 `to` 會回 400
- 範例：
```bash
curl -s "http://localhost:8000/reports/pnl/summary?portfolio_id=1&from=2025-01-01&to=2025-01-31"
```
```json
{
  "realized_pnl": "0",
  "income_total": "10.00",
  "income_dividend": "10.00",
  "income_reward": "0",
  "unrealized_pnl": "96.20",
  "price_return": "96.20",
  "total_return": "106.20",
  "invested_cashflow": "1805.00"
}
```
