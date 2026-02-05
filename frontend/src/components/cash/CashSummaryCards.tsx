
"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ArrowDownLeft, ArrowUpRight, DollarSign } from "lucide-react"

interface CashSummaryData {
    totalBalance: number
    ytdNetInflow: number
    ytdDividends: number
}

export function CashSummaryCards({ data }: { data: CashSummaryData }) {
    return (
        <div className="grid gap-4 md:grid-cols-3">
            <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">Total Cash Balance</CardTitle>
                    <DollarSign className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                    <div className="text-2xl font-bold">
                        {new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" }).format(data.totalBalance)}
                    </div>
                </CardContent>
            </Card>

            <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">YTD Net Inflow</CardTitle>
                    {data.ytdNetInflow >= 0 ?
                        <ArrowUpRight className="h-4 w-4 text-profit" /> :
                        <ArrowDownLeft className="h-4 w-4 text-loss" />
                    }
                </CardHeader>
                <CardContent>
                    <div className={`text-2xl font-bold ${data.ytdNetInflow >= 0 ? 'text-profit' : 'text-loss'}`}>
                        {new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" }).format(Math.abs(data.ytdNetInflow))}
                    </div>
                    <p className="text-xs text-muted-foreground">
                        Deposits - Withdrawals
                    </p>
                </CardContent>
            </Card>

            <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">YTD Dividends</CardTitle>
                    <DollarSign className="h-4 w-4 text-primary" />
                </CardHeader>
                <CardContent>
                    <div className="text-2xl font-bold text-primary">
                        {new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" }).format(data.ytdDividends)}
                    </div>
                    <p className="text-xs text-muted-foreground">
                        Total dividends received
                    </p>
                </CardContent>
            </Card>
        </div>
    )
}
