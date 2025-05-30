class TuringMachine:
    def __init__(self):
        self.transitions = {
            # Estado q0: espera 0
            ('q0', '0'): ('q1', 'X', 'R'),
            ('q0', '1'): ('qr', '1', 'R', "Error: debe comenzar con 0"),
            ('q0', 'X'): ('q3', 'X', 'R'),
            ('q0', '_'): ('qa', '_', 'R'),  # Cadena vacía aceptada si es ROBOT
            
            # Estado q1: espera 1 después de 0
            ('q1', '0'): ('qr', '0', 'R', "Error: dos 0 seguidos"),
            ('q1', '1'): ('q2', 'X', 'R'),
            ('q1', 'X'): ('qr', 'X', 'R', "Error: falta 1"),
            ('q1', '_'): ('qr', '_', 'R', "Error: cadena incompleta"),
            
            # Estado q2: espera 0 después de 1
            ('q2', '0'): ('q1', 'X', 'R'),
            ('q2', '1'): ('qr', '1', 'R', "Error: dos 1 seguidos"),
            ('q2', 'X'): ('q0', 'X', 'R'),  # Volver al inicio
            ('q2', '_'): ('qa', '_', 'R'),  # Aceptar si terminó correctamente
            
            # Estado q3: verificación final
            ('q3', 'X'): ('q3', 'X', 'R'),
            ('q3', '_'): ('qa', '_', 'R'),
            ('q3', '0'): ('qr', '0', 'R', "Error: 0 sin procesar"),
            ('q3', '1'): ('qr', '1', 'R', "Error: 1 sin procesar")
        }
        self.accept_state = 'qa'
        self.reject_state = 'qr'
    
    def run(self, input_str):
        tape = list(input_str + '_')
        head = 0
        state = 'q0'
        path = []
        rejection_reason = None
        
        max_steps = 100
        step_count = 0
        
        while state != self.accept_state and state != self.reject_state and step_count < max_steps:
            current_symbol = tape[head] if head < len(tape) else '_'
            
            path.append({
                'state': state,
                'head': head,
                'tape': ''.join(tape).replace('_', ' ').strip(),
                'symbol': current_symbol
            })
            
            key = (state, current_symbol)
            if key in self.transitions:
                transition = self.transitions[key]
                new_state = transition[0]
                write = transition[1]
                move = transition[2]
                
                if len(transition) > 3 and new_state == self.reject_state:
                    rejection_reason = transition[3]
                
                if head < len(tape):
                    tape[head] = write
                else:
                    tape.append(write)
                
                if move == 'R':
                    head += 1
                elif move == 'L':
                    head = max(0, head - 1)
                
                state = new_state
            else:
                state = self.reject_state
                rejection_reason = f"Transición no definida para estado '{state}' y símbolo '{current_symbol}'"
            
            step_count += 1
        
        # Estado final
        path.append({
            'state': state,
            'head': head,
            'tape': ''.join(tape).replace('_', ' ').strip(),
            'symbol': tape[head] if head < len(tape) else '_'
        })
        
        accepted = state == self.accept_state
        
        # Verificación adicional para cadenas válidas
        if accepted:
            # Verificar que sea alternancia perfecta
            for i in range(len(input_str)-1):
                if input_str[i] == input_str[i+1]:
                    accepted = False
                    rejection_reason = f"Los símbolos {i+1} y {i+2} son iguales ({input_str[i]})"
                    break
            
            # Verificar que termine en 1
            if accepted and input_str and input_str[-1] != '1':
                accepted = False
                rejection_reason = "La cadena debe terminar con 1"
        
        return {
            'accepted': accepted,
            'path': path,
            'final_tape': ''.join(tape).replace('_', ''),
            'message': "ES ROBOT" if accepted else "NO ES ROBOT",
            'reason': rejection_reason
        }