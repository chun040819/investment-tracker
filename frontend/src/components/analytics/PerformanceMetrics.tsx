
"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

interface Metrics {
    realizedPnL: number
    unrealizedPnL: number
    totalReturn: number
    returnPercent: number
}

export function PerformanceMetrics({ data }: { data: Metrics }) {
    return (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">Realized P&L</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="text-2xl font-bold text-profit">
                        {new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" }).format(data.realizedPnL)}
                    </div>
                </CardContent>
            </Card>
            <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">Unrealized P&L</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="text-2xl font-bold text-profit">
                        {new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" }).format(data.unrealizedPnL)}
                    </div>
                </CardContent>
            </Card>
            <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">Total Return</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="text-2xl font-bold text-profit">
                        {new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" }).format(data.totalReturn)}
                    </div>
                    <p className="text-xs text-muted-foreground">
                        +{data.returnPercent}%
                    </p>
                </CardContent>
            </Card>
        </div>
    )
}
