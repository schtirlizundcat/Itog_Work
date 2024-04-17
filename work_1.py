import json
import csv
from datetime import datetime

class Note:
    def __init__(self, title, message, creation_time=None):
        self.title = title
        self.message = message
        self.creation_time = creation_time or datetime.now()

    def to_dict(self):
        return {
            "title": self.title,
            "message": self.message,
            "creation_time": self.creation_time.isoformat()
        }

class NoteManager:
    def __init__(self, storage_format="json"):
        self.storage_format = storage_format
        self.data = []
        self.load_data()

    def load_data(self):
        if self.storage_format == "json":
            try:
                with open("notes.json", "r") as f:
                    self.data = json.load(f)
            except FileNotFoundError:
                pass
        elif self.storage_format == "csv":
            try:
                with open("notes.csv", "r") as f:
                    reader = csv.DictReader(f, delimiter=";")
                    self.data = [Note(row["title"], row["message"], datetime.fromisoformat(row["creation_time"])) for row in reader]
            except FileNotFoundError:
                pass

    def save_data(self):
        if self.storage_format == "json":
            with open("notes.json", "w") as f:
                json.dump([note.to_dict() for note in self.data], f)
        elif self.storage_format == "csv":
            with open("notes.csv", "w", newline="") as f:
                fieldnames = ["title", "message", "creation_time"]
                writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
                writer.writeheader()
                for note in self.data:
                    writer.writerow({
                        "title": note.title,
                        "message": note.message,
                        "creation_time": note.creation_time.isoformat()
                    })

    def add_note(self, title, message):
        new_note = Note(title, message)
        self.data.append(new_note)
        self.save_data()

    def show_notes(self, filter_date=None):
        filtered_data = self.data
        if filter_date:
            filtered_data = [note for note in self.data if abs((note.creation_time - filter_date).days) <= 1]
        for note in filtered_data:
            print(f"{note.title} - {note.creation_time.date()}")

    def edit_note(self, title, new_message):
        for note in self.data:
            if note.title == title:
                note.message = new_message
                self.save_data()
                break

    def delete_note(self, title):
        self.data = [note for note in self.data if note.title != title]
        self.save_data()

if __name__ == "__main__":
    manager = NoteManager()
    while True:
        action = input("Введите команду (add/show/edit/delete/exit): ")
        if action == "add":
            title = input("Введите заголовок заметки: ")
            message = input("Введите тело заметки: ")
            manager.add_note(title, message)
        elif action == "show":
            filter_date_str = input("Введите дату для фильтрации (YYYY-MM-DD, для просмотра всех заметок оставьте пустым): ")
            filter_date = datetime.strptime(filter_date_str, "%Y-%m-%d") if filter_date_str else None
            manager.show_notes(filter_date)
        elif action == "edit":
            title = input("Введите заголовок заметки для редактирования: ")
            message = input("Введите новое тело заметки: ")
            manager.edit_note(title, message)
        elif action == "delete":
            title = input("Введите заголовок заметки для удаления: ")
            manager.delete_note(title)
        elif action == "exit":
            break
        else:
            print("Неизвестная команда")