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
>2. git branch -M main
>3. git push -u origin main

## Path

> Importar os  
> ruta_local = os.path.abspath(os.path.dirname(__ file __))  
> Concatenar: "".join(ruta_local, nombre_archivo)


## Estructuras

#### Listas

> Métodos:
* .append(elemento) --> Agrega al final  
* .pop() --> Obtiene el último elemento de la lista.  
* .count(valor) --> Cantidad de elementos según X valor  
* lista = [numero for numero in numeros] --> crea lista a partir de una 
     iteración  
* lista = [numero for numero in numeros if numero % 2 == 0] --> crea lista a 
     partir de iterar y comparar.
* lista = list(filter(lambda x: x%2 == 0), [1,2,3,4,5,6]) -- > crea lista de
    numeros pares

#### Tuplas
> Declaracion:  
Métodos:

#### Diccionarios
> Declaracion:  
Métodos:

#### Conjuntos
> Declaracion:  
Métodos:

#### CSV
> Importar: Se realiza un "import csv"
>Descripcion:
     Los archivos de tipo CSV son de tipo binario  y estan conformados por un diccionario 
     que consta de un indice y muchos valores para ese indice haciendo una estructura mas 
     ordenada y legible. 
Metodos:
* with open ('archivo.csv', 'r') as variable -->Abre el archivo .csv para lectura
* variable = csv.reader (archivo) --> Almacena la direccion de memoria del arhivo (llamaremos aux en los ej)
* for variable in aux: 
     print (vriable)   --> Imprime primero los nombres de los indices y despues todos los valores por cada indice
                           linea por linea
* for variable in aux: 
     print (vriable[x]) --> Hace lo mismo que en el metodo anterior pero solo imprime los valores del indice que 
                            contiene x, por ej si los indices son (nombre,apellido,email) y x vale 1 solo imprimira
                            la columna del apellido (se cuanta desde 0)
* with open ('archivo.csv', 'w') as variable -->Abreo crea un archivo .csv para escritura



#### JSON

## 
