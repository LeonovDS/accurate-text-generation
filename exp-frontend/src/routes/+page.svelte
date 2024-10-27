<script>
    import CardContent from "$lib/components/ui/card/card-content.svelte";
    import CardHeader from "$lib/components/ui/card/card-header.svelte";
    import CardTitle from "$lib/components/ui/card/card-title.svelte";
    import Card from "$lib/components/ui/card/card.svelte";
    import { Select, SelectValue } from "$lib/components/ui/select";
    import SelectContent from "$lib/components/ui/select/select-content.svelte";
    import SelectItem from "$lib/components/ui/select/select-item.svelte";
    import SelectTrigger from "$lib/components/ui/select/select-trigger.svelte";
    
    const BASE_URL = "http://localhost:8080/";
    
</script>
<div class="h-screen w-screen flex">
    <Card class="m-auto">
        <CardHeader>
            <CardTitle>Экспериментариум</CardTitle>
        </CardHeader>
        <CardContent>
            <Select>
                <SelectTrigger>
                    <SelectValue placeholder="a"></SelectValue>
                </SelectTrigger>
                <SelectContent>
                    <SelectItem value="a">a</SelectItem>
                    <SelectItem value="b">b</SelectItem>
                </SelectContent>
            </Select>
        </CardContent>
    </Card>
</div>