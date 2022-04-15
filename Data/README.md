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
* lista = [numero for numero in números] --> crea lista a partir de una
     iteración  
* lista = [numero for numero in números if numero % 2 == 0] --> crea lista a
     partir de iterar y comparar.
* lista = list(filter(lambda x: x%2 == 0), [1,2,3,4,5,6]) -- > crea lista de
    números pares

#### Tuplas
> Heterogeneo, inmutable.  tupla = (valor1,valor2)  
Métodos:
  * .count(elemento): cantidad de veces que aparece.
  * tupla2 = tupla.__ add __(tuplaNueva): retorna la conjuncion de dos tuplas.

#### Diccionarios
> dicc = {"key":valor, "key2":valor2}  (los valores repetidos se descartan)  
Métodos:
 * dicc.keys(): obtiene las keys.
 * dicc.values(): obtiene los valores.
 * dicc.items(): keys y valores
 * dicc["key"]: obtener los valores de determinada key, si no existe tira error
 * dicc.get("valor"): obtener los valores de determinada key si no existe devuelve None.

#### Conjuntos
> conjunto = set(iterable). Guarda los elementos únicos.  
Métodos:
  * .update(iterable): agrega todos los elementos del iterable
  * .add(elemento): agrega un elemento
  * .pop(): obtiene el último elemento
  * .remove(): elimina elemento
  * .difference(iterable): devuelve un nuevo set con los elementos que no están.
  * .union(iterable): devuelve un nuevo set con los elementos de los dos iterables.

#### CSV



#### JSON

##
