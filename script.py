import telegram
from telegram.ext import CommandHandler, Updater
import pandas as pd
import time

# Set the access token for your bot
TOKEN = '5891586724:AAF76KqGash49FBnV50fmDRAqvAYfQsva8s'

# Define a dictionary to store the chat_ids of the users who start the /rastrella command
chat_ids = {}

# Define the /rastrella command
def rastrella(update, context):
    # Get the chat_id of the user who started the command
    chat_id = update.message.chat_id
    # Store the chat_id in the dictionary
    chat_ids[chat_id] = True
    # Send a message asking for the group ID
    context.bot.send_message(chat_id=chat_id, text="Inserisci l'ID del gruppo:")
    
# Define the /aggiungi command
def aggiungi(update, context):
    # Get the chat_id of the user who started the command
    chat_id = update.message.chat_id
    # Check if the user is an admin in the group
    if update.message.chat.type == "supergroup":
        chat_member = context.bot.get_chat_member(update.message.chat_id, update.message.from_user.id)
        if chat_member.status == "administrator":
            # Load the contacts from the Excel file
            contacts = pd.read_excel('contacts.xlsx')
            # Add the contacts to the group
            for index, row in contacts.iterrows():
                try:
                    context.bot.add_chat_member(chat_id=chat_id, user_id=row['ID'])
                    # Wait for 3 seconds before adding the next member
                    time.sleep(3)
                except telegram.TelegramError:
                    # If an error occurs, continue with the next member
                    pass
            context.bot.send_message(chat_id=chat_id, text="Contatti aggiunti al gruppo!")
        else:
            context.bot.send_message(chat_id=chat_id, text="Solo gli amministratori del gruppo possono utilizzare questo comando.")
    else:
        context.bot.send_message(chat_id=chat_id, text="Questo comando può essere utilizzato solo in un gruppo.")
        
# Define the /stop command
def stop(update, context):
    # Get the chat_id of the user who started the command
    chat_id = update.message.chat_id
    # Check if the user is the same user who started the /rastrella command
    if chat_id in chat_ids:
        # Remove the chat_id from the dictionary
        del chat_ids[chat_id]
        # Send a message confirming that the /rastrella command has been stopped
        context.bot.send_message(chat_id=chat_id, text="Il comando /rastrella è stato interrotto.")
    else:
        context.bot.send_message(chat_id=chat_id, text="Non è stata avviata alcuna operazione di raccolta contatti con il comando /rastrella.")

# Define a function to save the contacts to an Excel file
def save_contacts_to_excel(chat_id, contacts):
    # Load the existing contacts from the Excel file, if it exists
    try:
        existing_contacts = pd.read_excel('contacts.xlsx')
    except:
        existing_contacts = pd.DataFrame(columns=['ID', 'Username', 'Numero'])
    # Append the new contacts to the existing contacts, if they are not already in the list
    for index, row in contacts.iterrows():
        if row['ID'] not in existing_contacts['ID'].values:
            existing_contacts = existing_contacts.append(row, ignore_index)