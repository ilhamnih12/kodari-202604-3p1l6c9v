import os
import logging
from dotenv import load_dotenv

from neonize.client import NewClient
from neonize.events import ConnectedEv, MessageEv, QREv

# Command handlers imports
from commands import fun, economy, menu, games, utility, math, trivia, anime, memes, moderation, social

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
log = logging.getLogger("FunBot-WhatsApp")

client = NewClient("db.sqlite3")

COMMANDS = {}

def register_commands():
    # Register commands mapping
    COMMANDS.update(fun.get_commands())
    COMMANDS.update(economy.get_commands())
    COMMANDS.update(menu.get_commands())
    COMMANDS.update(games.get_commands())
    COMMANDS.update(utility.get_commands())
    COMMANDS.update(math.get_commands())
    COMMANDS.update(trivia.get_commands())
    COMMANDS.update(anime.get_commands())
    COMMANDS.update(memes.get_commands())
    COMMANDS.update(moderation.get_commands())
    COMMANDS.update(social.get_commands())

@client.event(QREv)
def on_qr(client: NewClient, event: QREv):
    log.info("Scan the QR Code to login!")

@client.event(ConnectedEv)
def on_connected(client: NewClient, event: ConnectedEv):
    log.info("Connected to WhatsApp!")

@client.event(MessageEv)
def on_message(client: NewClient, message: MessageEv):
    # Ignore our own messages
    if message.info.messageSource.isFromMe:
        return

    # Extract text from message
    text = ""
    if message.message.conversation:
        text = message.message.conversation
    elif message.message.extendedTextMessage and message.message.extendedTextMessage.text:
        text = message.message.extendedTextMessage.text

    text = text.strip()

    if not text.startswith("/"):
        return

    # Basic arg parsing
    parts = text.split(" ")
    command_name = parts[0][1:].lower() # remove slash
    args = parts[1:]

    # Parse sender user ID (JID)
    sender = message.info.sender
    sender_jid = f"{sender.user}@{sender.server}"

    log.info(f"Command received: {command_name} from {sender_jid}")

    if command_name in COMMANDS:
        try:
            COMMANDS[command_name](client, message, args, sender_jid)
        except Exception as e:
            log.error(f"Error executing command {command_name}: {e}")
            client.reply_message(f"Error: {str(e)}", message)

if __name__ == "__main__":
    log.info("Starting WhatsApp bot...")
    register_commands()
    client.connect()
