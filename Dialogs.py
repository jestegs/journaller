import j_enter_func as je
from tkinter import *
from tkinter import messagebox
import os
import tempfile


class SaveEntryDialog(Frame):

    def __init__(self, entry=[]):
        self.entry = entry
        self.auto_num = StringVar()
        self.auto_num.set("1")
        self.text = StringVar()
        self.text.set("Number (auto=" + str(self.auto_num.get()) + "):")

        #dropdown menu options
        self.options = je.get_journals()

        save_dialog = self.save_dialog = Toplevel()
        save_dialog.title("Save Journal Entry")

        save_frame = Frame(save_dialog, padx=50, pady=30)

        # tkinter variable
        tkvar = StringVar()
        #default value
        if not self.options:
            tkvar.set("NONE")
        else:
            tkvar.set(self.options[0])

        journal_menu = OptionMenu(save_frame, tkvar, *self.options, command=lambda journal: self.gen_num(journal))

        journal_label = Label(save_frame, text="Select Journal:")

        save_num_label = Label(save_frame, textvariable=self.text)
        save_title_label = Label(save_frame, text="Title:")
        save_date_label = Label(save_frame, text="Date:")
        save_tags_label = Label(save_frame, text="Tags:")
        save_content_label = Label(save_frame, text="Characters:")

        self.save_num_box = Entry(save_frame, width=20)
        #self.save_num_box.insert(0, self.auto_num.get())
        self.save_title_box = Entry(save_frame, width=20)
        self.save_title_box.insert(0, entry[1])
        self.save_date_box = Entry(save_frame, width=20)
        self.save_date_box.insert(0, entry[2])

        tag_count_label = Label(save_frame, text=self.tag_count())
        char_count_label = Label(save_frame, text=self.char_count())

        save_confirm = Button(save_frame, text="Save",
                              command=lambda: self.confirm(tkvar.get()), width=20)
        save_cancel = Button(save_frame, text="Cancel", command=self.close_win, width=20)

        save_frame.pack()

        journal_label.grid(row=0, column=0)
        journal_menu.grid(row=0, column=1)

        save_num_label.grid(row=1, column=0)
        save_title_label.grid(row=2, column=0)
        save_date_label.grid(row=3, column=0)
        save_tags_label.grid(row=4, column=0)
        save_content_label.grid(row=5, column=0)

        self.save_num_box.grid(row=1, column=1)
        self.save_title_box.grid(row=2, column=1)
        self.save_date_box.grid(row=3, column=1)
        tag_count_label.grid(row=4, column=1)
        char_count_label.grid(row=5, column=1)

        save_confirm.grid(row=6, column=0)
        save_cancel.grid(row=6, column=1)

        self.gen_num(tkvar.get())
        if tkvar.get() == "NONE":
            save_confirm["state"] = DISABLED
        else:
            save_confirm["state"] = NORMAL

        save_dialog.wait_window()

    def close_win(self):
        self.save_dialog.destroy()

    def confirm(self, journal):
        #save the entry to the appropriate file
        #check if all the fields are filled in

        JOURNAL_PATH = os.path.join(je.JOURNALS_PATH, journal)
        RAW_JOURNAL_PATH = os.path.join(JOURNAL_PATH, journal.lower() + ".txt")
        DATA_JOURNAL_PATH = os.path.join(JOURNAL_PATH, journal.lower() + " data.txt")

        is_duplicate = False

        os.chdir(JOURNAL_PATH)

        #entry_start = 0
        #entry_end = 0

        entry_num = self.save_num_box.get()
        self.entry = [entry_num,
                      self.save_title_box.get(),
                      self.save_date_box.get(),
                      self.entry[3],
                      self.entry[4]]

        if self.entry[3] == "" or "NONE," in self.entry[3]:
            self.entry[3] = "NONE"

        #check if entry number already exists (je function?)
        if je.find_entry(RAW_JOURNAL_PATH, entry_num):
            # if yes, ask to overwrite (fetch old dream size and delete at the pointer)
            #is_duplicate = True
            overwrite_msg = messagebox.askyesno("Overwrite Entry?", "An entry with this number already exists, "
                                                + "would you like to overwrite it?")
            if overwrite_msg:
                #iterate through temp file until the entry_num hit
                #write the new entry instead of the old
                #rewrite from temp file
                #record the id, size, and tags, do the same for the data file

                with tempfile.TemporaryFile("r+t", newline="\n") as temp_file:
                    with open(os.path.basename(RAW_JOURNAL_PATH), "r", newline="\n") as journal_file:
                        #line_size = 0
                        in_entry = False
                        for line in journal_file:
                            if line.strip() == str(entry_num):
                                #line_size = len(line)
                                in_entry = True
                                # write entry to temp file
                                for item in self.entry:
                                    temp_file.write(str(item) + "\n")
                                #break

                            elif in_entry:
                                if line == "\n" or line == "\r" or line == "\r\n":
                                    in_entry = False
                                    #temp_file.write(line)

                            elif not in_entry:
                                temp_file.write(line)

                    #must seek back to the beginning in the temp file!
                    temp_file.seek(0)
                    with open(os.path.basename(RAW_JOURNAL_PATH), "w", newline="\n") as journal_file:
                        for line in temp_file:
                            journal_file.write(line)

                #maybe its fixed? can't figure out how to reproduce it...

                #replace this with "manual" overwrite, similar to above
                je.write_data_file(RAW_JOURNAL_PATH, DATA_JOURNAL_PATH)

                #open the data file for read, write to temp file
                #run je write_data function to ensure the new size is recorded
                #seek to the line after the new one in the temp file and transfer to data file
                #with tempfile.TemporaryFile("r+t", newline="\n") as temp_file:
                    #with open(os.path.basename(DATA_JOURNAL_PATH), "r", newline="\n") as data_file:
                        #pass

        # if no, append
        else:
            #moved these two lines from up top, this context used to encompass this if-else
            with open(os.path.basename(RAW_JOURNAL_PATH), "a", newline="\n") as journal_file:
                #entry_start = journal_file.tell()

                for item in self.entry:
                    journal_file.write(str(item) + "\n")

            #entry_end = journal_file.tell()

        #if not is_duplicate:
            je.write_data_file(RAW_JOURNAL_PATH, DATA_JOURNAL_PATH)

        os.chdir(je.PROGRAM_DIR)

        self.save_dialog.destroy()

    def tag_count(self):
        if self.entry[3] == "NONE":
            return str(0)
        elif type(self.entry[3]) == str:
            return str(len(self.entry[3].split(",")))
        else:
            return str(len(self.entry[3]))

    def char_count(self):
        chars = 0
        for char in self.entry[4]:
            if char != "\n":
                chars += 1

        return str(chars)

    def gen_num(self, journal):
        JOURNAL_PATH = os.path.join(je.JOURNALS_PATH, journal)

        DATA_PATH = os.path.join(JOURNAL_PATH, os.path.basename(JOURNAL_PATH).lower() + " data.txt")

        os.chdir(JOURNAL_PATH)

        linenum = 0
        with open(os.path.basename(DATA_PATH), "r") as data_file:
            for line in data_file:
                if linenum == 0:
                    offset = line.split(":")[0]
                    linenum = int(offset)
                else:
                    linenum += 1

        os.chdir(je.PROGRAM_DIR)

        linenum += 1

        self.auto_num.set(str(linenum))
        self.save_num_box.delete(0, END)
        self.save_num_box.insert(0, str(self.auto_num.get()))
        self.text.set("Number (auto=" + str(self.auto_num.get()) + "):")


class LoadEntryDialog:

    def __init__(self, num, title, date, entry_tags, para):
        self.main_num = num
        self.main_title = title
        self.main_date = date
        self.main_entry_tags = entry_tags
        self.main_para = para

        load_dialog = self.load_dialog = Toplevel()
        load_dialog.title("Load Journal Entry")

        load_frame = Frame(load_dialog, padx=30, pady=30)

        # dropdown menu options
        self.options = je.get_journals()

        #tkinter variable
        tkvar = StringVar()
        # default value
        if not self.options:
            tkvar.set("NONE")
        else:
            tkvar.set(self.options[0])

        j_label = Label(load_frame, text="Journal:")
        j_option_menu = OptionMenu(load_frame, tkvar, *self.options)

        label = Label(load_frame, text="Entry Number:")
        entry = Entry(load_frame, width=20)

        confirm = Button(load_frame, text="Load", command=lambda: self.load_entry(tkvar.get(), entry.get()), width=20)
        cancel = Button(load_frame, text="Cancel", command=self.load_cancel, width=20)

        load_frame.pack()
        j_label.grid(row=0, column=0)
        j_option_menu.grid(row=0, column=1)
        label.grid(row=1, column=0)
        entry.grid(row=1, column=1)
        confirm.grid(row=2, column=0)
        cancel.grid(row=2, column=1)

        load_dialog.wait_window()

    def load_entry(self, journal_name, entry_num):
        #first find the entry in data, record size
        #then find it in the raw journal and pull in the entries

        #pass main window as constructor parameter?

        JOURNAL_PATH = os.path.join(je.JOURNALS_PATH, journal_name)
        JOURNAL = os.path.join(JOURNAL_PATH, journal_name + ".txt")
        DATA = os.path.join(JOURNAL_PATH, journal_name + " data.txt")

        os.chdir(JOURNAL_PATH)

        entry_size = 0
        entry_location = 0

        with open(os.path.basename(DATA), "r", newline="\n") as data_file:
            for line in data_file:
                split_line = line.split(":")
                if int(split_line[0]) == int(entry_num):
                    entry_size = split_line[1]
                    break
                else:
                    entry_location += int(split_line[1])

        with open(os.path.basename(JOURNAL), "r", newline="\n") as journal_file:
            journal_file.seek(entry_location)
            line_count = 0
            while journal_file.tell() < int(entry_size) + int(entry_location):
                raw_line = journal_file.readline()
                line = raw_line.strip()

                if line_count == 0:
                    self.main_num.delete(0, END)
                    self.main_num.insert(0, line)
                elif line_count == 1:
                    self.main_title.delete(0, END)
                    self.main_title.insert(0, line)
                elif line_count == 2:
                    self.main_date.delete(0, END)
                    self.main_date.insert(0, line)
                elif line_count == 3:
                    index = 0
                    for item in line.split(","):
                        new_item = item.replace(" ", "")
                        if new_item != "":
                            self.main_entry_tags.insert(index, new_item)
                        index += 1
                else:
                    if not line == "":
                        self.main_para.insert(END, line + "\n")

                line_count += 1

        self.load_dialog.destroy()

    def load_cancel(self):
        self.load_dialog.destroy()


class NewJournalDialog:

    def __init__(self):
        new_j_win = self.new_j_win = Toplevel()
        new_j_win.title("Create a New Journal")

        current_j_frame = LabelFrame(new_j_win, text="Current Journals")
        journals_listbox = Listbox(current_j_frame, width=15)

        current_journals = os.listdir(je.JOURNALS_PATH)
        index = 0
        for entry in current_journals:
            journals_listbox.insert(index, entry)
            index += 1

        new_j_frame = Frame(new_j_win, padx=10, pady=30)

        new_j_name = Label(new_j_frame, text="New Journal Name:")
        new_j_box = Entry(new_j_frame, width=15)

        okay_button = Button(new_j_frame, text="OK", width=15, command=lambda: self.okay(new_j_box.get()))
        cancel_button = Button(new_j_frame, text="Cancel", width=15, command=self.new_j_cancel)

        current_j_frame.pack(side=LEFT, padx=10, pady=30)
        new_j_frame.pack(side=RIGHT)

        journals_listbox.pack()
        new_j_name.grid(row=0, column=0)
        new_j_box.grid(row=0, column=1)

        okay_button.grid(row=1, column=0, pady=10)
        cancel_button.grid(row=1, column=1, pady=10)

    def okay(self, journal_name):
        JOURNAL_PATH = os.path.join(je.JOURNALS_PATH, journal_name)
        RAW_JOURNAL_PATH = os.path.join(JOURNAL_PATH, journal_name.lower() + ".txt")
        DATA_JOURNAL_PATH = os.path.join(JOURNAL_PATH, journal_name.lower() + " data.txt")

        if not os.path.exists(JOURNAL_PATH):
            os.mkdir(JOURNAL_PATH)

            os.chdir(JOURNAL_PATH)
            #initializing the files
            with open(os.path.basename(RAW_JOURNAL_PATH), "w") as f:
                pass
            with open(os.path.basename(DATA_JOURNAL_PATH), "w") as f:
                pass
            os.chdir(je.PROGRAM_DIR)
        else:
            print("The journal \"" + journal_name + "\" already exists.")

        self.new_j_win.destroy()

    def new_j_cancel(self):
        self.new_j_win.destroy()


class CreateTagDialog:

    def __init__(self):
        create_tag_win = self.create_tag_win = Toplevel()
        create_tag_win.title("Create New Tag")

        tag_frame = Frame(create_tag_win, padx=30, pady=30)

        label = Label(tag_frame, text="New Tag:")
        entry = Entry(tag_frame, width=15)
        confirm = Button(tag_frame, text="OK", command=lambda: self.confirm(entry.get()), width=15)
        cancel = Button(tag_frame, text="Cancel", command=self.close_win, width=15)

        tag_frame.pack()
        label.grid(row=0, column=0, pady=20)
        entry.grid(row=0, column=1, pady=20)
        confirm.grid(row=1, column=0)
        cancel.grid(row=1, column=1)

        create_tag_win.wait_window()

    def close_win(self):
        self.create_tag_win.destroy()

    def confirm(self, entry):
        je.save_tags(entry)

        self.create_tag_win.destroy()
