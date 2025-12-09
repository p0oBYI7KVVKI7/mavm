el formato mavm es un contenedor de video basado en mkv y json capaz de contener los archivos de menus y varios videos con sus pistas de audio y subtitulos

el archivo por defecto de ejecucion es el start.json ubicado dentro del un mkv renombrado con la extencion .mavm (matroska video menu)


los comandos de los menus son (cada que escribas un comando debes poner todos los parametros a no se que se espesifique que el parametro el opcional):

"start": [
-comandos-
]
donde se ejecutan los comandos al iniciar el video

despues esta

"loop":[
-comandos-
]
donde los comandos se ejecutan en bucle permanente hasta cerrar el video o cambiar el menu

{"menu": ["create", "-nombre_del_menu-"]}
este comando crea el contenedor del menu

{"-nombre_del_menu-": [-comando-]}
esto indica que el comando se va a ejecutar que va dentro de los de los []

{"resolution": [-resolucion_eje_X-,-resolucion_eje_Y-]}
con este comando define el tamaño de las coordenadas, estas no son pixeles, solo son coordenadas que indican cuanta definicion en las coordendas hay, esto para evitar los decimales

{"image": [-create/edit-,-id_de_la_imagen_a_crear_o_editar-, "coordinates",-cordenada_eje_x_inicio-,-cordenada_eje_y_inicio-,-cordenada_eje_x_fin-,-cordenada_eje_y_fin-, "-ubicacion_de_la_imagen_dentro_del_contenedor-"]}
este comando es para poner imagenes

{"button": [-create/edit-,-id_del_boton_a_crear_o_editar-, "coordinates",-cordenada_eje_x_inicio-,-cordenada_eje_y_inicio-,-cordenada_eje_x_fin-,-cordenada_eje_y_fin-, "title",-titulo_del_boton_-, "color",[-color_rgb_rojo-,-color_rgb_verde-,-color_rgb_azul-], "command_click",-comando_a_ejecutar_al_hacer_click-], "command4selection",-comando_que_ejecutar_al_seleccionar-, "command4no_selection",-comando_que_ejecutar_al_dejar_de_seleccionar-}
este comando es para crear botones que permiten ejecutar otro comando (o comandos si estan entre --> []) al hacerler click, al seleccionar y al dejar de seleccionar. Los parametros de  ""command_click",-comando_a_ejecutar_al_hacer_click-]", ""command4selection",-comando_que_ejecutar_al_seleccionar-" y ""command4no_selection",-comando_que_ejecutar_al_dejar_de_seleccionar-" son opcionales

{"teleport":[-ubicacion_del_archivo_a_teletransportar]}
el comando teleport cumple la funcion de teletrasnportarte a otro menu o a un video, si quieres que te teletransporte a mas de un video por dentro de los corchetes los lugares a los que quieres que te teletransporte en orden siendo el primer objeto puesto es el primer objeto al que te teletransporta y el ultimo objeto es el ultimo al que teletransporta

{"video":[-create/edit-,-id_del_video_a_crear_o_editar-, "coordinates",-cordenada_eje_x_inicio-,-cordenada_eje_y_inicio-,-cordenada_eje_x_fin-,-cordenada_eje_y_fin-, -ubicacion_del_video_dentro_del_contenedor-]}
este comando permite poner videos dentro de un menu que se iniciaran automaticamente al entrar al menu, no se esperara a que termine el video para ejecutar el siguiente comando, se hara a la vez

{"video":["edit",-id_del_video-, "restart"]}
este comando permite volver a iniciar el video, este comando no se puede volver a ejecutar con el mismo video hasta que el video haya terminado, porqué solo se puede resetear un video que ya haya terminado, no importa hace cuanto termino

{"time": ["wait",-tiempo_a_esperar-,-seconds/minutes/hours-]}
este comando es el unico (al escibir esto) que se ejcuta fuera de un comando tipo "{"-nombre_del_menu-": [-comando-]}" sirve para esperar "x" tiempo hasta el siguiente comando

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

en el archivo de ejemplo las imagenes, videos y menus estan organizados dentro de una misma carpeta, puedes hacerlo distinto pero se te puede complicar el comando teleport


archivo "
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



uso de creador_mavm.7z:

primero extrae el contenido
instala python (recomiendo python3.10 porque ese use para las pruebas)
segundo instalas las depedencias del archivo "requirements_creador_mavm.txt"
tercero crea los menus y archivo de metadata
cuarto crea el archivo que indique las ubicaciones de los archivos diferenciando los archivos por un salto de linea
quinto usar el script de python para conbinar todo, importante tener un video mkv, no importa mucho su contenido ya que este no se va a usar al reproducir

uso del script:
python3.10 creador_mavm.py --file_e -archivo_base- --files_r -archivo_txt_con_la_lista_de_archivos- --file_out -archiv_de_salida_.mavm-


nombracion de versiones:

v.-version_de_cambios_grandes-.-version_de_cambios_pequeños/medianos-.-correccion_de_errores--correciones_del_README.md_o_el_video_de_ejemplo_no_se_incluye_en_"mavm_version"_de_"metadata.json"-
