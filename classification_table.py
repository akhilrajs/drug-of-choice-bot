def main(search, user_id, user_name):
    import pandas as pd
    from os import getcwd
    import telepot


    token = ""
    bot = telepot.Bot(token)

    classification_index = pd.read_excel(r'classification_index_arranged.xlsx')

    list_of_titles = classification_index["title"].tolist()
    list_of_file_names = classification_index["file_name"].tolist()

    search = search
    index_no = []
    index_no_ = 0
    mark = []
    mark_ = 0
    for i in list_of_titles:
        j = i.split()
        for k in j:
            for l in range(len(search)):
                search
                if k.upper() == search[l].upper():
                    mark_ += 1
        mark.append(mark_)
        index_no.append(list_of_titles[index_no_])
        mark_ = 0
        index_no_ += 1
    greatest_mark = 0
    greatest_markman =""
    count = 0
    for i in mark :
        if int(i) > greatest_mark:
            greatest_mark = i
            greatest_markman = index_no[count]
        count += 1
    greatest_markman = str(greatest_markman)
    classification =  greatest_markman
    index_no = list_of_titles.index(classification)
    file_name = list_of_file_names[index_no]
    FILE = file_name
    user_name = user_name
    file_name = str(getcwd()) + "/classifications/classifications/" + file_name
    caption_ = "Classification of " + greatest_markman
    bot.sendPhoto(chat_id = user_id, photo=open(file_name, "rb"), caption=caption_)
