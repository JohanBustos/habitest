
# Modo de Ejecución

## Instalación de Dependencias

1. **Instalar Poetry**: Si no lo tienes, instálalo con:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```
2. **Instalar dependencias**: Ejecuta en el directorio raíz del proyecto:
   ```bash
   poetry install
   ```

## Configuración de la Base de Datos

1. **Requisitos**: Asegúrate de tener **Docker** instalado. Descárgalo desde [docker.com](https://www.docker.com/get-started).
2. **Iniciar la base de datos**:
   - Navega a `external_services`:
     ```bash
     cd external_services
     ```
   - Ejecuta:
     ```bash
     docker-compose up -d
     ```
3. **Configurar archivo `.env`**: Crea un archivo `.env` en la raíz del proyecto con:
   ```bash
   DB_HOST=localhost
   DB_NAME=habi
   DB_USER=user
   DB_PASSWORD=userpassword
   ```

## Ejecución del Servicio

1. Activa el entorno de Poetry:
   ```bash
   poetry shell
   ```
2. Ejecuta el servicio:
   ```bash
   python app.main
   ```

## Consumo del Servicio

El endpoint para consumir los datos del servicio es:

**POST** `http://host:port/property`

- **Consultar toda la información**: Envía un cuerpo vacío en la solicitud:
  ```json
  {}
  ```

- **Consultar con filtros**: Envía un JSON como este:
  ```json
  {
      "filters": {
          "state": "en_ventasss"
      },
      "order_by": "construction_year",
      "limit": 5
  }
  ```


### Detalles de los parámetros

Los siguientes parámetros son **opcionales** y te permiten personalizar la consulta:

- **filters**: Un diccionario donde las claves son nombres de columnas y los valores son condiciones de filtrado.
  - Los **campos disponibles** en `filters` corresponden a las columnas de la tabla `properties`:
    - `address`: Dirección de la propiedad (tipo `VARCHAR`).
    - `city`: Ciudad de la propiedad (tipo `VARCHAR`).
    - `state`: Estado de la propiedad (`ENUM` con valores `pre_venta`, `en_venta`, `vendido`).
    - `construction_year`: Año de construcción (tipo `INT`).
    - `price`: Precio de la propiedad (tipo `DECIMAL`).
    - `description`: Descripción de la propiedad (tipo `TEXT`).

#### Ejemplos de uso de `filters`:
1. **Filtrar por igualdad**:
   ```json
   {
       "filters": {
           "city": "Bogotá",
           "state": "en_venta"
       }
   }
   ```
   Este filtro devuelve todas las propiedades en la ciudad de Bogotá que están en venta.

2. **Filtrar por operadores**:
   ```json
   {
       "filters": {
           "price": [">", 500000000],
           "construction_year": ["<=", 2015]
       }
   }
   ```
   Este filtro devuelve todas las propiedades con un precio mayor a 500 millones y construidas hasta el año 2015.

3. **Filtrar con múltiples valores (`IN`)**:
   ```json
   {
       "filters": {
           "state": ["pre_venta", "en_venta"],
           "city": ["Medellín", "Cali"]
       }
   }
   ```
   Este filtro devuelve todas las propiedades que están en pre-venta o en venta y que están ubicadas en Medellín o Cali.

4. **Combinar diferentes tipos de filtros**:
   ```json
   {
       "filters": {
           "state": "vendido",
           "price": ["<", 300000000],
           "construction_year": [">", 2000]
       }
   }
   ```
   Este filtro devuelve propiedades vendidas con un precio menor a 300 millones y construidas después del año 2000.

- **order_by**: Una columna por la que deseas ordenar los resultados. Por ejemplo:
  ```json
  {
      "order_by": "price"
  }
  ```
  Esto devuelve los resultados ordenados por el precio de menor a mayor.

- **limit**: El número máximo de elementos a retornar. Por ejemplo:
  ```json
  {
      "limit": 10
  }
  ```
  Esto limita la cantidad de propiedades en el resultado a 10.

#### Ejemplo Completo
Si deseas obtener las propiedades en Bogotá o Cali que están en venta, ordenadas por el precio en orden descendente, con un límite de 5 propiedades, podrías usar el siguiente JSON:

```json
{
    "filters": {
        "city": ["Bogotá", "Cali"],
        "state": "en_venta"
    },
    "order_by": "price",
    "limit": 5
}
```

