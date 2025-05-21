> [!NOTE]
># Misión Interestelar
>Un sistema con interfaz gráfica que permita resolver un reto de exploración galáctica basado en una matriz MxN (mínimo 30x30), donde el objetivo es que una nave llegue desde una celda origen hasta una celda destino siguiendo ciertas reglas y restricciones complejas

> [!CAUTION]
>## Como instalar FastAPI
>pip install "fastapi[standard]" \
>Documentation: https://fastapi.tiangolo.com 

> [!IMPORTANT]
>## Como se debe correr el back 
>Se debe colocar este comando en la termina en la ubicacion de la carpeta principal, no se debe entrar a ninguna carpeta.\
>Comando: uvicorn app.main:app --reload 

> [!TIP]
 >## Que se esepera recibir al correr y probar con postman 
>al correr el back, se debe colocar esta  ruta en postman:
>http://localhost:8000/resolver/ \
>esta ruta es para un post, en el cual nos ubicamos en Body, luego en from-data, y eN la tabla ponemos en key: file, selecionamos al frente File, ya que siempre esta por defecto text, y en value, selecionamos el archivo JSON. Posteriormente podemos enviar la request, lo cual devuelve una ruta de solucion, como la siguiente:
 ```bash
{
  "mensaje": "Ruta encontrada",
  "camino": [
    [0, 0],
    [0, 1],
    [0, 2],
    [0, 3],
    [0, 4],
    [0, 5],
    [1, 5],
    [1, 6],
    [2, 6],
    [3, 6],
    [3, 7],
    [4, 7],
    [5, 7],
    [5, 8],
    [5, 9],
    [6, 9],
    [7, 9],
    [8, 9],
    [9, 9],
    [9, 10],
    [10, 10],
    [11, 10],
    [11, 11],
    [13, 13],
    [14, 13],
    [14, 14],
    [14, 15],
    [15, 15],
    [16, 15],
    [16, 16],
    [16, 17],
    [17, 17],
    [17, 18],
    [17, 19],
    [17, 20],
    [17, 21],
    [17, 22],
    [18, 22],
    [19, 22],
    [19, 23],
    [19, 24],
    [19, 25],
    [20, 25],
    [20, 26],
    [20, 27],
    [20, 28],
    [20, 29],
    [21, 29],
    [22, 29],
    [22, 30],
    [23, 30],
    [24, 30],
    [25, 30],
    [25, 31],
    [25, 32],
    [25, 33],
    [25, 34],
    [25, 35],
    [25, 36],
    [26, 36],
    [27, 36],
    [27, 37],
    [28, 37],
    [29, 37],
    [30, 37],
    [31, 37],
    [32, 37],
    [32, 38],
    [32, 39],
    [33, 39],
    [34, 39]
  ],
  "energiaRestante": 9,
  "pasosEvaluados": 1378
}
