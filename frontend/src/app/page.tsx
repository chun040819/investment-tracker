
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { KPIData, NetWorthHistoryData, AllocationData, RecentActivityData } from "@/lib/mock-data";
import { StatCard } from "@/components/dashboard/StatCard";
import { NetWorthChart } from "@/components/dashboard/NetWorthChart";
import { AllocationChart } from "@/components/dashboard/AllocationChart";
import { RecentActivity } from "@/components/dashboard/RecentActivity";
import { DollarSign, Percent, TrendingUp, Wallet } from "lucide-react";

export default function DashboardPage() {
  return (
    <div className="flex-1 space-y-4 p-8 pt-6">
      <div className="flex items-center justify-between space-y-2">
        <h2 className="text-3xl font-bold tracking-tight">Dashboard</h2>
      </div>
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <StatCard
          title="Total Net Worth"
          value={`$${KPIData.totalNetWorth.value.toLocaleString()}`}
          change={KPIData.totalNetWorth.change}
          changeType={KPIData.totalNetWorth.changeType as "profit" | "loss"}
          icon={DollarSign}
        />
        <StatCard
          title="Day Change"
          value={`$${KPIData.dayChange.value.toLocaleString()}`}
          change={KPIData.dayChange.change}
          changeType={KPIData.dayChange.changeType as "profit" | "loss"}
          icon={TrendingUp}
        />
        <StatCard
          title="Total Profit/Loss"
          value={`$${KPIData.totalProfitLoss.value.toLocaleString()}`}
          change={KPIData.totalProfitLoss.change}
          changeType={KPIData.totalProfitLoss.changeType as "profit" | "loss"}
          icon={Percent}
        />
        <StatCard
          title="Cash Balance"
          value={`$${KPIData.cashBalance.value.toLocaleString()}`}
          change={KPIData.cashBalance.change}
          changeType={KPIData.cashBalance.changeType as "profit" | "loss"}
          icon={Wallet}
        />
      </div>
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
        <Card className="col-span-4">
          <CardHeader>
            <CardTitle>Net Worth History</CardTitle>
            <CardDescription>
              Your asset growth over time.
            </CardDescription>
          </CardHeader>
          <CardContent className="pl-2">
            <NetWorthChart data={NetWorthHistoryData} />
          </CardContent>
        </Card>
        <Card className="col-span-3">
          <CardHeader>
            <CardTitle>Asset Allocation</CardTitle>
            <CardDescription>
              Distribution of your portfolio.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <AllocationChart data={AllocationData} />
          </CardContent>
        </Card>
      </div>
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
        <Card className="col-span-4">
          <CardHeader>
            <CardTitle>Recent Activity</CardTitle>
            <CardDescription>
              Your latest transactions.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <RecentActivity data={RecentActivityData} />
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
