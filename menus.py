class version_formato:
    def __new__(cls, version):
        version_soported = ('v.2.1.0','v.2.2.0','v.3.0.0','v.3.1.0',)
        interfaz_version = {'v.2.1.0': cls.interfaz_2_1_0,
                            'v.2.2.0': cls.interfaz_2_2_0,
                            'v.3.0.0': cls.interfaz_2_2_0,
                            'v.3.1.0': cls.interfaz_2_2_0}
        if version in version_soported:
            return [True, interfaz_version[version]]
        else:
            return [False, None]
    
    class interfaz_2_1_0:
        def __init__(self, menu):
            lista_comandos = {
                "resolucion":[],
                "start": [],
                "loop": []
                }
            m = []
            menu_name = ''
            start_comandos = menu["start"]
            for comandos in start_comandos:
                    comando    = list(comandos.keys())[0]
                    parametros = list(comandos.values())[0]
                    if comando == "menu":
                        menu_name = parametros[1]
                    elif comando == menu_name:
                        if list(parametros[0].keys())[0] == "resolution":
                            lista_comandos["resolucion"] = list(parametros[0].values())[0]
                        else:
                            lista_comandos["start"] = self.comando_x(parametros, lista_comandos["start"])
                    elif comando == "time":
                        lista_comandos["start"].append(["time", {
                            "wait": [parametros[1],parametros[2]]
                            }])
            
            loop_comandos = menu["loop"]
            for comandos in loop_comandos:
                    comando   = list(comandos.keys())[0]
                    parametros = list(comandos.values())[0]
                    if comando == menu_name:
                        lista_comandos["loop"] = self.comando_x(parametros, lista_comandos["loop"])
                    elif comando == "time":
                        lista_comandos["loop"].append(["time", {
                            "wait": [parametros[1],parametros[2]]
                            }])
            self.lista_comandos = lista_comandos

        def comando_x(self, comandos, lista_comandos):
                print(comandos)
                try:
                    comando   = list(comandos[0].keys())[0]
                    parametros = list(comandos[0].values())[0]
                except:
                    comando   = list(comandos.keys())[0]
                    parametros = list(comandos.values())[0]
                if comando == "image":
                    if parametros[0] == "create":
                        lista_comandos.append(["image", {
                            parametros[0]: parametros[1],
                            "coordinates": [
                                parametros[3], parametros[4],
                                parametros[5], parametros[6]
                                ],
                            "imagen": parametros[7]
                        }])
                    elif parametros[0] == "edit":
                        lista_comandos.append(["image", {
                            parametros[0]: parametros[1],
                            "coordinates": [
                                parametros[3], parametros[4],
                                parametros[5], parametros[6]
                                ],
                            "imagen": parametros[7]
                        }])
                elif comando == "text": 
                    lista_comandos.append(["text", {
                        "coordinates": [
                            parametros[1], parametros[2],
                            parametros[3], parametros[4]
                            ],
                        "text": parametros[6]
                    }])
                elif comando == "button":
                    if "command_click" in parametros:
                        if type(parametros[12]) == type([]):
                            coman = []
                            for com in parametros[12]:
                                coman.append(self.comando_x(com,[]))
                        else:
                            coman = self.comando_x([parametros[12]],[])
                        if "command4selection" in parametros:
                            if "command4no_selection" in parametros:
                                if type(parametros[14]) == type([]):
                                    coman2 = []
                                    for com in parametros[14]:
                                        coman2.append(self.comando_x(com,[]))
                                else:
                                    coman2 = self.comando_x([parametros[14]],[])

                                if type(parametros[16]) == type([]):
                                    coman3 = []
                                    for com in parametros[16]:
                                        coman3.append(self.comando_x(com,[]))
                                else:
                                    coman3 = self.comando_x([parametros[16]],[])
                                
                                lista_comandos.append(["button", {
                                    parametros[0]: parametros[1],
                                    "coordinates": [
                                        parametros[3], parametros[4],
                                        parametros[5], parametros[6]
                                        ],
                                    "title": parametros[8],
                                    "color": parametros[10],
                                    "command": coman,
                                    "command4selection": coman2,
                                    "command4no_selection": coman3
                                }])
                            else:
                                if type(parametros[14]) == type([]):
                                    coman2 = []
                                    for com in parametros[14]:
                                        coman2.append(self.comando_x(com,[]))
                                else:
                                    coman2 = self.comando_x([parametros[14]],[])
                                lista_comandos.append(["button", {
                                    parametros[0]: parametros[1],
                                    "coordinates": [
                                        parametros[3], parametros[4],
                                        parametros[5], parametros[6]
                                        ],
                                    "title": parametros[8],
                                    "color": parametros[10],
                                    "command": coman,
                                    "command4selection": coman2
                                }])
                        else:
                            lista_comandos.append(["button", {
                                    parametros[0]: parametros[1],
                                    "coordinates": [
                                        parametros[3], parametros[4],
                                        parametros[5], parametros[6]
                                        ],
                                    "title": parametros[8],
                                    "color": parametros[10],
                                    "command": coman
                                }])
                    else:
                        lista_comandos.append(["button", {
                            parametros[0]: parametros[1],
                            "coordinates": [
                                parametros[3], parametros[4],
                                parametros[5], parametros[6]
                                ],
                            "title": parametros[8],
                            "color": parametros[10]
                        }])
                elif comando == "teleport":
                    lista_comandos.append(["teleport", {
                        "ubicaciones": parametros
                    }]),
                elif comando == "video":
                    if parametros[0] == "create":
                        lista_comandos.append(["video", {
                            "create": parametros[1],
                            "coordinates": [parametros[3],parametros[4],
                                            parametros[5],parametros[6]],
                            "video": parametros[7]
                        }])
                    elif parametros[0] == "edit":
                        if parametros[2] == "restart":
                            lista_comandos.append(["video", {
                                "restart":parametros[1]
                            }])
                        else:
                            lista_comandos.append(["video", {
                                "edit": parametros[1],
                                "coordinates": [parametros[3],parametros[4],
                                                parametros[5],parametros[6]],
                                "video": parametros[7]
                            }])
                elif comando == "button_default":
                    lista_comandos.append(["button_default", {
                        "button": parametros[0]
                    }])
                elif comando == "sound":
                    if parametros[0] == "create":
                        lista_comandos.append(["sound", {
                            "create": parametros[1],
                            "sound": parametros[2],
                            "volume": parametros[4]
                        }])
                    elif parametros[0] == "edit":
                        lista_comandos.append(["sound", {
                            "edit": parametros[1],
                            "volume": parametros[3]
                        }])
                return lista_comandos
    
    class interfaz_2_2_0:
        def __init__(self, menu):
            lista_comandos = {
                "resolucion":[],
                "start": [],
                "loop": []
                }
            m = []
            menu_name = ''
            start_comandos = menu["start"]
            for comandos in start_comandos:
                    comando    = list(comandos.keys())[0]
                    parametros = list(comandos.values())[0]
                    if comando == "menu":
                        menu_name = parametros[1]
                    elif comando == menu_name:
                        if list(parametros[0].keys())[0] == "resolution":
                            lista_comandos["resolucion"] = list(parametros[0].values())[0]
                        else:
                            lista_comandos["start"] = self.comando_x(parametros, lista_comandos["start"])
                    elif comando == "time":
                        lista_comandos["start"].append(["time", {
                            "wait": [parametros[1],parametros[2]]
                            }])
            
            loop_comandos = menu["loop"]
            for comandos in loop_comandos:
                    comando   = list(comandos.keys())[0]
                    parametros = list(comandos.values())[0]
                    if comando == menu_name:
                        lista_comandos["loop"] = self.comando_x(parametros, lista_comandos["loop"])
                    elif comando == "time":
                        lista_comandos["loop"].append(["time", {
                            "wait": [parametros[1],parametros[2]]
                            }])
            self.lista_comandos = lista_comandos

        def comando_x(self, comandos, lista_comandos):
                print(comandos)
                try:
                    comando   = list(comandos[0].keys())[0]
                    parametros = list(comandos[0].values())[0]
                except Exception as e:
                    try:
                        print(e, "\n\n")
                        comando   = list(comandos.keys())[0]
                        parametros = list(comandos.values())[0]
                    except:
                        comando   = list(comandos[0][0].keys())[0]
                        parametros = list(comandos[0][0].values())[0]
                if comando == "image":
                    comando_r = ["image",{}]
                    parametro_num = 0
                    while parametro_num < len(parametros):
                        parametro = parametros[parametro_num]
                        if "coordinates" == parametro:
                            comando_r[1]["coordinates"] = [
                                parametros[parametro_num+1],parametros[parametro_num+2],
                                parametros[parametro_num+3],parametros[parametro_num+4]
                                ]
                            parametro_num += 4
                        elif "create" == parametro:
                            comando_r[1]["create"] = parametros[parametro_num+1]
                            parametro_num += 1
                        elif "edit" == parametro:
                            comando_r[1]["edit"] = parametros[parametro_num+1]
                            parametro_num += 1
                        elif parametro_num == len(parametros)-1:
                            comando_r[1]["imagen"] = parametros[parametro_num]
                        parametro_num += 1
                    lista_comandos.append(comando_r)
                elif comando == "text":
                    comando_r = ["text",{}]
                    parametro_num = 0
                    while parametro_num < len(parametros):
                        parametro = parametros[parametro_num]
                        if "coordinates" == parametro:
                            print(f"{parametros}\n{parametro_num}")
                            comando_r[1]["coordinates"] = [
                            parametros[parametro_num+1], parametros[parametro_num+2],
                            parametros[parametro_num+3], parametros[parametro_num+4]
                            ]
                            parametro_num += 4
                        elif "text" == parametro:
                            comando_r[1]["text"] = parametros[parametro_num+1]
                            parametro_num += 1
                        parametro_num += 1
                        if parametro_num >= len(parametros):
                            break
                    lista_comandos.append(comando_r)
                elif comando == "button":
                    comando_r = ["button",{}]
                    parametro_num = 0
                    while parametro_num < len(parametros):
                        parametro = parametros[parametro_num]
                        if "command_click" == parametro:
                            if type(parametros[parametro_num+1]) == type([]):
                                coman = []
                                for com in parametros[parametro_num+1]:
                                    coman.append(self.comando_x(com,[]))
                            else:
                                coman = self.comando_x([parametros[parametro_num+1]],[])
                            parametro_num += 1
                            comando_r[1]["command"] = coman
                        elif "command4selection" == parametro:
                            if type(parametros[parametro_num+1]) == type([]):
                                coman = []
                                for com in parametros[parametro_num+1]:
                                    coman.append(self.comando_x(com,[]))
                            else:
                                coman = self.comando_x([parametros[parametro_num+1]],[])
                            parametro_num += 1
                            comando_r[1]["command4selection"] = coman
                        elif "command4no_selection" == parametro:
                            #print(parametro)
                            #print(parametros)
                            if type(parametros[parametro_num+1]) == type([]):
                                coman = []
                                for com in parametros[parametro_num+1]:
                                    coman.append(self.comando_x(com,[]))
                            else:
                                coman = self.comando_x([parametros[parametro_num+1]],[])
                            parametro_num += 1
                            comando_r[1]["command4no_selection"] = coman
                        elif "coordinates" == parametro:
                            comando_r[1]["coordinates"] = [
                                        parametros[parametro_num+1], parametros[parametro_num+2],
                                        parametros[parametro_num+3], parametros[parametro_num+4]
                                        ]
                            parametro_num += 4
                        elif "title" == parametro:
                            comando_r[1]["title"] = parametros[parametro_num+1]
                        elif "image" == parametro:
                            comando_r[1]["image"] = parametros[parametro_num+1]
                            #comando_r[1]["title"] = parametros[parametro_num+1]
                        elif "color" == parametro:
                            comando_r[1]["color"] = parametros[parametro_num+1]
                        elif "create" == parametro:
                            comando_r[1]["create"] = parametros[parametro_num+1]
                        elif "edit" == parametro:
                            comando_r[1]["edit"] = parametros[parametro_num+1]
                        parametro_num += 1
                        if parametro_num >= len(parametros):
                            break
                    lista_comandos.append(comando_r)
                elif comando == "teleport":
                    lista_comandos.append(["teleport", {
                        "ubicaciones": parametros
                    }]),
                elif comando == "video":
                    comando_r = ["video",{}]
                    parametro_num = 0
                    while parametro_num < len(parametros):
                        parametro = parametros[parametro_num]
                        if "coordinates" == parametro:
                            comando_r[1]["coordinates"] = [
                                        parametros[parametro_num+1], parametros[parametro_num+2],
                                        parametros[parametro_num+3], parametros[parametro_num+4]
                                        ]
                            parametro_num += 4
                        elif "edit" == parametro:
                            comando_r[1]["edit"] = parametros[parametro_num+1]
                            parametro_num += 1
                        elif "create" == parametro:
                            comando_r[1]["create"] = parametros[parametro_num+1]
                            parametro_num += 1
                        elif "video_path" == parametro:
                            comando_r[1]["video"] = parametros[parametro_num+1]
                            parametro_num += 1
                        elif "restart" == parametro:
                            try:
                                comando_r[1]["restart"] = comando_r[1]["edit"]
                            except:
                                comando_r[1]["restart"] = parametros[parametro_num+2]
                                comando_r[1]["edit"]    = parametros[parametro_num+2]
                            break
                        parametro_num += 1
                        if parametro_num >= len(parametros):
                            break
                    lista_comandos.append(comando_r)
                elif comando == "button_default":
                    lista_comandos.append(["button_default", {
                        "button": parametros[0]
                    }])
                elif comando == "sound":
                    if parametros[0] == "create":
                        lista_comandos.append(["sound", {
                            "create": parametros[1],
                            "sound": parametros[2],
                            "volume": parametros[4]
                        }])
                    elif parametros[0] == "edit":
                        lista_comandos.append(["sound", {
                            "edit": parametros[1],
                            "volume": parametros[3]
                        }])
                return lista_comandos