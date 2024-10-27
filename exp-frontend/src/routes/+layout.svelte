<script>
    import '../app.css';
</script>
<div class="w-screen h-screen flex flex-col">
    <header class="sticky flex gap-7 items-center p-4 top-0 z-50 border-b-2 border-black">
        <div class="flex items-center gap-6 font-bold">
            <h1 class="text-xl font-extrabold">
                <a href="/" >
                    Генерация текстов по мотивам
                </a>
            </h1>
            <a class="text-xl font-light" href="/" >Экспериментариум</a>
            <a class="text-xl font-light" href="/config">Конфигурации</a>
        </div>
    </header>
    <slot/>
</div>