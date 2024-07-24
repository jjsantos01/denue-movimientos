# Análisis de altas y bajas en el DENUE entre 2015 y 2019

En este repositorio se encuentra un análisis comparativo entre 2015 y 2019 de la creación (altas) y cierre (bajas) de negocios registrados en el DENUE, que es el Directorio Estadístico Nacional de Unidades Económicas, el cual es un registro administrado por el INEGI que contiene información sobre las unidades económicas del país.

En el notebook [analisis_denue.ipynb](/analisis_denue.ipynb) viene el procesamiento de los datos originales del DENUE y el análisis de las altas y bajas de negocios en México entre 2015 y 2019, a nivel estatal, municipal y por sector económico. Para facilitar su consulta, creé una aplicación web con Streamlit que se encuentra en el folder [app](/app) y permite seleccionar de forma interactiva, cualquier estado, municipio y sector económico y despliega una visualización con las altas y bajas registradas.

Algunas de las gráficas que se generan en el notebook son las siguientes:

![](/graficas/denue_19_mex.png)

![](/graficas/denue_19_zmvm.png)

![](/graficas/denue_bajas_altas_15_19_mex.png)

![](/graficas/Unidades%20económicas%20dadas%20de%20alta%20y%20baja%20entre%202015%20y%202019,%20Nacional.png)

![](/graficas/Unidades%20económicas%20dadas%20de%20alta%20y%20baja%20entre%202015%20y%202019,%20sector%20Industria%20de%20las%20bebidas%20y%20del%20tabaco.png)

![](/graficas/Unidades%20económicas%20dadas%20de%20alta%20y%20baja%20entre%202015%20y%202019,%20sector%20Total.png)
