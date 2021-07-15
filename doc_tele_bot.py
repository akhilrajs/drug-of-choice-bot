# -*- coding: utf-8 -*-
"""
Created on Sun Jul  4 07:45:42 2021

@author: khilr
"""


import pandas as pd
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import threading
import xlsxwriter
from datetime import date
import telepot
import classification_table
from os import getcwd
from telegram import ParseMode


token = "1869000141:AAG4gGBsI7NC1-ql82H0OgEGnP3-Q2CJt38"
telepot.api.set_proxy('http://proxy.server:3128')



user_name_list = []
user_id_list = []
search_condition_list = []
search_result_list = []
search_category_list = []
list_classification = []
user_name_list_classification = []
user_id_list_classification = []
date_list = []
search_result = ""
index_ = '''
click any of the below to copy it and paste it and send it


`/classify ACNE VULGARIS DRUGS`.
`/classify ADRENERGIC DRUGS`
`/classify ANDROGEN DRUGS AND FOR ERECTILE DYSFUNCTION`
`/classify ANTERIOR PITUITARY DRUGS`
`/classify ANTI ANGINAL DRUGS`
`/classify ANTI ANXIETY DRUGS`
`/classify ANTI CHOLINERGIC DRUGS`
`/classify ANTI EMETICS`
`/classify ANTI EPILEPTIC DRUGS`
`/classify ANTI LEPROTIC DRUGS`
`/classify ANTI MALARIAL DRUGS`
`/classify ANTI PARKINSONIAN DRUGS`
`/classify ANTI PSYCHOTIC DRUGS`
`/classify ANTI RETROVIRAL DRUGS`
`/classify ANTI TUBERCULAR DRUGS`
`/classify ANTI TUBERCULAR DRUGS`
`/classify ANTI AMOEBIC DRUGS`
`/classify ANTI ARRHYTHMIC DRUGS`
`/classify ANTI BACTERIAL DRUGS`
`/classify ANTICANCER DRUGS - 1`
`/classify ANTICANCER DRUGS - 2`
`/classify ANTICANCER DRUGS - 3`
`/classify ANTICOAGULANTS`
`/classify ANTIDEPRESSANTS`
`/classify ANTIFUNGAL DRUGS`
`/classify ANTIHELMINTHIC DRUGS`
`/classify ANTIHYPERTENSIVE DRUGS`
`/classify ANTIHYPERTENSIVE DRUGS`
`/classify ANTIPLATELET DRUGS`
`/classify ANTIVIRAL DRUGS (NON RETRIVIRAL)`
`/classify APLHA ADRENERGIC BLOCKING DRUGS , ALPHA BLOCKERS`
`/classify BETA ADRENERGIC BLOCKING DRUGS , BETA BLOCKERS`
`/classify BRONCHIAL ASTHMA DRUGS`
`/classify CEPHALOSPORINS`
`/classify CHOLINERGIC DRUGS`
`/classify CNS STIMULANTS`
`/classify COAGULANTS`
`/classify COGNITION ENHANCERS`
`/classify CONGESTIVE HEART FAILURE DRUGS`
`/classify CORTICOSTEROIDS AND TOPICAL STEROID DRUGS`
`/classify COUGH DRUGS`
`/classify DIARRHOEA DRUGS`
`/classify DIURETICS`
`/classify ESTROGEN AND RELATED DRUGS`
`/classify GANGLIONIC BLOCKERS AND STIMULANTS`
`/classify GENERAL ANAESTHETICS`
`/classify HAEMATINICS`
`/classify HALLUCINOGENS`
`/classify HISTAMINERGIC AGONIST AND ANTAGONIST`
`/classify HORMONAL CONTRACEPTIVES`
`/classify HYPOLIPIDAEMIC DRUGS`
`/classify IMMUNOSUPPRESSANT DRUGS`
`/classify INSULINS`
`/classify LAXATIVES`
`/classify LOCAL ANAESTHETICS`
`/classify MANIA , BIPOLAR DISORDERS DRUGS`
`/classify MIGRAINE DRUGS`
`/classify NSAIDS / ANTIPYRETIC DRUGS`
`/classify ORAL ANALGESICS AND ANTAGONISTS`
`/classify ORAL ANTI DIABETIC DRUGS`
`/classify PENICILLINS`
`/classify PEPTIC ULCER DRUGS`
`/classify PERIPHERAL VASCULAR DISEASES DRUGS`
`/classify PRE ANAESTHETIC MEDICATION DRUGS`
`/classify PROGESTINS`
`/classify PROSTAGLANDINS`
`/classify QIONOLONE ANTIMICROBIALS`
`/classify RHEUMATIC FEVER AND GOUT DRUGS`
`/classify SEDATIVE HYPNOTIC DRUGS`
`/classify SEROTONIN ANTAGONIST`
`/classify SKELETAL MUSCLE RELAXANTS`
`/classify SULPHONAMIDES`
`/classify THYROID INHIBITING DRUGS`
`/classify TOPICAL DRUGS FOR GLAUCOMA`
`/classify UTERINE STIMULANTS AND RELAXANTS`
`/classify VACCINES`

click any of the above to copy it and paste it and send it '''

data = pd.read_excel (r'database.xlsx')
classification_index = pd.read_excel(r'classification_index_arranged.xlsx')


list_of_titles = classification_index["title"].tolist()
list_of_file_names = classification_index["file_name"].tolist()


condition = data["Condition"].tolist()
doc = data["DOC"].tolist()
dose = data["dose"].tolist()



# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')
    update.message.reply_text(''' Welcome to Drug Of Choice bot by ARTEC

Enter the condition to which you want to know the drug of choice or enter the drug to which you want to know which is the condition in which it is used as a Drug Of Choice
please make sure the spelling is correct .

To get the classifcation of drugs table for example : "/classify beta blockers"  to get the table of beta blocker classification. To see the index of classification go to "MENU" on the bottom left corner and click "/classification_index"

The database is updated according to the latest syllabus according to the NEXT exam ''')


def contact(update, context):
    update.message.reply_text('''Click here to contact developer : https://wa.link/z1sjsn''')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('''This bot will help you find the drug of choice for certain diseases. All you need to do is

1) Enter the condition for which you want to find the corresponding drug of choice and click send

2) Enter the drug name to find out which condition it is used as a drug of choice

3) To see classification tables click "MENU" in the bottom left corner and click "/classify"

4) To see the classification index click "MENU" in the bottom left corner and click "/classification_index" . Touch any topic in the list to automatically copy it to your clipboard and paste it and send to me. i will send you the classification table of that topic.

The reults will be send to you in a second, however if the result coud not be found in our database, we will be updating it accordingly in a matter of time.If you have any doubt contact me @ : https://wa.link/z1sjsn''')


def input_keys_to_condition(update, context):
    search_result = "NOT FOUND"
    search_category = "-------"
    search_keyword = (update.message.text)
    search_keyword = search_keyword.upper()
    count_i = 0
    for i in condition :
      i = i.upper()
      j = doc[count_i]
      if (i.count(search_keyword)>0):
          search_result = "FOUND"
          search_category = "CONDITION"
          update.message.reply_text(f'''Condition : {condition[count_i]}

Drug of Choice : {doc[count_i]}

Dose : {dose[count_i]}
''')
      count_i += 1


      if (j.count(search_keyword)>0):
          search_result = "FOUND"
          search_category = "DRUG"
          update.message.reply_text(f'''Drug : {doc[count_i-1]}

Condition of choice : {condition[count_i-1]}

Dose : {dose[count_i-1]}
''')
    if search_result == "NOT FOUND":
          update.message.reply_text('''Not found in Database. This bot is still in development the database will be updated ASAP and will be officially launched.''')
    global column
    global row
    user = update.message.from_user
    user_name = (str(user['username']))
    user_id = (str(user['id']))
    search_condition = search_keyword
    user_name_list.append(user_name)
    user_id_list.append(user_id)
    search_condition_list.append(search_condition)
    search_result_list.append(search_result)
    search_category_list.append(search_category)
    user_base = pd.DataFrame({'User_name':user_name_list,'User_ID':user_id_list,'Search':search_condition_list,'Category':search_category_list, 'Result':search_result_list})
    user_base_file = "user_database_" + str(date.today()) + ".xlsx"
    open(user_base_file, 'a').close()
    user_base.to_excel(user_base_file)
    print(user_name + " " + user_id + " " + "'" +  search_condition + "'" + " " + search_category + " " + search_result)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def classification(update, context):
    try:
        user = update.message.from_user
        user_name = (str(user['username']))
        user_id = (str(user['id']))
        drug_class = []
        drug_class = (context.args)
        token = "1869000141:AAG4gGBsI7NC1-ql82H0OgEGnP3-Q2CJt38"
        bot = telepot.Bot(token)
        bot.sendMessage(user_id, text="sending ...", parse_mode=ParseMode.MARKDOWN)

        classification_table.main(drug_class, user_id, user_name)
        user = update.message.from_user
        user_name = (str(user['username']))
        user_id = (str(user['id']))
        classification_searched = str(drug_class)
        list_classification.append(classification_searched)
        user_name_list_classification.append(user_name)
        user_id_list_classification.append(user_id)
        date_ = str(date.today())
        date_list.append(date_)
        user_base_classification = pd.DataFrame({'Date':date_list, 'User_name':user_name_list_classification,'User_ID':user_id_list_classification,'Classification':list_classification})
        user_base_classification_file = "user_database_classification.xlsx"
        open(user_base_classification_file, 'a').close()
        user_base_classification.to_excel(user_base_classification_file)
        print(user_name + " " + user_id + " " +  classification_searched)
    except (IndexError, ValueError):
        update.message.reply_text('long press > /classify and type the drug class after that ')
        update.message.reply_text('''for example :
/classify beta blockers
/classify anti anginal drugs

to see the index click > /classification_index

If you have any doubt contact me @ : https://wa.link/z1sjsn''')

def classification_index(update, context):
    user = update.message.from_user
    user_id = str(user['id'])
    user_id = user_id
    token = "1869000141:AAG4gGBsI7NC1-ql82H0OgEGnP3-Q2CJt38"
    bot = telepot.Bot(token)
    bot.sendMessage(user_id, text=index_, parse_mode=ParseMode.MARKDOWN)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1869000141:AAG4gGBsI7NC1-ql82H0OgEGnP3-Q2CJt38", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("contact_dev", contact))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("classify", classification, pass_args="True"))
    dp.add_handler(CommandHandler("classification_index", classification_index))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, input_keys_to_condition))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()