
import { notFound } from "next/navigation"

import {
    AssetActivityData,
    AssetPriceHistory,
    PortfolioData,
} from "@/lib/mock-data"
import { AssetChart } from "@/components/asset/AssetChart"
import { AssetHeader } from "@/components/asset/AssetHeader"
import { historyColumns } from "@/components/asset/history-columns"
import { PositionCard } from "@/components/asset/PositionCard"
import { DataTable } from "@/components/portfolio/data-table"

// In a real app, this would fetch data based on the symbol
function getAssetData(symbol: string) {
    const position = PortfolioData.find(
        (p) => p.symbol.toUpperCase() === symbol.toUpperCase()
    )
    const history = AssetPriceHistory
    const activity = AssetActivityData.filter(
        (a) => a.asset.toUpperCase() === symbol.toUpperCase()
    )

    // Use current mock data for pricing if position exists, otherwise mock
    const currentPrice = position?.currentPrice || 150.0
    const name = position?.name || "Unknown Asset"

    return {
        symbol,
        name,
        position,
        history,
        activity,
        currentPrice,
    }
}

export default async function AssetPage({
    params,
}: {
    params: Promise<{ symbol: string }>
}) {
    const { symbol } = await params
    const data = getAssetData(symbol)

    // Calculate day change (mocked as random for now or based on history)
    const lastPrice = data.history[data.history.length - 1].price
    const dayChange = data.currentPrice - lastPrice
    const dayChangePercent = (dayChange / lastPrice) * 100

    return (
        <div className="container mx-auto py-10 space-y-8">
            <AssetHeader
                symbol={data.symbol}
                name={data.name}
                price={data.currentPrice}
                change={dayChange}
                changePercent={dayChangePercent}
            />

            <div className="grid gap-4 md:grid-cols-4 lg:grid-cols-5">
                <AssetChart data={data.history} />
                <div className="md:col-span-4 lg:col-span-1">
                    {data.position ? (
                        <PositionCard
                            quantity={data.position.quantity}
                            avgCost={data.position.avgCost}
                            currentPrice={data.currentPrice}
                        />
                    ) : (
                        <div className="p-4 border rounded-md bg-muted text-muted-foreground text-center">
                            No position currently held.
                        </div>
                    )}
                </div>
            </div>

            <div className="space-y-4">
                <h3 className="text-xl font-semibold tracking-tight">
                    Transaction History
                </h3>
                <DataTable columns={historyColumns} data={data.activity} />
            </div>
        </div>
    )
}
