
"use client"

import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import { format } from "date-fns"
import { CalendarIcon } from "lucide-react"

import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Calendar } from "@/components/ui/calendar"
import { Label } from "@/components/ui/label"
import {
    Form,
    FormControl,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import {
    Popover,
    PopoverContent,
    PopoverTrigger,
} from "@/components/ui/popover"
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { useEffect } from "react"

const formSchema = z.object({
    type: z.enum(["buy", "sell", "dividend"]),
    date: z.date(),
    symbol: z.string().min(1, "Symbol is required").transform((val) => val.toUpperCase()),
    quantity: z.coerce.number().positive("Quantity must be positive"),
    price: z.coerce.number().positive("Price must be positive"),
    fees: z.coerce.number().min(0).default(0),
})

type FormValues = z.infer<typeof formSchema>

export function TransactionForm({ onSuccess }: { onSuccess?: () => void }) {
    const form = useForm({
        resolver: zodResolver(formSchema),
        defaultValues: {
            type: "buy",
            date: new Date(),
            symbol: "",
            quantity: 0,
            price: 0,
            fees: 0,
        },
    })

    // Watch values for calculating total and changing button color
    const type = form.watch("type")
    const quantity = form.watch("quantity")
    const price = form.watch("price")
    const fees = form.watch("fees")

    const total = (Number(quantity || 0) * Number(price || 0)) + Number(fees || 0)

    function onSubmit(data: any) {
        const values = data as FormValues
        console.log(values)
        // Here we would call the API to save the transaction
        if (onSuccess) {
            onSuccess()
        }
    }

    // Effect to uppercase symbol on change (optional, already handled by transform but good for UI)
    const symbol = form.watch("symbol")
    useEffect(() => {
        if (symbol) {
            form.setValue("symbol", symbol.toUpperCase())
        }
    }, [symbol, form])


    return (
        <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
                <FormField
                    control={form.control}
                    name="type"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Transaction Type</FormLabel>
                            <FormControl>
                                <Tabs
                                    onValueChange={field.onChange}
                                    defaultValue={field.value as string}
                                    className="w-full"
                                >
                                    <TabsList className="grid w-full grid-cols-3">
                                        <TabsTrigger value="buy">Buy</TabsTrigger>
                                        <TabsTrigger value="sell">Sell</TabsTrigger>
                                        <TabsTrigger value="dividend">Dividend</TabsTrigger>
                                    </TabsList>
                                </Tabs>
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                />

                <div className="grid grid-cols-2 gap-4">
                    <FormField
                        control={form.control}
                        name="date"
                        render={({ field }) => (
                            <FormItem className="flex flex-col">
                                <FormLabel>Date</FormLabel>
                                <Popover>
                                    <PopoverTrigger asChild>
                                        <FormControl>
                                            <Button
                                                variant={"outline"}
                                                className={cn(
                                                    "w-full pl-3 text-left font-normal",
                                                    !field.value && "text-muted-foreground"
                                                )}
                                            >
                                                {field.value ? (
                                                    format(field.value, "PPP")
                                                ) : (
                                                    <span>Pick a date</span>
                                                )}
                                                <CalendarIcon className="ml-auto h-4 w-4 opacity-50" />
                                            </Button>
                                        </FormControl>
                                    </PopoverTrigger>
                                    <PopoverContent className="w-auto p-0" align="start">
                                        <Calendar
                                            mode="single"
                                            selected={field.value}
                                            onSelect={field.onChange}
                                            disabled={(date) =>
                                                date > new Date() || date < new Date("1900-01-01")
                                            }
                                            initialFocus
                                        />
                                    </PopoverContent>
                                </Popover>
                                <FormMessage />
                            </FormItem>
                        )}
                    />
                    <FormField
                        control={form.control}
                        name="symbol"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel>Symbol</FormLabel>
                                <FormControl>
                                    <Input placeholder="AAPL" {...field} value={field.value as string} />
                                </FormControl>
                                <FormMessage />
                            </FormItem>
                        )}
                    />
                </div>

                <div className="grid grid-cols-2 gap-4">
                    <FormField
                        control={form.control}
                        name="quantity"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel>Quantity</FormLabel>
                                <FormControl>
                                    <Input type="number" step="any" placeholder="0" {...field} value={field.value as number} />
                                </FormControl>
                                <FormMessage />
                            </FormItem>
                        )}
                    />
                    <FormField
                        control={form.control}
                        name="price"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel>Price per Share</FormLabel>
                                <FormControl>
                                    <Input type="number" step="0.01" placeholder="0.00" {...field} value={field.value as number} />
                                </FormControl>
                                <FormMessage />
                            </FormItem>
                        )}
                    />
                </div>

                <div className="grid grid-cols-2 gap-4">
                    <FormField
                        control={form.control}
                        name="fees"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel>Fees (Optional)</FormLabel>
                                <FormControl>
                                    <Input type="number" step="0.01" placeholder="0.00" {...field} value={field.value as number} />
                                </FormControl>
                                <FormMessage />
                            </FormItem>
                        )}
                    />
                    <div className="flex flex-col gap-2">
                        <Label>Total Amount</Label>
                        <div className="flex h-9 w-full items-center rounded-md border border-input bg-muted px-3 py-1 text-sm shadow-sm">
                            ${total.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                        </div>
                    </div>
                </div>

                <Button
                    type="submit"
                    className={cn(
                        "w-full",
                        type === 'sell' && "bg-destructive hover:bg-destructive/90",
                        type === 'buy' && "bg-profit hover:bg-profit/90 text-white",
                        type === 'dividend' && "bg-primary"
                    )}
                >
                    {type === 'buy' ? 'Buy Asset' : type === 'sell' ? 'Sell Asset' : 'Record Dividend'}
                </Button>
            </form>
        </Form>
    )
}
