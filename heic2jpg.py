import os
import glob
import argparse
from PIL import Image
import pillow_heif
from tqdm import tqdm
import concurrent.futures
import multiprocessing

# Registrar el decodificador HEIF con Pillow
pillow_heif.register_heif_opener()

def convert_heic_to_jpg(heic_file, output_dir=None, quality=95):
    """
    Convierte un archivo HEIC a JPG con la calidad especificada.
    
    Args:
        heic_file (str): Ruta al archivo HEIC
        output_dir (str): Directorio de salida para el archivo JPG (si es None, se usa el mismo directorio)
        quality (int): Calidad de compresión JPG (1-100)
        
    Returns:
        str: Ruta del archivo JPG generado
    """
    try:
        # Obtener el nombre base sin extensión y el directorio
        file_dir, file_name = os.path.split(heic_file)
        base_name = os.path.splitext(file_name)[0]
        
        # Determinar el directorio de salida
        if output_dir is None:
            output_dir = file_dir
        
        # Crear el directorio de salida si no existe
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Ruta completa del archivo JPG
        jpg_file = os.path.join(output_dir, f"{base_name}.jpg")
        
        # Abrir y convertir la imagen
        img = Image.open(heic_file)
        
        # Preservar metadatos EXIF si están disponibles
        exif_data = img.info.get('exif', None)
        
        # Guardar como JPG con la calidad especificada
        if exif_data:
            img.save(jpg_file, format="JPEG", quality=quality, exif=exif_data, optimize=True)
        else:
            img.save(jpg_file, format="JPEG", quality=quality, optimize=True)
        
        return jpg_file
    except Exception as e:
        print(f"Error al convertir {heic_file}: {str(e)}")
        return None

def process_directory(input_dir, output_dir=None, quality=95, max_workers=None):
    """
    Procesa todos los archivos HEIC en un directorio y los convierte a JPG.
    
    Args:
        input_dir (str): Directorio con archivos HEIC
        output_dir (str): Directorio de salida para los archivos JPG (si es None, se usa input_dir)
        quality (int): Calidad de compresión JPG (1-100)
        max_workers (int): Número máximo de trabajadores en paralelo
    """
    # Si max_workers no se especifica, usar el número de núcleos disponibles
    if max_workers is None:
        max_workers = multiprocessing.cpu_count()
    
    # Si output_dir no se especifica, usar el mismo directorio de entrada
    if output_dir is None:
        output_dir = input_dir
    
    # Crear el directorio de salida si no existe
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            print(f"Creado directorio de salida: {output_dir}")
        except Exception as e:
            print(f"Error al crear directorio de salida: {str(e)}")
            return
    
    # Encontrar todos los archivos HEIC (con mayúsculas y minúsculas)
    heic_files = []
    heic_files.extend(glob.glob(os.path.join(input_dir, "*.heic")))
    heic_files.extend(glob.glob(os.path.join(input_dir, "*.HEIC")))
    
    if not heic_files:
        print(f"No se encontraron archivos HEIC en {input_dir}")
        return
    
    print(f"Encontrados {len(heic_files)} archivos HEIC en {input_dir}")
    print(f"Las imágenes convertidas se guardarán en: {output_dir}")
    
    # Convertir archivos en paralelo para mayor eficiencia
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Preparar las tareas con los archivos, directorio de salida y el nivel de calidad
        tasks = {executor.submit(convert_heic_to_jpg, heic_file, output_dir, quality): heic_file for heic_file in heic_files}
        
        # Procesar los resultados con una barra de progreso
        converted_files = 0
        failed_files = 0
        
        with tqdm(total=len(heic_files), desc="Convirtiendo imágenes") as progress_bar:
            for future in concurrent.futures.as_completed(tasks):
                heic_file = tasks[future]
                try:
                    jpg_file = future.result()
                    if jpg_file:
                        converted_files += 1
                    else:
                        failed_files += 1
                except Exception as e:
                    print(f"Error procesando {heic_file}: {str(e)}")
                    failed_files += 1
                
                progress_bar.update(1)
    
    print(f"\nConversión completada: {converted_files} archivos convertidos, {failed_files} fallidos.")

def main():
    parser = argparse.ArgumentParser(description="Conversor de HEIC a JPG con alta calidad")
    parser.add_argument("--input", "-i", type=str, help="Directorio con archivos HEIC")
    parser.add_argument("--output", "-o", type=str, help="Directorio de salida para archivos JPG (por defecto: igual al de entrada)")
    parser.add_argument("--quality", "-q", type=int, default=95, 
                        help="Calidad de compresión JPG (1-100, por defecto: 95)")
    parser.add_argument("--workers", "-w", type=int, default=None,
                        help="Número de trabajadores en paralelo (por defecto: número de núcleos CPU)")
    
    args = parser.parse_args()
    
    if args.input is None:
        # Solicitar el directorio de entrada al usuario si no se proporcionó como argumento
        args.input = input("Introduce el directorio donde se encuentran los archivos HEIC: ")
    
    # Verificar si el directorio de entrada existe
    if not os.path.isdir(args.input):
        print(f"Error: El directorio de entrada '{args.input}' no existe.")
        return
    
    if args.output is None:
        # Preguntar por el directorio de salida, si el usuario deja vacío se usa el mismo que el de entrada
        output_input = input("Introduce el directorio donde guardar los archivos JPG (deja vacío para usar el mismo que el de entrada): ")
        if output_input.strip():  # Si el usuario introdujo algo
            args.output = output_input
        else:
            args.output = args.input
    
    # Verificar el valor de calidad
    if args.quality < 1 or args.quality > 100:
        print("Error: La calidad debe estar entre 1 y 100.")
        return
    
    process_directory(args.input, args.output, args.quality, args.workers)

if __name__ == "__main__":
    main()