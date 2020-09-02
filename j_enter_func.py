import os


PROGRAM_DIR = os.getcwd()
JOURNALS_PATH = os.path.join(PROGRAM_DIR, "Journals")
STYLES_PATH = os.path.join(PROGRAM_DIR, "Styles")
TAG_LIST_PATH = os.path.join(PROGRAM_DIR, "tag_list.txt")


def init_directories():
    global JOURNALS_PATH
    global TAG_LIST_PATH

    if not os.path.exists(JOURNALS_PATH):
        os.mkdir(JOURNALS_PATH)

    if not os.path.exists(STYLES_PATH):
        os.mkdir(STYLES_PATH)

    if not os.path.exists(TAG_LIST_PATH):
        with open(TAG_LIST_PATH, "w") as f:
            pass

    #for each journal path, make sure that there is a journal and a data file too
    os.chdir(JOURNALS_PATH)
    journals = os.listdir(JOURNALS_PATH)
    for journal in journals:
        JOURNAL_PATH = os.path.join(JOURNALS_PATH, journal)
        RAW_JOURNAL = os.path.join(JOURNAL_PATH, journal.lower() + ".txt")
        RAW_DATA = os.path.join(JOURNAL_PATH, journal.lower() + " data.txt")

        if not os.path.exists(RAW_JOURNAL):
            with open(os.path.basename(RAW_JOURNAL), "w") as f:
                pass
        if not os.path.exists(RAW_DATA):
            with open(os.path.basename(RAW_DATA), "w") as f:
                pass
        write_data_file(RAW_JOURNAL, RAW_DATA)

    os.chdir(PROGRAM_DIR)


def write_data_file(JOURNAL_PATH, DATA_PATH):
    with open(JOURNAL_PATH, "rt", newline="\n") as journal_file:
        with open(DATA_PATH, "w", newline="\n") as data_file:
            journal_file.seek(0, 2)
            size_of_file = journal_file.tell()
            journal_file.seek(0)

            #debug_counter = 0

            data_info = [0, 0, 0]

            size_of_entry = 0

            line_counter = 0
            in_entry = True

            #print("File size: " + str(size_of_file))
            #scope of entry
            while in_entry:
                if journal_file.tell() >= size_of_file:
                    break
                #if debug_counter > 200:
                    #print("debug limit reached")
                    #break
                #debug_counter += 1

                line = journal_file.readline()
                #adding one because len counts newline as one character?
                size_of_entry += len(line)
                line_counter += 1

                #only being triggered once?
                if line == "\n" or line == "\r\n" or line == "\r":
                    data_info[1] = size_of_entry

                    size_of_entry = 0

                    data_file.write(data_info[0])
                    data_file.write(":")
                    data_file.write(str(data_info[1]))
                    data_file.write(":")
                    data_file.write(data_info[2])
                    data_file.write("\n") #data_info[2] does not record a newline

                    line_counter = 0

                if line_counter == 1:
                    data_info[0] = make_entry_id(str(line.strip()))
                elif line_counter == 4:
                    data_info[2] = line.strip()


def make_entry_id(entry_num):
    if len(str(entry_num)) == 1:
        entry_id = "0000" + str(entry_num)
    elif len(str(entry_num)) == 2:
        entry_id = "000" + str(entry_num)
    elif len(str(entry_num)) == 3:
        entry_id = "00" + str(entry_num)
    elif len(str(entry_num)) == 4:
        entry_id = "0" + str(entry_num)
    elif len(str(entry_num)) == 5:
        entry_id = str(entry_num)
    else:
        print("Error finding length of entry_num (je make_entry_id(int): " + str(entry_num))
        entry_id = "ERROR"

    return entry_id


def get_journals():
    global JOURNALS_PATH

    avail_journals = []

    for directory in os.listdir(JOURNALS_PATH):
        if os.path.isdir(os.path.join(JOURNALS_PATH, directory)):
            avail_journals.append(directory)

    if not avail_journals:
        avail_journals.append("NONE")

    return avail_journals


def save_tags(entry):
    global TAG_LIST_PATH
    with open(TAG_LIST_PATH, "a") as tag_file:
        tag_file.write(str(entry) + "\n")

    organize_tags()


def find_entry(RAW_JOURNAL_PATH, entry_num):
    with open(RAW_JOURNAL_PATH, "r") as journal_file:
        for line in journal_file:
            if line == str(entry_num) or line == str(entry_num+"\n"):
                return True
    return False


def calc_entry_size(entry=[]):
    entry_size = 0
    for item in entry:
        print(str(item) + ":" + str(len(str(item))))
        entry_size += len(str(item))

    return entry_size


def organize_tags():
    tag_list = []
    global TAG_LIST_PATH

    with open(TAG_LIST_PATH, "r") as tag_file:
        for line in tag_file:
            if line == "\n":
                line = ""
            tag_list.append(line)

    #remove duplicates by converting to a set
    unique_tags = list(set(tag_list))
    unique_tags.sort()

    with open(TAG_LIST_PATH, "w") as tag_file:
        for tag in unique_tags:
            tag_file.write(tag)
