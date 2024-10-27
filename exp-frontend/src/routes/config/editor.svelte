<script>
    import { onMount } from "svelte";
    import hljs from "highlight.js";

    let {
        cls,
        value = $bindable()
    } = $props();
    
    const highlight = (editor) => {
        editor.innerHTML = hljs.highlight(editor.textContent || "", { language: 'toml' }).value;
    };
    
    const toggleComments = (editor) => {
        const selection = window.getSelection();
        if (!selection || selection.rangeCount === 0) return;
        
        const range = selection.getRangeAt(0);
        
        // Get the selected nodes (start and end)
        const startNode = range.startContainer;
        const endNode = range.endContainer;
        
        if (!startNode || !endNode || !editor.contains(startNode) || !editor.contains(endNode)) {
            return; // Ensure the selection is within the editor
        }
        
        // Split the editor content into lines
        const content = editor.textContent || '';
        const lines = content.split('\n');
        
        // Find start and end positions within the content
        const startOffset = content.substring(0, range.startOffset).split('\n').length - 1;
        const endOffset = content.substring(0, range.endOffset).split('\n').length - 1;
        
        // Toggle comment (add or remove `#` from each line in the selection)
        for (let i = startOffset; i <= endOffset; i++) {
            if (lines[i].trim().startsWith('#')) {
                lines[i] = lines[i].replace(/^#\s*/, ''); // Uncomment the line
            } else {
                lines[i] = `# ${lines[i]}`; // Comment the line
            }
        }
        
        editor.textContent = lines.join('\n');
        highlight(editor);
    }
    
    onMount(async () => {
        const editor = document.querySelector('.editor');
        if (editor === null) return;
        editor.addEventListener("keyup", (e) => {
            if (e.ctrlKey && e.key === "/") {
                e.preventDefault();
                toggleComments(editor);
            }
        });
        const CodeJar = (await import('codejar')).CodeJar;
        CodeJar(editor, highlight);
    })
</script>
<div class="editor language-toml {cls}" bind:innerText={value} contenteditable></div>