import pykeepass
import json

from pprint import pprint

class ContactList:

    def __init__(self, kdbxfile) -> None:
        self.key_meta = 'metadata'
        self.key_counter = 'contact_counter'
        self.key_group = 'covid_contacts'
        self.kdbxfile = kdbxfile
        self.kb = None

    def open(self, password):
        self.kb = pykeepass.PyKeePass(self.kdbxfile, password=password)

    def save(self):
        self.kb.save()

    def close(self):
        if self.kb:
            self.save()
            self.kb = None

    def next_number(self):
        entry = self.kb.find_entries(title='metadata', group=self.kb.root_group, first=True)
        if not entry:
            entry = self.kb.add_entry(self.kb.root_group, 'metadata', '', '')
            entry.set_custom_property(self.key_counter, '0')

        nextnumber = int(entry.get_custom_property(self.key_counter)) + 1
        entry.delete_custom_property(self.key_counter)
        entry.set_custom_property(self.key_counter, str(nextnumber))

        return nextnumber

    def append(self, info):
        self.kb.reload()

        group = self.kb.find_groups_by_name(self.key_group, group=self.kb.root_group, first=True)

        if not group:
            group = self.kb.add_group(self.kb.root_group, self.key_group)

        nextnumber = self.next_number()
        title = f"#{nextnumber:05d}: {info['lastname']}, {info['firstname']}"
        entry = self.kb.add_entry(group, title, "", "")

        for key in info.keys():
            entry.set_custom_property(key, info[key])

        return (nextnumber, title)

    def verify(self, title):
        self.kb.reload()
        group = self.kb.find_groups_by_name(self.key_group, group=self.kb.root_group, first=True)
        entry = self.kb.find_entries_by_title(title, group=group, first=True)
        return entry is not None
