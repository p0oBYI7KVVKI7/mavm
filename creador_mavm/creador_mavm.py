from pymkv import MKVFile
import argparse

class create_mavm:
    def __init__(self, file_e="", files="", file_out="video.mavm", r=None):
        self.file_e   = file_e
        self.file_out = file_out
        if r:
            files_names_txt = open(files, 'r')
            files_names     = files_names_txt.read().split('\n')
            files_names_txt.close()
            self.create_r(files=files_names) #aca se crea el archivo mavm en base a los otros archivos
        else:
            self.create_r(files=files)
    def create_r(self, files):
        mkv = MKVFile(self.file_e)
        for file in files:
            try:
                mkv.add_attachment(file)
                mkv.mux(self.file_out)
            except:
                pass
    def create(self, file):
        mkv = MKVFile(self.file_e)
        mkv.add_attachment(file)
        mkv.mux(self.file_out)

def main():
    parser = argparse.ArgumentParser(description="creador MaVM")
    parser.add_argument("--file_e", help="archivo base\n") #archivo de encapsulado
    parser.add_argument("--files_r", help="documento txt con los archivos a importar\n") #archivos a guardado
    parser.add_argument("--file", help="archivo a importar (JSON/MKV/OPUS)\n") #archivos a importas
    parser.add_argument("--file_out", help="archivo de salida .mavm\n", default="video.mavm") #archivo de salida

    args = parser.parse_args()
    
    if not('.mavm' in args.file_out.lower()):
        print("el archivo de salida debe ser .mavm")
        exit()
    elif args.files_r == None and args.file == None:
        print("tienes que estables el o los archivo(s) de entrada")
        exit()
    if args.files_r == None:
        create_mavm(file_e=args.file_e,files=args.file,file_out=args.file_out)
    elif args.file == None:
        create_mavm(file_e=args.file_e,files=args.files_r,file_out=args.file_out,r=True)

main()
