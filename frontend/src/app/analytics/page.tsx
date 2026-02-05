
import {
    DividendByAsset,
    DividendHistory,
    FeesDistribution,
    PerformanceHistory,
    PerformanceMetricsData,
} from "@/lib/mock-data"
import { DateRangePicker } from "@/components/analytics/DateRangePicker"
import { DividendChart } from "@/components/analytics/DividendChart"
import { DividendTable } from "@/components/analytics/DividendTable"
import { FeesChart } from "@/components/analytics/FeesChart"
import { PerformanceChart } from "@/components/analytics/PerformanceChart"
import { PerformanceMetrics } from "@/components/analytics/PerformanceMetrics"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

export default function AnalyticsPage() {
    return (
        <div className="container mx-auto py-10 space-y-8">
            <div className="flex flex-col md:flex-row md:items-center justify-between space-y-2 md:space-y-0">
                <h2 className="text-3xl font-bold tracking-tight">Analytics & Reports</h2>
                <div className="flex items-center space-x-2">
                    <DateRangePicker />
                </div>
            </div>

            <Tabs defaultValue="performance" className="space-y-4">
                <TabsList>
                    <TabsTrigger value="performance">Performance</TabsTrigger>
                    <TabsTrigger value="dividends">Dividends</TabsTrigger>
                    <TabsTrigger value="fees">Fees</TabsTrigger>
                </TabsList>
                <TabsContent value="performance" className="space-y-4">
                    <PerformanceMetrics data={PerformanceMetricsData} />
                    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                        <PerformanceChart data={PerformanceHistory} />
                    </div>
                </TabsContent>
                <TabsContent value="dividends" className="space-y-4">
                    <div className="grid gap-4 md:grid-cols-7">
                        <DividendChart data={DividendHistory} />
                        <DividendTable data={DividendByAsset} />
                    </div>
                </TabsContent>
                <TabsContent value="fees" className="space-y-4">
                    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                        <FeesChart data={FeesDistribution} />
                    </div>
                </TabsContent>
            </Tabs>
        </div>
    )
}
