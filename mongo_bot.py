from telegram.ext import *
from pymongo import MongoClient
from telegram import InputFile

bot_key='6116669963:AAEq9yV0rkauao5Fa6BWMdcFmA8rPyz0Prk'
updater=Updater(bot_key,use_context=True)
bot=updater.bot

USERNAME,PASSWORD,DATABASE,COLLECTION=range(4)
conversation_time=300
def cancel(update,context):
    print('conversation has ended ...')
    return ConversationHandler.END

def get_all_data(username,password,database,collection):
    key=f'mongodb+srv://{username}:{password}@cluster0.lqxzvm9.mongodb.net/?retryWrites=true&w=majority&ssl=true'
    client=MongoClient(key)
    
    database=client.get_database(database)
    document=database.get_collection(collection)
    
    docs=list(document.find())
    text=''
    for i in docs:
        for key in i:
            if key!='_id':
                st=f'{key}:{i[key]} \n'
                text+=st
        text+='................................................. \n'
    
    return text
#get_all_data('Venkataswarao','Kvr*112218','doclocker','autentication')
def start(update,context):
    update.message.reply_text('Enter Username ...')
    return USERNAME
def username(update,context):
    context.user_data['username']=update.message.text
    update.message.reply_text('Password ...')
    return PASSWORD
def password(update,context):
    context.user_data['password']=update.message.text
    update.message.reply_text('Database name ...')
    return DATABASE
    
def database(update,context):
    context.user_data['database']=update.message.text
    update.message.reply_text('Collection name  ...')
    return COLLECTION
def collection(update,context):
    collection=update.message.text
    username=context.user_data['username']
    password=context.user_data['password']
    database=context.user_data['database']
    
    try:
        
        file=get_all_data(username,password,database,collection)
        print(file)
        file=bytes(file,'utf-8')
        document=InputFile(file,f'{collection}.txt')
        bot.send_document(chat_id=update.message.chat_id,document=document)
    except Exception as e:
        update.message.reply_text(bytes(str(e),'utf-8'))

        return USERNAME


def main():
    print('bot started ...')
    start_conv=ConversationHandler(
        entry_points=[CommandHandler('start',start)],
        states={
            USERNAME:[MessageHandler(Filters.text | Filters.command,username)],
            PASSWORD:[MessageHandler(Filters.text | Filters.command,password)],
            DATABASE:[MessageHandler(Filters.text | Filters.command,database)],
            COLLECTION:[MessageHandler(Filters.text | Filters.command,collection)]
            },
        allow_reentry=True,
        conversation_timeout=conversation_time,
        fallbacks=[MessageHandler(Filters.command,cancel)],
        )
    dp=updater.dispatcher
    dp.add_handler(start_conv,1)

    updater.start_polling()
    updater.idle()
main()
    



