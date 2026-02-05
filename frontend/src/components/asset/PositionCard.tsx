
"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

interface PositionCardProps {
    quantity: number
    avgCost: number
    currentPrice: number
}

export function PositionCard({ quantity, avgCost, currentPrice }: PositionCardProps) {
    const marketValue = quantity * currentPrice
    const totalCost = quantity * avgCost
    const totalReturn = marketValue - totalCost
    const returnPercent = (totalReturn / totalCost) * 100
    const isProfit = totalReturn >= 0

    return (
        <Card>
            <CardHeader>
                <CardTitle>Your Position</CardTitle>
            </CardHeader>
            <CardContent className="grid gap-4">
                <div className="flex items-center justify-between">
                    <span className="text-sm text-muted-foreground">Quantity</span>
                    <span className="font-bold">{quantity}</span>
                </div>
                <div className="flex items-center justify-between">
                    <span className="text-sm text-muted-foreground">Avg Cost</span>
                    <span className="font-bold">
                        {new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" }).format(avgCost)}
                    </span>
                </div>
                <div className="flex items-center justify-between">
                    <span className="text-sm text-muted-foreground">Market Value</span>
                    <span className="font-bold">
                        {new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" }).format(marketValue)}
                    </span>
                </div>
                <div className="flex items-center justify-between">
                    <span className="text-sm text-muted-foreground">Total Return</span>
                    <div className={`font-bold ${isProfit ? "text-profit" : "text-loss"}`}>
                        {isProfit ? "+" : ""}
                        {new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" }).format(totalReturn)}
                        <span className="ml-1 text-xs">
                            ({isProfit ? "+" : ""}{returnPercent.toFixed(2)}%)
                        </span>
                    </div>
                </div>
            </CardContent>
        </Card>
    )
}
