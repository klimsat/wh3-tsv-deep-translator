import os
import time
from tkinter import Tk, Button, Label, Frame
from tkinter.filedialog import askdirectory
from deep_translator import GoogleTranslator
import customtkinter

def select_directory(event=None):
    directory = askdirectory()
    directory_label.config(text=directory if directory else "Папка ещё не выбрана")

def start_translation(event=None):
    directory = directory_label.cget("text")
    if not directory or directory == "Папка ещё не выбрана":
        return

    tsv_files = [filename for filename in os.listdir(directory) if filename.endswith('.tsv')]
    total_files = len(tsv_files)
    total_lines = 0
    for filename in tsv_files:
        with open(os.path.join(directory, filename), 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if i < 2 or line.startswith('\t'):
                    continue
                total_lines += 1

    file_label.config(text=f'Всего файлов для перевода: {total_files}')
    line_label.config(text=f'Всего строк для перевода: {total_lines}')

    translated_lines = 0
    for i, filename in enumerate(tsv_files):
        progress_label.config(text=f'Обрабатывается файл {i+1} из {total_files}: {filename}')
        with open(os.path.join(directory, filename), 'r', encoding='utf-8') as f:
            lines = f.readlines()
            newline = '\n' if '\r\n' not in lines else '\r\n'
        new_lines = []
        for j, line in enumerate(lines):
            if j < 2:
                new_lines.append(line)
                continue
            if line.startswith('\t'):
                new_lines[-1] = new_lines[-1].rstrip() + '\ttrue' + newline
                continue
            parts = line.split('\t')
            if len(parts) < 2:
                new_lines.append(line)
                continue
            text_to_translate = parts[1]
            translated_text = translator.translate(text_to_translate)
            if len(parts) == 3 and parts[2].strip() in ['true', 'false']:
                new_line = f'{parts[0]}\t{translated_text}\t{parts[2]}'
                new_lines.append(new_line)
            else:
                new_line = f'{parts[0]}\t{translated_text}{newline}'
                new_lines.append(new_line)
            translated_lines += 1
            progress = round(translated_lines / total_lines * 100, 2)
            line_label.config(text=f'Перевод строки {j+1} из {len(lines)}. Общий прогресс: {progress}%')
            root.update()
        with open(os.path.join(directory, filename), 'w', encoding='utf-8', newline=newline) as f:
            f.writelines(new_lines)

    progress_label.config(text='Перевод завершен! Используйте RPFM для импорта переведенных строк в ваши таблицы.')
    line_label.config(text=f'Всего переведено {translated_lines} строк. Общий прогресс: {progress}%') # Отображение общего количества переведенных строк

translator = GoogleTranslator(source='en', target='ru')

customtkinter.set_appearance_mode("light") # Режимы: system (по умолчанию), light, dark
customtkinter.set_default_color_theme("dark-blue") # Темы: blue (по умолчанию), dark-blue, green

root = customtkinter.CTk()
root.title("Переводчик .tsv файлов для Total War: Warhammer III")

main_frame = Frame(root)
main_frame.pack(padx=25, pady=25) # Установка отступов в 25 пикселей со всех сторон

frame1 = Frame(main_frame)
frame1.pack(pady=5)

select_label = Label(frame1, text="Выберите папку, в которой находятся .tsv файлы для перевода")
select_label.pack(side="left")

select_button = customtkinter.CTkButton(frame1, text="Обзор")
select_button.pack(side="right")
select_button.bind("<ButtonRelease-1>", select_directory)

directory_label = Label(main_frame, text="Папка ещё не выбрана")
directory_label.pack()

start_button = customtkinter.CTkButton(main_frame, text="Начать перевод")
start_button.pack(pady=15)
start_button.bind("<ButtonRelease-1>", start_translation)

file_label = Label(main_frame)
file_label.pack()

line_label = Label(main_frame)
line_label.pack()

progress_label = Label(main_frame)
progress_label.pack()

root.mainloop()
