# wildlife-insights-utils

`wiutils` tiene utilidades para la transformación y la exploración de información descargada de proyectos de Wildlife Insights.

## Instalación

Con `pip`:
```shell
pip install wiutils
```

Con `conda`:
```shell
conda install -c conda-forge wiutils
```

## Ejecución
Para asegurarse que la instalación de `wiutils` fue satisfactoria ejecute el siguiente comando:

```shell
python -c "import wiutils"
```
Si el comando no arroja ningún error, la instalación fue satisfactoria.

Puede acceder a las funciones de `wiutils` importando el paquete desde una consola o un script de Python. Para mayor información sobre las funciones disponibles, consulte la [documentación](https://wiutils.readthedocs.io).

## Cómo contribuir

Se recomienda que la instalación del paquete en modo de desarrollo se haga en un [entorno virtual](https://www.python.org/dev/peps/pep-0405/) para no alterar otras instalaciones existentes de Python en el sistema.

1. Clone este repositorio en su máquina:
```shell
git clone https://github.com/PEM-Humboldt/wildlife-insights-utils.git
```

2. Ubíquese en la raíz del proyecto:
```shell
cd wildlife-insights-utils
```

3. Instale el paquete en modo de desarrollo:
```shell
pip install --editable .[dev,docs,test]
```


### Ejecución de pruebas unitarias
Ubicado dentro del proyecto, ejecute:

```
pytest tests/
```

## Autores y contribuidores

* Angélica Diaz-Pulido
* Marcelo Villa-Piñeros - [marcelovilla](https://github.com/marcelovilla)

## Licencia
Este paquete tiene una licencia MIT. Ver [LICENSE.txt](LICENSE.txt) para más información.

[1]: https://github.com/Toblerity/Fiona#installation
[2]: https://github.com/mapbox/rasterio#installation
