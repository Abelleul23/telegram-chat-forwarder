import logging
import traceback
import queue
from telegram import Update, Bot
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
    Updater,
    CallbackContext,
)


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Bot started. Send a post!"

    )


def parse_telegram_links(post):
    links = []
    if post is not None:
        words = post.split()

        for word in words:
            if word.startswith('@') or word.startswith('https://t.me/') or word.startswith('t.me/'):
                links.append(word.strip('@'))

    return links


async def handle_message(update, context):
    message = update.message
    caption = message.caption
    text = message.text
    modified_text = text
    group_id = '-group_id'

    parsed_links = parse_telegram_links(
        text) if text else parse_telegram_links(caption)
    if parsed_links:
        modified_text = text if text else caption
        for link in parsed_links:
            modified_text = modified_text.replace(link, 'link')

    if message.photo:
        # Handle photo message
        photo = message.photo[-1]  # Get the highest quality photo
        file_id = photo.file_id
        # Use 'await' to asynchronously get the file
        file = await context.bot.get_file(file_id)
        # Use 'await' to asynchronously download the file as a byte array
        byte_array = await file.download_as_bytearray()
        # Save the photo locally
        with open('downloaded_photo.jpg', 'wb') as photo_file:
            photo_file.write(byte_array)
        # Send the photo back to the user with the caption
        with open('downloaded_photo.jpg', 'rb') as photo_file:
            await context.bot.send_photo(chat_id=group_id, photo=photo_file, caption=modified_text)
            # await context.bot.forward_message(chat_id=group_id, from_chat_id=message.chat_id, message_id=message.message_id)

    elif message.video:
        # Handle video message
        video = message.video
        file_id = video.file_id
        # Use 'await' to asynchronously get the file
        file = await context.bot.get_file(file_id)
        # Use 'await' to asynchronously download the file as a byte array
        byte_array = await file.download_as_bytearray()
        # Save the video locally
        with open('downloaded_video.mp4', 'wb') as video_file:
            video_file.write(byte_array)
        # Send the video back to the user with the caption
        with open('downloaded_video.mp4', 'rb') as video_file:
            await context.bot.send_video(chat_id=group_id, video=video_file, caption=modified_text)
    elif message.document:
        # Handle document message
        document = message.document
        file_id = document.file_id
        # Use 'await' to asynchronously get the file
        file = await context.bot.get_file(file_id)
        # Use 'await' to asynchronously download the file as a byte array
        byte_array = await file.download_as_bytearray()
        # Save the document locally
        with open('downloaded_document.pdf', 'wb') as document_file:
            document_file.write(byte_array)
        # Send the document back to the user with the caption
        with open('downloaded_document.pdf', 'rb') as document_file:
            await context.bot.send_document(chat_id=group_id, document=document_file, caption=modified_text)

    else:
        # await context.bot.send_message(chat_id=message.chat_id, text=modified_text)
        await context.bot.send_message(chat_id=group_id, text=modified_text)


def main() -> None:
    update_queue = queue.Queue()
    updater = Updater(bot=Bot, update_queue=update_queue)

    start_handler = CommandHandler('start', start)
    message_handler = MessageHandler(
        filters.ALL & ~(filters.COMMAND), handle_message)

    application = Application.builder().token(
        "token").build()

    application.add_handler(start_handler)
    application.add_handler(message_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
