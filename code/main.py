#librerias
from tkinter import filedialog,messagebox
from screeninfo import get_monitors
from PIL import Image,ImageTk
#from pymkv import MKVFile
from ebooklib import epub
import tkinter as tk
import subprocess
import threading
import argparse
import platform
import ebooklib
import pygame
import shutil
import imgkit
import time
import json
#import cv2
import sys
import os

#scripts para otros procesos
import menus
from mavm import MaVM

exit_ = False

def install_w():
    if shutil.which("ffmpeg") is None:
        print("Install FFmpeg")
        exit_ = True
    if shutil.which("mkvmerge") is None:
        print("Install MKVToolNix")
        exit_ = True
    if shutil.which("wkhtmltopdf") is None:
        print("Install wkhtmltopdf")
        exit_ = True

def install_lin(a=None, exit_=False):
    if not(a==None):
        if os.path.exists("/etc/os-release"):
            with open("/etc/os-release") as file:
                data = file.read().lower()
            if "ubuntu" in data or "debian" in data:
                print("run in the terminal:\n","sudo","apt-get","install",a)
            elif "fedora" in data or "red hat" in data:
                print("run in the terminal:\n","sudo","dnf","install",a)
            elif "arch" in data:
                print("run in the terminal:\n","sudo","pacman","-S",a)
            else:
                install_w()
            return True
    else:
        return True

if platform.system() == "Windows":
    install_w()
elif platform.system() == "Darwin":
    install_w()
else:
    if shutil.which("ffmpeg") is None:
        exit_ = install_lin("ffmpeg",exit_)
    if shutil.which("mkvmerge") is None:
        exit_ = install_lin("mkvtoolnix",exit_)
    if shutil.which("wkhtmltopdf") is None:
        exit_ = install_lin("wkhtmltopdf",exit_)

pygame.mixer.init()
try:
    shutil.rmtree(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp')) #borra la carpeta completa
    os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp'))
except:
    os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp'))

try:
    shutil.rmtree(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp_video')) #borra #borra la carpeta completa
    os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp_video'))
except:
    os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp_video'))

class ventana:
    def __init__(self, ventana_tk, file):
        #ventana
        self.ventana_tk = ventana_tk
        self.ventana_tk.title("MaVM player")
        self.ventana_tk.geometry("800x450")
        self.ventana_tk.minsize(800,450)
        self.ventana_tk.config(bg="#404040")

        monitor = get_monitors()[0]

        y = (monitor.height // 2) - 225
        x = (monitor.width // 2) - 400

        self.ventana_tk.geometry(f"800x450+{x}+{y}")

        icon = tk.PhotoImage(file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.png"))
        self.ventana_tk.iconphoto(True, icon)
        #self.ventana_tk.protocol("WM_DELETE_WINDOW", self.exit)


        #variables
        self.file = file
        if getattr(sys, 'frozen', False):
            self.raiz_proyecto = os.path.dirname(sys.executable)
        else:
            self.raiz_proyecto = os.path.dirname(os.path.abspath(__file__))
        #self.raiz_proyecto = os.path.dirname(os.path.abspath(__file__))
        print(self.raiz_proyecto)
        self.carpeta_temporal = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp')
        self.carpeta_temporal_video = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp_video')
        self.resolution_menu = [False, None]
        self.detectar_botones = ""
        self.objetos_menu = []
        self.video_repr = False
        self.used_vid = {}
        self.menu_r = True

        self.pista_audio_name = tk.StringVar(self.ventana_tk)
        self.pista_audio_name.set("none")
        self.pista_video_name = tk.StringVar(self.ventana_tk)
        self.pista_video_name.set("none")
        self.pista_subtitulos_name = tk.StringVar(self.ventana_tk)
        self.pista_subtitulos_name.set("none")
        self.bucle = tk.StringVar(self.ventana_tk)
        self.bucle.set("none")
        self.archivos_accion_name = tk.StringVar(self.ventana_tk)
        self.archivos_accion_name.set("files")
        self.editar_accion_name = tk.StringVar(self.ventana_tk)
        self.editar_accion_name.set("edit")
        self.config_json = {}


        #objetos
        #arriba
        self.archivos_menu = tk.OptionMenu(self.ventana_tk, self.archivos_accion_name, "none")
        archivos_menu = self.archivos_menu["menu"]
        archivos_menu.delete(0, "end")

        for opcion in ['open file','save settings']:
            def _set_val(v=opcion):
                if v != 'files':
                    {'open file':self.archivos_ventana,'save settings':self.save_settings}[v]()
                    #{'open file':self.archivos_ventana}[v]()
                self.archivos_accion_name.set("files")
            archivos_menu.add_command(
                label=opcion,
                command=_set_val
            )
        
        self.archivos_accion_name.set("files")

        self.archivos_menu.config(bg='#404040', fg='#FFFFFF', activeforeground="#404040", activebackground="#FFFFFF")
        self.archivos_menu.place(x=780,y=430,width=20,height=16)

        self.editar_menu = tk.OptionMenu(self.ventana_tk, self.editar_accion_name, "none")
        editar_menu = self.editar_menu["menu"]
        editar_menu.delete(0, "end")

        for opcion in ['settings']:
            def _set_val(v=opcion):
                if v != 'files':
                    #{'settings':self.archivos_ventana,
                     #'open file':self.window_files}[v]()
                    {'settings':self.settings_edit}[v]()
                self.editar_accion_name.set("edit")
            editar_menu.add_command(
                label=opcion,
                command=_set_val
            )

        self.editar_accion_name.set("edit")

        self.editar_menu.config(bg='#404040', fg='#FFFFFF', activeforeground="#404040", activebackground="#FFFFFF")
        self.editar_menu.place(x=780,y=430,width=20,height=16)

        #self.archivos = tk.Button(self.ventana_tk, text="files", bg='#404040', fg='#FFFFFF', activeforeground="#404040", activebackground="#FFFFFF", command=self.archivos_ventana)
        #self.archivos.place(x=0,y=0,width=80,height=16)

        self.pista_audio_text = tk.Label(self.ventana_tk, text="audio>", bg='#404040', fg='#FFFFFF')

        self.pista_audio_menu = tk.OptionMenu(self.ventana_tk, self.pista_audio_name, "none")
        self.pista_audio_menu.config(bg='#404040', fg='#FFFFFF', activeforeground="#404040", activebackground="#FFFFFF")
        self.pista_audio_menu.place(x=780,y=430,width=20,height=16)

        self.pista_video_text = tk.Label(self.ventana_tk, text="video>", bg='#404040', fg='#FFFFFF')

        self.pista_video_menu = tk.OptionMenu(self.ventana_tk, self.pista_video_name, "none")
        self.pista_video_menu.config(bg='#404040', fg='#FFFFFF', activeforeground="#404040", activebackground="#FFFFFF")
        self.pista_video_menu.place(x=760,y=430,width=20,height=16)

        self.pista_subtitulos_text = tk.Label(self.ventana_tk, text="subtitles>", bg='#404040', fg='#FFFFFF')

        self.pista_subtitulos_menu = tk.OptionMenu(self.ventana_tk, self.pista_subtitulos_name, "none")
        self.pista_subtitulos_menu.config(bg='#404040', fg='#FFFFFF', activeforeground="#404040", activebackground="#FFFFFF")
        self.pista_subtitulos_menu.place(x=760,y=430,width=20,height=16)

        #madio
        self.reproductor = tk.Frame(self.ventana_tk, bg='black')
        self.reproductor.place(x=0,y=20)

        #abajo
        self.bucle_boton = tk.Checkbutton(self.ventana_tk, text="loop", bg='#404040', fg='#808080', variable=self.bucle, command=self.ventana_tk_config_actualizar_valores)
        self.bucle_boton.place(x=0,y=430,width=20,height=16)

        self.atras_boton = tk.Button(self.ventana_tk, text="<-10s", bg='#404040', fg='#FFFFFF', command=self.detectar_botones_fun_atras)
        self.atras_boton.place(x=0,y=430,width=20,height=16)

        self.ventana_tk.bind("<Left>", self.detectar_botones_fun_atras)

        self.play_boton = tk.Button(self.ventana_tk, text="play/pause", bg='#404040', fg='#FFFFFF', command=self.detectar_botones_fun_stop_play)
        self.atras_boton.place(x=0,y=430,width=20,height=16)

        self.ventana_tk.bind("<space>", self.detectar_botones_fun_stop_play)

        self.adelante_boton = tk.Button(self.ventana_tk, text="10s->", bg='#404040', fg='#FFFFFF', command=self.detectar_botones_fun_adel)
        self.adelante_boton.place(x=780,y=430,width=20,height=16)

        self.ventana_tk.bind("<Right>", self.detectar_botones_fun_adel)

        #self.volume_text = tk.Label(self.ventana_tk, text="volume>s", bg='#404040', fg='#FFFFFF')

        self.volume = tk.Scale(self.ventana_tk, from_=0, to=100, orient="horizontal", bg='#404040', fg='#FFFFFF', showvalue=1, resolution=.1, tickinterval=0)
        self.volume.set(37)


        #codigo
        self.ventana_tk.after(10, self.actalizar_medidas)

        self.load_settings()

        self.actualizar_color()

        if self.file:
            self.ventana_tk.after(100, self.repdorucir)
    
    def exit(self):
        exit()

    def reset_botones_fun(self):
        self.detectar_botones = ""

    def detectar_botones_fun_atras(self, event=None):
        self.detectar_botones = "atras"

    def detectar_botones_fun_stop_play(self, event=None):
        self.detectar_botones = "stop-play"

    def detectar_botones_fun_adel(self, event=None):
        self.detectar_botones = "adelante"

    def settings_edit(self):
        self.ventana_tk_config = tk.Tk()
        self.ventana_tk_config.title("MaVM player configuration")
        
        x_ventana_tk = self.ventana_tk.winfo_x()
        y_ventana_tk = self.ventana_tk.winfo_y()
        ancho_ventana_tk = self.ventana_tk.winfo_width()
        alto_ventana_tk = self.ventana_tk.winfo_height()

        x = x_ventana_tk + (ancho_ventana_tk // 2) - 200
        y = y_ventana_tk + (alto_ventana_tk // 2) - 100

        self.ventana_tk_config.geometry(f"400x200+{x}+{y}")
        self.ventana_tk_config.minsize(400,200)
        self.ventana_tk_config.config(bg="#404040")

        self.ventana_tk_config_x = self.ventana_tk_config.winfo_width()
        self.ventana_tk_config_y = self.ventana_tk_config.winfo_height()

        self.modo_color_name = tk.Label(self.ventana_tk_config, text="dark mode", bg='#404040', fg='#FFFFFF')
        self.modo_color_name.place(x=0,y=0,width=int(self.ventana_tk_config_x/3),height=int(self.ventana_tk_config_y/9))

        self.modo_color = tk.Scale(self.ventana_tk_config, from_=0, to=1, orient="horizontal", bg='#404040', fg='#FFFFFF', showvalue=1, resolution=1, tickinterval=0)
        self.modo_color.place(x=self.ventana_tk_config_x/3,y=0,width=int(2*self.ventana_tk_config_x/7),height=int(self.ventana_tk_config_y/9))

        self.modo_color_red_name = tk.Label(self.ventana_tk_config, text="red mode", bg='#404040', fg='#FFFFFF')
        self.modo_color_red_name.place(x=0,y=int(self.ventana_tk_config_y/9),width=int(self.ventana_tk_config_x/3),height=int(self.ventana_tk_config_y/9))

        self.modo_color_red = tk.Scale(self.ventana_tk_config, from_=-1, to=1, orient="horizontal", bg='#404040', fg='#FFFFFF', showvalue=1, resolution=.5, tickinterval=0)
        self.modo_color_red.place(x=self.ventana_tk_config_x/3,y=2*int(self.ventana_tk_config_y/9),width=int(2*self.ventana_tk_config_x/7),height=int(self.ventana_tk_config_y/9))

        self.modo_color_green_name = tk.Label(self.ventana_tk_config, text="green mode", bg='#404040', fg='#FFFFFF')
        self.modo_color_green_name.place(x=0,y=3*int(self.ventana_tk_config_y/9),width=int(self.ventana_tk_config_x/3),height=int(self.ventana_tk_config_y/9))

        self.modo_color_green = tk.Scale(self.ventana_tk_config, from_=-1, to=1, orient="horizontal", bg='#404040', fg='#FFFFFF', showvalue=1, resolution=.5, tickinterval=0)
        self.modo_color_green.place(x=self.ventana_tk_config_x/3,y=4*int(self.ventana_tk_config_y/9),width=int(2*self.ventana_tk_config_x/7),height=int(self.ventana_tk_config_y/9))
        
        self.modo_color_blue_name = tk.Label(self.ventana_tk_config, text="blue mode", bg='#404040', fg='#FFFFFF')
        self.modo_color_blue_name.place(x=0,y=5*int(self.ventana_tk_config_y/9),width=int(self.ventana_tk_config_x/3),height=int(self.ventana_tk_config_y/9))

        self.modo_color_blue = tk.Scale(self.ventana_tk_config, from_=-1, to=1, orient="horizontal", bg='#404040', fg='#FFFFFF', showvalue=1, resolution=.5, tickinterval=0)
        self.modo_color_blue.place(x=self.ventana_tk_config_x/3,y=6*int(self.ventana_tk_config_y/9),width=int(2*self.ventana_tk_config_x/7),height=int(self.ventana_tk_config_y/9))

        try:
            self.modo_color.set(self.config_json['modo_color'][0])
            self.modo_color_red.set(self.config_json['modo_color'][1])
            self.modo_color_blue.set(self.config_json['modo_color'][3])
            self.modo_color_green.set(self.config_json['modo_color'][2])
        except:
            self.modo_color.set(1)
            self.modo_color_red.set(0)
            self.modo_color_blue.set(0)
            self.modo_color_green.set(0)
            self.config_json['modo_color'] = [1,0,0,0]

        self.menu_r_config = True
        self.ventana_tk_config.after(10, self.ventana_tk_config_actualizar_valores)

        self.ventana_tk_config.after(10, self.actualizar_color)

        self.ventana_tk_config.mainloop()

    def ventana_tk_config_actualizar_valores(self):
        try:
            if self.config_json['bucle'] != self.modo_color.get():
                self.config_json['bucle'] = self.bucle.get()
            if self.config_json['modo_color'][0] != self.modo_color.get():
                self.config_json['modo_color'][0] = self.modo_color.get()
                self.ventana_tk.after(10, self.actualizar_color)
            if self.config_json['modo_color'][1] != self.modo_color_red.get():
                self.config_json['modo_color'][1] = self.modo_color_red.get()
                self.ventana_tk.after(10, self.actualizar_color)
            if self.config_json['modo_color'][3] != self.modo_color_blue.get():
                self.config_json['modo_color'][3] = self.modo_color_blue.get()
                self.ventana_tk.after(10, self.actualizar_color)
            if self.config_json['modo_color'][2] != self.modo_color_green.get():
                self.config_json['modo_color'][2] = self.modo_color_green.get()
                self.ventana_tk.after(10, self.actualizar_color)
        except:
            self.config_json['bucle'] = self.bucle.get()
            try:
                self.config_json['modo_color'] = self.modo_color.get()
            except:
                pass
            self.ventana_tk.after(10, self.actualizar_color)
        
        try:
            self.ventana_tk_config_x = self.ventana_tk_config.winfo_width()
            self.ventana_tk_config_y = self.ventana_tk_config.winfo_height()

            self.modo_color_name.place(x=0,y=0,width=int(self.ventana_tk_config_x/3),height=int(self.ventana_tk_config_y/4.5))

            self.modo_color.place(x=self.ventana_tk_config_x/3,y=0,width=int(self.ventana_tk_config_x/7),height=int(self.ventana_tk_config_y/4.5))

            self.modo_color_red_name.place(x=0,y=int(self.ventana_tk_config_y/4.5),width=int(self.ventana_tk_config_x/3),height=int(self.ventana_tk_config_y/4.5))

            self.modo_color_red.place(x=self.ventana_tk_config_x/3,y=int(self.ventana_tk_config_y/4.5),width=int(2*self.ventana_tk_config_x/7),height=int(self.ventana_tk_config_y/4.5))

            self.modo_color_green_name.place(x=0,y=2*int(self.ventana_tk_config_y/4.5),width=int(self.ventana_tk_config_x/3),height=int(self.ventana_tk_config_y/4.5))

            self.modo_color_green.place(x=self.ventana_tk_config_x/3,y=2*int(self.ventana_tk_config_y/4.5),width=int(2*self.ventana_tk_config_x/7),height=int(self.ventana_tk_config_y/4.5))
            
            self.modo_color_blue_name.place(x=0,y=3*int(self.ventana_tk_config_y/4.5),width=int(self.ventana_tk_config_x/3),height=int(self.ventana_tk_config_y/4.5))

            self.modo_color_blue.place(x=self.ventana_tk_config_x/3,y=3*int(self.ventana_tk_config_y/4.5),width=int(2*self.ventana_tk_config_x/7),height=int(self.ventana_tk_config_y/4.5))


            if self.ventana_tk_config.winfo_viewable():
                self.ventana_tk_config.after(10, self.ventana_tk_config_actualizar_valores)
        except:
            pass

    def actualizar_color(self):
        #print("self.config_json['modo_color']",self.config_json['modo_color'])
        if self.config_json['modo_color'][0] == 1:
            #format(64, '02x')
            bg1 = f"#{format(int(64+32*self.config_json['modo_color'][1]), '02x')}{format(int(64+32*self.config_json['modo_color'][2]), '02x')}{format(int(64+32*self.config_json['modo_color'][3]), '02x')}"

            #format(32, '02x')
            bg2 = f"#{format(int(32+32*self.config_json['modo_color'][1]), '02x')}{format(int(32+32*self.config_json['modo_color'][2]), '02x')}{format(int(32+32*self.config_json['modo_color'][3]), '02x')}"

            #format(159, '02x')
            
            fg1 = f"#{format(int(159+32*self.config_json['modo_color'][1]), '02x')}{format(int(159+32*self.config_json['modo_color'][2]), '02x')}{format(int(159+32*self.config_json['modo_color'][3]), '02x')}"

            self.ventana_tk.config(bg=bg1)

            for i in self.ventana_tk.winfo_children():
                if not(i is self.reproductor):
                    i.config(bg=bg1, fg=fg1)
                else:
                    i.config(bg=bg2)
            try:
                if self.ventana_tk_config.winfo_viewable():
                    self.ventana_tk_config.config(bg=bg1)
                    for i in self.ventana_tk_config.winfo_children():
                        i.config(bg=bg1, fg=fg1)
            except:
                pass
        else:
            #format(191, '02x')
            bg1 = f"#{format(int(191+32*self.config_json['modo_color'][1]), '02x')}{format(int(191+32*self.config_json['modo_color'][2]), '02x')}{format(int(191+32*self.config_json['modo_color'][3]), '02x')}"

            #format(223, '02x')
            bg2 = f"#{format(int(223+32*self.config_json['modo_color'][1]), '02x')}{format(int(223+32*self.config_json['modo_color'][2]), '02x')}{format(int(223+32*self.config_json['modo_color'][3]), '02x')}"

            #format(64, '02x')
            fg1 = f"#{format(int(64+32*self.config_json['modo_color'][1]), '02x')}{format(int(64+32*self.config_json['modo_color'][2]), '02x')}{format(int(64+32*self.config_json['modo_color'][3]), '02x')}"

            self.ventana_tk.config(bg=bg1)

            for i in self.ventana_tk.winfo_children():
                if not(i is self.reproductor):
                    i.config(bg=bg1, fg=fg1)
                else:
                    i.config(bg=bg2)
            try:
                if self.ventana_tk_config.winfo_viewable():
                    self.ventana_tk_config.config(bg=bg1)
                    for i in self.ventana_tk_config.winfo_children():
                        i.config(bg=bg1, fg=fg1)
            except:
                pass

    def save_settings(self):
        self.config_json['volume'] = self.volume.get()
        config = json.dumps(self.config_json)
        print(config)

        if os.path.exists(os.path.join(os.path.expanduser("~"), "mavmplayer")):
            print('os.path.exists(os.path.join(os.path.expanduser("~"), "mavmplayer"))',os.path.exists(os.path.join(os.path.expanduser("~"), "mavmplayer")))
            config_file = open(os.path.join(os.path.expanduser("~"), "mavmplayer", 'config.json'),'w')
            config_file.write(config)
            config_file.close()
        else:
            print('os.path.exists(os.path.join(os.path.expanduser("~"), "mavmplayer"))',os.path.exists(os.path.join(os.path.expanduser("~"), "mavmplayer")))
                
            os.mkdir(os.path.join(os.path.expanduser("~"), "mavmplayer"))

            config_file = open(os.path.join(os.path.expanduser("~"), "mavmplayer", 'config.json'),'w')
            config_file.write(config)
            config_file.close()

    def load_settings(self):
        try:
            if os.path.exists(os.path.join(os.path.expanduser("~"), "mavmplayer")):
                config_file = open(os.path.join(os.path.expanduser("~"), "mavmplayer", 'config.json'),'r')
                config_txt = config_file.read()
                config_file.close()
            else:
                os.mkdir(os.path.join(os.path.expanduser("~"), "mavmplayer"))

                config_file = open(os.path.join(os.path.expanduser("~"), "mavmplayer", 'config.json'),'r')
                config_txt = config_file.read()
                config_file.close()

            if json.loads(config_txt)['modo_color'] == 1 or json.loads(config_txt)['modo_color'] == 0:
                config_json = json.loads(config_txt)
                self.bucle.set(config_json["bucle"])
                self.volume.set(config_json['volume'])
                self.config_json['modo_color'] = [config_json[modo_color],0,0,0]
                self.config_json['volume']     = self.config_json['volume']
                self.config_json["bucle"]      = config_json["bucle"]
            else:
                self.config_json = json.loads(config_txt)
                self.bucle.set(self.config_json["bucle"])
                self.volume.set(self.config_json['volume'])
                self.config_json['modo_color'] = [self.config_json['modo_color'][0],self.config_json['modo_color'][1],self.config_json['modo_color'][2],self.config_json['modo_color'][3]]
                self.config_json['volume']     = self.config_json['volume']
        except Exception as e:
            print(e)
            self.config_json = {"bucle":"0","modo_color":[1,0,0,0],"volume":37.0}

    def archivos_ventana(self):
        self.file = filedialog.askopenfilename(title='buscar video MaVM', filetypes=(('video MaVM', '*.mavm'),('todos los archivos', '*.*')))
        print(self.file)
        self.repdorucir()

    def start(self):
        for widget in self.reproductor.winfo_children():
            widget.destroy()  #elimina cada widget
        
        metadata_path   = self.contenido_dat['metadata.json']
        start_menu_path = self.contenido_dat['start.json']
        
        metadata_file = open(metadata_path, 'r')
        metadata_text = metadata_file.read()
        metadata_json = json.loads(metadata_text)
        metadata_file.close()

        start_menu_file = open(start_menu_path, 'r')
        start_menu_text = start_menu_file.read()
        start_menu_json = json.loads(start_menu_text)
        start_menu_file.close()

        self.video_mavm_version = metadata_json["mavm_version"]
        if not(self.video_mavm_version in ['v.2.1.0','v.2.2.0','v.3.0.0','v.3.1.0','v.3.2.0','v.3.3.0']):
            messagebox.showerror("File version error", "The file version is not supported. This program only supports versions 2.1.0 to 3.3.0")
            exit()
        print(self.video_mavm_version)

        version_compatible = menus.version_formato(self.video_mavm_version)[0]
        print(version_compatible)

        descripcion = tk.Label(self.reproductor,text=metadata_json["descripcion"]["text"],fg="#ffffff",background="black")
        descripcion.place(x=self.reproductor.winfo_width()//2-4*len(metadata_json["descripcion"]["text"]),y=self.reproductor.winfo_height()//2)
        self.reproductor.update_idletasks()
        print(metadata_json["descripcion"]["text"])

        for i in range(1,metadata_json["descripcion"]["duration"]*100):
            time.sleep(1/100)
        
        self.menu(start_menu_json)

    def menu(self, menu_json):
        try:
            pygame.mixer.pause()
        except:
            try:
                for i in list(self.used_vid.keys()):
                    try:
                        self.used_vid[i][3].pause()
                    except:
                        pass
            except:
                pass
        self.used_vid = {}
        self.loop_comandos_on = False
        self.objetos_menu = []
        y = True
        for widget in self.reproductor.winfo_children():
            try:
                if widget is self.espacio_mv:
                    y = False
                else: 
                    widget.destroy()  #elimina cada widget
            except:
                widget.destroy()  #elimina cada widget
        
        #crear espacio para menu y video

        if y:
            self.espacio_mv = tk.Frame(self.reproductor, bg='white')
            self.espacio_mv.place()
        else:
            for widget_mv in self.espacio_mv.winfo_children():
                widget_mv.destroy()
        
        menu_dat = menus.version_formato(self.video_mavm_version)
        lista_comandos = menu_dat[1](menu_json).lista_comandos
        print("lc",lista_comandos)

        self.resolution_menu = [True, lista_comandos["resolucion"]]
        self.menu_resize()

        #self.objetos_menu = 
        #comando[1]["imagen"]
        print("start:",lista_comandos["start"])
        #for comando in lista_comandos["start"]:
         #   print("lcc", comando)
          #  t = self.comnado_ejecutar(comando, self.espacio_mv)
           # print("sleep",t)
            #for i in range(t*1000):
             #   time.sleep(1/1000)
              #  self.menu_resize(menu_r_b=False)
            #time.sleep(16/1000)
        self.menu_comand(lista_comandos["start"])
        
        print(lista_comandos["loop"])
        if 0 == len(lista_comandos["loop"]):
            pass
        else:
            print("loop:",lista_comandos["loop"])
            self.loop_comandos_on = True
            self.menu_loop(lista_comandos["loop"])

    def menu_comand(self, lista_comandos, time_a=None, i=0):
        if i <= len(lista_comandos)-1:
            print(i)
            #if time_a != None:
            print(time_a)
            if time_a:
                print("time_a",time_a)
                print("time.time()",time.time())
                print("time.time() >= time_a",time.time() >= time_a)
                if time.time() >= time_a:
                    #print("lcc", comando)
                    comando = lista_comandos[i+1]
                    t = self.comnado_ejecutar(comando, self.espacio_mv)
                    if t != 0:
                        time_a = time.time()+t

                        self.ventana_tk.after(10, lambda: self.menu_comand(lista_comandos, time_a, i))
                    else:
                        time_a = None

                        self.ventana_tk.after(10, lambda: self.menu_comand(lista_comandos, time_a, i+1))
                else:
                    self.ventana_tk.after(10, lambda: self.menu_comand(lista_comandos, time_a, i))
            else:
                #print("lcc", comando)
                comando = lista_comandos[i]
                t = self.comnado_ejecutar(comando, self.espacio_mv)
                if t != 0:
                    time_a = time.time()+t

                    self.ventana_tk.after(10, lambda: self.menu_comand(lista_comandos, time_a, i))
                else:
                    time_a = None

                    self.ventana_tk.after(10, lambda: self.menu_comand(lista_comandos, time_a, i+1))

    def menu_loop(self, lista_comandos):
        if self.loop_comandos_on:
            self.menu_comand(lista_comandos)
            #time.sleep(10/1000)
            #threading.Thread(target=lambda: self.menu_loop(lista_comandos)).start()
            self.ventana_tk.after(10, lambda: self.menu_loop(lista_comandos))
        else:
            pass

    def comnado_ejecutar(self, comando, v):
            #t = 16/1000
            t = 0
            #print("contenido comando:", comando)
            if comando[0] == "image":
                print(comando[1]["imagen"])
                imagen_file = Image.open(self.contenido_dat[comando[1]["imagen"]])
                imagen = ImageTk.PhotoImage(imagen_file)
                if "create" in comando[1].keys():
                    self.objetos_menu.append({"id":comando[1]["create"],"objeto":tk.Label(v, image=imagen), "cordenadas":comando[1]["coordinates"], "imagen":imagen_file})
                    self.objetos_menu[len(self.objetos_menu)-1]["objeto"].image = imagen
                    self.objetos_menu[len(self.objetos_menu)-1]["objeto"].place(x=0,y=0)
                    print(self.objetos_menu[len(self.objetos_menu)-1])
                elif "edit" in comando[1].keys():
                    print("Buscando objeto con id:", comando[1]["edit"])
                    for i in range(len(self.objetos_menu)-1):
                        if "id" in self.objetos_menu[i].keys():
                            if self.objetos_menu[i]["id"] == comando[1]["edit"]:
                                print("Objeto encontrado:", self.objetos_menu[i])
                                self.objetos_menu[i]["cordenadas"] = comando[1]["coordinates"]
                                self.objetos_menu[i]["imagen"] = imagen_file
                                self.objetos_menu[i]["objeto"].place(x=0,y=0)
                                print(self.objetos_menu[i])
            elif comando[0] == "ebook":
                print(comando[1]["epub_path"])
            
                book = epub.read_epub(self.contenido_dat[comando[1]["epub_path"]])

                #obtener todos los documentos (capítulos/secciones)
                items = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))

                #seleccionar el índice deseado
                chapter_items = [item for item in items if "section" in item.get_name()]
                html_content = chapter_items[comando[1]['page']].get_content().decode("utf-8")
                #html_content = items[comando[1]['page']].get_content().decode("utf-8")  # por ejemplo, el tercero
                
                #HTML(string=html_content).write_png(f"{comando[1]['epub_path']}_{comando[1]['page']}.png")
                output_file_path = os.path.join(self.carpeta_temporal,f"{comando[1]['epub_path']}_{comando[1]['page']}.png")
                file_html = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"cap_html_temp.html"), 'w')
                file_html.write(html_content)
                file_html.close()

                subprocess.run(['wkhtmltoimage',f'{os.path.join(os.path.dirname(os.path.abspath(__file__)),"cap_html_temp.html")}',f'{output_file_path}'])
                
                img  = Image.open(f"{output_file_path}")
                imgb = img.convert("L")
                pixels = imgb.load()
                ancho, alto = imgb.size

                #buscar el borde derecho
                x_max = 0
                for x in range(ancho-1, -1, -1):  # derecha a izquierda
                    for y in range(alto):
                        if pixels[x, y] < 250:  # píxel no blanco
                            x_max = x
                            break
                    if x_max > 0:
                        break

                #ajustar con margen y evitar pasarse del ancho
                margen = 10
                nuevo_ancho = min(ancho, x_max + margen)
                imagen_file = img.crop((0, 0, nuevo_ancho, alto))

                imagen = ImageTk.PhotoImage(imagen_file)
                if "create" in comando[1].keys():
                    self.objetos_menu.append({"id":comando[1]["create"],"objeto":tk.Label(v, image=imagen), "cordenadas":comando[1]["coordinates"], "imagen":imagen_file})
                    self.objetos_menu[len(self.objetos_menu)-1]["objeto"].image = imagen
                    self.objetos_menu[len(self.objetos_menu)-1]["objeto"].place(x=0,y=0)
                    print(self.objetos_menu[len(self.objetos_menu)-1])
                elif "edit" in comando[1].keys():
                    print("Buscando objeto con id:", comando[1]["edit"])
                    for i in range(len(self.objetos_menu)-1):
                        if "id" in self.objetos_menu[i].keys():
                            if self.objetos_menu[i]["id"] == comando[1]["edit"]:
                                print("Objeto encontrado:", self.objetos_menu[i])
                                self.objetos_menu[i]["cordenadas"] = comando[1]["coordinates"]
                                self.objetos_menu[i]["imagen"] = imagen_file
                                self.objetos_menu[i]["objeto"].place(x=0,y=0)
                                print(self.objetos_menu[i])
            elif comando[0] == "text":
                self.objetos_menu.append({"objeto": tk.Label(v,text=comando[1]["text"],fg="#808080"), "cordenadas":comando[1]["coordinates"]})
            elif comando[0] == "button":
                if "create" in comando[1].keys():
                    if "image" in comando[1].keys():
                        if "command" in comando[1].keys():
                            print(comando[1]["image"])
                            print(self.contenido_dat[comando[1]["image"]])
                            imagen_file = Image.open(self.contenido_dat[comando[1]["image"]])
                            imagen = ImageTk.PhotoImage(imagen_file)

                            print(comando[1]["coordinates"])

                            self.objetos_menu.append({"id":comando[1]["create"],
                            "objeto":tk.Label(self.espacio_mv, image=imagen), "cordenadas":comando[1]["coordinates"],"imagen":imagen_file})

                            self.objetos_menu[len(self.objetos_menu)-1]["objeto"].image = imagen
                            self.objetos_menu[len(self.objetos_menu)-1]["objeto"].bind("<Button-1>", lambda event, cmd=comando[1]["command"]: self.ejecutar_boton(cmd))

                            self.objetos_menu[len(self.objetos_menu)-1]["objeto"].place()
                        else:
                            print(comando[1]["image"])
                            print(self.contenido_dat[comando[1]["image"]])
                            imagen_file = Image.open(self.contenido_dat[comando[1]["image"]])
                            imagen = ImageTk.PhotoImage(imagen_file)

                            self.objetos_menu.append({"id":comando[1]["create"],
                            "objeto":tk.Label(self.espacio_mv, image=imagen), "cordenadas":comando[1]["coordinates"],"imagen":imagen_file})

                            self.objetos_menu[len(self.objetos_menu)-1]["objeto"].place()

                        if "command4selection" in comando[1].keys():
                            self.objetos_menu[len(self.objetos_menu)-1]["objeto"].bind("<Enter>", lambda e: self.ejecutar_boton(comando[1]["command4selection"]))
                            self.objetos_menu[len(self.objetos_menu)-1]["objeto"].place()
                        if "command4no_selection" in comando[1].keys():
                            self.objetos_menu[len(self.objetos_menu)-1]["objeto"].bind("<Leave>", lambda e: self.ejecutar_boton(comando[1]["command4no_selection"]))
                            self.objetos_menu[len(self.objetos_menu)-1]["objeto"].place()
                    else:
                        self.objetos_menu.append({"id":comando[1]["create"],"objeto":tk.Button(v, text=comando[1]["title"],bg=f'#{comando[1]["color"][0]:02x}{comando[1]["color"][1]:02x}{comando[1]["color"][2]:02x}'), "cordenadas":comando[1]["coordinates"]})
                        self.objetos_menu[len(self.objetos_menu)-1]["objeto"].place()

                        if "command" in comando[1].keys():
                            self.objetos_menu[len(self.objetos_menu)-1]["objeto"].config(command=lambda: self.ejecutar_boton(comando[1]["command"]))
                        if "command4selection" in comando[1].keys():
                            self.objetos_menu[len(self.objetos_menu)-1]["objeto"].bind("<Enter>", lambda e: self.ejecutar_boton(comando[1]["command4selection"]))
                        if "command4no_selection" in comando[1].keys():
                            self.objetos_menu[len(self.objetos_menu)-1]["objeto"].bind("<Leave>", lambda e: self.ejecutar_boton(comando[1]["command4no_selection"]))
                elif "edit" in comando[1].keys():
                    for i in range(len(self.objetos_menu)):
                        if "id" in self.objetos_menu[i].keys():
                            if self.objetos_menu[i]["id"] == comando[1]["edit"]:
                                if "image" in comando[1].keys():
                                    if "command" in comando[1].keys():
                                        print(comando[1]["image"])
                                        print(self.contenido_dat[comando[1]["image"]])
                                        imagen_file = Image.open(self.contenido_dat[comando[1]["image"]])
                                        imagen = ImageTk.PhotoImage(imagen_file)

                                        print(comando[1]["coordinates"])

                                        self.objetos_menu[i] = {"id":comando[1]["edit"],"objeto":self.objetos_menu[i]["objeto"], "cordenadas":comando[1]["coordinates"],"imagen":imagen_file}

                                        self.objetos_menu[i]["objeto"].image = imagen
                                        self.objetos_menu[i]["objeto"].bind("<Button-1>", lambda event, cmd=comando[1]["command"]: self.ejecutar_boton(cmd))

                                        self.objetos_menu[i]["objeto"].place()
                                    else:
                                        print(comando[1]["image"])
                                        print(self.contenido_dat[comando[1]["image"]])
                                        imagen_file = Image.open(self.contenido_dat[comando[1]["image"]])
                                        imagen = ImageTk.PhotoImage(imagen_file)

                                        print(comando[1]["coordinates"])

                                        self.objetos_menu[i] = {"id":comando[1]["edit"],"objeto":self.objetos_menu[i]["objeto"], "cordenadas":comando[1]["coordinates"],"imagen":imagen_file}

                                        self.objetos_menu[len(self.objetos_menu)-1]["objeto"].place()
                                        print(comando[1]["image"])
                                        print(self.contenido_dat[comando[1]["image"]])
                                        imagen_file = Image.open(self.contenido_dat[comando[1]["image"]])
                                        imagen = ImageTk.PhotoImage(imagen_file)

                                        self.objetos_menu.append({"id":comando[1]["create"],
                                        "objeto":tk.Label(self.espacio_mv, image=imagen), "cordenadas":comando[1]["coordinates"],"imagen":imagen_file})

                                        self.objetos_menu[i]["objeto"].place()
                                    if "command4selection" in comando[1].keys():
                                        self.objetos_menu[i]["objeto"].bind("<Enter>", lambda e: self.ejecutar_boton(comando[1]["command4selection"]))
                                        self.objetos_menu[i]["objeto"].place()
                                    if "command4no_selection" in comando[1].keys():
                                        self.objetos_menu[i]["objeto"].bind("<Leave>", lambda e: self.ejecutar_boton(comando[1]["command4no_selection"]))
                                        self.objetos_menu[i]["objeto"].place()
                                else:
                                    if "command" in comando[1].keys():
                                        self.objetos_menu[i] = {"id":comando[1]["edit"],"objeto":self.objetos_menu[i]["objeto"], "cordenadas":comando[1]["coordinates"]}

                                        self.objetos_menu[i]["objeto"].bind("<Button-1>", lambda event, cmd=comando[1]["command"]: self.ejecutar_boton(cmd))

                                        self.objetos_menu[i]["objeto"].config(text=comando[1]["title"])
                                    else:
                                        self.objetos_menu[i] = {"id":comando[1]["edit"],"objeto":self.objetos_menu[i]["objeto"], "cordenadas":comando[1]["coordinates"]}

                                        self.objetos_menu[i]["objeto"].config(text=comando[1]["title"])
                                    if "command4selection" in comando[1].keys():
                                        self.objetos_menu[i]["objeto"].bind("<Enter>", lambda e: self.ejecutar_boton(comando[1]["command4selection"]))

                                        self.objetos_menu[i]["objeto"].place()
                                    if "command4no_selection" in comando[1].keys():
                                        self.objetos_menu[i]["objeto"].bind("<Leave>", lambda e: self.ejecutar_boton(comando[1]["command4no_selection"]))

                                        self.objetos_menu[i]["objeto"].place()
            elif comando[0] == "sound":
                if "create" in comando[1].keys():
                    self.objetos_menu.append({"id":comando[1]["create"],"objeto":pygame.mixer.Sound(self.contenido_dat[comando[1]["sound"]])})
                    self.objetos_menu[len(self.objetos_menu)-1]["objeto"].play()
                    self.objetos_menu[len(self.objetos_menu)-1]["objeto"].set_volume(self.volume.get()*comando[1]["volume"]/100)
                    print("sonido play")
                elif "edit" in comando[1].keys():
                    for i in range(len(self.objetos_menu)-1):
                        if "id" in self.objetos_menu[i].keys():
                            if self.objetos_menu[i]["id"] == comando[1]["edit"]:
                                self.objetos_menu[i]["objeto"].set_volume(self.volume.get()/100*comando[1]["volume"]/100)
            elif comando[0] == "time":
                if "wait" in comando[1].keys():
                    tiempo = comando[1]["wait"][0]
                    unidad = comando[1]["wait"][1]
                    if unidad == "seconds":
                        t = tiempo
                    elif unidad == "minutes":
                        t = tiempo*60
                    elif unidad == "hours":
                        t = iempo*3600
            elif comando[0] == "teleport":
                self.teleport(comando[1]["ubicaciones"])
            elif comando[0] == "video":
                print(comando)
                if not("restart" in comando[1].keys()):
                    file, extension = os.path.splitext(comando[1]["video"])

                    try:
                        os.makedirs(os.path.join(self.carpeta_temporal_video,file))
                    except:
                        shutil.rmtree(os.path.join(self.carpeta_temporal_video),file)
                        os.makedirs(os.path.join(self.carpeta_temporal_video,file))
                    
                    subprocess.run(["ffmpeg", "-y", "-i",self.contenido_dat[comando[1]["video"]],"frame_%04d.png"], cwd=f"{self.carpeta_temporal_video}/{file}")
                    subprocess.run(["ffmpeg", "-y", "-i",self.contenido_dat[comando[1]["video"]],"-vn","-c:a","libopus",f"{file}.opus"], cwd=f"{self.carpeta_temporal_video}")
                
                if "create" in comando[1].keys():
                    print("create")
                    self.objetos_menu.append({"id":comando[1]["create"],"objeto":tk.Label(v), "cordenadas":comando[1]["coordinates"], "video":file, "video_path":self.contenido_dat[comando[1]["video"]], "video_r":file})
                    self.objetos_menu[len(self.objetos_menu)-1]["objeto"].place(x=0,y=0)
                    print(self.objetos_menu[len(self.objetos_menu)-1])

                    self.used_vid[file] = [False,0]

                    fps = self.get_fps(self.objetos_menu[len(self.objetos_menu)-1]["video_path"])

                    self.video_r(len(self.objetos_menu)-1, file, fps, self.contenido_dat[comando[1]["video"]])
                elif "restart" in comando[1].keys():
                    for i in range(len(self.objetos_menu)):
                        if "id" in self.objetos_menu[i].keys():
                            if self.objetos_menu[i]["id"] == comando[1]["restart"]:
                                print('self.objetos_menu[i]["id"] == comando[1]["restart"]')
                                if not(self.used_vid[self.objetos_menu[i]["video"]][0]):
                                    print('not(self.used_vid[self.objetos_menu[i]["video"]][0])', not(self.used_vid[self.objetos_menu[i]["video"]][0]))
                                    self.used_vid[self.objetos_menu[i]["video"]] = [True,0]
                                    
                                    fps = self.get_fps(self.objetos_menu[i]["video_path"])

                                    self.video_r(i, self.objetos_menu[i]["video"], fps, self.objetos_menu[i]["video_path"])
                elif "edit" in comando[1].keys():
                    for i in range(len(self.objetos_menu)-1):
                        if "id" in self.objetos_menu[i].keys():
                            if self.objetos_menu[i]["id"] == comando[1]["edit"]:
                                self.objetos_menu[i].append({"id":comando[1]["create"],"objeto":tk.Label(v), "cordenadas":comando[1]["coordinates"], "video":file, "video_path":self.contenido_dat[comando[1]["video"]]})
                                elf.objetos_menu[len(self.objetos_menu)-1]["objeto"].place(x=0,y=0)
                                print(self.objetos_menu[len(self.objetos_menu)-1])
            return t

    def _teleport(self, paths, paths_b=None):
        print("h")
        print(paths)
        if type(paths) == type([]):
            for path_num in range(0,len(paths)-1):
                self.teleport(paths[path_num])
        else:
            self.loop_comandos_on = False
            nombre, extension = os.path.splitext(paths)
            if extension == ".mkv":
                self.menu_r = False
                self.video_repr = True
                self.video(self.contenido_dat[paths], paths_b)
                #while self.video_repr:
                 #   if not(self.video_repr):
                  #      break
            elif extension == ".json":
                print("path_menu",self.contenido_dat[paths])
                menu_f = open(self.contenido_dat[paths])
                menu_t = menu_f.read()
                menu_j = json.loads(menu_t)
                menu_f.close()
                print("menu:",menu_j)
                time.sleep(16/1000)
                self.menu(menu_j)

    def teleport(self, paths, paths_b=None, mkv_t=None):
        print("h")
        print(paths)
        if type(paths) == type([]):
            if 0 == len(paths)-1:
                nombre, extension = os.path.splitext(paths[0])
                if extension == ".mkv":
                    self.menu_r = True
                    self.video_repr = True
                    self.video(self.contenido_dat[paths[0]], [], mkv_time=None)
                    #while self.video_repr:
                     #   if not(self.video_repr):
                      #      break
                elif extension == ".json":
                    print("path_menu",self.contenido_dat[paths[0]])
                    menu_f = open(self.contenido_dat[paths[0]])
                    menu_t = menu_f.read()
                    menu_j = json.loads(menu_t)
                    menu_f.close()
                    print("menu:",menu_j)
                    time.sleep(16/1000)
                    self.menu(menu_j)
                    self.reproductor.update_idletasks()
                    self.espacio_mv.update_idletasks()
            else:
                path_num = 0
                while path_num <= len(paths)-1:
                    nombre, extension = os.path.splitext(paths[path_num])
                    if extension == ".mkv":
                        if len(paths)-1>=path_num+1:
                            self.menu_r = True
                            self.video_repr = True
                            if type(paths[path_num+1]) == type([]):
                                self.video(self.contenido_dat[paths[path_num]], paths[path_num+2:], mkv_time=paths[path_num+1])
                            else:
                                self.video(self.contenido_dat[paths[path_num]], paths[path_num+1:], mkv_time=None)
                            #while self.video_repr:
                            #   if not(self.video_repr):
                            #      break
                            break
                        else:
                            self.menu_r = True
                            self.video_repr = True
                            self.video(self.contenido_dat[paths[path_num]], [])
                            #while self.video_repr:
                            #   if not(self.video_repr):
                            #      break
                            break
                    elif extension == ".json":
                        print("path_menu",self.contenido_dat[paths[path_num]])
                        menu_f = open(self.contenido_dat[paths[path_num]])
                        menu_t = menu_f.read()
                        menu_j = json.loads(menu_t)
                        menu_f.close()
                        print("menu:",menu_j)
                        time.sleep(16/1000)
                        self.menu(menu_j)
                        self.reproductor.update_idletasks()
                        self.espacio_mv.update_idletasks()
                    path_num += 1
        else:
            self.loop_comandos_on = False
            nombre, extension = os.path.splitext(paths)
            if extension == ".mkv":
                if mkv_t != None:
                    self.menu_r = True
                    self.video_repr = True


                    self.pista_audio_name.set("0")

                    self.pista_video_name.set("0")

                    self.pista_subtitulos_name.set("none")


                    self.video(self.contenido_dat[paths], paths_b, mkv_time=mkv_t)
                else:
                    self.menu_r = True
                    self.video_repr = True
                    self.video(self.contenido_dat[paths], paths_b, mkv_time=None)
                #while self.video_repr:
                 #   if not(self.video_repr):
                  #      break
            elif extension == ".json":
                print("path_menu",self.contenido_dat[paths])
                menu_f = open(self.contenido_dat[paths])
                menu_t = menu_f.read()
                menu_j = json.loads(menu_t)
                menu_f.close()
                print("menu:",menu_j)
                time.sleep(16/1000)
                self.menu(menu_j)
                self.reproductor.update_idletasks()
                self.espacio_mv.update_idletasks()

    def video_r(self, vid, file_name, fps, video_path):
        print("video-r1")
        print(f"{self.carpeta_temporal_video}/{file_name}")
        frames = sorted(os.listdir(f"{self.carpeta_temporal_video}/{file_name}"))
        print("ff", frames)
        self.used_vid[file_name][1] = 0
        if self.used_vid[file_name][0] == False:
            try:
                print("sound")
                self.used_vid[file_name].append(pygame.mixer.Sound(f"{self.carpeta_temporal_video}/{file_name}.opus"))
                self.used_vid[file_name][2].set_volume(self.volume.get()/100)
                self.used_vid[file_name].append(self.used_vid[file_name][2].play())
            except Exception as e:
                print(e)
            print("vp", video_path)
            self.used_vid[file_name] = [True,0]
            video_hilo = threading.Thread(target=lambda: self.update_frame_vid(frames,fps,file_name,video_path,vid))
            video_hilo.start()

    def update_frame_vid(self, frames, fps, file_name, video_path, vid):
        print("video-r2")
        for frame in frames:
            if self.used_vid[file_name][0] and self.get_frames_num(video_path) > self.used_vid[file_name][1] and self.ventana_tk.winfo_viewable():
                try:
                    frame_file = os.path.join(self.carpeta_temporal_video,file_name,frame)
                    imagen_file = Image.open(frame_file)
                    imagen = ImageTk.PhotoImage(imagen_file)
                    #self.objetos_menu[vid]["objeto"].image = imagen
                    self.objetos_menu[vid]["imagen"] = imagen_file
                    self.used_vid[file_name][1] += 1
                    time.sleep(1/fps)
                    print(frame)
                    self.used_vid[file_name][2].set_volume(self.volume.get()/100)
                except:
                    break
            else:
                try:
                    self.used_vid[file_name][2].stop()
                except:
                    pass
                self.used_vid[file_name][0] = False
        self.used_vid[file_name][0] = False
    
    def get_frames_num(self, filename):
        cmd = [
            "ffprobe", "-v", "error", "-count_frames",
            "-select_streams", "v:0",
            "-show_entries", "stream=nb_read_frames",
            "-of", "default=nokey=1:noprint_wrappers=1",
            filename
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return int(result.stdout.strip())

    def get_fps(self, filename):
        cmd = [
            "ffprobe", "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=r_frame_rate",
            "-of", "json", filename
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        data = json.loads(result.stdout)
        rate = data["streams"][0]["r_frame_rate"]
        num, den = map(int, rate.split('/'))
        fps = num / den

        print(num, den)
        print(f"FPS: {fps}")
        return fps
    
    def ejecutar_boton(self, comandos):
        if type(comandos[0]) == type([]):
            print("op")
            print(comandos)
            for comando in comandos:
                print("op2")
                print(comando)
                self.ejecutar_boton(comando)
        else:
            time.sleep(16/1000)
            self.comnado_ejecutar(comandos,self.espacio_mv)

    def actalizar_medidas(self):
        try:
            ancho_ventana = self.ventana_tk.winfo_width()
            alto_ventana = self.ventana_tk.winfo_height()

            interfaz_alto = max(int(self.ventana_tk.winfo_height()/12),35)
            interfaz_ancho = max(int(self.ventana_tk.winfo_width()/8),18) #/16
            play_ancho = max(int(self.ventana_tk.winfo_width()/8),56) #*.1875

            self.reproductor.config(width=ancho_ventana,height=alto_ventana-(alto_ventana/25+interfaz_alto))
            self.reproductor.place(x=0,y=alto_ventana/25)

            self.bucle_boton.place(x=0,y=alto_ventana-interfaz_alto,width=interfaz_ancho,height=interfaz_alto)

            #self.atras_boton.place(x=int(ancho_ventana/2.5)-(int(play_ancho*2)),y=alto_ventana-interfaz_alto,width=interfaz_ancho,height=interfaz_alto)

            #self.play_boton.place(x=int(ancho_ventana/2.5)-int(play_ancho/2),y=alto_ventana-interfaz_alto,width=play_ancho,height=interfaz_alto)

            #self.adelante_boton.place(x=int(ancho_ventana/2.5)+(int(play_ancho)),y=alto_ventana-interfaz_alto,width=interfaz_ancho,height=interfaz_alto)

            self.atras_boton.place(x=int(ancho_ventana/2)-(int(play_ancho*2)),y=alto_ventana-interfaz_alto,width=interfaz_ancho,height=interfaz_alto)

            self.play_boton.place(x=int(ancho_ventana/2)-int(play_ancho/2),y=alto_ventana-interfaz_alto,width=play_ancho,height=interfaz_alto)

            self.adelante_boton.place(x=int(ancho_ventana/2)+(int(play_ancho)),y=alto_ventana-interfaz_alto,width=interfaz_ancho,height=interfaz_alto)

            #self.volume_text.place(x=ancho_ventana-int(interfaz_ancho+int(interfaz_ancho*3/2)),y=alto_ventana-interfaz_alto,width=int(interfaz_ancho),height=interfaz_alto)

            self.volume.place(x=ancho_ventana-int(interfaz_ancho*3/2),y=alto_ventana-interfaz_alto,width=int(interfaz_ancho*3/2),height=interfaz_alto)
            self.volume.config(length=int(play_ancho*3/2)) #(interfaz_alto-20)/100

            self.archivos_menu.place(x=0,y=0,width=ancho_ventana/8,height=alto_ventana/25)

            self.editar_menu.place(x=ancho_ventana/8,y=0,width=ancho_ventana/8,height=alto_ventana/25)

            self.pista_subtitulos_text.place(x=2*ancho_ventana/8,y=0,width=ancho_ventana/8,height=alto_ventana/25)
            self.pista_subtitulos_menu.place(x=3*ancho_ventana/8,y=0,width=ancho_ventana/8,height=alto_ventana/25)

            self.pista_audio_text.place(x=4*ancho_ventana/8,y=0,width=ancho_ventana/8,height=alto_ventana/25)
            self.pista_audio_menu.place(x=5*ancho_ventana/8,y=0,width=ancho_ventana/8,height=alto_ventana/25)

            self.pista_video_text.place(x=6*ancho_ventana/8,y=0,width=ancho_ventana/8,height=alto_ventana/25)

            self.pista_video_menu.place(x=7*ancho_ventana/8,y=0,width=ancho_ventana/8,height=alto_ventana/25)
            self.reproductor.update_idletasks()
        except Exception as e:
            print(e)
            pass
        if self.menu_r:
            self.ventana_tk.after(10, self.actalizar_medidas)

    def menu_resize(self, menu_r_b=True):
        try:
            if self.resolution_menu[0]:
                reproductor_ancho = self.reproductor.winfo_width()
                reproductor_alto = self.reproductor.winfo_height()

                escala_ancho = self.resolution_menu[1][0]
                escala_alto = self.resolution_menu[1][1]

                escala_relacion_de_aspecto = escala_ancho/escala_alto
                reproductor_relacion_de_aspecto = reproductor_ancho/reproductor_alto

                if escala_relacion_de_aspecto < reproductor_relacion_de_aspecto: #mas ancho que el menu
                    espacio_mv_ancho = reproductor_alto*escala_relacion_de_aspecto
                    espacio_mv_x     = (reproductor_ancho-espacio_mv_ancho)//2
                    espacio_mv_alto  = reproductor_alto
                    espacio_mv_y     = 0
                else: #mas alto que el menu
                    espacio_mv_alto  = reproductor_ancho/escala_relacion_de_aspecto
                    espacio_mv_y     = (reproductor_alto-espacio_mv_alto)//2
                    espacio_mv_ancho = reproductor_ancho
                    espacio_mv_x     = 0
                
                self.espacio_mv.place(x=espacio_mv_x,y=espacio_mv_y,width=espacio_mv_ancho,height=espacio_mv_alto)

                diferencia_escala_espacio_mv = [espacio_mv_ancho/escala_ancho,espacio_mv_alto/escala_alto]
                
                for objeto_num, objeto in enumerate(self.objetos_menu):
                    if isinstance(objeto["objeto"], pygame.mixer.Sound):
                        objeto["objeto"].set_volume(self.volume.get()/100*comando[1]["volume"]/100)
                    elif "video_r" in objeto.keys():
                        if "video_rr" in objeto.keys():
                            cordenadas = [0,0,escala_ancho,escala_alto-int(escala_alto/10)]
                        else:
                            cordenadas = [0,0,escala_ancho,escala_alto]
                        ancho_imagen=int(cordenadas[2]*diferencia_escala_espacio_mv[0])-int(cordenadas[0]*diferencia_escala_espacio_mv[0])
                        alto_imagen=int(cordenadas[3]*diferencia_escala_espacio_mv[1])-int(cordenadas[1]*diferencia_escala_espacio_mv[1])

                        imagen =  ImageTk.PhotoImage(objeto["imagen"].resize((ancho_imagen,alto_imagen), Image.Resampling.LANCZOS))

                        objeto["objeto"].config(image=imagen)
                        objeto["objeto"].image = imagen

                        objeto["objeto"].place(x=int(cordenadas[0]*diferencia_escala_espacio_mv[0]),
                                            y=int(cordenadas[1]*diferencia_escala_espacio_mv[1]),
                                            width=int(cordenadas[2]*diferencia_escala_espacio_mv[0])-int(cordenadas[0]*diferencia_escala_espacio_mv[0]),
                                            height=int(cordenadas[3]*diferencia_escala_espacio_mv[1])-int(cordenadas[1]*diferencia_escala_espacio_mv[1]))
                    elif "imagen" in objeto.keys():
                        cordenadas = objeto["cordenadas"]

                        ancho_imagen=int(cordenadas[2]*diferencia_escala_espacio_mv[0])-int(cordenadas[0]*diferencia_escala_espacio_mv[0])
                        alto_imagen=int(cordenadas[3]*diferencia_escala_espacio_mv[1])-int(cordenadas[1]*diferencia_escala_espacio_mv[1])

                        imagen =  ImageTk.PhotoImage(objeto["imagen"].resize((ancho_imagen,alto_imagen), Image.Resampling.LANCZOS))

                        objeto["objeto"].config(image=imagen)
                        objeto["objeto"].image = imagen

                        objeto["objeto"].place(x=int(cordenadas[0]*diferencia_escala_espacio_mv[0]),
                                            y=int(cordenadas[1]*diferencia_escala_espacio_mv[1]),
                                            width=int(cordenadas[2]*diferencia_escala_espacio_mv[0])-int(cordenadas[0]*diferencia_escala_espacio_mv[0]),
                                            height=int(cordenadas[3]*diferencia_escala_espacio_mv[1])-int(cordenadas[1]*diferencia_escala_espacio_mv[1]))
                    else:
                        cordenadas = objeto["cordenadas"]

                        objeto["objeto"].place(x=int(cordenadas[0]*diferencia_escala_espacio_mv[0]),
                                            y=int(cordenadas[1]*diferencia_escala_espacio_mv[1]),
                                            width=int(cordenadas[2]*diferencia_escala_espacio_mv[0])-int(cordenadas[0]*diferencia_escala_espacio_mv[0]),
                                            height=int(cordenadas[3]*diferencia_escala_espacio_mv[1])-int(cordenadas[1]*diferencia_escala_espacio_mv[1]))

            self.reproductor.update_idletasks()
            self.espacio_mv.update_idletasks()
        except:
            pass
        if self.menu_r and menu_r_b:
            self.ventana_tk.after(10, self.menu_resize)

    def repdorucir(self):
        paths = MaVM.extrac_type_all(file=self.file, output_folder=self.carpeta_temporal, content_type=None)
        #videos = MaVM.extrac_type_all(file=self.file, output_folder=self.carpeta_temporal, content_type="video/x-matroska")

        self.contenido_dat = {}
        for path in paths:
            directorio, archivo = os.path.split(path)
            self.contenido_dat[archivo] = path
            print(archivo)
        self.start()

    def leer_subtitulo(self, subtitulo_path, time_sub_segundos):
        file = open(subtitulo_path,'r')
        subtitulo_encode = file.read()
        file.close()

        subtitulo_list = subtitulo_encode.split('\n\n')
        subtitulo_decode = []
        for sub_x in subtitulo_list:
            try:
                sub_y = sub_x.split('\n')[1:]
                times_sub = sub_y[0].split(' --> ')
                sub = sub_y[1]

                time_sub_x = times_sub[0].replace(',','.').split(':')

                time_sub_y = times_sub[1].replace(',','.').split(':')

                times_sub = [float(f'{(time_sub_x[0]*3600)+(time_sub_x[1]*60)+time_sub_x[2]}'),
                             float(f'{(time_sub_y[0]*3600)+(time_sub_y[1]*60)+time_sub_y[2]}')]
                
                subtitulo_decode.append([times_sub,sub])
            except:
                pass
        
        for s in subtitulo_decode:
            if s[0][0] <= time_sub_segundos < s[0][1]:
                return s[1]

    def video(self,video_path,paths,mkv_time=None):
        if mkv_time != None:
            if type(mkv_time[0]) == type(""):
                try:
                    if type(mkv_t[3]) == type(2):
                        mkv_t = (mkv_time[0][:-1],mkv_time[1][:-1])
                        mkv_p = (mkv_time[2],mkv_time[3],mkv_time[4])
                    else:
                        mkv_t = (mkv_time[0][:-1],mkv_time[1][:-1])
                        mkv_p = None
                except:
                    mkv_t = (mkv_time[0][:-1],mkv_time[1][:-1])
                    mkv_p = None
            else:
                try:
                    if type(mkv_time[3]) == type(""):
                        mkv_t = (mkv_time[3][:-1],mkv_time[4][:-1])
                        mkv_p = (mkv_time[0],mkv_time[1],mkv_time[2])
                    else:
                        mkv_t = None
                        mkv_p = (mkv_time[0],mkv_time[1])
                except:
                    mkv_t = None
                    mkv_p = (mkv_time[0],mkv_time[1],mkv_time[2])
        else:
            mkv_t = None
            mkv_p = None

        self.loop_comandos_on = False
        self.objetos_menu = []
        self.used_vid = {}
        for widget in self.reproductor.winfo_children():
            try:
                if widget is self.espacio_mv:
                    y = False
                else: 
                    widget.destroy()  #elimina cada widget
            except:
                widget.destroy()  #elimina cada widget
        
        for widget in self.espacio_mv.winfo_children():
            try:
                if widget is self.espacio_mv:
                    y = False
                else: 
                    widget.destroy()  #elimina cada widget
            except:
                widget.destroy()  #elimina cada widget
        
        archivo = os.path.basename(video_path)

        file_name, extension = os.path.splitext(archivo)
        
        try:
            shutil.rmtree(os.path.join(self.carpeta_temporal_video,file_name))
            os.makedirs(os.path.join(self.carpeta_temporal_video,file_name))
        except:
            os.makedirs(os.path.join(self.carpeta_temporal_video,file_name))
        
        contenido_video = subprocess.run(["ffprobe", "-v", "quiet", "-print_format", "json", "-show_streams", video_path],capture_output=True,text=True)
        
        contenidos_video_json = json.loads(contenido_video.stdout)["streams"]

        print(contenidos_video_json)

        video_subtitulos = ["none"]
        video_audios     = []
        video_videos     = []

        self.pista_audio_name.set("none")

        for contenido in contenidos_video_json:
            if "codec_type" in contenido.keys():
                if contenido["codec_type"] == "audio":
                    video_audios.append(str(len(video_audios)))
                    self.pista_audio_name.set("0")
                elif contenido["codec_type"] == "video":
                    video_videos.append(str(len(video_videos)))
                elif contenido["codec_long_name"] == "SubRip subtitle":
                    video_subtitulos.append(str(len(video_subtitulos)-1))

        print(video_subtitulos,'\n',video_audios,'\n',video_videos)

        menu_audio = self.pista_audio_menu["menu"]
        menu_audio.delete(0, "end")

        if mkv_p == None:
            self.pista_audio_name.set("0")
        else:
            if mkv_p[2]:
                self.pista_audio_name.set(f"{mkv_p[2]}")
            else:
                self.pista_audio_name.set("none")

        opciones_audio = video_audios
        for opcion in opciones_audio:
            def _set_val(v=opcion):
                print("audio seleccionado", v)
                self.pista_audio_name.set(v)
            menu_audio.add_command(
                label=opcion,
                command=_set_val
            )

        try:
            shutil.rmtree(os.path.join(self.carpeta_temporal_video,f"{self.carpeta_temporal_video}/{file_name}"))
            os.makedirs(os.path.join(self.carpeta_temporal_video,f"{self.carpeta_temporal_video}/{file_name}"))
        except:
            os.makedirs(os.path.join(self.carpeta_temporal_video,f"{self.carpeta_temporal_video}/{file_name}"))
        
        for audio_num, audio in enumerate(video_audios):
            if mkv_t:
                subprocess.run(["ffmpeg", "-i",video_path, "-ss",mkv_t[0], "-to",mkv_t[1], "-map",f"0:a:{audio_num}", "-c:a","libopus", f"{audio_num}.opus"], cwd=f"{self.carpeta_temporal_video}/{file_name}")
            else:
                subprocess.run(["ffmpeg", "-i",video_path, "-map",f"0:a:{audio_num}", "-c:a","libopus", f"{audio_num}.opus"], cwd=f"{self.carpeta_temporal_video}/{file_name}")

        menu_video = self.pista_video_menu["menu"]
        menu_video.delete(0, "end")

        if mkv_p == None:
            self.pista_video_name.set("0")
        else:
            self.pista_video_name.set(f"{mkv_p[0]}")

        opciones_video = video_videos
        for opcion in opciones_video:
            def _set_val_v(v=opcion):
                print("video seleccionado", v)
                self.pista_video_name.set(v)
            menu_video.add_command(
                label=opcion,
                command=_set_val_v
            )

        for video_num, video in enumerate(video_videos):
            try:
                shutil.rmtree(os.path.join(self.carpeta_temporal_video,file_name,str(video_num)))
                os.makedirs(os.path.join(self.carpeta_temporal_video,file_name,str(video_num)))
            except:
                os.makedirs(os.path.join(self.carpeta_temporal_video,file_name,str(video_num)))
            if mkv_t:
                subprocess.run(["ffmpeg", "-i",video_path, "-ss",mkv_t[0], "-to",mkv_t[1], "-map",f"0:v:{video_num}", "fotograma_%04d.png"], cwd=f"{os.path.join(self.carpeta_temporal_video,file_name,str(video_num))}")
            else:
                subprocess.run(["ffmpeg", "-i",video_path, "-map",f"0:v:{video_num}", "fotograma_%04d.png"], cwd=f"{os.path.join(self.carpeta_temporal_video,file_name,str(video_num))}")
        
        menu_subtitulos = self.pista_subtitulos_menu["menu"]
        menu_subtitulos.delete(0, "end")

        if mkv_p == None:
            self.pista_subtitulos_name.set("none")
        else:
            if mkv_p[2]:
                self.pista_subtitulos_name.set(f"{mkv_p[2]}")
            else:
                self.pista_subtitulos_name.set("none")

        opciones_subtitulos = video_subtitulos
        for opcion in video_subtitulos:
            def _set_val_v(v=opcion):
                print("video seleccionado", v)
                self.pista_subtitulos_name.set(v)
            menu_subtitulos.add_command(
                label=opcion,
                command=_set_val_v
            )

        for subtitulo_num, subtitulo in enumerate(video_subtitulos):
            if mkv_t:
                subprocess.run(["ffmpeg", "-i",video_path, "-ss",mkv_t[0], "-to",mkv_t[1], "-map",f"0:s:{subtitulo_num}", "-c:s", "srt", f"{subtitulo_num}.srt"], cwd=f"{self.carpeta_temporal_video}/{file_name}")
            else:
                subprocess.run(["ffmpeg", "-i",video_path, "-map",f"0:s:{subtitulo_num}", "-c:s", "srt", f"{subtitulo_num}.srt"], cwd=f"{self.carpeta_temporal_video}/{file_name}")
        
        #subprocess.run(['mpv', video_path])

        fps = self.get_fps(video_path)

        try:
            audio = [True, pygame.mixer.music.load(os.path.join(self.carpeta_temporal_video,f"{file_name}.opus"))]
            pygame.mixer.music.play()
        except:
            audio = [False]
        print(audio)
        #audi0.set_volume(50/100)

        self.used_vid[file_name] = [False,0]
        #try:
        #    self.used_vid[file_name][2] = pygame.mixer.music(f"{self.carpeta_temporal_video}/{video_path}.opus")
        #    self.used_vid[file_name].append(self.used_vid[file_name][2].play())
        #except:
        #    pass
        print("vp", video_path)
        
        frame_num = -1
        #print(frames)
        #frames_num = len(frames)-1

        self.objetos_menu.append({"objeto":tk.Label(self.espacio_mv), "video_r":archivo, "video_path":video_path, "imagen": None})
        vid = len(self.objetos_menu)-1
        self.objetos_menu[vid]["objeto"].place()

        if audio[0]:
            pygame.mixer.music.play()
        
        self.pista_audio = "none"

        self.objetos_menu.append({"objeto": tk.Label(self.espacio_mv,text='',bg="#000000",fg="#E6E600"), "cordenadas":[0,int(9*self.resolution_menu[1][1]/10),self.resolution_menu[1][0],self.resolution_menu[1][1]],"video_rr":1})
        
        self.video_repr = True
        self.video_b(file_name=file_name,vid=vid,frame_num=frame_num,play=True,paths=paths,audio=audio)
    
    def get_seconds(self, video_path):
        """Obtiene la duración del video usando ffprobe."""
        comando = [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", video_path
        ]
        try:
            resultado = subprocess.run(comando, capture_output=True, text=True, check=True)
            duracion = float(resultado.stdout.strip())
            return duracion
        except subprocess.CalledProcessError as e:
            return None

    def video_b(self,file_name,vid,frame_num,play,paths,audio):
        frames = sorted(os.listdir(f"{self.carpeta_temporal_video}/{file_name}/{self.pista_video_name.get()}"))
        frames_num = len(frames)-1

        #while not(frame_num == frames_num):
        #if not(frame_num == frames_num):
        if frame_num >= frames_num:
            if self.bucle.get() == "1":
                frame_num = 0

                self.reproductor.update_idletasks()
                
                self.espacio_mv.update_idletasks()

                pygame.mixer.music.play(start=0)
                self.ventana_tk.after(10, lambda: self.video_b(file_name,vid,frame_num,play,paths,audio))
            else:
                if self.pista_audio_name.get() != "none":
                    pygame.mixer.music.pause()
                for widget in self.reproductor.winfo_children():
                    try:
                        if widget is self.espacio_mv:
                            y = False
                        else: 
                            widget.destroy()  #elimina cada widget
                    except:
                        widget.destroy()  #elimina cada widget
                
                for widget in self.espacio_mv.winfo_children():
                    try:
                        if widget is self.espacio_mv:
                            y = False
                        else: 
                            widget.destroy()  #elimina cada widget
                    except:
                        widget.destroy()  #elimina cada widget
                
                self.menu_r = True
                self.video_repr = False


                self.pista_audio_name.set("0")

                self.pista_video_name.set("0")

                self.pista_subtitulos_name.set("none")


                self.teleport(paths)

                #self.menu_resize()
                #self.actalizar_medidas()
                return
        elif self.video_repr:
            print(f"{file_name}.mkv")
            fps = len(frames)/self.get_seconds(self.contenido_dat[f"{file_name}.mkv"])

            segundos_por_fotograma = 1/fps
            fotogramas_cambio = int(10*fps)

            segundos_cambio = fotogramas_cambio/fps

            if play:
                try:
                    accion = self.detectar_botones
                    
                    frame = frames[frame_num]

                    print(frame)
                    if accion == "stop-play":
                        play = False
                        self.reset_botones_fun()
                        if self.pista_audio_name.get() != "none":
                            #if self.pista_audio_name.get() != self.pista_audio:
                            #   pygame.mixer.music.load(os.path.join(self.carpeta_temporal_video,file_name,f"{self.pista_video_name.get()}.opus"))
                            #pygame.mixer.music.pause()
                            pygame.mixer.music.pause()
                    elif accion == "adelante":
                        if (frame_num+fotogramas_cambio)>frames_num or (frame_num+fotogramas_cambio)==frames_num:
                            frame_num = frames_num
                        else:
                            frame_num += fotogramas_cambio
                        self.reset_botones_fun()
                        if self.pista_audio_name.get() != "none":
                            #if self.pista_audio_name.get() != self.pista_audio:
                            #   pygame.mixer.music.load(os.path.join(self.carpeta_temporal_video,file_name,f"{self.pista_video_name.get()}.opus"))
                            #pygame.mixer.music.pause()
                            pygame.mixer.music.load(os.path.join(self.carpeta_temporal_video,file_name,f"{self.pista_audio_name.get()}.opus"))
                            print(os.path.join(self.carpeta_temporal_video,file_name,f"{self.pista_audio_name.get()}.opus"))
                            self.pista_audio = self.pista_audio_name.get()
                        pygame.mixer.music.play(start=frame_num/fps)

                    elif accion == "atras":
                        if (frame_num-fotogramas_cambio)<0 or (frame_num-fotogramas_cambio)==0:
                            frame_num = 0
                        else:
                            frame_num -= fotogramas_cambio
                        self.reset_botones_fun()
                        if self.pista_audio_name.get() != "none":
                            #if self.pista_audio_name.get() != self.pista_audio:
                            #   pygame.mixer.music.load(os.path.join(self.carpeta_temporal_video,file_name,f"{self.pista_video_name.get()}.opus"))
                            #pygame.mixer.music.pause()
                            pygame.mixer.music.load(os.path.join(self.carpeta_temporal_video,file_name,f"{self.pista_audio_name.get()}.opus"))
                            print(os.path.join(self.carpeta_temporal_video,file_name,f"{self.pista_audio_name.get()}.opus"))
                            self.pista_audio = self.pista_audio_name.get()
                        pygame.mixer.music.play(start=frame_num/fps)
                    else:
                        frame_num +=1

                    if self.pista_audio_name.get() != "none":
                        if self.pista_audio_name.get() != self.pista_audio:
                            pygame.mixer.music.load(os.path.join(self.carpeta_temporal_video,file_name,f"{self.pista_video_name.get()}.opus"))
                            #pygame.mixer.music.pause()
                            pygame.mixer.music.load(os.path.join(self.carpeta_temporal_video,file_name,f"{self.pista_audio_name.get()}.opus"))
                            print(os.path.join(self.carpeta_temporal_video,file_name,f"{self.pista_audio_name.get()}.opus"))
                            pygame.mixer.music.play(start=frame_num/fps)
                        self.pista_audio = self.pista_audio_name.get()
                        pygame.mixer.music.set_volume(self.volume.get()/100)

                    if self.pista_subtitulos_name.get() != "none":
                        sub = self.leer_subtitulo(subtitulo_path=os.path.join(self.carpeta_temporal_video,file_name,f"{self.pista_subtitulos_name.get()}.srt"),
                                                  time_sub_segundos=frame_num/fps)
                        self.objetos_menu[1]["objeto"].config(text=sub)
                    
                    print(f"frame_num:{frame_num}\nframes_num:{frames_num}")
                    #os.path.join(
                    frame_file_path = os.path.join(self.carpeta_temporal_video,file_name,self.pista_video_name.get(),frame)
                    imagen_file = Image.open(frame_file_path)
                    imagen = ImageTk.PhotoImage(imagen_file)
                    #self.objetos_menu[vid]["objeto"].image = imagen
                    self.objetos_menu[vid]["imagen"] = imagen_file
                    self.used_vid[file_name][1] += 1
                except Exception as e:
                    print(e)
            else:
                accion = self.detectar_botones
                if accion == "stop-play":
                    play = True
                    self.reset_botones_fun()
                    if self.pista_audio_name.get() != "none":
                        pygame.mixer.music.play(start=frame_num/fps)
                
            self.reproductor.update_idletasks()
                
            self.espacio_mv.update_idletasks()

            self.ventana_tk.after(int(segundos_por_fotograma*1000), lambda: self.video_b(file_name,vid,frame_num,play,paths,audio))

def args():
    parser = argparse.ArgumentParser(description="reproductor MaVM")
    parser.add_argument("file", nargs='?', help="ruta del video .mavm")
    parser.add_argument('--version',"-v", action="store_true", help="player version number")
    
    args_var = parser.parse_args()
    
    if args_var.version:
        print('v.1.20.0.0')
    else:
        if args_var.file:
            if not('.mavm' in args_var.file.lower()):
                print("el archivo debe ser .mavm")
                exit()
            elif not(os.path.exists(args_var.file)):
                print("el archivo no existe")
                exit()
            else:
                file = os.path.abspath(args_var.file)
                ventana_tk = tk.Tk()
                ventana(ventana_tk=ventana_tk, file=file)
                ventana_tk.mainloop()
        else:
            ventana_tk = tk.Tk()
            ventana(ventana_tk, None)
            ventana_tk.mainloop()


if not(exit_):
    args()
