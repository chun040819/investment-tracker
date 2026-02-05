
"use client"

import { ColumnDef } from "@tanstack/react-table"

export type AssetTransaction = {
    id: number
    type: string
    date: string
    amount?: number // total value
    price?: number
    quantity?: number
    status: string
}

export const historyColumns: ColumnDef<AssetTransaction>[] = [
    {
        accessorKey: "date",
        header: "Date",
    },
    {
        accessorKey: "type",
        header: "Type",
        cell: ({ row }) => {
            const type = row.getValue("type") as string;
            const color = type === 'Buy' ? 'text-profit' : type === 'Sell' ? 'text-loss' : 'text-primary';
            return <span className={`font-medium ${color}`}>{type}</span>
        }
    },
    {
        accessorKey: "price",
        header: () => <div className="text-right">Price</div>,
        cell: ({ row }) => {
            const amount = parseFloat(row.getValue("price") || "0")
            if (amount === 0) return <div className="text-right">-</div>;

            const formatted = new Intl.NumberFormat("en-US", {
                style: "currency",
                currency: "USD",
            }).format(amount)
            return <div className="text-right font-mono">{formatted}</div>
        }
    },
    {
        accessorKey: "quantity",
        header: () => <div className="text-right">Qty</div>,
        cell: ({ row }) => {
            const q = parseFloat(row.getValue("quantity") || "0")
            if (q === 0) return <div className="text-right">-</div>;
            return <div className="text-right font-mono">{q}</div>
        }
    },
    {
        accessorKey: "amount",
        header: () => <div className="text-right">Total</div>,
        cell: ({ row }) => {
            const amount = parseFloat(row.getValue("amount"))
            const formatted = new Intl.NumberFormat("en-US", {
                style: "currency",
                currency: "USD",
            }).format(amount)

            return <div className="text-right font-mono">{formatted}</div>
        },
    },
    {
        accessorKey: "status",
        header: "Status",
    },
]
