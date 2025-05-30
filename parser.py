class Parser:
    def __init__(self):
        self.current_token = 0
        self.tokens = []
        self.errors = []
        
    def parse(self, tokens):
        self.tokens = tokens
        self.current_token = 0
        self.errors = []
        
        try:
            self.program()
            
            if self.errors:
                return {
                    "status": "error",
                    "errors": self.errors
                }
            return {
                "status": "success",
                "message": "Análisis sintáctico completado sin errores"
            }
        except Exception as e:
            return {
                "status": "error",
                "errors": self.errors + [{
                    "message": f"Error fatal: {str(e)}",
                    "line": self.get_current_line(),
                    "correction": "Revise la estructura del programa"
                }]
            }
    
    def program(self):
        while self.current_token < len(self.tokens):
            self.statement()
    
    def statement(self):
        token = self.peek()
        
        if token[0] == 'KEYWORD' and token[1] == 'si':
            self.if_statement()
        elif token[0] == 'KEYWORD' and token[1] == 'mientras':
            self.while_statement()
        elif token[0] == 'IDENT':
            self.assignment()
        elif token[0] in ('NUMBER', '(', 'OPERATOR', 'STRING') or (token[0] == 'SYMBOL' and token[1] == '('):
            self.expression()
            self.match('SYMBOL', ';', "Falta ';' al final de la expresión")
        else:
            self.error(f"Declaración no válida: '{token[1]}'", 
                      "Ejemplos válidos:\nx = 5 + 5;\n5 + 5;\nsi (x > 5) entonces { ... } fin")
            self.consume()
    
    def if_statement(self):
        self.match('KEYWORD', 'si', "Use 'si (condición) entonces'")
        self.match('SYMBOL', '(', "Falta '(' después de 'si'")
        self.logical_expression()
        self.match('SYMBOL', ')', "Falta ')' después de la condición")
        self.match('KEYWORD', 'entonces', "Falta 'entonces' después del if")
        
        if self.peek()[1] == '{':
            self.match('SYMBOL', '{', "Falta '{' después de 'entonces'")
            while not (self.peek()[0] == 'SYMBOL' and self.peek()[1] == '}'):
                self.statement()
            self.match('SYMBOL', '}', "Falta '}' para cerrar el bloque")
        else:
            self.statement()
        
        if self.peek()[1] == 'sino':
            self.match('KEYWORD', 'sino', None)
            if self.peek()[1] == '{':
                self.match('SYMBOL', '{', "Falta '{' después de 'sino'")
                while not (self.peek()[0] == 'SYMBOL' and self.peek()[1] == '}'):
                    self.statement()
                self.match('SYMBOL', '}', "Falta '}' para cerrar el bloque")
            else:
                self.statement()
        
        self.match('KEYWORD', 'fin', "Falta 'fin' para cerrar el condicional")
    
    def while_statement(self):
        self.match('KEYWORD', 'mientras', "Use 'mientras (condición) hacer'")
        self.match('SYMBOL', '(', "Falta '(' después de 'mientras'")
        self.logical_expression()
        self.match('SYMBOL', ')', "Falta ')' después de la condición")
        self.match('KEYWORD', 'hacer', "Falta 'hacer' después del while")
        
        if self.peek()[1] == '{':
            self.match('SYMBOL', '{', "Falta '{' después de 'hacer'")
            while not (self.peek()[0] == 'SYMBOL' and self.peek()[1] == '}'):
                self.statement()
            self.match('SYMBOL', '}', "Falta '}' para cerrar el bloque")
        else:
            self.statement()
        
        if self.peek()[1] == 'fin':
            self.match('KEYWORD', 'fin', None)
    
    def logical_expression(self):
        self.comparison()
        while self.peek()[0] == 'OPERATOR' and self.peek()[1] in ['&&', '||']:
            op = self.peek()[1]
            self.consume()
            self.comparison()
    
    def comparison(self):
        self.expression()
        while self.peek()[0] == 'OPERATOR' and self.peek()[1] in ['==', '!=', '<', '>', '<=', '>=']:
            op = self.peek()[1]
            self.consume()
            self.expression()
    
    def assignment(self):
        ident = self.peek()
        self.match('IDENT', None, None)
        self.match('OPERATOR', '=', "Falta '=' en la asignación")
        self.expression()
        self.match('SYMBOL', ';', "Falta ';' al final de la asignación")
    
    def expression(self):
        self.term()
        while self.peek()[0] == 'OPERATOR' and self.peek()[1] in '+-':
            op = self.peek()[1]
            self.consume()
            self.term()
    
    def term(self):
        self.factor()
        while self.peek()[0] == 'OPERATOR' and self.peek()[1] in '*/':
            op = self.peek()[1]
            self.consume()
            self.factor()
    
    def factor(self):
        token = self.peek()
        if token[0] in ('NUMBER', 'IDENT', 'STRING'):
            self.consume()
        elif token[1] == '(':
            self.match('SYMBOL', '(', None)
            self.logical_expression()
            self.match('SYMBOL', ')', "Falta ')' para cerrar la expresión")
        else:
            self.error(f"Factor no válido: {token[1]}", 
                      "Use un número, variable, string o expresión entre paréntesis")
            self.consume()
    
    def peek(self):
        if self.current_token < len(self.tokens):
            return self.tokens[self.current_token]
        return ('EOF', '', -1)
    
    def consume(self):
        if self.current_token < len(self.tokens):
            self.current_token += 1
    
    def match(self, expected_type, expected_value=None, correction_msg=None):
        token = self.peek()
        if token[0] == expected_type and (expected_value is None or token[1] == expected_value):
            self.consume()
        else:
            if expected_value:
                msg = f"Se esperaba '{expected_value}' pero se encontró '{token[1]}'"
            else:
                msg = f"Se esperaba {expected_type} pero se encontró {token[0]} ('{token[1]}')"
            
            self.error(msg, correction_msg)
            self.consume()
    
    def error(self, message, correction=None):
        line = self.get_current_line()
        self.errors.append({
            "message": message,
            "line": line,
            "correction": correction
        })
    
    def get_current_line(self):
        token = self.peek()
        if len(token) >= 3 and isinstance(token[2], int):
            return token[2]
        for i in range(self.current_token, max(-1, self.current_token-5), -1):
            if i < len(self.tokens) and len(self.tokens[i]) >= 3:
                return self.tokens[i][2]
        return 1