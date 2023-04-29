# Ejemplo de Map Reduce

Este ejemplo asume que ya tiene la BBDD MongoDB iniciada en Docker y accesible por Consola.

## Ejemplo

Obtener cuantaas películas se hicieron por lenguaje utilizando Map Reduce.

Resultado:
```
[
  { _id: 'Spanish', count: 135 },
  { _id: 'Chinese', count: 135 },
  { _id: 'Japanese', count: 134 },
  { _id: 'German', count: 134 },
  { _id: 'French', count: 134 },
  { _id: 'English', count: 119 },
  { _id: 'Russian', count: 107 },
  { _id: 'Italian', count: 102 }
]
```

### Solución
1. Se ingresa a la BBDD:

```
docker exec -it mcd-mongo-mysql_mongo_1 bash
```
2. Ya dentro del contenedor se ejecuta `mongosh -u root -p example`

3. Se ingresa a Sakila: `use sakila`.

4. Revisamos la estructura de la BBDD:

```javascript
db.film.find().limit(10)
```

5. Hacemos el map reduce.

```javascript
db.film.mapReduce(
    function map() {
        // this repreenta al documento
        emit(this.language_id, 1); // Para cad documento el language_id será el idioma y devolvemos 1 porque es lo que vamos a contar
    },
    function reduce(key, values) {
        return Array.sum(values)
    },
    {
        query: { rating: "R"},
        out: "language_qtty"
    }
);
```