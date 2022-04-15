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
> Descripcion:
     Los archivos de tipo CSV son de tipo binario  y estan conformados por un diccionario 
     que consta de un indice y muchos valores para ese indice haciendo una estructura mas 
     ordenada y legible. 
Metodos:
* with open ('archivo.csv', 'r') as variable --> Abre el archivo .csv para lectura
* variable = csv.reader (archivo) --> Almacena la direccion de memoria del arhivo (llamaremos aux en los ej)
* for variable in aux:  
     print (vriable)   --> Imprime primero los nombres de los indices y despues todos los valores por cada indice
                           linea por linea
* for variable in aux:   
     print (variable[x]) --> Hace lo mismo que en el metodo anterior pero solo imprime los valores del indice que 
                            contiene x, por ej si los indices son (nombre,apellido,email) y x vale 1 solo imprimira
                            la columna del apellido (se cuanta desde 0)
* with open ('archivo.csv', 'w') as variable --> Abro crea un archivo .csv para escritura (llamaremos aux2 en los ej)
* variable = csv.writer(aux2) --> Se copia la informacion del archivo la informacion de la variable (si la variable
                                     contiene el arhcivo se pasa todo el archivo)



#### JSON


## Archivos
### Path

> Importar os  
> ruta_local = os.path.abspath(os.path.dirname(__ file __))  
> Concatenar: "".join(ruta_local, nombre_archivo)

#### CSV
> Importar: Se realiza un "import csv"  
> Descripcion:
     Los archivos de tipo CSV son de tipo binario  y estan conformados por un diccionario 
     que consta de un indice y muchos valores para ese indice haciendo una estructura mas 
     ordenada y legible. 
Metodos:
* with open ('archivo.csv', 'r') as variable --> Abre el archivo .csv para lectura
* variable = csv.reader (archivo) --> Almacena la direccion de memoria del arhivo (llamaremos aux en los ej)
* for variable in aux:  
     print (vriable)   --> Imprime primero los nombres de los indices y despues todos los valores por cada indice
                           linea por linea
* for variable in aux:   
     print (variable[x]) --> Hace lo mismo que en el metodo anterior pero solo imprime los valores del indice que 
                            contiene x, por ej si los indices son (nombre,apellido,email) y x vale 1 solo imprimira
                            la columna del apellido (se cuanta desde 0)
* variable = csv.DictReader(aux) --> Hace que se imprima todo el contenido del archivo liena por linea con la 
                                    diferencia que imprime cada valor con si indice a su lado (con csv.reader seria
                                    por ej ['Matias', 'Daglio', 'mailej@gmial.com'], pero con csv.DictReader seria 
                                    [('nombre', 'Matias'),('apellido', 'Dalgio'),('email', 'mailej@gmial.com')] )
* with open ('archivo.csv', 'w') as variable --> Abro crea un archivo .csv para escritura (llamaremos aux2 en los ej)
* variable = csv.writer(aux2) --> Se copia la información del archivo la informacion de la variable (si la variable
                                  contiene el arhcivo se pasa todo el archivo)
* variable = csv.writer(aux2, delimeter = 'caracter') --> El delimeter busca donde se termina cada valor del indice
                                                          y lo delimita con el caracter que se haya puesto despues 
                                                          del delimiter. Por ej si se tiene Matias Daglio mailej@gmial.com 
                                                          naturalmente se almacena Matias,Daglio,mailej@gmial.com, ahora 
                                                          supongamos que se uso el delimeter con caracter = '-', entonces 
                                                          quedaria Matias-Daglio-mailej@gmial.com y en caso de que algun 
                                                          valor tenga ese caracter, por ej Mat-ias, quedaria 
                                                          "Mat-ias",Daglio,mailej@gmial.com usando las " para decir que el 
                                                          string ese los que hay ente comillas y el caracter '-' no es 
                                                          un separador