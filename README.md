# WOW TRADE MANIAC
Dashboard está diseñado para los jugadores de World of Warcraft para mejorar sus experiencias de comercio. Se proporciona información sobre los precios de los objetos, recetas de elaboración y la relación entre diferentes objetos en el juego. Permite a los jugadores tomar decisiones informadas sobre la compra, venta y elaboración de objetos.
### Características

- Búsqueda y Filtro de Objetos: Busca fácilmente objetos y filtéralos por categorías.
- Información Gráfica: Visualiza varios gráficos que proporcionan información sobre los precios de los objetos y su historial.
- Árboles de Elaboración: Visualiza las dependencias de elaboración y comprende los componentes necesarios para crear objetos.


## Instalación
### 1. Clonar el Repositorio
```
git clone https://github.com/Nispeter/WOW_Trade_Maniac.git
cd WOW_Trade_Maniac 
```
### 2. Crear y Activar un Entorno Virtual

En Windows:
```
python -m venv venv
venv\Scripts\activate
```
En macOS y Linux:
```
python3 -m venv venv
source venv/bin/activate
```
### 3. Instalar las Dependencias
```
pip install -r requirements.txt
```
## Ejecución del Proyecto
Para ejecutar el proyecto, navega al directorio app y ejecuta el siguiente comando:
```
cd app
python app.py
```

## Gráficos del Dashboard

- Grafo de dependencias: Muestra la relación de dependencia entre los crafteos, indicando la cantidad y precio de las dependencias. Es útil para visualizar y entender los componentes necesarios para elaborar un objeto y sus costos asociados.
- Gráfico de Precio Mínimo a lo Largo del Tiempo
        Utilidad: Muestra el precio más bajo de un objeto en diferentes momentos.
- Gráfico de Distribución de Precios
        Utilidad: Proporciona una visión general de la variabilidad del precio de un objeto en un periodo determinado, muestra la volatilidad del mercado.
- Gráfico de Cantidad Vendida a lo Largo del Tiempo
        Utilidad: Muestra la cantidad de unidades vendidas en diferentes momentos, muestra la demanda de un objeto.
- Gráfico de Dispersión Precio vs Cantidad Vendida
        Utilidad: Permite visualizar la relación entre el precio de un objeto y la cantidad vendida, muestra el precio óptimo de un objeto

## Utilidad adicional del Dashboard

- Búsqueda por categoría: Barra lateral izquierda con todas las categorías del juego. Al seleccionar una categoría, se limita la lista de objetos en el buscador a esa categoría.\
        ![](https://github.com/Nispeter/WOW_Trade_Maniac/blob/main/app/assets/sidebar.png)
- Botón de limpiar búsqueda: Limpia el objeto buscado y las categorías seleccionadas.\
        ![](https://github.com/Nispeter/WOW_Trade_Maniac/blob/main/app/assets/reset.png)
- Barra por nombre: Permite buscar objetos específicos por su nombre, adicionalmente muestra los objetos limitados por la categoria en la seccion de dropdown.\
        ![](https://github.com/Nispeter/WOW_Trade_Maniac/blob/main/app/assets/Barra%20Superior.png)

## Consideraciones
- Los botones en la parte superior no tienen funcionalidad activa debido a una reducción en el alcance del proyecto.\
        ![](https://github.com/Nispeter/WOW_Trade_Maniac/blob/main/app/assets/botones.png)
- El proyecto puede demorar en cargar ya que no se diseñó una base de datos; en su lugar, todos los datos se cargan en la caché.
- La primera vez que se abre el proyecto, es posible que se deba recargar la página dos veces debido a un error en los callbacks que aún no ha sido solucionado.
