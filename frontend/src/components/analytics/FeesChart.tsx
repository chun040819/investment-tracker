
"use client"

import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip, Legend } from "recharts"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

export function FeesChart({ data }: { data: any[] }) {
    return (
        <Card className="col-span-4">
            <CardHeader>
                <CardTitle>Loss Distribution (Fees & Taxes)</CardTitle>
            </CardHeader>
            <CardContent className="pl-2">
                <ResponsiveContainer width="100%" height={350}>
                    <PieChart>
                        <Pie
                            data={data}
                            cx="50%"
                            cy="50%"
                            innerRadius={60}
                            outerRadius={100}
                            paddingAngle={5}
                            dataKey="value"
                        >
                            {data.map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={entry.color} />
                            ))}
                        </Pie>
                        <Tooltip
                            contentStyle={{ backgroundColor: 'var(--background)', borderColor: 'var(--border)' }}
                            itemStyle={{ color: 'var(--foreground)' }}
                            formatter={(value: any) => new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" }).format(value)}
                        />
                        <Legend />
                    </PieChart>
                </ResponsiveContainer>
            </CardContent>
        </Card>
    )
}
