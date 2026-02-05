
"use client"

interface AssetHeaderProps {
    symbol: string
    name: string
    price: number
    change: number
    changePercent: number
}

export function AssetHeader({
    symbol,
    name,
    price,
    change,
    changePercent,
}: AssetHeaderProps) {
    const isPositive = change >= 0

    return (
        <div className="flex items-center justify-between">
            <div>
                <h2 className="text-3xl font-bold tracking-tight">{symbol}</h2>
                <p className="text-muted-foreground">{name}</p>
            </div>
            <div className="text-right">
                <div className="text-3xl font-bold">
                    {new Intl.NumberFormat("en-US", {
                        style: "currency",
                        currency: "USD",
                    }).format(price)}
                </div>
                <div className={`text-sm font-medium ${isPositive ? "text-profit" : "text-loss"}`}>
                    {isPositive ? "+" : ""}{change.toFixed(2)} ({isPositive ? "+" : ""}{changePercent.toFixed(2)}%)
                </div>
            </div>
        </div>
    )
}
