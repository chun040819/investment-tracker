
"use client"

import { ColumnDef } from "@tanstack/react-table"
import { ArrowDownLeft, ArrowUpRight } from "lucide-react"

export type CashTransaction = {
    id: string
    date: string
    type: string
    amount: number
    currency: string
    note: string
}

export const cashColumns: ColumnDef<CashTransaction>[] = [
    {
        accessorKey: "date",
        header: "Date",
    },
    {
        accessorKey: "type",
        header: "Type",
        cell: ({ row }) => {
            const type = row.getValue("type") as string;
            let color = "";
            if (type === 'Deposit' || type === 'Interest' || type === 'Dividend') color = "text-profit";
            else if (type === 'Withdrawal') color = "text-loss";
            else if (type === 'Trade') color = "text-accent-foreground"; // Neutral or distinct for linked trades

            return <span className={`font-medium ${color}`}>{type}</span>
        },
        filterFn: (row, id, value) => {
            return value.includes(row.getValue(id))
        },
    },
    {
        accessorKey: "note",
        header: "Note",
    },
    {
        accessorKey: "amount",
        header: () => <div className="text-right">Amount</div>,
        cell: ({ row }) => {
            const amount = parseFloat(row.getValue("amount"))
            const formatted = new Intl.NumberFormat("en-US", {
                style: "currency",
                currency: "USD",
            }).format(Math.abs(amount))

            return (
                <div className={`text-right font-mono font-medium ${amount >= 0 ? "text-profit" : "text-loss"}`}>
                    {amount >= 0 ? "+" : "-"}{formatted}
                </div>
            )
        },
    },
]
