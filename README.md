# Instructivo para usar el software de Python  
Dentro del repositorio hay un archivo de texto llamado requirements.txt.  
Un vez descargado el repositorio en local, ejecutar la siguiente línea de comandos dentro de la carpeta raiz del proyecto:  
* pip install -r requirements.txt  *  
En windows utilizar preferentemente la consola de *Git Bash* o en su defecto el *PowerShell*.  
Esto hará que se instalen los paquetes necesarios en las mismas versiones que se estuvo trabajando para el desarrollo.  

# Instructivo para usar el software  
Abrir el archivo main.py con algún IDE de Python. Se puede ejecutar directamente o debuggear, de cualquier forma debería funcionar.  
Un vez que se muestre la interfaz de usuario, en el panel izquierdo aparecerán las opciones para configurar la señal de excitación 
y el set-up para la muestra. Aparecen parámetros por defecto, pero se puede modificar sin problema. En caso de que comentan algún 
algún error en escribir algún parámetro, no hay problema, coloqué chequeos de parámetros, así que no debería haber problema.  

# Funcionamiento y descripción del sistema  
El sistema consta de básicamente de 2 componentes: la interfaz de usuario (la última parte del script) y la comunicación serie. 
El primer componente es el encargado de mostrar en pantalla los parámetros, los botones y el panel para graficar. El segundo se 
encarga de establecer la comunicación con el puerto serie adecuado y de enviar y recibir datos hacia y desde la placa.  
Es necesario hacer el emparejamiento de la placa (módulo HC-05) con la PC a mano, antes de comenzar un estudio.  

## Módulos  
- **main.py:** Módulo donde está el bucle principal de la interfaz gráfica y el control del puerto serie.  
- **funciones.py:** Módulo que implementa funciones para futuras implementaciones (recorte estas funcionalidades para ahorar tiempo).  
- **Paramenters.py:** Módulo para poner valores por defecto en el panel izquierdo y que almacena dichos parámetros.  
- **Study.py:** Función para chequeo de parámetros y almacenamiento de los datos recibidos.  
- **SerialCommands.py:** Funciones para enviar y recibir información por el puerto serie.  

Si revisan los archivos encontrarán funciones que no están implementadas. No he tenido tiempo de acomodarlos. No obstante, el sistema 
se encuentra funcionando de manera satisfactoria.  