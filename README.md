# Dashboard WOW TRADE MANIAC
Dashboard está diseñado para los jugadores de World of Warcraft para mejorar sus experiencias de comercio. Se proporciona información sobre los precios de los objetos, recetas de elaboración y la relación entre diferentes objetos en el juego. Permite a los jugadores tomar decisiones informadas sobre la compra, venta y elaboración de objetos.
### Características

- Búsqueda y Filtro de Objetos: Busca fácilmente objetos y filtéralos por categorías.
- Información Gráfica: Visualiza varios gráficos que proporcionan información sobre los precios de los objetos y su historial.
- Árboles de Elaboración: Visualiza las dependencias de elaboración y comprende los componentes necesarios para crear objetos.

## Contexto
World of Warcraft  es un juego de rol multijugador masivo en línea (MMORPG) desarrollado por Blizzard Entertainment. Desde su lanzamiento en 2004, WoW ha cautivado a millones de jugadores con su vasto mundo de fantasía, misiones épicas y complejas mecánicas de juego. Los jugadores pueden elegir entre diversas razas y clases, participar en misiones, explorar mazmorras y competir en batallas PvP.
El WoW Trade Maniac Dashboard está diseñado específicamente para jugadores interesados en el comercio y la elaboración de objetos dentro del juego. El comercio en WoW es una parte crucial del juego, donde los jugadores pueden comprar, vender e intercambiar una amplia variedad de objetos, desde materiales de elaboración hasta poderosos equipos y consumibles por medio de una casa de subastas, la cual se ocupa de gestionar las transacciones entre jugadores, simulando economia real.
![Auction_House_8 3](https://github.com/Nispeter/WOW_Trade_Maniac/assets/64810836/3ff422dd-cbff-488e-ae3f-de5ca8630f32)
*imagen de la UI de la casa de subastas dentro del juego*

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

- Grafo de dependencias: Muestra la relación de dependencia entre los crafteos, indicando la cantidad y precio de las dependencias. Es útil para visualizar y entender los componentes necesarios para elaborar un objeto y sus costos asociados.\
![](https://github.com/Nispeter/WOW_Trade_Maniac/blob/main/app/assets/grafico_grafo.png)
- Gráfico de Precio Mínimo a lo Largo del Tiempo:
        Muestra el precio más bajo de un objeto en diferentes momentos.\
![](https://github.com/Nispeter/WOW_Trade_Maniac/blob/main/app/assets/precio_minimo.png)
- Gráfico de Distribución de Precios:
        Proporciona una visión general de la variabilidad del precio de un objeto en un periodo determinado, muestra la volatilidad del mercado.\
  ![](https://github.com/Nispeter/WOW_Trade_Maniac/blob/main/app/assets/distribucion.png)
- Gráfico de Cantidad Vendida a lo Largo del Tiempo:
        Muestra la cantidad de unidades vendidas en diferentes momentos, muestra la demanda de un objeto.\
  ![](https://github.com/Nispeter/WOW_Trade_Maniac/blob/main/app/assets/cantidad_vendida.png)
- Gráfico de Dispersión Precio vs Cantidad Vendida:
        Permite visualizar la relación entre el precio de un objeto y la cantidad vendida, muestra el precio óptimo de un objeto\
![](https://github.com/Nispeter/WOW_Trade_Maniac/blob/main/app/assets/dispersion.png)

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
- La primera vez que se abre el proyecto, es posible que se deba recargar la página dos veces debido a un error en los callbacks que aún no ha sido solucionado.\
![](https://github.com/Nispeter/WOW_Trade_Maniac/blob/main/app/assets/error.png)
