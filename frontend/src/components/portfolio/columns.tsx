
"use client"

import { ColumnDef } from "@tanstack/react-table"
import { MoreHorizontal } from "lucide-react"

import { Button } from "@/components/ui/button"
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"

// Define the shape of our data.
export type PortfolioPosition = {
    symbol: string
    name: string
    quantity: number
    avgCost: number
    currentPrice: number
}

export const columns: ColumnDef<PortfolioPosition>[] = [
    {
        accessorKey: "symbol",
        header: "Asset",
        cell: ({ row }) => {
            const position = row.original
            return (
                <div>
                    <div className="font-bold">{position.symbol}</div>
                    <div className="text-xs text-muted-foreground">{position.name}</div>
                </div>
            )
        },
    },
    {
        accessorKey: "quantity",
        header: () => <div className="text-right">Quantity</div>,
        cell: ({ row }) => {
            const amount = parseFloat(row.getValue("quantity"))
            return <div className="text-right font-mono">{amount.toLocaleString()}</div>
        },
    },
    {
        accessorKey: "avgCost",
        header: () => <div className="text-right">Avg Cost</div>,
        cell: ({ row }) => {
            const amount = parseFloat(row.getValue("avgCost"))
            const formatted = new Intl.NumberFormat("en-US", {
                style: "currency",
                currency: "USD",
            }).format(amount)

            return <div className="text-right font-mono">{formatted}</div>
        },
    },
    {
        accessorKey: "currentPrice",
        header: () => <div className="text-right">Current Price</div>,
        cell: ({ row }) => {
            const amount = parseFloat(row.getValue("currentPrice"))
            const formatted = new Intl.NumberFormat("en-US", {
                style: "currency",
                currency: "USD",
            }).format(amount)

            return <div className="text-right font-mono">{formatted}</div>
        },
    },
    {
        id: "marketValue",
        header: () => <div className="text-right">Market Value</div>,
        cell: ({ row }) => {
            const position = row.original;
            const marketValue = position.quantity * position.currentPrice;
            const formatted = new Intl.NumberFormat("en-US", {
                style: "currency",
                currency: "USD",
            }).format(marketValue);
            return <div className="text-right font-mono">{formatted}</div>
        }
    },
    {
        id: "pnl",
        header: () => <div className="text-right">Unrealized P&L</div>,
        cell: ({ row }) => {
            const position = row.original;
            const pnl = (position.currentPrice - position.avgCost) * position.quantity;
            const pnlPercent = ((position.currentPrice - position.avgCost) / position.avgCost) * 100;

            const isProfit = pnl >= 0;
            const formattedPnl = new Intl.NumberFormat("en-US", {
                style: "currency",
                currency: "USD",
            }).format(pnl);

            return (
                <div className={`text-right font-mono ${isProfit ? "text-profit" : "text-loss"}`}>
                    <div>{formattedPnl}</div>
                    <div className="text-xs">
                        {isProfit ? "+" : ""}{pnlPercent.toFixed(2)}%
                    </div>
                </div>
            )
        }
    },
    {
        id: "actions",
        cell: ({ row }) => {
            const payment = row.original

            return (
                <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                        <Button variant="ghost" className="h-8 w-8 p-0">
                            <span className="sr-only">Open menu</span>
                            <MoreHorizontal className="h-4 w-4" />
                        </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                        <DropdownMenuLabel>Actions</DropdownMenuLabel>
                        <DropdownMenuItem
                            onClick={() => navigator.clipboard.writeText(payment.symbol)}
                        >
                            Copy Symbol
                        </DropdownMenuItem>
                        <DropdownMenuSeparator />
                        <DropdownMenuItem>Buy More</DropdownMenuItem>
                        <DropdownMenuItem>Sell</DropdownMenuItem>
                        <DropdownMenuItem>View Details</DropdownMenuItem>
                    </DropdownMenuContent>
                </DropdownMenu>
            )
        },
    },
]
