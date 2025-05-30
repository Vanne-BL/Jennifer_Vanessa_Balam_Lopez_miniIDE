# PROYECTO INTEGRADOR - MINI IDE WEB   

## INFORMACIÓN DEL ESTUDIANTE  


|**Datos**        |   **Descripción**                  |
|-----------------|------------------------------------|
| Nombre          | Jennifer Vanessa Balam López       |
| Matrícula       | 22230690                           |
| Materia         | Leng. Autómatas 1                  |
| Profesor        | Kevin David Molina Gómez           |
| Fecha de entrega| 30 de mayo de 2025                 |


## ESTRUCTURA 

![image](https://github.com/user-attachments/assets/b6b7008a-ea3b-4ecd-a072-f08920b29be5)


## GUÍA DE EJECUCIÓN  

### Requisitos previos
1. Asegúrate de tener Python 3.10+ instalado
2. Instala las dependencias necesarias: Flask 
3. Navegador web 

### Pasos para ejecución 
1. Descomprimir el proyecto: `Jennifer_Balam_miniIDE.zip` o entrar a la liga de github
2. Abrir la aplicación en Python: `app.py`
3. Ejecutar: `app.py`
4. Abrir en el navegador la liga proporcionada: `http://127.0.0.1:5000`

## DICCIONARIO DE LENGUAJE 


|**Palabras Clave**     | **Descripción** |
|-----------------------|-------------|
| Bloque verdadero      | entonces    |
| Bloque falso          | sino        |
| Inicia bucle          | mientras    |
| Ejecuta bucle         | hacer       |
| Termina bloque        | fin         |


| **Operadores**           |    **Descripción**                    |
|--------------------------|------------------------|
| Aritméticos              | + - * /                |
| Asignación/comparación   | = == !=                |
| Comparación              | < > <= >=              |
| Paréntesis               | ( )                    |
| Bloques de código        | { }                    |
| Fin de línea             | ;                      |


| **Tipo  de datos**      |     **Descripción**                    |
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

### Lexico
- 42:
- "Hola"
- x != y
- 2+3*4-7/9

  ![image](https://github.com/user-attachments/assets/96c3dbc3-c3a5-4e82-83d2-52690db17449)


### Sintactico
- edad = 25;
- total = (precio * cantidad) + iva;
- mientras (i == 0) hacer {
    i = i + 1;
}
- si (edad >= 18) entonces {
    status = "adulto"; 
} sino {
    status = "menor";  
} fin

![image](https://github.com/user-attachments/assets/b252518d-a559-49a1-811c-18726743a6e6)


### Maquina de turing
- 01
- 0101
- 010101
- 01010101

![image](https://github.com/user-attachments/assets/ba230465-ef8f-438f-8b9c-f0ee4dd9ea31)


# EJEMPLOS NO VALIDOS
### Lexico
- y=x#2;
- msg = "Hola;
- x=12.23.56;
- var&iable=3;

![image](https://github.com/user-attachments/assets/7c51fb91-d5c9-4bd6-bc9a-c1f814ba2952)


### Sintactico
- si (x > 5) entonces {
    y = 10;
}  
- mensaje = "Hola mundo;"
-  si (x = 5) entonces {  
    z = 20;
} fin
- resultado = a == b;  

![image](https://github.com/user-attachments/assets/22d5dfc8-cbcc-41b7-88cb-523469c1196e)


### Maquina de turing
- 0110
- 10101
- 110100
- 1011101

![image](https://github.com/user-attachments/assets/aa8a5561-d037-4462-9452-27406208ea4c)


