from pyrogram import Client, filters
from pyrogram.types import Message

api_id = "17103351"
api_hash = "90553f0af0565accb28ebf8833cc6d39"

app = Client("998912900099", api_id=api_id, api_hash=api_hash)

# Define a function to handle messages
@app.on_message()
def handle_message_in_specific_chat(client, message: Message):
    # Handle messages in the chat with the specific title
    if "Telegram" in message.chat.title:
    	print(message.text)


# Define a function to handle messages in another chat
@app.on_message(filters.chat(lambda chat: chat.title == "Another Chat Title"))
def handle_message_in_another_chat(client, message: Message):
    # Handle messages in the chat with another specific title
    message.reply_text("This is another special chat!")

if __name__ == "__main__":
    app.run()
