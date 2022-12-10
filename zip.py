""" mobin zip application. """
from getpass import getuser
from os import path, walk, getcwd, mkdir
from sys import argv
from tkinter import Entry, StringVar, Tk
from tkinter.ttk import Button, Label, Style
from zipfile import ZIP_DEFLATED
from subprocess import getoutput
from tkinter.filedialog import askopenfilename, askdirectory
from tkinter.messagebox import showinfo
from zipfile import ZipFile
from pathlib import Path
from colorama import Fore as F


def application_help():
    """ help function [--help] """
    text = f"""
{F.BLUE}Welcome{F.RESET} {F.LIGHTBLUE_EX}to my{F.RESET} {F.BLUE}Z{F.RED}i{F.GREEN}p{F.RESET} {F.YELLOW}Application{F.RESET} {F.GREEN}{getuser()}{F.RESET} {F.LIGHTBLACK_EX}:){F.RESET} 

{F.LIGHTGREEN_EX}To extract a file{F.RESET}:
    {F.RED}zip filename.zip path_to_extract{F.RESET}
    
{F.LIGHTGREEN_EX}To zip a folder{F.RESET}:
    {F.RED}zip folder_to_zip filename.zip{F.RESET}

{F.LIGHTGREEN_EX}To use gui mode type{F.RESET}:
    {F.RED}zip --gui{F.RESET}
    {F.LIGHTBLACK_EX}or{F.RESET}
    {F.RED}zip --window{F.RESET}
""".strip()
    print(text)


def get_all_file_paths(directory):
    """ get the path of files """
    file_paths = []
    for root, directories, files in walk(directory):
        for filename in files:
            filepath = path.join(root, filename)
            file_paths.append(filepath)
    return file_paths


def zip_file_cli(foldername: str, zip_file_name: str):
    """ zip a file with this function """
    try:
        file_paths = get_all_file_paths(foldername)
        with ZipFile(zip_file_name, 'a') as zFile:
            for file in file_paths:
                zFile.write(file)
        print(
            f'[{F.GREEN}√{F.RESET}] folder {F.LIGHTGREEN_EX}{foldername}{F.RESET} was successfully zipped into'
            f' {F.CYAN}{zip_file_name}{F.RESET}!')
    except Exception as e:
        print(f'{F.LIGHTRED_EX}There was an error while zipping a folder{F.RESET} [{F.RED}{e}{F.RESET}]')


def extract_cli(zip_file_name: str, extract_folder: str):
    """ extract a zip file with this function """
    try:
        if path.exists(extract_folder):
            extract_folder += '1'
        else:
            mkdir(extract_folder)
        with ZipFile(zip_file_name) as zFile:
            zFile.extractall(extract_folder)
        print(
            f'[{F.GREEN}√{F.RESET}] file {F.CYAN}{zip_file_name}{F.RESET} was successfully extracted to '
            f'{F.LIGHTGREEN_EX}{extract_folder}{F.RESET}!')
    except Exception as e:
        print(f"{F.LIGHTRED_EX}There was an error while extracting{F.RESET} [{F.RED}{e}{F.RESET}]")


class StartGui:
    """ start GUI window. """

    def __init__(self):
        root = Tk()
        style = Style(root)
        style.theme_use('clam')
        style.configure('Fun.TButton', font=('arial', 16))
        root.title('Zip Application')
        root.config(background='white')
        Label(text=f'Welcome to \nMobin Zip Application \n{getuser()}', font=('arial', 22),
              background='white').pack()
        Button(root, style='Fun.TButton', text='extract', command=self.extract_gui).pack()
        Button(root, text='zip', style='Fun.TButton', command=self.zip_file_gui).pack(pady=20)
        root.mainloop()

    def extract_gui(self):
        """ initialize application extract GUI """
        root = Tk()
        root.title('extract')
        root.config(background='white')
        root.geometry('350x300')
        root.attributes("-topmost", True)
        self.var_input_zip = StringVar(root)
        self.var_input_folder = StringVar(root)
        style = Style(root)
        style.theme_use('clam')
        self.input_file_zip = Entry(root, textvariable=self.var_input_zip, font=('arial', 18), state='readonly')
        self.input_extract_folder = Entry(root, textvariable=self.var_input_folder, font=('arial', 18),
                                          state='readonly')
        self.btn_select_zip_file = Button(root, text='...', width=3, command=self.select_zip_file_dialog)
        self.btn_select_extract_folder = Button(root, text='...', width=3, command=self.select_extract_folder_dialog)
        self.input_file_zip.grid(column=0, row=0, padx=5, pady=5)
        self.input_extract_folder.grid(column=0, row=1, padx=5, pady=5)
        self.btn_select_zip_file.grid(column=1, row=0, padx=5, pady=5)
        self.btn_select_extract_folder.grid(column=1, row=1, padx=5, pady=5)
        self.submit_btn = Button(root, text='extract', command=self.submit_extract)
        self.submit_btn.grid(column=0, row=2)
        self.var_input_zip.set('choose zip file...')
        self.var_input_folder.set('choose extract folder...')

    def select_zip_file_dialog(self):
        """ select zip file dialog!. """
        a = askopenfilename(filetypes=[("Zip files", "*.zip")])
        self.var_input_zip.set(a)

    def submit_extract(self):
        """ submit and extract the zip file. """
        if self.var_input_zip.get() != 'choose zip file...' and \
                self.var_input_folder.get() != 'choose extract folder...':
            try:
                with ZipFile(self.var_input_zip.get()) as file:
                    file.extractall(self.var_input_folder.get())
                showinfo('Success',
                         f'File {self.var_input_zip.get()} was successfully extracted to {self.var_input_folder.get()}')
                getoutput(f'cd {self.var_input_folder.get()} && explorer.exe .')

            except:
                pass

    def select_extract_folder_dialog(self):
        """ asc for extract directory. """
        a = askdirectory()
        self.var_input_folder.set(a)

    def zip_file_gui(self):
        """ initialize application zip GUI. """
        root = Tk()
        root.title('zip')
        root.config(background='white')
        root.geometry('350x300')
        root.attributes("-topmost", True)
        self.var_input_folder_to_zip = StringVar(root)
        self.var_input_folder_to_save = StringVar(root)
        self.var_name_zip_file = StringVar(root)
        style = Style(root)
        style.theme_use('clam')
        self.input_folder_to_zip = Entry(root, textvariable=self.var_input_folder_to_zip, font=('arial', 18),
                                         state='readonly')
        self.input_folder_to_save = Entry(root, textvariable=self.var_input_folder_to_save, font=('arial', 18),
                                          state='readonly')
        self.input_name_zip_file = Entry(root, textvariable=self.var_name_zip_file, font=('arial', 12))
        self.btn_select_folder_to_zip = Button(root, text='...', width=3, command=self.select_folder_to_zip_dialog)
        self.btn_select_folder_to_save = Button(root, text='...', width=3, command=self.select_folder_to_save_dialog)
        self.input_folder_to_zip.grid(column=0, row=0, padx=5, pady=5)
        self.input_folder_to_save.grid(column=0, row=1, padx=5, pady=5)
        self.btn_select_folder_to_zip.grid(column=1, row=0, padx=5, pady=5)
        self.btn_select_folder_to_save.grid(column=1, row=1, padx=5, pady=5)
        self.submit_btn_zip = Button(root, text='zip', command=self.submit_zip)
        self.submit_btn_zip.grid(column=0, row=3)
        self.input_name_zip_file.grid(column=0, row=2, padx=5, pady=5)
        self.var_input_folder_to_zip.set('choose folder to zip...')
        self.var_input_folder_to_save.set('choose save folder...')
        self.var_name_zip_file.set('name of the zip file...')

    def select_folder_to_zip_dialog(self):
        """ just asc for directory to zip. """
        a = askdirectory()
        self.var_input_folder_to_zip.set(a)

    def select_folder_to_save_dialog(self):
        """ just asc for directory to save. """
        a = askdirectory()
        self.var_input_folder_to_save.set(a)

    def submit_zip(self):
        """ submit and zip the following folder. """
        if self.var_input_folder_to_zip.get() != 'choose folder to zip...' \
                and self.var_input_folder_to_save.get() != 'choose save folder...':
            try:
                file_paths = get_all_file_paths(Path(self.var_input_folder_to_zip.get()).name)
                with ZipFile(
                        f'{self.var_input_folder_to_save.get()}/{self.var_name_zip_file.get() if self.var_name_zip_file.get() and self.var_name_zip_file.get() != "name of the zip file..." else "test"}.zip',
                        'a', compression=ZIP_DEFLATED,
                        compresslevel=9) as f:
                    for file in file_paths:
                        f.write(file)
                showinfo('Success',
                         f'contents of {self.var_input_folder_to_zip.get()} was zipped in'
                         f' {self.var_input_folder_to_save.get()}.zip')
                getoutput(f'cd {self.var_input_folder_to_save.get()} && explorer.exe .')
            except:
                pass


def main():
    """ main function """
    if argv[1:]:
        try:
            if argv[2:]:
                # -zip file
                # get the folder to zip and the zip file name
                if argv[1:][0] and argv[1:][1].endswith('.zip'):
                    zip_file_cli(argv[1:][0], argv[1:][1])
                # -unzip
                # get a zip file and get the folder to unzip
                elif argv[1:][0].endswith('.zip') and argv[1:][1]:
                    extract_cli(argv[1:][0], argv[1:][1])
            elif argv[1:][0] == '--gui' or argv[1:][0] == '--window':
                StartGui()
            elif argv[1:][0] == "--help":
                application_help()
        except:
            pass
    else:
        application_help()


if __name__ == '__main__':
    main()
