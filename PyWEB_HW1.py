from collections import UserDict
import re


class AbsractClass:
    def show_record(self):
        raise NotImplementedError

    def show_records(self):
        raise NotImplementedError


class AddressBook(UserDict, AbstractClass):

    def __eq__(self, other: object) -> bool:
        return self.value == other.value

    def add_record(self, record):
        self.data[record.name.value] = record

    def remove_record(self, record):
        self.data.pop(record, None)

    def change_name(self, old_name, new_name):
        self.data[new_name] = copy.deepcopy(self.data[old_name])
        self.data[new_name].name.value = new_name
        self.remove_record(old_name)

    def change_address(self, record, new_address):
        self.data[record].address.value = new_address

    def change_email(self, record, new_email):
        self.data[record].email.value = new_email

    def change_birthday(self, record, new_birthday):
        self.data[record].birthday.value = new_birthday

    def edit_phone(self, record, new_phone):
        self.data[record].add_phone(new_phone)

    def clear_phones(self, record):
        self.data[record].phones = []

    def get_phones(self, record):
        return self.data[record].phones

    def set_phones(self, record, phone_list):
        self.data[record].phones = phone_list

    def show_records(self):
        return self.data

    def show_record(self, contact):
        try:
            return self.data[contact]
        except:
            return None

    def iterator(self, n=1):
        records = list(self.data.keys())
        records_num = len(records)
        if n > records_num:
            n = records_num
        for i in range(0, records_num, n):
            yield [self.data[records[i+j]].show_contact() for j in range(n) if i + j < records_num]

    def serialize(self, file_name="addressbook.bin"):
        with open(file_name, "wb") as file:
            pickle.dump(self.data, file)

    def deserialize(self, file_name="addressbook.bin"):
        with open(file_name, "rb") as file:
            self.data = pickle.load(file)

    def find_info_by_name(self, name):
        users_search = []
        for user, info in self.data.items():
            if name.lower() in info.name.value.lower():
                users_search.append(self.data[user])
        if users_search:
            return users_search
        else:
            return "Nothing found"

    def find_info_by_phone(self, search_phone):
        users_search = []
        for user, info in self.data.items():
            if info.phones and info.phones[0].value != None:
                for phone in info.phones:
                    if str(search_phone) in phone.value:
                        users_search.append(self.data[user])
        if users_search:
            return users_search
        else:
            return "Nothing found"

    def show_contacts_by_birthday(self, days):
        result = [self.data[record] for record in self.data if self.data[record].birthday.value != None and self.data[record].days_to_birthday()
                  <= days]
        return result

class NoteBook(UserDict, AbstractClass):
    def __init__(self):
        self.data = {}

    def __repr__(self):
        return f'{self.data}'

    def add_note(self, record):
        self.data[record.name.value] = record

    def change_name(self, old_name, new_name):
        self.data[new_name] = copy.deepcopy(self.data[old_name])
        self.data[new_name].name.value = new_name
        self.data.pop(old_name)

    def change_tag(self, name, tags):
        new_tag = Tags(tags)
        for k, v in self.data.items():
            if k == name:
                self.data[k].tags = []
                self.data[k].tags.append(new_tag)

    def change_note(self, name, new_note):
        new_note = Notes(new_note)
        for k in self.data:
            if k == name:
                self.data[k].note = new_note

    def change_status(self, name, new_status):
        if new_status.lower() in ["in progress", "done"]:
            self.data[name].status.value = new_status.lower()

    def show_records(self):
        return self.data

    def show_record(self, name):
        if name in self.data.keys():
            return self.data[name]

    def show_note(self, name):
        for k in self.data:
            if k == name:
                return self.data[k]

    def delete_note(self, rec: RecordNote):
        for a, v in self.data.items():
            if v.note == rec.note:
                deleted_note = a.note
                self.data.pop(a)
                return deleted_note

    def dellete_notes_by_status(self, status):
        result = {}
        for name, record in self.data.items():
            if record.status.value != status:
                result[name] = record
        self.data = result

    def delete_tag(self, name, del_tag):
        old_tags = self.data[name].tags
        new_tags = [tag for tag in old_tags if tag.value != del_tag]
        self.data[name].tags = new_tags

    def add_tag(self, name, new_tag):
        if new_tag.value not in [i.value for i in self.data[name].tags]:
            self.data[name].tags.append(new_tag)

    def find_info_by_name(self, keyword):
        result = []
        for name, record in self.data.items():
            if keyword.lower() == name.lower():
                result.append(self.data[name])
                break
        return result

    def find_info_by_tag(self, keyword):
        result = []
        for name, record in self.data.items():
            for tag in record.tags:
                if keyword.lower() == tag.value.lower():
                    result.append(self.data[name])
                    break
        return result

    def find_info_by_status(self, keyword):
        result = []
        for name, record in self.data.items():
            if keyword.lower() == record.status.value.lower():
                result.append(self.data[name])
        return result

    def get_tags(self, name):
        return self.data[name].tags

    def change_tag(self, name, old_tag, new_tag):
        for i in range(len(self.data[name].tags)):
            if old_tag.value == self.data[name].tags[i].value:
                self.data[name].tags[i].value = new_tag.value

    def serialize(self, file_name="notebook.bin"):
        with open(file_name, 'wb') as file:
            pickle.dump(self.data, file)

    def deserialize(self, file_name="notebook.bin"):
        with open(file_name, 'rb') as file:
            self.data = pickle.load(file)

    def show_records(self):
        return self.data