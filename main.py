import os.path
import subprocess
from tkinter import BOTTOM, Button, Entry, END, filedialog, font, Frame, Tk, Label, LEFT, Radiobutton, Scale, StringVar
from pathlib import Path
from ffmpeg_supported_ext import list_ffmpeg_demuxer_supported, list_ffmpeg_muxer_supported

def run_cmd_line(string, out):
    try:
        label_conversion_en_cours.pack(side=BOTTOM)
        fen.update()
        subprocess.run(string, check=True)
        print(f"Conversion réussie : {out} a été créé.")
        label_conversion_en_cours.pack_forget()
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de FFmpeg : {e}")

def check_path_entries_correct() -> bool:
    """ Checke si les les entrys pour les chemins de fichiers contiennent la bonne valeur """
    errors = False

    # On checke les 3 entrys principales pour connaître les erreurs générales

    for entry in [entry_input_path, entry_input_file_name, entry_output_file_name]: # checks pour toutes les entrys
        entry_content = entry.get()
        custom_message = ""

        if entry_content == "" or entry_content.isspace():
            # si le contenu est vide
            custom_message = "| Le nom est vide "
            errors = True

        elif entry_content[0] == " ":
            custom_message = "| Le nom commence par \" \" "
            errors = True

        show_error_champ(entry, custom_message)

    # On checke les extensions pour voir si elles sont bonnes

    ext1 = entry_input_file_ext.get()
    ext2 = entry_output_file_ext.get()

    if not ext1 in list_ffmpeg_demuxer_supported:
        label_error_input_file["text"] += f"| L'extension \"{ext1}\" n'est pas supportée"
        label_error_input_file.update()
        errors = True

    if not ext2 in list_ffmpeg_muxer_supported:
        label_error_output_file["text"] += f"| L'extension \"{ext2}\" n'est pas supportée"
        label_error_output_file.update()
        errors = True

    if errors:
        return False

    hide_error_champs()
    return True

def show_error_champ(entry, error_message) -> None:
    # assacie chaque entry à son message d'erreur
    dic_entry_labels = {entry_input_path: label_error_path, entry_input_file_name: label_error_input_file, entry_output_file_name: label_error_output_file}

    # On vise le bon label en fonction de l'entry
    loc_error_label = dic_entry_labels[entry]

    # Changer le nom du label et l'afficher
    loc_error_label.configure(text=error_message)
    loc_error_label.pack(side=LEFT, padx=5)

def hide_error_champs() -> None:
    label_error_path["text"] = ""
    label_error_input_file["text"] = ""
    label_error_output_file["text"] = ""
    label_error_path.pack_forget()
    label_error_input_file.pack_forget()
    label_error_output_file.pack_forget()
    fen.update()

def get_main_paths() -> tuple:
    loc_main_path = entry_input_path.get()
    return loc_main_path, \
           loc_main_path + entry_input_file_name.get() + entry_input_file_ext.get(), \
           loc_main_path + entry_output_file_name.get() + entry_output_file_ext.get()

def input_file_exist(file_path) -> bool:
    if os.path.exists(file_path):
        return True

    label_error_input_file["text"] = f"\"{file_path}\" -> non existant : veuillez revérifier le nom/le chemin"
    label_error_input_file.pack(side=LEFT, padx=5)
    return False



class MediaObject:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path


    def compress(self) -> str:
        """ Compression du fichier """
        cmd_command = f"ffmpeg -i {self.input_path} {self.output_path}"
        return cmd_command


    def convert(self, lossy: bool) -> str:
        """ Conversion (voire compression) du fichier """
        if lossy:
            cmd_command = f"ffmpeg -i {self.input_path} {self.output_path}"
        else:
            cmd_command = f"ffmpeg -i {self.input_path} -c:v copy -c:a copy {self.output_path}"
        return cmd_command


    def extract_image(self):
        """ Extraction de la piste image """
        cmd_command = f"ffmpeg -i {self.input_path} -an -c:v copy {self.output_path}"
        return cmd_command


    def extract_audio(self):
        """ Extraction de la piste audio """
        cmd_command = f"ffmpeg -i {self.input_path} -vn -c:a copy {self.output_path}"
        return cmd_command


    def rotate(self, rotation: str = None):
        """ Rotation de l'image """
        dic_rotations = {"right": "transpose=1",
                        "left": "transpose=2",
                        "180": "transpose=2,transpose=2",
                        "haut-bas": "vflip",
                        "gauche-droite": "hflip"}

        cmd_command = f"ffmpeg -i {self.input_path} -vf \"{dic_rotations[rotation]}\" {self.output_path}"

        return cmd_command


    def cut_duration(self, begin: str, end: str): # ex : 05h20m05s
        """ Cut de la durée excédente """
        begin_s = int(begin[0:2]) * 3600 + int(begin[3:5]) * 60 + int(begin[6:8])
        end_s = int(end[0:2]) * 3600 + int(end[3:5]) * 60 + int(end[6:8])

        duration_s = end_s - begin_s
        duration_h = duration_s // 3600
        duration_s %= 3600
        duration_m = duration_s // 60
        duration_s %= 60

        duration = f"{duration_h:02}:{duration_m:02}:{duration_s:02}"
        cmd_command = f"ffmpeg -ss {begin} -i {self.input_path} -t {duration} -c copy {self.output_path}"

        return cmd_command


    def crop(self, width: str, height: str, x: str="0", y: str="0"):
        """ Rognage de la vidéo """
        cmd_command = f"ffmpeg -i {self.input_path} -vf \"crop={width}:{height}:{x}:{y}\" {self.output_path}"
        return cmd_command


class FilesInput:
    def __init__(self, input_path: str, output_path: str):
        self.input_path = input_path
        self.output_path = output_path


    def concatenate_images(self, framerate: str, quality: str):
        cmd_command = f"ffmpeg -framerate {framerate} -i /{self.input_path} -c:v libx264 -crf {quality} -pix_fmt yuv420p {self.output_path}"
        return cmd_command


    def concatenate_videos(self):
        cmd_command = f"ffmpeg -f concat -safe 0 -i {self.input_path} -c copy {self.output_path}"
        return cmd_command


def hide_one_input_file_divs():
    Compress().hide()
    Convert().hide()
    Extract().hide()
    Rotate().hide()
    Cut().hide()
    Crop().hide()


class Compress:
    def __init__(self):
        self.div_compress = div_compress
        self.label_compress = Label(div_compress, text="Compresser : ", font=bold_font)
        self.div_slider = Frame(div_compress)
        self.label_qualite = Label(self.div_slider, text="Compression :")
        self.slider_quality = Scale(self.div_slider, from_=0, to=100, orient='horizontal')

        self.btn_go = Button(div_compress, text="=>GO", command=self.execute)

    def show(self):
        hide_one_input_file_divs()
        self.div_compress.pack(pady=20)
        self.label_compress.pack()
        self.div_slider.pack()
        self.label_qualite.pack(side=LEFT)
        self.slider_quality.pack(side=LEFT)

        self.btn_go.pack(side=BOTTOM, pady=10)

    def hide(self):
        self.div_compress.pack_forget()

    @staticmethod
    def execute():
        """
        Actions :
        1/ Checke validité des entries
        2/ Obtient les chemins input et output
        3/ Checke si l'input existe
        4/ Run la commande ffmpeg adéquate
        """
        if not check_path_entries_correct():
            return

        path, input_file, output_file = get_main_paths()

        if not input_file_exist(input_file):
            return

        cmd_line = MediaObject(input_path=input_file, output_path=output_file).compress()
        run_cmd_line(cmd_line, output_file)


class Convert:
    def __init__(self):
        self.div_convert = div_convert
        self.label_convert = Label(div_convert, text="Convertir : ", font=bold_font)
        self.div_slider = Frame(div_convert)
        self.label_qualite = Label(self.div_slider, text="Compression : ")
        self.slider_quality = Scale(self.div_slider, from_=0, to=100, orient='horizontal')

        self.btn_go = Button(div_convert, text="=>GO", command=self.execute)

    def show(self):
        hide_one_input_file_divs()
        self.div_convert.pack(pady=20)
        self.label_convert.pack()
        self.div_slider.pack()
        self.label_qualite.pack(side=LEFT)
        self.slider_quality.pack(side=LEFT)

        self.btn_go.pack(side=BOTTOM, pady=10)

    def hide(self):
        self.div_convert.pack_forget()

    @staticmethod
    def execute():

        if not check_path_entries_correct():
            return

        path, input_file, output_file = get_main_paths()

        if not input_file_exist(input_file):
            return

        cmd_line = MediaObject(input_path=input_file, output_path=output_file).convert(lossy=False)
        run_cmd_line(cmd_line, output_file)

class Extract:
    def __init__(self):
        self.div_extract = div_extract
        self.div_choice = Frame(div_extract)
        self.label_choice = Label(self.div_choice, text="Extraire : ", font=bold_font)

        self.extract_value = StringVar()
        self.extract_value.set("audio")

        self.div_radiobuttons = Frame(self.div_choice)
        self.div_radiobuttons_audio = Frame(self.div_radiobuttons)
        self.radiobutton_audio = Radiobutton(self.div_radiobuttons_audio, variable=self.extract_value, value="audio")
        self.label_radiobutton_audio = Label(self.div_radiobuttons_audio, text="audio")

        self.div_radiobuttons_video = Frame(self.div_radiobuttons)
        self.radiobutton_video = Radiobutton(self.div_radiobuttons_video, variable=self.extract_value, value="vidéo")
        self.label_radiobutton_video = Label(self.div_radiobuttons_video, text="vidéo")

        self.btn_go = Button(self.div_extract, text="=>GO", command=self.execute)

    def show(self):
        hide_one_input_file_divs()
        self.div_extract.pack(pady=20)
        self.div_choice.pack()
        self.label_choice.pack(side=LEFT)
        self.div_radiobuttons.pack(side=LEFT)

        self.div_radiobuttons_audio.pack()
        self.radiobutton_audio.pack(side=LEFT)
        self.label_radiobutton_audio.pack(side=LEFT)

        self.div_radiobuttons_video.pack()
        self.radiobutton_video.pack(side=LEFT)
        self.label_radiobutton_video.pack(side=LEFT)

        self.radiobutton_audio.pack()
        self.radiobutton_video.pack()

        self.btn_go.pack(side=BOTTOM, pady=10)

    def hide(self):
        self.div_extract.pack_forget()

    def execute(self):

        if not check_path_entries_correct():
            return

        path, input_file, output_file = get_main_paths()

        if not input_file_exist(input_file):
            return

        if self.extract_value.get() == "audio":
            cmd_line = MediaObject(input_path=input_file, output_path=output_file).extract_audio()
        else:
            cmd_line = MediaObject(input_path=input_file, output_path=output_file).extract_image()

        run_cmd_line(cmd_line, output_file)

class Rotate:

    def __init__(self):
        self.div_rotate = div_rotate
        self.div_rotate_centre = Frame(self.div_rotate)
        self.div_rotate_gauche = Frame(self.div_rotate_centre)
        self.label_rotate = Label(self.div_rotate_gauche, text="Pivoter : ", font=bold_font)
        self.div_radiobutton = Frame(self.div_rotate_centre)

        self.rotate_value = StringVar()
        self.rotate_value.set("left")

        self.div_radiobutton_left = Frame(self.div_rotate_centre)
        self.label_radiobutton_left = Label(self.div_radiobutton_left, text="gauche")
        self.radiobutton_left = Radiobutton(self.div_radiobutton_left, variable=self.rotate_value, value="left")

        self.div_radiobutton_right = Frame(self.div_rotate_centre)
        self.label_radiobutton_right = Label(self.div_radiobutton_right, text="droite")
        self.radiobutton_right = Radiobutton(self.div_radiobutton_right, variable=self.rotate_value, value="right")

        self.div_radiobutton_180 = Frame(self.div_rotate_centre)
        self.label_radiobutton_180 = Label(self.div_radiobutton_180, text="180")
        self.radiobutton_180 = Radiobutton(self.div_radiobutton_180, variable=self.rotate_value, value="180")

        self.div_radiobutton_gauche_droite = Frame(self.div_rotate_centre)
        self.label_radiobutton_gauche_droite = Label(self.div_radiobutton_gauche_droite, text="gauche-droite")
        self.radiobutton_gauche_droite = Radiobutton(self.div_radiobutton_gauche_droite, variable=self.rotate_value, value="gauche-droite")

        self.div_radiobutton_haut_bas = Frame(self.div_rotate_centre)
        self.label_radiobutton_haut_bas = Label(self.div_radiobutton_haut_bas, text="haut-bas")
        self.radiobutton_haut_bas = Radiobutton(self.div_radiobutton_haut_bas, variable=self.rotate_value, value="haut-bas")

        self.btn_go = Button(self.div_rotate, text="=>GO", command=self.execute)

    def show(self):
        hide_one_input_file_divs()
        self.div_rotate.pack(pady=20)
        self.div_rotate_centre.pack()
        self.div_rotate_gauche.pack(side=LEFT)
        self.label_rotate.pack()
        self.div_radiobutton.pack(side=LEFT)

        self.div_radiobutton_left.pack(anchor="w")
        self.div_radiobutton_right.pack(anchor="w")
        self.div_radiobutton_180.pack(anchor="w")
        self.div_radiobutton_gauche_droite.pack(anchor="w")
        self.div_radiobutton_haut_bas.pack(anchor="w")

        self.radiobutton_left.pack(side=LEFT)
        self.radiobutton_right.pack(side=LEFT)
        self.radiobutton_180.pack(side=LEFT)
        self.radiobutton_gauche_droite.pack(side=LEFT)
        self.radiobutton_haut_bas.pack(side=LEFT)

        self.label_radiobutton_left.pack(side=LEFT)
        self.label_radiobutton_right.pack(side=LEFT)
        self.label_radiobutton_180.pack(side=LEFT)
        self.label_radiobutton_gauche_droite.pack(side=LEFT)
        self.label_radiobutton_haut_bas.pack(side=LEFT)

        self.btn_go.pack(side=BOTTOM, pady=10)

    def hide(self):
        self.div_rotate.pack_forget()

    def execute(self):

        if not check_path_entries_correct():
            return

        path, input_file, output_file = get_main_paths()

        if not input_file_exist(input_file):
            return

        rotation_var = self.rotate_value.get()

        cmd_line = MediaObject(input_path=input_file, output_path=output_file).rotate(rotation=rotation_var)
        run_cmd_line(cmd_line, output_file)


class Cut:

    def __init__(self):
        self.div_cut = div_cut
        self.label_cut = Label(div_cut, text="Sauvegarder (couper l'excédent) :", font=bold_font)
        self.div_haut = Frame(div_cut)

        self.label_pre1 = Label(self.div_haut, text="de")

        self.entryhour1 = Entry(self.div_haut, width=2)
        self.entryhour1.insert(0, "00")
        self.label_h1 = Label(self.div_haut, text="h ")

        self.entryminute1 = Entry(self.div_haut, width=2)
        self.entryminute1.insert(0, "00")
        self.label_m1 = Label(self.div_haut, text="m ")

        self.entrysecond1 = Entry(self.div_haut, width=2)
        self.entrysecond1.insert(0, "00")
        self.label_s1 = Label(self.div_haut, text="s")

        self.label_error1 = Label(self.div_haut, text="Mauvaise valeur (format accepté : \"..H..M..S\")", fg="red")


        self.div_bas = Frame(div_cut)

        self.label_pre2 = Label(self.div_bas, text="à")

        self.entryhour2 = Entry(self.div_bas, width=2)
        self.entryhour2.insert(0, "00")
        self.label_h2 = Label(self.div_bas, text="h ")

        self.entryminute2 = Entry(self.div_bas, width=2)
        self.entryminute2.insert(0, "00")
        self.label_m2 = Label(self.div_bas, text="m ")

        self.entrysecond2 = Entry(self.div_bas, width=2)
        self.entrysecond2.insert(0, "30")
        self.label_s2 = Label(self.div_bas, text="s")

        self.label_error2 = Label(self.div_bas, text="Mauvaise valeur (format accepté : \"..H..M..S\")", fg="red")

        self.btn_go = Button(div_cut, text="=>GO", command=self.execute)

    def show(self):
        hide_one_input_file_divs()
        self.div_cut.pack(pady=20)
        self.label_cut.pack(pady=10)

        self.div_haut.pack(pady=10)
        self.label_pre1.pack(side=LEFT, padx=10)
        self.entryhour1.pack(side=LEFT)
        self.label_h1.pack(side=LEFT)
        self.entryminute1.pack(side=LEFT)
        self.label_m1.pack(side=LEFT)
        self.entrysecond1.pack(side=LEFT)
        self.label_s1.pack(side=LEFT)

        self.div_bas.pack(pady=10)
        self.label_pre2.pack(side=LEFT, padx=10)
        self.entryhour2.pack(side=LEFT)
        self.label_h2.pack(side=LEFT)
        self.entryminute2.pack(side=LEFT)
        self.label_m2.pack(side=LEFT)
        self.entrysecond2.pack(side=LEFT)
        self.label_s2.pack(side=LEFT)

        self.btn_go.pack(side=BOTTOM, pady=10)

    def hide(self):
        self.div_cut.pack_forget()

    def execute(self):

        if not check_path_entries_correct():
            return

        path, input_file, output_file = get_main_paths()

        if not input_file_exist(input_file):
            return

        hour1 = self.entryhour1.get()
        minute1 = self.entryminute1.get()
        second1 = self.entrysecond1.get()
        hour2= self.entryhour2.get()
        minute2 = self.entryminute2.get()
        second2 = self.entrysecond2.get()


        errors = False
        if (len(hour1 + minute1 + second1) != 6) or not((hour1 + minute1 + second1).isdigit()):
            errors = True
            self.label_error1.pack(side=LEFT)
        if (len(hour2 + minute2 + second2) != 6) or not((hour2 + minute2 + second2).isdigit()):
            errors = True
            self.label_error2.pack(side=LEFT)
        if errors:
            return

        self.label_error1.pack_forget()
        self.label_error2.pack_forget()


        begin = f"{hour1}:{minute1}:{second1}"
        end = f"{hour2}:{minute2}:{second2}"


        cmd_line = MediaObject(input_path=input_file, output_path=output_file).cut_duration(begin=begin, end=end)
        run_cmd_line(cmd_line, output_file)


class Crop:

    def __init__(self):
        self.div_crop = div_crop
        self.label_crop = Label(self.div_crop, text="Rogner :", font=bold_font)
        self.div_position = Frame(self.div_crop)

        self.div_position_gauche = Frame(self.div_position)
        self.label_position = Label(self.div_position_gauche, text="position :")

        self.div_position_droite = Frame(self.div_position)

        self.div_position_droite_haut = Frame(self.div_position_droite)
        self.label_x = Label(self.div_position_droite_haut, text="x = ")
        self.entry_x = Entry(self.div_position_droite_haut, width=4)
        self.entry_x.insert(0, "0")
        self.label_error_x = Label(self.div_position_droite_haut, text="Entrez une valeur correcte", fg="red")

        self.div_position_droite_bas = Frame(self.div_position_droite)
        self.label_y = Label(self.div_position_droite_bas, text="y = ")
        self.entry_y = Entry(self.div_position_droite_bas, width=4)
        self.entry_y.insert(0, "0")
        self.label_error_y = Label(self.div_position_droite_bas, text="Entrez une valeur correcte", fg="red")


        self.div_dimensions = Frame(self.div_crop)

        self.div_dimensions_gauche = Frame(self.div_dimensions)
        self.label_dimensions = Label(self.div_dimensions_gauche, text="dimensions :")

        self.div_dimensions_droite = Frame(self.div_dimensions)

        self.div_dimensions_droite_haut = Frame(self.div_dimensions_droite)
        self.label_largeur = Label(self.div_dimensions_droite_haut, text="largeur = ")
        self.entry_largeur = Entry(self.div_dimensions_droite_haut, width=4)
        self.entry_largeur.insert(0, "100")
        self.label_error_largeur = Label(self.div_dimensions_droite_haut, text="Entrez une valeur correcte",
                                            fg="red")

        self.div_dimensions_droite_bas = Frame(self.div_dimensions_droite)
        self.label_hauteur = Label(self.div_dimensions_droite_bas, text="hauteur = ")
        self.entry_hauteur = Entry(self.div_dimensions_droite_bas, width=4)
        self.entry_hauteur.insert(0, "100")
        self.label_error_hauteur = Label(self.div_dimensions_droite_bas, text="Entrez une valeur correcte",
                                            fg="red")

        self.btn_go = Button(div_crop, text="=>GO", command=self.execute)

    def show(self):
        hide_one_input_file_divs()
        self.div_crop.pack(pady=20)
        self.label_crop.pack()
        self.div_position.pack(pady=10)
        self.div_position_gauche.pack(side=LEFT)
        self.label_position.pack(padx=10)

        self.div_position_droite.pack(side=LEFT)

        self.div_position_droite_haut.pack(pady=5)
        self.label_x.pack(side=LEFT)
        self.entry_x.pack(side=LEFT)

        self.div_position_droite_bas.pack(pady=5)
        self.label_y.pack(side=LEFT)
        self.entry_y.pack(side=LEFT)

        self.div_dimensions.pack(pady=10)
        self.div_dimensions_gauche.pack(side=LEFT)
        self.label_dimensions.pack(padx=10)

        self.div_dimensions_droite.pack(side=LEFT)

        self.div_dimensions_droite_haut.pack(pady=5)
        self.label_largeur.pack(side=LEFT)
        self.entry_largeur.pack(side=LEFT)

        self.div_dimensions_droite_bas.pack(pady=5)
        self.label_hauteur.pack(side=LEFT)
        self.entry_hauteur.pack(side=LEFT)

        self.btn_go.pack(side=BOTTOM, pady=10)

    def hide(self):
        self.div_crop.pack_forget()

    def execute(self):

        if not check_path_entries_correct():
            return

        path, input_file, output_file = get_main_paths()

        if not input_file_exist(input_file):
            return

        x = self.entry_x.get()
        y = self.entry_y.get()
        largeur = self.entry_largeur.get()
        hauteur = self.entry_hauteur.get()

        # Checke la validité des entrys
        crop_entry_errors = False
        if x == "" or x.isspace():
            crop_entry_errors = True
            self.label_error_x.pack(side=LEFT)
        if y == "" or y.isspace():
            crop_entry_errors = True
            self.label_error_y.pack(side=LEFT)
        if largeur == "" or largeur.isspace():
            crop_entry_errors = True
            self.label_error_largeur.pack(side=LEFT)
        if hauteur == "" or hauteur.isspace():
            crop_entry_errors = True
            self.label_error_hauteur.pack(side=LEFT)

        if crop_entry_errors:
            return

        self.label_error_x.pack_forget()
        self.label_error_y.pack_forget()
        self.label_error_largeur.pack_forget()
        self.label_error_hauteur.pack_forget()

        cmd_line = MediaObject(input_path=input_file, output_path=output_file).crop(width=largeur, height=hauteur, x=x, y=y)
        run_cmd_line(cmd_line, output_file)



def hide_all_multiple_inputs_divs():
    div_concatenate.pack_forget()

class Concatenate:
    def __init__(self):
        self.div_concatenate = div_concatenate
        self.label_compress = Label(self.div_concatenate, text="Concatener : ", font=bold_font)

        self.label_tuto = Label(self.div_concatenate, text=f"Format du nom de fichier d'entrée :\n"
                                                              f"\"image001.jpeg\" -> \"image%01d.jpeg\"")

        self.div_choice = Frame(div_concatenate)

        self.label_choice = Label(self.div_choice, text="Concatener : ")

        self.concatenate_type = StringVar()
        self.concatenate_type.set("image")

        self.div_radiobuttons = Frame(self.div_choice)
        self.div_radiobuttons_image = Frame(self.div_radiobuttons)
        self.radiobutton_image = Radiobutton(self.div_radiobuttons_image, variable=self.concatenate_type,
                                                value="image", command=self.show_framerate_quality)
        self.label_radiobutton_image = Label(self.div_radiobuttons_image, text="image")

        self.div_radiobuttons_video = Frame(self.div_radiobuttons)
        self.radiobutton_video = Radiobutton(self.div_radiobuttons_video, variable=self.concatenate_type,
                                                value="video", command=self.hide_framerate_quality)
        self.label_radiobutton_video = Label(self.div_radiobuttons_video, text="vidéos")


        self.div_framerate = Frame(self.div_concatenate)
        self.label_framerate = Label(self.div_framerate, text="framerate : ")
        self.entry_framerate = Entry(self.div_framerate, width=3)
        self.entry_framerate.insert(0, "30")
        self.label_error_framerate = Label(self.div_framerate, text="Veuillez entrer un framerate correct", fg="red")

        self.div_slider = Frame(self.div_concatenate)
        self.label_qualite = Label(self.div_slider, text="Compression :")
        self.slider_quality = Scale(self.div_slider, from_=0, to=100, orient='horizontal')

        self.btn_go = Button(self.div_concatenate, text="=>GO", command=self.execute)

    def hide_framerate_quality(self):
        self.div_framerate.pack_forget()
        self.div_slider.pack_forget()
        self.label_tuto["text"] = f"Format du nom de fichier d'entrée : \"videos.txt\"\n" \
                                  f"Disposition dans le fichier : \n\n" \
                                  f"file video1.mp4\n" \
                                  f"file video2.mp4\n" \
                                  f"file video3.mp4\n" \
                                  f"...\n"

    def show_framerate_quality(self):
        self.div_framerate.pack()
        self.div_slider.pack()
        self.label_tuto["text"] = f"Format du nom de fichier d'entrée :\n" \
                                  f"\"image001.jpeg\" -> \"image%01d.jpeg\""

    def show(self):
        hide_all_multiple_inputs_divs()
        self.div_concatenate.pack(pady=20)
        self.label_compress.pack()

        self.label_tuto.pack(pady=10)

        self.div_choice.pack(pady=10)
        self.label_choice.pack(side=LEFT)

        self.div_radiobuttons.pack(side=LEFT)

        self.div_radiobuttons_image.pack()
        self.radiobutton_image.pack(side=LEFT)
        self.label_radiobutton_image.pack(side=LEFT)

        self.div_radiobuttons_video.pack()
        self.radiobutton_video.pack(side=LEFT)
        self.label_radiobutton_video.pack(side=LEFT)


        self.div_framerate.pack(pady=10)
        self.label_framerate.pack(side=LEFT)
        self.entry_framerate.pack(side=LEFT)

        self.div_slider.pack()
        self.label_qualite.pack(side=LEFT)
        self.slider_quality.pack(side=LEFT)

        self.btn_go.pack(side=BOTTOM, pady=10)

    def hide(self):
        self.div_concatenate.pack_forget()

    def execute(self):

        quality = self.slider_quality.get()
        framerate = self.entry_framerate.get()
        errors = False

        if not check_path_entries_correct():
            errors = True

        if framerate == "" or framerate[0] == " " or framerate.isspace() or not(framerate.isdigit()):
            self.label_error_framerate.pack(side=LEFT, padx=5)
            errors = True

        if errors:
            return

        self.label_error_framerate.pack_forget()

        path, input_file, output_file = get_main_paths()

        if self.concatenate_type.get() == "image":
            cmd_command = FilesInput(input_path=input_file, output_path=output_file)\
                .concatenate_images(framerate=framerate, quality=str(quality))
        else:
            cmd_command = FilesInput(input_path=input_file, output_path=output_file).concatenate_videos()

        run_cmd_line(cmd_command, output_file)







fen  = Tk()
fen.title("ffmpeg-python")
bold_font = font.Font(family="Arial", size=10, weight="bold")
div_main = Frame(fen)
div_main.pack(padx=20, pady=20)
div_boutons_1 = Frame(div_main)
div_boutons_1.pack()

def show_div_x_entries():
    div_one_file.pack_forget()
    div_multiple_inputs.pack()

def show_div_one_file():
    div_multiple_inputs.pack_forget()
    div_one_file.pack()

def chercher_repertoire() -> None:
    text = filedialog.askdirectory() + "/"
    if text == "":  # Parfois un bug où la recherche renvoie un string vide
        text = str(Path.home() / "Downloads")
    entry_input_path.delete(0, END)
    entry_input_path.insert(0, text)


btn_one_file = Button(div_boutons_1, text="1 fichier", command=show_div_one_file)
btn_one_file.pack(side=LEFT, padx=2)
btn_x_entries = Button(div_boutons_1, text="plusieurs fichiers", command=show_div_x_entries)
btn_x_entries.pack(side=LEFT, padx=2)



div_entries = Frame(div_main)
div_entries.pack(pady=20)
div_entry_input_path = Frame(div_entries)
div_entry_input_path.pack()
label_entry_input_path = Label(div_entry_input_path, text="Chemin : ")
label_entry_input_path.pack(side=LEFT)
entry_input_path = Entry(div_entry_input_path, width=30)
entry_input_path.insert(0, r"C:/Users/Eleve/ffmpeg_python/")
entry_input_path.pack(side=LEFT)
btn_chercher_chemin = Button(div_entry_input_path, text="Chercher", command=chercher_repertoire)
btn_chercher_chemin.pack(side=LEFT, padx=5)
label_error_path = Label(div_entry_input_path, text="Veuillez renseigner ce champ", fg="red")

div_entry_input_file = Frame(div_entries)
div_entry_input_file.pack(pady=5)
label_entry_input_file = Label(div_entry_input_file, text="Fichier d'entrée : ")
label_entry_input_file.pack(side=LEFT)
entry_input_file_name = Entry(div_entry_input_file, width=10)
entry_input_file_name.insert(0, "in")
entry_input_file_name.pack(side=LEFT)
entry_input_file_ext = Entry(div_entry_input_file, width=8)
entry_input_file_ext.insert(0, ".mp4")
entry_input_file_ext.pack(side=LEFT)
label_error_input_file = Label(div_entry_input_file, text="Veuillez renseigner ce champ", fg="red")

div_entry_output_file = Frame(div_entries)
div_entry_output_file.pack(pady=5)
label_entry_output_file = Label(div_entry_output_file, text="Fichier de sortie : ")
label_entry_output_file.pack(side=LEFT)
entry_output_file_name = Entry(div_entry_output_file, width=10)
entry_output_file_name.pack(side=LEFT)
entry_output_file_name.insert(0, "out")
entry_output_file_ext = Entry(div_entry_output_file, width=8)
entry_output_file_ext.insert(0, ".mp4")
entry_output_file_ext.pack(side=LEFT)
label_error_output_file = Label(div_entry_output_file, text="Veuillez renseigner ce champ", fg="red")


div_one_file = Frame(div_main)
div_one_file.pack()

div_compress = Frame(div_one_file)
div_convert = Frame(div_one_file)
div_extract = Frame(div_one_file)
div_rotate = Frame(div_one_file)
div_cut = Frame(div_one_file)
div_crop = Frame(div_one_file)

div_boutons_one_file_input = Frame(div_one_file)
div_boutons_one_file_input.pack()
btn_compress = Button(div_boutons_one_file_input, text="Compresser", command=Compress().show)
btn_compress.pack(side=LEFT)
btn_convert = Button(div_boutons_one_file_input, text="Convertir", command=Convert().show)
btn_convert.pack(side=LEFT, padx=3)
btn_extract = Button(div_boutons_one_file_input, text="Extraire", command=Extract().show)
btn_extract.pack(side=LEFT, padx=3)
btn_rotate = Button(div_boutons_one_file_input, text="Pivoter", command=Rotate().show)
btn_rotate.pack(side=LEFT, padx=3)
btn_cut = Button(div_boutons_one_file_input, text="Couper", command=Cut().show)
btn_cut.pack(side=LEFT, padx=3)
btn_crop = Button(div_boutons_one_file_input, text="Rogner", command=Crop().show)
btn_crop.pack(side=LEFT, padx=3)




div_multiple_inputs = Frame(div_main) # étant invisible au démarrage, on ne la pack pas

div_concatenate = Frame(div_multiple_inputs)

div_btns_multiple_file_input = Frame(div_multiple_inputs)
div_btns_multiple_file_input.pack()
btn_concatenate = Button(div_btns_multiple_file_input, text="Concatener", command=Concatenate().show)
btn_concatenate.pack(side=LEFT, padx=5)




label_conversion_en_cours = Label(div_main, text="Action en cours (voir cmd pour précisions)", font=bold_font)

fen.mainloop()

"""
# ajouter changement de couleur aussi
# ajouter carré qui bouge quand rotaté

# ajouter transfos audio (disto/chorus/flanger)
"""