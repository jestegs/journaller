import j_enter_func as je
import Dialogs as dialog
from tkinter import *
from tkinter import messagebox
import os


def main():
    """
    Initialize all necessary files and directories.
    :return:
    """
    je.init_directories()
    load_tags()


def change_theme(theme_file):
    """
    Changes the theme of the program.
    :param theme_file:
    :return:
    """
    window.option_clear()

    if theme_file != "default":
        window.option_readfile(os.path.join(je.STYLES_PATH, theme_file))

    window.update_idletasks()


def load_tags():
    """
    Load tags into the program
    :return:
    """
    je.organize_tags()
    tag_list.delete(0, END)
    with open(je.TAG_LIST_PATH, "r") as tag_file:
        index = 0
        for line in tag_file:
            tag_list.insert(index, line)
            index += 1


#button functions
def create_tag():
    """
    Adds a new tag to the tag list
    :return:
    """
    #open dialog window
    dialog.CreateTagDialog()
    load_tags()


def del_tag():
    """
    Delete tags from tag_list.txt
    :return:
    """
    #gets the index of the marked tags
    marked_tags = tag_list.curselection()

    #reversed to prevent indexes from changing
    for tag_index in reversed(marked_tags):
        tag_list.delete(tag_index)

    with open(je.TAG_LIST_PATH, "w") as tag_file:
        for tag in tag_list.get(0, END):
            tag_file.write(tag)


def manual_callback(event):
    #entry_tag_list.insert(END, event.widget.get())
    add_tag_to_entry(event.widget.get())
    je.save_tags(event.widget.get())
    manual_entry_tags.delete(0, END)
    load_tags()


def add_tag_to_entry(new_tag=None):
    """
    Adds tag to the entry's tag list
    :return:
    """

    #get items from selection, add to other listbox
    marked_tags = tag_list.curselection()

    for tag_index in marked_tags:
        tag = tag_list.get(tag_index)

        # append to listbox
        entry_tag_list.insert(END, tag)

    entry_tag_list.insert(END, new_tag)

    #sorting entry tags
    tags_sorted = []
    for tag in entry_tag_list.get(0, END):
        tags_sorted.append(tag)

    entry_tag_list.delete(0, END)

    #use set() to remove duplicates, convert back to list
    unique_list = list(set(tags_sorted))
    unique_list.sort()

    for tag in unique_list:
        entry_tag_list.insert(END, tag)



def del_tag_from_entry():
    """
    Delete tags from journal entry
    :return:
    """
    marked_tags = entry_tag_list.curselection()

    for tag_index in reversed(marked_tags):
        entry_tag_list.delete(tag_index)


def save_entry():
    """
    Save journal entry
    Journal Entry consists of number, title, date, list of tags, and the content
    :return:
    """
    entry_tags = str(entry_tag_list.get(0, END))
    #change tuple to string: "item, item, item"
    entry_tags = entry_tags.replace("(", "")
    entry_tags = entry_tags.replace("'", "")
    entry_tags = entry_tags.replace("\\n", "")
    entry_tags = entry_tags.replace(")", "")

    entry = [num_box.get(),
             title_box.get(),
             date_box.get(),
             entry_tags,
             para_box.get("1.0", "end-1c")]

    dialog.SaveEntryDialog(entry)


def load_entry():
    """
    Load entry from file system into program
    :return:
    """
    new_entry()
    dialog.LoadEntryDialog(num_box, title_box, date_box, entry_tag_list, para_box)


def new_entry():
    """
    Delete what is currently in the entry fields.
    :return:
    """
    new_entry_msg = messagebox.askokcancel("Create New Entry?",
                                           "This will delete what is currently in the entry fields.")
    if new_entry_msg:
        num_box.delete(0, END)
        title_box.delete(0, END)
        date_box.delete(0, END)
        para_box.delete(1.0, END)
        entry_tag_list.delete(0, END)


def new_journal():
    """
    Create a new journal.
    :return:
    """
    dialog.NewJournalDialog()


def exit_prgm():
    """
    Exits the program
    :return:
    """
    window.quit()


window = Tk()
window.title("Journal Entry Program")
window.geometry("1000x800")
icon = PhotoImage(file="./images/journal_book.png")
window.iconphoto(True, icon)

window.configure(background="grey35")
window.option_readfile(os.path.join(je.STYLES_PATH, "journal.xdefaults"))

#menubar
menu_bar = Menu(window)

#relating to entry operations
file_menu = Menu(menu_bar, tearoff=0)

file_menu.add_command(label="New", command=new_entry)
file_menu.add_command(label="Open...", command=load_entry)
file_menu.add_command(label="Save As...", command=save_entry)
file_menu.add_separator()
file_menu.add_command(label="New Journal...", command=new_journal)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_prgm)
#interface preferences, styling
edit_menu = Menu(menu_bar, tearoff=0)
theme_menu = Menu(edit_menu, tearoff=0)

#theme_menu.add_command(label="Dark", command=lambda: change_theme("dark.xdefaults"))
#theme_menu.add_command(label="Default", command=lambda: change_theme("default"))
#theme_menu.add_command(label="Journal", command=lambda: change_theme("journal.xdefaults"))

edit_menu.add_cascade(label="Theme...", menu=theme_menu)

#help with the program
help_menu = Menu(menu_bar, tearoff=0)

menu_bar.add_cascade(label="File", menu=file_menu)
menu_bar.add_cascade(label="Edit", menu=edit_menu)
menu_bar.add_cascade(label="Help", menu=help_menu)

#frames
frame_master = Frame(window)
frame_tags = LabelFrame(frame_master, text="Tags")
frame_entry = LabelFrame(frame_master, text="Entry")

tag_scroll_frame = Frame(frame_tags)
entry_scroll_frame = Frame(frame_entry)

frame_header = Frame(frame_entry)

frame_label = Frame(frame_header)
frame_data = Frame(frame_header)

tag_scroll = Scrollbar(tag_scroll_frame)
tag_scroll.pack(fill=Y, side=RIGHT)
para_scroll = Scrollbar(entry_scroll_frame)
para_scroll.pack(fill=Y, side=RIGHT)

#tag frame
tag_list = Listbox(tag_scroll_frame, width=15, height=13, selectmode=MULTIPLE, yscrollcommand=tag_scroll.set)

create_tag = Button(frame_tags, text="Create New", command=create_tag)
del_tag = Button(frame_tags, text="Delete", command=del_tag)

#entry frame
frame_entry_tags = Frame(frame_entry)
label_manual_entry = Label(frame_entry_tags, text="Enter Tags:")
manual_entry_tags = Entry(frame_entry_tags, width=15)

label_entry_tags = Label(frame_entry_tags, text="Entry Tags")
entry_tag_scroll_frame = Frame(frame_entry_tags)
entry_tag_scroll = Scrollbar(entry_tag_scroll_frame)
entry_tag_scroll.pack(fill=Y, side=RIGHT)
entry_tag_list = Listbox(entry_tag_scroll_frame, width=15, height=9, selectmode=MULTIPLE, yscrollcommand=entry_tag_scroll.set)

add_tag = Button(frame_entry_tags, text="Add", command=add_tag_to_entry)
remove_tag = Button(frame_entry_tags, text="Remove", command=del_tag_from_entry)

label_num = Label(frame_label, text="Number:")
label_title = Label(frame_label, text="Title:")
label_date = Label(frame_label, text="Date:")
num_box = Entry(frame_data, width=20, state=NORMAL)
num_box.insert(0, "Default")
title_box = Entry(frame_data, width=20)
date_box = Entry(frame_data, width=20)
para_box = Text(entry_scroll_frame, width=80, height=5, wrap="word", spacing3=10, yscrollcommand=para_scroll.set)

frame_entry_buttons = Frame(frame_entry)

#packing
frame_master.pack(fill=Y, expand=True)
frame_tags.pack(fill=Y, side=LEFT)
frame_entry.pack(fill=Y, side=RIGHT)
frame_entry_tags.pack(fill=Y, side=LEFT)
frame_header.pack(fill=Y)

label_manual_entry.pack()
manual_entry_tags.pack()
label_entry_tags.pack()
entry_tag_scroll_frame.pack(fill=Y, expand=True)
tag_scroll_frame.pack(fill=Y, expand=True)
entry_scroll_frame.pack(fill=Y, expand=True)

tag_list.pack(fill=Y, expand=True)
create_tag.pack(fill=X)
del_tag.pack(fill=X)

entry_tag_list.pack(fill=Y, expand=True)
add_tag.pack(fill=X)
remove_tag.pack(fill=X)

frame_label.pack(side=LEFT)
frame_data.pack(side=RIGHT)

label_num.pack()
label_title.pack()
label_date.pack()
num_box.pack()
title_box.pack()
date_box.pack()
para_box.pack(fill=Y, expand=True)

frame_entry_buttons.pack(fill=X, pady=25)

tag_scroll.config(command=tag_list.yview)
entry_tag_scroll.config(command=entry_tag_list.yview)
para_scroll.config(command=para_box.yview)

manual_entry_tags.bind("<Return>", manual_callback)

window.config(menu=menu_bar)

main()

window.mainloop()
