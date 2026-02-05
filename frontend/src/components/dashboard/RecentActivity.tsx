
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";

interface Transaction {
    id: number;
    type: string;
    asset: string;
    amount: number;
    date: string;
    status: string;
}

interface RecentActivityProps {
    data: Transaction[];
}

export function RecentActivity({ data }: RecentActivityProps) {
    return (
        <div className="space-y-8">
            {data.map((transaction) => (
                <div key={transaction.id} className="flex items-center">
                    <Avatar className="h-9 w-9">
                        <AvatarImage src="/avatars/01.png" alt="Avatar" />
                        <AvatarFallback>{transaction.asset.substring(0, 2)}</AvatarFallback>
                    </Avatar>
                    <div className="ml-4 space-y-1">
                        <p className="text-sm font-medium leading-none">{transaction.type} {transaction.asset}</p>
                        <p className="text-xs text-muted-foreground">{transaction.date}</p>
                    </div>
                    <div className="ml-auto font-medium">
                        {transaction.type === 'Buy' || transaction.type === 'Deposit' ? '+' : '-'}${transaction.amount.toLocaleString()}
                    </div>
                </div>
            ))}
        </div>
    );
}
