import telegram
import time
import xlwt
import xlrd
import os

# Inizializzazione del bot Telegram
bot = telegram.Bot('INSERISCI_IL_TOKEN_DEL_TUO_BOT_QUI')

# Funzione che salva i contatti in un file XLS
def rastrella(update, context):
    # Richiede all'utente l'ID del gruppo da analizzare
    context.bot.send_message(chat_id=update.message.chat_id, text='Inserisci l\'ID del gruppo')
    group_id = int(context.bot.get_updates()[-1].message.text)

    # Recupera i membri del gruppo
    members = []
    for member in bot.get_chat_members(group_id):
        if member.user.username is not None:
            members.append(member.user)

    # Crea un nuovo file XLS se non esiste già
    if not os.path.isfile('contatti.xls'):
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('Contatti')
        worksheet.write(0, 0, 'Username')
        worksheet.write(0, 1, 'ID Telegram')
        worksheet.write(0, 2, 'Numero di telefono')
        workbook.save('contatti.xls')

    # Aggiunge i contatti al file XLS
    workbook = xlrd.open_workbook('contatti.xls')
    worksheet = workbook.sheet_by_name('Contatti')
    num_rows = worksheet.nrows
    existing_usernames = []
    for i in range(1, num_rows):
        existing_usernames.append(worksheet.cell_value(i, 0))

    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet('Contatti')
    worksheet.write(0, 0, 'Username')
    worksheet.write(0, 1, 'ID Telegram')
    worksheet.write(0, 2, 'Numero di telefono')
    row = 1
    for member in members:
        if member.username not in existing_usernames:
            context.bot.send_message(chat_id=update.message.chat_id, text='Raccolta informazioni per ' + member.username)
            try:
                user_id = member.id
                phone_number = member.phone_number
                worksheet.write(row, 0, member.username)
                worksheet.write(row, 1, user_id)
                worksheet.write(row, 2, phone_number)
                row += 1
            except:
                context.bot.send_message(chat_id=update.message.chat_id, text='Impossibile recuperare le informazioni per ' + member.username)
                continue
        else:
            context.bot.send_message(chat_id=update.message.chat_id, text=member.username + ' già presente nella lista')

        # Aggiunge una pausa per evitare il ban da Telegram
        time.sleep(1)

    # Salva il file XLS
    workbook.save('contatti.xls')

    context.bot.send_message(chat_id=update.message.chat_id, text='Raccolta contatti completata')

# Funzione che aggiunge i contatti al gruppo
def aggiungi(update, context):
    # Recupera i contatti dal file XLS
    workbook = xlrd.open_workbook('contatti.xls')
    worksheet = workbook.sheet_by_name('Contatti')
    num_rows = worksheet.nrows
    usernames = []
    for i in range(1, num_rows):
        usernames.append(worksheet.cell_value(i, 0))

    # Aggiunge i contatti al gruppo
    for username in usernames:
        try:
            bot