import os
import json


def print_with_indent(value, indent=0):
    indentation = '\t' * indent
    print(f'{indentation}{value}')


class Entry:
    def __init__(self, title, entries=None, parent=None):
        if entries is None:
            entries = []
        self.title = title
        self.entries = entries
        self.parent = parent

    def __str__(self):
        return self.title

    def add_entry(self, entry):
        self.entries.append(entry)
        entry.parent = self

    def print_entries(self, indent=0):
        print_with_indent(self, indent)
        for entry in self.entries:
            entry.print_entries(indent=indent + 1)

    def json(self):
        res = {"title": self.title, "entries": [entry.json() for entry in self.entries]}
        return res

    @classmethod
    def from_json(cls, value: dict):
        new_entry = cls(value['title'])
        for item in value.get('entries', []):
            new_entry.add_entry(cls.from_json(item))
        return new_entry

    def save(self, path):
        file = self.json()
        with open(f'{path}/{self.title}.json', 'w', encoding='utf-8') as f:
            json.dump(file, f)

    @classmethod
    def load(cls, filename):
        with open(filename, 'r') as f:
            content = json.load(f)
            return cls.from_json(content)


grocery_list = {
    "title": "Продукты",
    "entries": [
        {
            "title": "Молочные",
            "entries": [
                {
                    "title": "Йогурт",
                    "entries": []
                },
                {
                    "title": "Сыр",
                    "entries": []
                }
            ]
        }
    ]
}


class EntryManager:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.entries = []

    def save(self):
        for entry in self.entries:
            entry.save(self.data_path)

    def load(self):
        if not os.path.isdir(self.data_path):
            os.makedirs(self.data_path)
        else:
            for filename in os.listdir(self.data_path):
                if filename.endswith('json'):
                    entry = Entry.load(os.path.join(self.data_path, filename))
                    self.entries.append(entry)
        return self

    def add_entry(self, title: str):
        self.entries.append(Entry(title))



