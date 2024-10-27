<script>
    import Input from "$lib/components/ui/input/input.svelte";
    import { ResizablePane, ResizablePaneGroup } from "$lib/components/ui/resizable";
    import ResizableHandle from "$lib/components/ui/resizable/resizable-handle.svelte";
    import ScrollArea from "$lib/components/ui/scroll-area/scroll-area.svelte";
    import Separator from "$lib/components/ui/separator/separator.svelte";
    import Editor from "./editor.svelte";
    
    const items = [
    { id: 1, name: 'Test 1', description: 'Test description 1', times_used: 10 },
    { id: 2, name: 'Test 2', description: 'Test description 2', times_used: 5 },
    { id: 3, name: 'Test 3', description: 'Test description 3', times_used: 2 },
    { id: 4, name: 'Test 4', description: 'Test description 4', times_used: 1 },
    ];
    const items2 = items.concat(items).concat(items).concat(items).concat(items);   

    let value = $state("[hello]")
    $effect(() => {
        console.log(value)
    })
</script>
<ResizablePaneGroup class="h-screen w-screen flex" direction="horizontal">
    <ResizablePane class="flex flex-col" defaultSize={25}>
        <h1 class="sticky top-0 p-4 font-bold text-xl" >Конфигурации</h1>
        <Separator/>
        <ScrollArea>
            {#each items2 as item}
            <div class="p-4 ">
                <h2 class="font-bold text-lg pb-1">{item.name}</h2>
                <p>{item.description}</p>
                <p class="font-light">Использовано раз: {item.times_used}</p>
            </div>
            <Separator/>
            {/each}
        </ScrollArea>
    </ResizablePane>
    <ResizableHandle/>
    <ResizablePane defaultSize={75}> 
        <Input class="h-7 m-4 text-xl font-bold border-0" placeholder="Имя конфигурации"/>
        <Separator/>
        <Editor cls="p-4 text-lg w-screen h-screen" bind:value={value}/>
    </ResizablePane>
</ResizablePaneGroup>