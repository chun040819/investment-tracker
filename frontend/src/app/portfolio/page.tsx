
import { PortfolioData } from "@/lib/mock-data";
import { columns } from "@/components/portfolio/columns";
import { DataTable } from "@/components/portfolio/data-table";
import { AddTransactionDialog } from "@/components/transactions/AddTransactionDialog";

export default function PortfolioPage() {
    return (
        <div className="container mx-auto py-10">
            <div className="flex items-center justify-between space-y-2 mb-8">
                <h2 className="text-3xl font-bold tracking-tight">Portfolio</h2>
                <AddTransactionDialog />
            </div>
            <DataTable columns={columns} data={PortfolioData} />
        </div>
    );
}
