
import { ArrowUpIcon, ArrowDownIcon, LucideIcon } from "lucide-react";

interface StatCardProps {
    title: string;
    value: string | number;
    change?: number;
    changeType?: "profit" | "loss";
    icon?: LucideIcon;
}

export function StatCard({
    title,
    value,
    change,
    changeType,
    icon: Icon,
}: StatCardProps) {
    const isProfit = changeType === "profit";
    const isLoss = changeType === "loss";

    return (
        <div className="bg-card text-card-foreground rounded-lg border shadow-sm p-6">
            <div className="flex flex-row items-center justify-between space-y-0 pb-2">
                <h3 className="tracking-tight text-sm font-medium text-muted-foreground">
                    {title}
                </h3>
                {Icon && <Icon className="h-4 w-4 text-muted-foreground" />}
            </div>
            <div>
                <div className="text-2xl font-bold">{value}</div>
                {change !== undefined && (
                    <p className="text-xs flex items-center mt-1">
                        <span
                            className={`flex items-center font-medium ${isProfit ? "text-profit" : isLoss ? "text-loss" : "text-muted-foreground"
                                }`}
                        >
                            {isProfit ? (
                                <ArrowUpIcon className="mr-1 h-3 w-3" />
                            ) : isLoss ? (
                                <ArrowDownIcon className="mr-1 h-3 w-3" />
                            ) : null}
                            {Math.abs(change)}%
                        </span>
                        <span className="text-muted-foreground ml-1">from last month</span>
                    </p>
                )}
            </div>
        </div>
    );
}
