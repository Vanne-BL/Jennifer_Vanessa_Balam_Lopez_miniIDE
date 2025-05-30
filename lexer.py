import re

class Lexer:
    def __init__(self):
        self.keywords = ['si', 'entonces', 'sino', 'mientras', 'hacer', 'fin']
        self.operators = ['+', '-', '*', '/', '=', '==', '!=', '<', '>', '<=', '>=', '&&', '||']
        self.symbols = ['(', ')', '{', '}', ';']
        
    def tokenize(self, code):
        code = re.sub(r'//.*', '', code)
        
        tokens = []
        errors = []
        line_number = 1
        line_start = 0
        
        token_specs = [
            ('NUMBER', r'\d+(\.\d+)?'),
            ('OPERATOR', r'(\+|-|\*|/|==?|!=|<=?|>=?|\|\|)'),
            ('STRING', r'"[^"]*"'),
            ('KEYWORD', r'\b(si|entonces|sino|mientras|hacer|fin)\b'),
            ('SYMBOL', r'[(){};]'),
            ('IDENT', r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('NEWLINE', r'\n'),
            ('SKIP', r'[ \t]+'),
            ('MISMATCH', r'.')
        ]
        
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specs)
        
        for mo in re.finditer(tok_regex, code):
            kind = mo.lastgroup
            value = mo.group()
            column = mo.start() - line_start
            
            if kind == 'NEWLINE':
                line_number += 1
                line_start = mo.end()
                continue
            elif kind == 'SKIP':
                continue
            elif kind == 'MISMATCH':
                errors.append({
                    'message': f"Carácter no válido: '{value}'",
                    'line': line_number,
                    'correction': self.suggest_correction(value, line_number, code)
                })
                continue
            
            if kind == 'IDENT' and value in self.keywords:
                kind = 'KEYWORD'
            
            tokens.append((kind, value, line_number))
        
        return tokens, errors
    
    def suggest_correction(self, char, line, code):
        lines = code.split('\n')
        current_line = lines[line-1]
        
        if char == '"':
            return 'Cierra el string con comillas: "texto"'
            
        if not current_line.strip().endswith(';') and any(op in current_line for op in ['+', '-', '*', '/', '=']):
            return f"Falta ';' al final. Ejemplo: {current_line.strip()};"
            
        if 'si' in current_line or 'mientras' in current_line:
            if '(' not in current_line:
                return current_line.replace('si', 'si (').replace('mientras', 'mientras (') + ')'
                
        return "Revise la sintaxis de la expresión"