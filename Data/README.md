# Módulos

## Git

#### Comandos

> **Crear repositorio local**: git init  
> **Agregar archivos**: git add nombre archivo   
> **Agregar todo**: git add .  
> **Remover archivos**: git rm nombre archivo  
> **Realizar cambios**: git commit -m "Mensaje"  
> **Subir al repositorio**: git push origin "rama"  
> **Bajar del repositorio**: git pull origin "rama"  
> **Revisar modificaciones**: git log  
>
> **Enlazar repositorio local y virtual**
>1. git clone "enlace" (sin las comillas)
>2. git pull origin main (actualiza repositorio local)
>3. git push origin main (actualiza repositorio virtual)




## Estructuras

#### Listas

> Métodos:
> * **Agrega al final:** lista.append(elemento)
> * **Obtiene el último elemento de la lista:** lista.pop()  
> * **Cantidad de elementos según X valor:** lista.count(valor)  
> * **Crear lista a partir de una iteración:** lista = [numero for numero in números]  
> * **Crear lista a partir de iterar y comparar:** lista = [numero for numero in números if numero % 2 == 0]
> * **Crear lista con filter:** lista = list(filter(lambda x: x%2 == 0), [1,2,3,4,5,6]) (filter guarda los valores para los que la comparación es verdadera) 

#### Tuplas
> Heterogeneo, inmutable.  tupla = (valor1,valor2)  
Métodos:
>  * **.count(elemento):** cantidad de veces que aparece el elemento.
>  * **tupla2 = tupla.__ add __(tuplaNueva):** retorna la conjuncion de dos tuplas.

#### Diccionarios
> dicc = {"key":valor, "key2":valor2}  (los valores repetidos se descartan)  
Métodos:
> * **dicc.keys():** obtiene las keys.
> * **dicc.values():** obtiene los valores.
> * **dicc.items():** keys y valores
> * **dicc["key"]:** obtener los valores de determinada key, si no existe tira error
> * **dicc.get("valor")**: obtener los valores de determinada key si no existe devuelve None.

#### Conjuntos
> conjunto = set(iterable). Guarda los elementos únicos.  
Métodos:
>   * **.update(iterable):** agrega todos los elementos del iterable
>   * **.add(elemento):** agrega un elemento
>   * **.pop():** obtiene el último elemento
>   * **.remove():** elimina elemento
>   * **.difference(iterable):** devuelve un nuevo set con los elementos que no están.
>   * **.union(iterable):** devuelve un nuevo set con los elementos de los dos iterables.



## Archivos
#### Path

> Importar os  
> ruta_local = os.path.abspath(os.path.dirname(__ file __))  
> Concatenar: "".join(ruta_local, nombre_archivo)

#### CSV
> Los archivo CSV son archivos de texto separados por coma que representan una tabla. En la primera fila están los headers, contienen la "categoría" de cada item en las filas siguientes. Para usar las funciones hay que hacer **import csv**.
>
>Funciones:
> * **Modo lectura:** archivo = open ('archivo.csv', 'r', encoding='utf-8') luego se cierra con archivo.close()
>  * _**Obtener el contenido**_
>      *  Cada linea del contenido como lista: **contenido = csv.reader(archivo)**
>      *  Contenido como diccionario donde las keys son los items de la cabecera y los valores
           son los items de cada fila. **contenido = csv.DictReader(archivo)**
> * **Modo escritura:** archivo = open ('archivo.csv', 'w', encoding='utf-8') luego se cierra con archivo.close()
>  * _**Escribir contenido**_
>      



*********************************************
* with open ('archivo.csv', 'w') as variable --> Abro crea un archivo .csv para escritura (llamaremos aux2 en los ej)
* variable = csv.writer(aux2) --> Se copia la información del archivo la información de la variable (si la variable contiene el archivo se pasa todo el archivo)
* variable = csv.writer(aux2, delimeter = 'caracter') --> El delimeter busca donde se termina cada valor del indice y lo delimita con el carácter que se haya puesto después del delimiter. Por ej si se tiene Matias Daglio mailej@gmial.com naturalmente se almacena Matias,Daglio,mailej@gmial.com, ahora supongamos que se uso el delimeter con caracter = '-', entonces quedaría Matias-Daglio-mailej@gmial.com y en caso de que algún valor tenga ese caracter, por ej Mat-ias, quedaria "Mat-ias",Daglio,mailej@gmial.com usando las " para decir que el string ese los que hay ente comillas y el caracter '-' no es un separador
