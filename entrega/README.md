# Laboratorio 03

Carlos Daniel Estrada Vega - 20853. Trabajo individual.

El informe contiene la investigación, el diagrama AES-128, el análisis del código,
las mejoras, la descripción del reparto MPI, las pruebas y los tiempos reales.
Incluye seis capturas reales de compilación y ejecución en Windows Terminal,
además de los registros completos de la evaluación automatizada.

## Compilar en Ubuntu o WSL

```bash
sudo apt update
sudo apt install build-essential libssl-dev libopenmpi-dev openmpi-bin python3
cd programas
make
```

El Makefile compila el programa original, el mejorado y el paralelo con C11,
optimización `-O2` y advertencias activadas. Los ejecutables incluidos corresponden
a Linux x86-64; se recomienda recompilar en el equipo de evaluación.

## Ejecutar

```bash
./busqueda_clave_aes_secuencial
./busqueda_clave_aes_mejorada preparar ../resultados/datos.aes 1048575 'Puedes lograrlo!'
./busqueda_clave_aes_mejorada buscar ../resultados/datos.aes 1048576
mpirun --bind-to core -n 2 ./busqueda_clave_aes_mpi ../resultados/datos.aes 1048576 4096
mpirun --bind-to core -n 3 ./busqueda_clave_aes_mpi ../resultados/datos.aes 1048576 4096
mpirun --bind-to core -n 4 ./busqueda_clave_aes_mpi ../resultados/datos.aes 1048576 4096
```

Si la sesión de Ubuntu es `root`, agregar `--allow-run-as-root` después de `mpirun`.
No se necesitan varias computadoras: los procesos corren en el mismo equipo.

La búsqueda acepta un límite entre 1 y 4294967296, exclusivo por arriba:
con límite 17 se prueban las candidatas 0 a 16. El mensaje admite de 1 a 4096
bytes UTF-8, sin byte nulo. La preparación puede usar candidatas de 0 a
18446744073709551614; solo se recuperan si están dentro del rango buscado.
Las claves numeradas son un conjunto reducido para estudiar fuerza bruta.
El archivo `.aes` no incluye la clave ni el mensaje original.

Código de salida: `0` éxito, `1` error de entrada/API y `2` rango agotado.

## Repetir la evaluación

```bash
python3 evaluar.py
```

El script recompila, comprueba el vector GCM, compara las versiones en casos
límite, hace un calentamiento y mide cinco repeticiones por configuración.
Escribe los resultados nuevos en `resultados/` y los registros en `evidencias/`.
El PDF documenta las mediciones de la sesión original, no se actualiza al
ejecutar el script. No reemplazar los CSV originales sin guardar otra copia.

## Evidencia de pantalla

Las seis imágenes en `evidencias/` muestran la compilación, la ejecución original,
la secuencial mejorada y las ejecuciones MPI con 2, 3 y 4 procesos. Se incluyen
en el PDF en páginas horizontales para facilitar su lectura.

Esta sesión adicional tiene sus propios tiempos y speedups en
`resultados/tiempos_capturas.csv`. La tabla principal del informe utiliza
las medianas de cinco repeticiones de la evaluación automatizada. Los dos
conjuntos de resultados están identificados por separado.
