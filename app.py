from flask import Flask, render_template, request, jsonify
from lexer import Lexer
from parser import Parser
from turing_machine import TuringMachine
import json

app = Flask(__name__)

# Datos actualizados del estudiante
STUDENT_INFO = {
    "Nombre": "JENNIFER VANESSA BALAM LÓPEZ",
    "Matricula": "22230690",
    "Materia": "LENG.AUTÓMATAS I",
    "Profesor": "KEVIN DAVID MOLINA GÓMEZ"
}

@app.route('/')
def index():
    return render_template('index.html', student_info=STUDENT_INFO)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    code = data['code']
    action = data['action']
    
    try:
        if action == "lexical":
            lexer = Lexer()
            tokens, errors = lexer.tokenize(code)
            
            formatted_tokens = []
            for token in tokens:
                if len(token) == 3:
                    formatted_tokens.append(token)
                else:
                    formatted_tokens.append((token[0], token[1], "N/A"))
            
            return jsonify({
                "tokens": formatted_tokens,
                "errors": errors
            })
        
        elif action == "syntax":
            lexer = Lexer()
            parser = Parser()
            tokens, lex_errors = lexer.tokenize(code)
            
            if lex_errors:
                return jsonify({
                    "status": "error",
                    "errors": lex_errors
                })
            
            parse_result = parser.parse(tokens)
            return jsonify(parse_result)
        
        elif action == "turing":
            tm = TuringMachine()
            result = tm.run(code)
            return jsonify(result)
        
        return jsonify({"error": "Acción no válida"}), 400
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "errors": [{
                "message": f"Error interno: {str(e)}",
                "line": 1,
                "correction": "Revise la sintaxis del código"
            }]
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)