document.addEventListener('DOMContentLoaded', function() {
    const editor = CodeMirror.fromTextArea(document.getElementById('editor'), {
        mode: 'text/x-csrc',
        theme: 'dracula',
        lineNumbers: true,
        indentUnit: 4,
        tabSize: 4,
        lineWrapping: true,
        matchBrackets: true,
        extraKeys: {"Ctrl-Space": "autocomplete"}
    });
    
    let errorMarkers = [];
    let errorTooltips = [];
    
    function clearErrors() {
        errorMarkers.forEach(marker => marker.clear());
        errorTooltips.forEach(tooltip => tooltip.remove());
        errorMarkers = [];
        errorTooltips = [];
        
        editor.getAllMarks().forEach(marker => {
            if (marker.className === 'error-marker' || marker.className === 'error-line') {
                marker.clear();
            }
        });
        
        document.querySelector('#errors-table tbody').innerHTML = 
            '<tr><td colspan="3" class="no-errors">No se encontraron errores</td></tr>';
    }
    
    function showError(line, message, correction) {
        line = Math.max(1, line);
        const noErrorsRow = document.querySelector('#errors-table .no-errors');
        if (noErrorsRow) noErrorsRow.remove();
        
        const marker = editor.markText(
            {line: line - 1, ch: 0},
            {line: line - 1},
            {className: 'error-line', attributes: {title: message}}
        );
        
        errorMarkers.push(marker);
        
        const errorsTable = document.querySelector('#errors-table tbody');
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${line}</td>
            <td>${message}</td>
            <td>${correction || 'Revise la sintaxis'}</td>
        `;
        errorsTable.appendChild(row);
    }
    
    document.querySelectorAll('.tab-btn').forEach(button => {
        button.addEventListener('click', function() {
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
            
            this.classList.add('active');
            const tabId = this.getAttribute('data-tab') + '-tab';
            document.getElementById(tabId).classList.add('active');
        });
    });
    
    document.getElementById('lexical-btn').addEventListener('click', function() {
        clearErrors();
        const code = editor.getValue();
        
        fetch('/analyze', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({code: code, action: "lexical"})
        })
        .then(response => response.json())
        .then(data => {
            const tokensTable = document.querySelector('#tokens-table tbody');
            tokensTable.innerHTML = '';
            
            data.tokens.forEach(token => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${token[0]}</td>
                    <td>${token[1]}</td>
                    <td>${token[2] || '-'}</td>
                `;
                tokensTable.appendChild(row);
            });
            
            if (data.errors.length > 0) {
                const errorsTable = document.querySelector('#errors-table tbody');
                errorsTable.innerHTML = '<tr><td colspan="3" style="text-align: center; color: var(--error-color);">Errores léxicos detectados</td></tr>';
                
                data.errors.forEach(error => {
                    showError(error.line, error.message, error.correction);
                });
                
                document.querySelector('.tab-btn[data-tab="errors"]').click();
            } else {
                document.querySelector('.tab-btn[data-tab="tokens"]').click();
            }
        });
    });
    
    document.getElementById('syntax-btn').addEventListener('click', function() {
        clearErrors();
        const code = editor.getValue();
        
        fetch('/analyze', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({code: code, action: "syntax"})
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'error') {
                const errorsTable = document.querySelector('#errors-table tbody');
                errorsTable.innerHTML = '<tr><td colspan="3" style="text-align: center; color: var(--error-color);">Errores sintácticos detectados</td></tr>';
                
                data.errors.forEach(error => {
                    const line = Math.max(1, error.line);
                    showError(line, error.message, error.correction);
                    
                    const editorLine = line - 1;
                    const lineText = editor.getLine(editorLine) || '';
                    let ch = 0;
                    
                    if (error.message.includes("';'")) {
                        ch = lineText.length;
                    } else if (error.message.includes("'('")) {
                        ch = Math.max(0, lineText.indexOf('('));
                    } else if (error.message.includes("')'")) {
                        ch = Math.max(0, lineText.indexOf(')'));
                    } else if (error.message.includes("'{'")) {
                        ch = Math.max(0, lineText.indexOf('{'));
                    } else if (error.message.includes("'}'")) {
                        ch = Math.max(0, lineText.indexOf('}'));
                    } else if (error.message.includes("'=='")) {
                        ch = Math.max(0, lineText.indexOf('=='));
                    }
                    
                    const marker = editor.markText(
                        {line: editorLine, ch: ch},
                        {line: editorLine, ch: ch + 1},
                        {
                            className: 'error-marker',
                            attributes: {style: 'border-bottom: 2px solid #ff0000; background-color: rgba(255, 0, 0, 0.3);'}
                        }
                    );
                    errorMarkers.push(marker);
                });
                
                document.querySelector('.tab-btn[data-tab="errors"]').click();
                
                if (data.errors.length > 0) {
                    editor.setCursor({
                        line: Math.max(0, data.errors[0].line - 1), 
                        ch: 0
                    });
                    editor.focus();
                }
            } else {
                const errorsTable = document.querySelector('#errors-table tbody');
                errorsTable.innerHTML = `
                    <tr>
                        <td colspan="3" style="text-align: center; color: var(--success-color);">
                            ✅ Análisis sintáctico completado sin errores
                        </td>
                    </tr>
                `;
                document.querySelector('.tab-btn[data-tab="errors"]').click();
            }
        });
    });
    
    document.getElementById('turing-btn').addEventListener('click', function() {
        document.querySelector('.tab-btn[data-tab="turing"]').click();
    });
    
    document.getElementById('run-turing-btn').addEventListener('click', function() {
        const input = document.getElementById('turing-input').value;
        
        if (!/^[01]+$/.test(input)) {
            alert("Por favor ingresa solo 0s y 1s");
            return;
        }
        
        fetch('/analyze', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({code: input, action: "turing"})
        })
        .then(response => response.json())
        .then(data => {
            const resultDiv = document.getElementById('turing-result');
            const pathDiv = document.getElementById('turing-path');
            const explanationDiv = document.getElementById('turing-explanation');
            
            resultDiv.textContent = data.accepted ? "ES ROBOT" : "NO ES ROBOT";
            resultDiv.className = data.accepted ? "accepted" : "rejected";
            
            explanationDiv.innerHTML = `
                <p>La Máquina de Turing validó que la cadena <strong>"${input}"</strong> ${data.accepted ? 'cumple' : 'no cumple'} con el patrón ROBOT.</p>
                <p>Una cadena ROBOT válida debe:</p>
                <ul>
                    <li>Empezar con 0</li>
                    <li>Alternar perfectamente entre 0 y 1</li>
                    <li>Terminar con 1</li>
                </ul>
                ${!data.accepted ? `<p><strong>Razón:</strong> ${data.reason || 'Patrón incorrecto'}</p>` : ''}
            `;
            
            pathDiv.innerHTML = '';
            data.path.forEach((step, index) => {
                const stepDiv = document.createElement('div');
                stepDiv.className = 'path-step';
                stepDiv.innerHTML = `
                    <strong>Paso ${index + 1}:</strong> Estado ${step.state} | 
                    Símbolo '${step.symbol}' | Cinta: ${step.tape} | 
                    Cabezal: posición ${step.head}
                `;
                pathDiv.appendChild(stepDiv);
            });
        });
    });
    
    document.getElementById('clear-btn').addEventListener('click', function() {
        editor.setValue('');
        document.querySelector('#tokens-table tbody').innerHTML = '';
        clearErrors();
        document.getElementById('turing-result').textContent = 'NO ES ROBOT';
        document.getElementById('turing-result').className = 'rejected';
        document.getElementById('turing-explanation').innerHTML = `
            <p>La Máquina de Turing validará si la cadena cumple con el patrón ROBOT.</p>
            <p>Una cadena ROBOT válida debe:</p>
            <ul>
                <li>Empezar con 0</li>
                <li>Alternar perfectamente entre 0 y 1</li>
                <li>Terminar con 1</li>
            </ul>
        `;
        document.getElementById('turing-path').innerHTML = '<div class="path-step">Ingresa una cadena y haz clic en Validar</div>';
        document.getElementById('turing-input').value = '0101';
    });
    
    let timeout;
    editor.on('change', function() {
        clearTimeout(timeout);
        timeout = setTimeout(function() {
            const code = editor.getValue();
            if (code.trim() === '') return;
            
            fetch('/analyze', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({code: code, action: "lexical"})
            })
            .then(response => response.json())
            .then(data => {
                clearErrors();
                data.errors.forEach(error => {
                    showError(error.line, error.message, error.correction);
                });
            });
        }, 1000);
    });
    
    clearErrors();
});