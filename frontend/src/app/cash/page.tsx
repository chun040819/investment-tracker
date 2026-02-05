
import { CashSummaryData, CashTransactionsData } from "@/lib/mock-data"
import { CashSummaryCards } from "@/components/cash/CashSummaryCards"
import { cashColumns } from "@/components/cash/cash-columns"
import { TransferDialog } from "@/components/cash/TransferDialog"
import { DataTable } from "@/components/portfolio/data-table"

export default function CashPage() {
    return (
        <div className="container mx-auto py-10 space-y-8">
            <div className="flex items-center justify-between space-y-2">
                <h2 className="text-3xl font-bold tracking-tight">Cash Ledger</h2>
                <div className="flex items-center space-x-2">
                    <TransferDialog />
                </div>
            </div>

            <CashSummaryCards data={CashSummaryData} />

            <div className="space-y-4">
                <div className="flex items-center justify-between">
                    <h3 className="text-xl font-semibold tracking-tight">Transactions</h3>
                    {/* Filter could be added here or inside DataTable if extended */}
                </div>
                <DataTable columns={cashColumns} data={CashTransactionsData} />
            </div>
        </div>
    )
}
