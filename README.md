# PROYECTO INTEGRADOR - MINI IDE WEB   

## INFORMACIÓN DEL ESTUDIANTE  


|**Datos**        |                                     |
|-----------------|------------------------------------|
| Nombre          | Jennifer Vanessa Balam López       |
| Matrícula       | 22230690                           |
| Materia         | Leng. Autómatas 1                  |
| Profesor        | Kevin David Molina Gómez           |
| Fecha de entrega| 30 de mayo de 2025                 |


## ESTRUCTURA 

miniIDE/
├── app.py # Aplicación principal Flask
├── lexer.py # Analisis léxico
├── parser.py # Analisis sintáctico
├── README.md # Intructivo
├── turing_machine.py # Máquina de Turing
├── templates/
│ └── index.html # Interfaz web
└── static/
├── style.css # Estilos CSS
└── script.js # Lógica frontend


## GUÍA DE EJECUCIÓN  

### Requisitos previos
1. Asegúrate de tener Python 3.10+ instalado
2. Instala las dependencias necesarias: Flask 
3. Navegador web 

### Pasos para ejecución 
1. Descomprimir el proyecto: `Jennifer_Balam_miniIDE.zip`
2. Abrir la aplicación en Python: `app.py`
3. Ejecutar: `app.py`
4. Abrir en el navegador la liga proporcionada: `http://127.0.0.1:5000`

## DICCIONARIO DE LENGUAJE 


|**Palabras Clave**     |             |
|-----------------------|-------------|
| Bloque verdadero      | entonces    |
| Bloque falso          | sino        |
| Inicia bucle          | mientras    |
| Ejecuta bucle         | hacer       |
| Termina bloque        | fin         |


| **Operadores             |                        |
|--------------------------|------------------------|
| Aritméticos              | + - * /                |
| Asignación/comparación   | = == !=                |
| Comparación              | < > <= >=              |
| Paréntesis               | ( )                    |
| Bloques de código        | { }                    |
| Fin de línea             | ;                      |


| **Tipo  de datos**      |                         |
|-------------------------|-------------------------|
| Números enteros         | 123                     |
| Números decimales       | 12.34                   |
| Cadenas                 | "texto"                 |
| Identificadores         | variable                |

## TOKENS

| **Datos**| **Descripción**                                             |
|----------|-------------------------------------------------------------|
| NUMBER   | Números enteros o decimales                                 |
| OPERATOR | Operadores aritméticos y relacionales                       |
| STRING   | Cadenas de texto entre comillas dobles                      |
| KEYWORD  | Palabras reservadas del lenguaje                            |
| SYMBOL   | Símbolos y delimitadores                                    |
| IDENT    | Identificadores                                             |

## MANEJO DE ERRORES 

### Léxicos

1. **Caracteres no válidos**  
   - Ejemplo: `x = @5;`  
   - Corrección: Carácter no válido: `@` - Remueva el símbolo no reconocido

2. **Strings no cerrados**  
   - Ejemplo: `mensaje = "Hola mundo;`  
   - Corrección: Cierre el string con comillas: `"texto"`

3. **Comentarios mal formados**  
   - Ejemplo: `/ esto no es un comentario válido`  
   - Corrección: Use `//` para comentarios de una línea

### Sintácticos

1. **Falta de punto y coma**  
   - Ejemplo: `x = 5`  
   - Corrección: `x = 5;`

2. **Condicionales mal formados**  
   - Ejemplo: `si x > 5) entonces y=10;fin`  
   - Corrección: `si (x > 5) entonces y=10;fin`

3. **Paréntesis no balanceados**  
   - Ejemplo: `y = (5 + (3 * 2);`  
   - Corrección: `y = (5 + (3 * 2));`

4. **Bloques no abiertos**  
   - Ejemplo: `mientras (x < 10) hacer  x = x + 1;}`  
   - Corrección: `mientras (x < 10) hacer { x = x + 1; }`

5. **Estructuras incompletas**  
   - Ejemplo: `si (cond) entonces { }`  
   - Corrección: `si (cond) entonces { } fin`

### Máquina de Turing

1. **Cadena no binaria**  
   - Ejemplo: `012`  
   - Corrección: La cadena debe contener solo 0s y 1s

2. **No comienza con 0**  
   - Ejemplo: `1010`  
   - Corrección: La cadena debe comenzar con 0

3. **Dos símbolos iguales consecutivos**  
   - Ejemplo: `0011`  
   - Corrección: Los símbolos 2 y 3 son iguales (0)

4. **No termina con 1**  
   - Ejemplo: `0100`  
   - Corrección: La cadena debe terminar con 1

5. **Transición no definida**  
   - Ejemplo: Cadena vacía  
   - Corrección: Transición no definida para estado q0 y símbolo `_`

## EJEMPLOS VÁLIDOS

**Lexico**
1. 42:
2. "Hola"
3. x != y
4. 2+3*4-7/9

**Sintactico**
1. edad = 25;
2. total = (precio * cantidad) + iva;
3. mientras (i == 0) hacer {
    i = i + 1;
}
4. si (edad >= 18) entonces {
    status = "adulto"; 
} sino {
    status = "menor";  
} fin

**Maquina de turing**
1. 01
2. 0101
3. 010101
4. 01010101


# EJEMPLOS NO VALIDOS
**Lexico**
1. y=x#2;
2. msg = "Hola;
3. x=12.23.56;
4. var&iable=3;

**Sintactico**
1. si (x > 5) entonces {
    y = 10;
}  
2. mensaje = "Hola mundo;"
3. si (x = 5) entonces {  
    z = 20;
} fin
4. resultado = a == b;  

**Maquina de turing**
1. 0110
2. 10101
3. 110100
4. 1011101

