"""
Лабораторная 9 Вариант 9
Написать GUI приложение, которое представляет собой книгу заметок, позволяющую создавать новые заметки, редактировать
и удалять существующие. Приложение позволяет создавать группы заметок и выполнять сортировку по дате.
"""

import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class Note:
    def __init__(self, title, content):
        self.title = title
        self.content = content
        self.creation_date = datetime.now()
        self.group = None

class NoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Книга заметок")

        self.notes = []
        self.current_note = None

        self.title_label = tk.Label(root, text="Заголовок:")
        self.title_label.pack()

        self.title_entry = tk.Entry(root)
        self.title_entry.pack()

        self.content_label = tk.Label(root, text="Содержание:")
        self.content_label.pack()

        self.content_text = tk.Text(root)
        self.content_text.pack()

        self.save_button = tk.Button(root, text="Сохранить", command=self.save_note)
        self.save_button.pack()

        self.note_listbox = tk.Listbox(root)
        self.note_listbox.pack()

        self.edit_button = tk.Button(root, text="Редактировать", command=self.edit_note)
        self.edit_button.pack()

        self.delete_button = tk.Button(root, text="Удалить", command=self.delete_note)
        self.delete_button.pack()

        self.group_label = tk.Label(root, text="Группа:")
        self.group_label.pack()

        self.group_entry = tk.Entry(root)
        self.group_entry.pack()

        self.group_button = tk.Button(root, text="Создать группу", command=self.create_group)
        self.group_button.pack()

        self.sort_button = tk.Button(root, text="Сортировать по дате", command=self.sort_notes)
        self.sort_button.pack()

        self.load_notes()

    def save_note(self):
        title = self.title_entry.get()
        content = self.content_text.get("1.0", "end-1c")

        if not title or not content:
            messagebox.showerror("Ошибка", "Заголовок и содержание не могут быть пустыми.")
            return

        if self.current_note is None:
            self.notes.append(Note(title, content))
        else:
            self.current_note.title = title
            self.current_note.content = content
            self.current_note.creation_date = datetime.now()
            self.current_note = None

        self.clear_fields()
        self.update_note_listbox()
        self.save_notes()

    def edit_note(self):
        selected_index = self.note_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            self.current_note = self.notes[index]
            self.title_entry.delete(0, "end")
            self.title_entry.insert(0, self.current_note.title)
            self.content_text.delete("1.0", "end")
            self.content_text.insert("1.0", self.current_note.content)

    def delete_note(self):
        selected_index = self.note_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            del self.notes[index]
            self.clear_fields()
            self.update_note_listbox()
            self.save_notes()

    def create_group(self):
        group_name = self.group_entry.get()
        if group_name:
            selected_indices = self.note_listbox.curselection()
            if selected_indices:
                for index in selected_indices:
                    self.notes[index].group = group_name
                self.save_notes()

    def sort_notes(self):
        self.notes.sort(key=lambda x: x.creation_date)
        self.update_note_listbox()

    def clear_fields(self):
        self.title_entry.delete(0, "end")
        self.content_text.delete("1.0", "end")

    def update_note_listbox(self):
        self.note_listbox.delete(0, "end")
        for note in self.notes:
            self.note_listbox.insert("end", note.title)

    def save_notes(self):
        with open("notes.txt", "w") as file:
            for note in self.notes:
                file.write(f"{note.title}\n{note.content}\n{note.creation_date}\n{note.group}\n")

    def load_notes(self):
        try:
            with open("notes.txt", "r") as file:
                lines = file.readlines()
                for i in range(0, len(lines), 4):
                    title = lines[i].strip()
                    content = lines[i + 1].strip()
                    date_str = lines[i + 2].strip()
                    date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f")
                    group = lines[i + 3].strip()
                    note = Note(title, content)
                    note.creation_date = date
                    note.group = group
                    self.notes.append(note)
                self.update_note_listbox()
        except FileNotFoundError:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = NoteApp(root)
    root.mainloop()