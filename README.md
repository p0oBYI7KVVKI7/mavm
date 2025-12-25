<h1>MaVM</h1>

## English:

## The MAVM format is a video container based on MKV and JSON, capable of holding menu files and multiple videos with their audio tracks and subtitles.

Player for the format: [SoPepo32/MaVMPlayer](https://github.com/SoPepo32/reproductormavm)

The default execution file is start.json, located within the file with the .mavm extension (Matroska Video Menu).

## .mavm file format:
```MaVM
-++<filename_including_extension>+--<file_contained_in_binary_format>
```
and repeats for each file

## The menu commands are (Every time you write a command, you must include all parameters unless it is specified that the parameter is optional):

"start": [
-commands-
]
where the commands are executed when the video starts.

Then there is:

"loop": [
-commands-
]
where the commands are executed in a continuous loop until the video closes or the menu changes.

{"menu": ["create", -menu_name-]}
This command creates the menu container.

{-menu_name-: [-command-]}
This indicates that the command inside the square brackets [] will be executed.

{"resolution": [-x_axis_resolution-,-y_axis_resolution-]}
This command defines the size of the coordinates. These are not pixels; they are coordinates that indicate the level of detail in the coordinates, avoiding decimals.

{"image": [-create/edit-,-id_of_the_image_to_create_or_edit-, "coordinates",-start_x_axis_coordinates-,-start_y_axis_coordinates-,-end_x_axis_coordinates-, -image_location_within_the_container-]}
This command is for setting Images

{"button": [-create/edit-,-id_of_the_button_to_create_or_edit-, "coordinates",-start_x_axis_coordinate-,-start_y_axis_coordinate-,-end_x_axis_coordinate-,-end_y_axis_coordinate-, "title",-button_title-, "color",[-red_rgb_color-,-green_rgb_color-,-blue_rgb_color-], "command_click",[-command_to_execute_on_click-], "command4selection",-command_to_execute_on_selection-, "command4no_selection",-command_to_execute_on_de-selection-]}
This command is for creating buttons that allow you to execute another command (or commands if they are between --> []) when clicked. When selected and when deselected. The parameters ""command_click",-command_to_execute_on_click-", ""command4selection",-command_to_execute_on_selection- and ""command4no_selection",-command_to_execute_on_deselection- are optional.

{"teleport":[-location_of_file_to_teleport]}
The teleport command teleports you to another menu or a video. If you want to teleport to more than one video, place the locations you want to teleport to inside the brackets, in order. The first item listed is the first item you teleport to, and the last item is the final item you teleport to. If you use it to teleport to a video, you can (optionally) specify the part of the video to which you teleport using ["-hour:minutes:seconds-","-hour:minutes:seconds-"], where the first value is the starting point and the second value is the ending point. For example... Usage: {"teleport":["video.mkv", ["00:00:05.5000","00:00:30.0000"]]} Here, only seconds 5.5 to 30 are played, and yes, you have to include the full number of zeros and decimal places even if you're not using minutes and hours. If the hours are more than 99 (unlikely), just use "-100:minutes:seconds-" (replacing 100 with the hours). I hope this clarifies that hours can have as many digits as you need, but they cannot be less than 2. If it's one hour, use 01; if it's 10, use 10; and if it's 100, use 100.

{"video":[-create/edit-,-id_of_video_to_create_or_edit-, "coordinates", -start_x_coordinate-, -start_y_coordinate-, -end_x_coordinate-, -end_y_coordinate-, "video_path",-video_location_within_container-]}
This command allows you to place videos within a menu that will start automatically when the menu is accessed. It won't wait for the video to finish before executing the next command; it will execute both simultaneously.

{"video":[-create/edit-,-id_of_video_to_create_or_edit-, "coordinates",-start_x_axis_coordinate-,-start_y_axis_coordinate-,-end_x_axis_coordinate-,-end_y_axis_coordinate-, "video_path",-location_of_video_within_the_container-]}
This command allows you to place videos within a menu that will start automatically when you enter the menu. It won't wait for the video to finish before executing the next command; it will run simultaneously.

{"time": ["wait", -wait_time-, -seconds/minutes/hours-]}
This command is the only one (when written) that executes outside of a command like "{-menu_name-: [-command-]}" is used to wait "x" amount of time until the next command.

{"button_default":[-button_id-]}
This command allows you to set a button as the default button selected when entering the menu.

{"sound":["create",-sound_id-, -sound_to_play-, "volume",-sound_volume_from_1_to_100-]}
This command allows you to play sounds when, for example, a button is pressed, and you can choose the volume.

{"sound":["edit",-sound_id-, "volume",-sound_volume_from_1_to_100-]}
This command allows you to edit the volume of a sound.

{"text":["create",-text_id- "coordinates", -start_x_axis_coordinates-, -start_y_axis_coordinates-, -end_x_axis_coordinates-, -end_y_axis_coordinates-, "text", -text-]}
This command is used to create text.

{"text":["edit", -id_of_text_to_edit- "coordinates", -start_x_axis_coordinates-, -start_y_axis_coordinates-, -end_x_axis_coordinates-, -end_y_axis_coordinates-, "text", -text-]}
This command is used to edit text.

Images, buttons, and videos will be placed one on top of the other depending on which one is written first (editing is not taken into account for this). If the "x" command is written before the "z" command (as long as they are images, videos, or buttons; otherwise, for example, if it is a teleport, the screen is cleared and the (displays the video/menu to which the teleport sends) The "z" command will be above the "x" command in the display.

## In the example file, the images, videos, and menus are organized within the same folder. You can do it differently, but it might complicate the teleport command.

File "metadata.json"
Example content:
{
"mavm_version": "v.2.0.0",
"description": {
"text": "example description",
"duration": 3

}
}

"mavm_version" is the MAVM version the file uses.
"description" is the file description, the data that will be displayed when the file is opened, along with the duration in seconds it will be displayed.

## Using mavm_packager:
First, install Python (I recommend Python 3.10 because that's what I used for testing).
Second, install the dependencies listed in the "requirements.txt" file.
Third, create the menus and metadata file.
Fourth, create the file that specifies the file locations, separating them with a line break.
Fifth, use the Python script to combine everything.

Script usage:
python3.10 mavm_packager.py --file_e -base_file- --files_r -txt_file_with_the_file_list- --file_out -output_file_.mavm-

python3.10 mavm_packager.py -h
For more information

Version naming:

v - version of large changes - version of small/medium changes - bug_corrections - corrections of the README.md. The example video (video_de_ejemplo.mavm) or the MAVM creator is not included in the "mavm_version" of the "metadata.json" file.

## License
All content in this repository is under GPL-3.0.

## Español:

## el formato mavm es un contenedor de video basado en mkv y json capaz de contener los archivos de menus y varios videos con sus pistas de audio y subtitulos

reproductor para el formato: [RreproductorMaVM](https://github.com/SoPepo32/reproductormavm)

El archivo de ejecución predeterminado es start.json, ubicado dentro del archivo con la extensión .mavm (Matroska Video Menu).

### Formato de archivo .mavm:
```MaVM
-++<nombre_de_archivo_incluida_la_extensión>+--<archivo_contenido_en_formato_binario>
```
y se repite para cada archivo

## los comandos de los menus son (cada que escribas un comando debes poner todos los parametros a no ser que se especifique que el parametro es opcional):

"start": [
-comandos-
]
donde se ejecutan los comandos al iniciar el video

despues esta

"loop":[
-comandos-
]
donde los comandos se ejecutan en bucle permanente hasta cerrar el video o cambiar el menu

{"menu": ["create", -nombre_del_menu-]}
este comando crea el contenedor del menu

{-nombre_del_menu-: [-comando-]}
esto indica que el comando se va a ejecutar que va dentro de los de los []

{"resolution": [-resolucion_eje_X-,-resolucion_eje_Y-]}
con este comando define el tamaño de las coordenadas, estas no son pixeles, solo son coordenadas que indican cuanta definicion en las coordendas hay, esto para evitar los decimales

{"image": [-create/edit-,-id_de_la_imagen_a_crear_o_editar-, "coordinates",-cordenada_eje_x_inicio-,-cordenada_eje_y_inicio-,-cordenada_eje_x_fin-,-cordenada_eje_y_fin-, -ubicacion_de_la_imagen_dentro_del_contenedor-]}
este comando es para poner imagenes

{"button": [-create/edit-,-id_of_the_button_to_create_or_edit-, "coordinates",-inicio_x_coordenada-,-inicio_y_coordenadas-,-final_x_coordenadas-,-final_y_coordenadas-, -title/image-,-title_del_boton/ubicacion_de_la_imagen_en_el_contenedor-, "color",[-red_rgb_color-,-green_rgb_color-,-blue_rgb_color-], "command_click",-command_to_execute_on_click-], "command4selection",-command_to_execute_on_selection-, "command4no_selection",-command_to_execute_on_deletion-}
Este comando permite crear botones que permiten ejecutar otro comando (o comandos si están entre --> []) al hacer clic, al seleccionar y al deseleccionar. Los parámetros "command_click", "command_to_execute_on_click", "command4selection", "command_to_execute_on_selection" y "command4no_selection", "command_to_execute_on_deselection" son opcionales.

{"teleport":[-ubicacion_del_archivo_a_teletransportar-]}
el comando teleport cumple la funcion de teletrasnportarte a otro menu o a un video, si quieres que te teletransporte a mas de un video por dentro de los corchetes los lugares a los que quieres que te teletransporte en orden siendo el primer objeto puesto es el primer objeto al que te teletransporta y el ultimo objeto es el ultimo al que teletransporta. si lo usas para teletransportarte a un video puede (opcional) establecer a que parte del video con ["-hora:minutos:segundos-","-hora:minutos:segundos-"] siendo el primer valor de donde empiezas y donde terminas el segundo valor ejemplo. de uso: {"teleport":["video.mkv", ["00:00:05.5000","00:00:30.0000"]]} aca solo se reproduce del segundo 5.5 al 30 y si, se tienen que poner los ceros y decimales completos aun que no se usen los minutos y horas, si las horas son mas de 99 (cosa poco probable) solo pones "-100:minutos:segundos-" (remplazas 100 por las horas) espero que con esta aclacion haya quedado claro que las horas pueden tener cuantos digitos necesites pero no puen ser menos de 2 si es una hora se pone 01 si son 10 se pone 10 y si son 100 se pone 100

{"video":[-create/edit-,-id_del_video_a_crear_o_editar-, "coordinates",-cordenada_eje_x_inicio-,-cordenada_eje_y_inicio-,-cordenada_eje_x_fin-,-cordenada_eje_y_fin-, "video_path",-ubicacion_del_video_dentro_del_contenedor-]}
este comando permite poner videos dentro de un menu que se iniciaran automaticamente al entrar al menu, no se esperara a que termine el video para ejecutar el siguiente comando, se hara a la vez

{"video":["edit",-id_del_video-, "restart"]}
este comando permite volver a iniciar el video, este comando no se puede volver a ejecutar con el mismo video hasta que el video haya terminado, porqué solo se puede resetear un video que ya haya terminado, no importa hace cuanto termino

{"time": ["wait",-tiempo_a_esperar-,-seconds/minutes/hours-]}
este comando es el unico (al escibir esto) que se ejcuta fuera de un comando tipo "{-nombre_del_menu-: [-comando-]}" sirve para esperar "x" tiempo hasta el siguiente comando

{"button_default":[-id_del_boton-]}
este comando permite establecer un boton como el por defecto seleccionado al entrar al menu

{"sound":["create",-id_del_sonido-, -sonido_a_reproducir-, "volume",-volumen_del_sonido_del_1_al_100-]}
este comando permite ejecutar sonidos al, por ejemplo, presionar un boton pudiendo elegir el volumen

{"sound":["edit",-id_del_sonido-, "volume",-volumen_del_sonido_del_1_al_100-]}
este comando permite editar el volumen de un sonido

{"text":["create",-id_del_texto_a_crear- "coordinates",-cordenada_eje_x_inicio-,-cordenada_eje_y_inicio-,-cordenada_eje_x_fin-,-cordenada_eje_y_fin-, "text",-texto-]}
este comando sirve para crear un texto

{"text":["edit",-id_del_texto_a_editar- "coordinates",-cordenada_eje_x_inicio-,-cordenada_eje_y_inicio-,-cordenada_eje_x_fin-,-cordenada_eje_y_fin-, "text",-texto-]}
este comando sirve para editar un texto

las imagenes, botones y videos se pondran uno encima del otro dependiendo de cual este escrita su creacion primero (no se toma en cuenta la edicion para eso) si "x" comando se escribe antes que "z" comando (siempre y cuando sean imagenes, videos o botones, en caso contrario, por ejemplo sea un teleport se limpia la pantalla y se muestra el video/menu al que mando el teleport) "z" comando estara arriba de "x" comando en la visualizacion

## en el archivo de ejemplo las imagenes, videos y menus estan organizados dentro de una misma carpeta, puedes hacerlo distinto pero se te puede complicar el comando teleport


archivo "metadata.json"
contenido ejemplo:
{
    "mavm_version": "v.2.0.0",
    "descripcion": {
        "text": "example description",
        "duration":3
    }
}

"mavm_version" es la version de mavm con la que trabaja el archivo
"descripcion" es la descripcion del archivo, datos que se mostraran al abrir el archivo junto al tiempo por el que se mostrara en segundos



## Usando mavm_packager:

Primero, instala Python (recomiendo Python 3.10 porque es el que usé para las pruebas).
Segundo, instala las dependencias listadas en el archivo "requirements.txt".
Tercero, crea el archivo de menús y metadatos.
Cuarto, crea el archivo que especifica las ubicaciones de los archivos, separándolos con un salto de línea.
Quinto, usa el script de Python para combinar todo.

uso del script:
python3.10 mavm_packager.py --files_r -archivo_txt_con_la_lista_de_archivos- --file_out -archiv_de_salida_.mavm-

python3.10 mavm_packager.py -h
Para más información

nombracion de versiones:

v.-version_de_cambios_grandes-.-version_de_cambios_pequeños/medianos-.-correccion_de_errores--correciones_del_README.md_el_video_de_ejemplo(video_de_ejemplo.mavm)_o_creador_mavm_no_se_incluye_en_"mavm_version"_de_"metadata.json-

## Licencia
Todo el contenido de este repositorio está bajo GPL-3.0.
