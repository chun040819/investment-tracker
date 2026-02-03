from fastapi import APIRouter

from app.routers.portfolio import router as portfolio_router
from app.routers.account import router as account_router
from app.routers.asset import router as asset_router
from app.routers.trade import router as trade_router
from app.routers.cash_transaction import router as cash_txn_router
from app.routers.price import router as price_router
from app.routers.report import router as report_router
from app.routers.fx_rate import router as fx_rate_router
from app.routers.tag import router as tag_router
from app.routers.corporate_action import router as corporate_action_router

# Root API router to plug future route modules into.
api_router = APIRouter()

api_router.include_router(portfolio_router)
api_router.include_router(account_router)
api_router.include_router(asset_router)
api_router.include_router(trade_router)
api_router.include_router(cash_txn_router)
api_router.include_router(price_router)
api_router.include_router(report_router)
api_router.include_router(fx_rate_router)
api_router.include_router(tag_router)
api_router.include_router(corporate_action_router)
