# Conversor de HEIC a JPG

## Objetivo del Código
El propósito de este código es convertir archivos de imagen en formato HEIC (High Efficiency Image Coding) a formato JPG (JPEG), lo cual puede ser útil cuando se desea utilizar las imágenes en sistemas o aplicaciones que no soportan el formato HEIC. El código permite realizar la conversión de una manera eficiente, aprovechando múltiples núcleos de CPU para procesar las imágenes en paralelo, y asegurando que la calidad de la imagen resultante sea configurable.

Este código puede ser utilizado como una herramienta de línea de comandos para convertir archivos HEIC a JPG en un directorio especificado, con la opción de elegir el directorio de salida, la calidad de la imagen JPG resultante y el número de trabajadores en paralelo.

## Instrucciones de Uso

### Requisitos previos:
1. **Python 3.x**: Este código debe ejecutarse en un entorno Python 3.
2. **Dependencias**:
   - `Pillow`: Librería para abrir y manipular imágenes.
   - `pillow-heif`: Plugin que permite abrir y manipular archivos HEIC.
   - `tqdm`: Para mostrar una barra de progreso durante la conversión.
   - `concurrent.futures`: Para manejar tareas en paralelo.
   - `argparse`: Para analizar argumentos de línea de comandos.
   - `glob`: Para buscar archivos HEIC en el sistema de archivos.

   Puedes instalar las dependencias necesarias con el siguiente comando:
   ```bash
   pip install Pillow pillow-heif tqdm
   ```

### Ejecución:
Para ejecutar el programa, usa la siguiente sintaxis desde la línea de comandos:
```bash
python script.py --input <directorio_entrada> --output <directorio_salida> --quality <calidad> --workers <numero_trabajadores>
```

#### Parámetros:
- `--input` o `-i`: Directorio de entrada donde se encuentran los archivos HEIC. Si no se proporciona, el código solicitará el directorio al usuario.
- `--output` o `-o`: Directorio de salida donde se guardarán los archivos JPG. Si no se proporciona, se utilizará el mismo directorio que el de entrada.
- `--quality` o `-q`: Calidad de la compresión JPG (1-100). El valor predeterminado es 95.
- `--workers` o `-w`: Número de trabajadores en paralelo. Si no se proporciona, se utilizará el número de núcleos de CPU disponibles en el sistema.

### Ejemplo de uso:
```bash
python convert_heic_to_jpg.py --input ./imagenes_heic --output ./imagenes_jpg --quality 90 --workers 4
```

Este comando convertirá todos los archivos HEIC en el directorio `./imagenes_heic` a JPG de calidad 90 y los guardará en el directorio `./imagenes_jpg`, utilizando 4 trabajadores en paralelo.

## Explicación del Funcionamiento

El programa consta de varias funciones principales que trabajan juntas para lograr la conversión de archivos HEIC a JPG:

1. **`convert_heic_to_jpg(heic_file, output_dir, quality)`**:
   - Esta función se encarga de abrir el archivo HEIC y convertirlo a formato JPG con la calidad especificada.
   - Si el archivo HEIC contiene metadatos EXIF, estos son preservados en el archivo JPG.
   - Devuelve la ruta del archivo JPG generado.

2. **`process_directory(input_dir, output_dir, quality, max_workers)`**:
   - Esta función procesa todos los archivos HEIC dentro de un directorio de entrada especificado.
   - Busca archivos con las extensiones `.heic` o `.HEIC` y los convierte en paralelo usando la función `convert_heic_to_jpg`.
   - Utiliza un `ThreadPoolExecutor` de `concurrent.futures` para ejecutar las conversiones de manera eficiente en paralelo.
   - Muestra una barra de progreso utilizando `tqdm`.

3. **`main()`**:
   - La función principal que gestiona la interacción con el usuario a través de la línea de comandos.
   - Procesa los argumentos de la línea de comandos y valida la entrada.
   - Llama a `process_directory` con los parámetros obtenidos.

## Detalles de los Algoritmos

### Algoritmo Principal:
1. **Buscar Archivos HEIC**:
   - Se utilizan las bibliotecas `glob` para encontrar todos los archivos `.heic` y `.HEIC` en el directorio de entrada.

2. **Conversión de Imagen**:
   - Cada archivo HEIC es procesado en paralelo utilizando la función `convert_heic_to_jpg`, la cual utiliza `Pillow` para abrir el archivo HEIC y guardarlo como JPG con la calidad indicada.

3. **Ejecución Paralela**:
   - Para mejorar el rendimiento, las conversiones se ejecutan en paralelo mediante `ThreadPoolExecutor`, lo que permite que el código utilice múltiples núcleos de CPU.
   
### Pseudocódigo:
```plaintext
Para cada archivo HEIC en el directorio de entrada:
    Si no existe el directorio de salida, crearlo.
    Convertir archivo HEIC a JPG usando Pillow y guardar los metadatos EXIF si están disponibles.
Mostrar barra de progreso mientras las conversiones se realizan.
Al finalizar, imprimir estadísticas sobre el número de archivos convertidos y fallidos.
```

## Explicación Técnica de los Algoritmos

- **Complejidad**:
   - La conversión de una sola imagen tiene una complejidad de O(1), ya que implica la apertura de la imagen y su guardado en otro formato.
   - La búsqueda de archivos HEIC en el directorio tiene una complejidad de O(n), donde n es el número de archivos en el directorio.
   - El uso de paralelismo mejora la eficiencia del proceso de conversión, reduciendo significativamente el tiempo total para directorios con muchos archivos.
   
- **Rendimiento**:
   - El uso de múltiples trabajadores en paralelo (mediante `ThreadPoolExecutor`) asegura que el código pueda procesar grandes cantidades de imágenes más rápido, aprovechando la capacidad de múltiples núcleos de la CPU.

## Estructura del Código

1. **Líneas iniciales**:
   - Se importan las bibliotecas necesarias, como `os`, `glob`, `argparse`, `PIL.Image`, `pillow_heif`, `tqdm`, `concurrent.futures` y `multiprocessing`.

2. **`convert_heic_to_jpg`**:
   - Convierte un archivo HEIC a JPG manteniendo los metadatos EXIF.

3. **`process_directory`**:
   - Procesa un directorio completo de archivos HEIC y los convierte a JPG, utilizando procesamiento en paralelo y barra de progreso.

4. **`main`**:
   - Administra la entrada del usuario a través de la línea de comandos y llama a la función principal de procesamiento.

## Ejemplos de Entrada y Salida

### Ejemplo de Entrada:
El programa puede recibir como entrada una carpeta con archivos HEIC, por ejemplo:

```
./imagenes_heic/foto1.HEIC
./imagenes_heic/foto2.heic
```

### Ejemplo de Salida:
El programa generará archivos JPG en el directorio especificado:

```
./imagenes_jpg/foto1.jpg
./imagenes_jpg/foto2.jpg
```

## Manejo de Errores

- **Archivos no encontrados**: Si no se encuentran archivos HEIC en el directorio de entrada, el programa lo notificará al usuario.
- **Errores al convertir**: Si ocurre un error durante la conversión de cualquier archivo, este será capturado y el programa continuará con los siguientes archivos.
- **Directorios no existentes**: Si el directorio de entrada no existe, el programa informará al usuario y terminará la ejecución.

## Dependencias y Requisitos

1. **Python 3.6+**.
2. **Bibliotecas**:
   - `Pillow` >= 8.0.0
   - `pillow-heif` >= 0.1.0
   - `tqdm` >= 4.50.0

Instala las dependencias con:
```bash
pip install Pillow pillow-heif tqdm
```

## Notas sobre Rendimiento y Optimización

- **Paralelización**: El uso de múltiples hilos para procesar las imágenes en paralelo es una técnica clave para mejorar el rendimiento, especialmente cuando se manejan grandes cantidades de archivos.
- **Optimización de calidad**: La función `img.save(..., optimize=True)` mejora la eficiencia en la compresión de las imágenes JPG.

## Comentarios dentro del Código

Los comentarios están dispersos a lo largo del código, explicando cada paso del proceso, especialmente en las secciones complejas como la conversión de imágenes, manejo de metadatos EXIF, y el uso de `ThreadPoolExecutor` para paralelizar la conversión de imágenes.
