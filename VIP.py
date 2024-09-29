from flask import Flask
from threading import Thread
import re
from datetime import datetime
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError, UserNotParticipantError
import asyncio
app = Flask(__name__)
@app.route('/')
def index():
    return 'Server is running!'
def run_flask():
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

api_id = 23844616
api_hash = '4aeca3680a20f9b8bc669f9897d5402f'
bot_token = '7439119181:AAGNLDxB17VwJakp71O0q7SB2RhhTPD7Tw0'

# Create the client and connect
client = TelegramClient('quotex_results', api_id, api_hash).start(bot_token=bot_token)

# Dictionary to store trade results
trade_results = []

# Dictionary to map currency pairs to flags
currency_flags = {
    'AUDUSD': '🇦🇺🇺🇸',
'USDINR': '🇺🇸🇮🇳',
'USDINR': '🇺🇸🇮🇳',
'USD/EGP': '🇺🇸🇪🇬',
'EURUSD': '🇪🇺🇺🇸',
'GBP/NZD': '🇬🇧🇳🇿',
'USDJPY': '🇺🇸🇯🇵',
'USD/PKR': '🇺🇸🇵🇰',
'USD/BRL': '🇺🇸🇧🇷',
'AUD/NZD': '🇦🇺🇳🇿',
'EURCAD': '🇪🇺🇨🇦',
'EURJPY': '🇪🇺🇯🇵',
'GBPJPY': '🇬🇧🇯🇵',
'USD/BDT': '🇺🇸🇧🇩',
'EURSGD': '🇪🇺🇸🇬',
'GBPCAD': '🇬🇧🇨🇦',
'EURAUD': '🇪🇺🇦🇺',
'USDCAD': '🇺🇸🇨🇦',
'GBPCHF': '🇬🇧🇨🇭',
'NZDCAD': '🇳🇿🇨🇦',
'USDCOP': '🇺🇸🇨🇴',
'USDNGN': '🇺🇸🇳🇬',
'USDTRY': '🇺🇸🇹🇷',
'AUDCAD': '🇦🇺🇨🇦',
'USDARS': '🇺🇸🇦🇷',
'CADCHF': '🇨🇦🇨🇭',
'CHFJPY': '🇨🇭🇯🇵',
'GBPAUD': '🇬🇧🇦🇺',
'NZDCHF': '🇳🇿🇨🇭',
'NZDJPY': '🇳🇿🇯🇵',
'USDCHF': '🇺🇸🇨🇭',
'USDDZD': '🇺🇸🇩🇿',
'USDIDR': '🇺🇸🇮🇩',
'EURGBP': '🇪🇺🇬🇧',
'NZDUSD': '🇳🇿🇺🇸',
'USDMXN': '🇺🇸🇲🇽',
'AUDJPY': '🇦🇺🇯🇵',
'CADJPY': '🇨🇦🇯🇵',
}

# Define sticker IDs for win and loss
WIN_STICKER_ID = 180398513446716419  # Replace with your actual win sticker ID
LOSS_STICKER_ID = 180398513446716420  # Replace with your actual loss sticker ID

# Function to format numbers with emojis
def format_number_with_emojis(number):
    return ' '.join(f"{num}️⃣" for num in str(number))

# Function to extract trade details from a message
def extract_trade_details(message):
    pattern = r'📊 Currency: (.+?)-OTC\n⏳ Expiration: (.+?)\n⏱ Check-in: (.+?)\n↕️ Direction: (.+?)\n'
    match = re.search(pattern, message)
    if match:
        currency = match.group(1)
        return {
            'currency': currency,
            'expiration': match.group(2),
            'check_in': match.group(3),
            'direction': match.group(4).strip(),
            'result': 'Pending'  # Initialize with pending result
        }
    return None

# Event handler for new messages
@client.on(events.NewMessage)
async def handler(event):
    try:
        message = event.message.message
        print(f"Received Message: {message}")  # Log message to terminal
        
        if message == '/start':
            user = await client.get_entity(event.sender_id)
            user_name = user.first_name if user.first_name else "User"
            start_message = (
                f"𝙃𝙄 #{user_name} 𝙒𝙚𝙡𝙘𝙤𝙢𝙚 👋🏻 ❕\n"
                "〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️\n"
                "🎉 𝙎𝙤 𝙄 𝙈𝙖𝙙𝙚 𝙏𝙝𝙚 𝘽𝙤𝙩 𝙏𝙤 𝘿𝙚𝙘𝙡𝙖𝙧𝙚 𝙏𝙝𝙚\n"
                "𝙑𝙄𝙋 𝙎𝙚𝙨𝙨𝙞𝙤𝙣 𝙍𝙚𝙨𝙪𝙡𝙩𝙨 𝙄𝙣 𝙅𝙪𝙨𝙩 𝘼 𝘾𝙡𝙞𝙘𝙠 ❕\n"
                "〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️\n"
                "💬 𝙁𝙤𝙧 𝙎𝙪𝙥𝙥𝙤𝙧𝙩 𝙈𝙚𝙨𝙨𝙖𝙜𝙚 ➡️ @Advik_Ahooja\n"
                "〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️\n"
                "❤️ 𝙏𝙃𝘼𝙉𝙆𝙎 ❤️"
            )
            await event.respond(start_message)
            
        elif '📊 Currency' in message:
            trade_details = extract_trade_details(message)
            if trade_details:
                trade_results.append(trade_details)
                print(f"Trade details added: {trade_details}")  # Log added trade details
            
        elif event.message.sticker:
            sticker_id = event.message.media.document.id  # Get sticker ID
            print(f"Received Sticker File ID: {sticker_id}")
            
            if trade_results:  # Check if there are any trades to update
                last_trade = trade_results[-1]
                if sticker_id == WIN_STICKER_ID:
                    last_trade['result'] = '✅'  # Mark as WIN
                    print(f"Updated last trade with result: {last_trade}")  # Log updated trade details
                elif sticker_id == LOSS_STICKER_ID:
                    last_trade['result'] = '💔'  # Mark as Loss
                    print(f"Updated last trade with result: {last_trade}")  # Log updated trade details

    except (FloodWaitError, UserNotParticipantError) as e:
        print(f"Error occurred: {str(e)}")
        await event.respond("An error occurred. Please try again later.")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")  # Log unexpected errors
        await event.respond("An unexpected error occurred. Please contact support.")

# Event handler for /result command
@client.on(events.NewMessage(pattern='/result'))
async def result_command_handler(event):
    try:
        # Generate the report
        report = '📋 **REPORT**\n🗒️ {}\n\n'.format(datetime.now().strftime('%A, %b %d, %Y'))
        
        for trade in trade_results:
            # Remove 'OTC' from currency for matching with the flag
            currency = trade['currency'].replace('-OTC', '')
            flags = currency_flags.get(currency, '')
            result = trade.get('result', 'Pending')  # Use 'Pending' if no result is set
            
            # Check the direction and set the appropriate arrow
            if 'UP' in trade['direction'] or '🟢UP' in trade['direction'] or '🟢 UP' in trade['direction']:
                direction_arrow = '⬆️'
            elif 'DOWN' in trade['direction'] or '🔴DOWN' in trade['direction'] or '🔴 DOWN' in trade['direction']:
                direction_arrow = '⬇️'
            else:
                direction_arrow = '❓'  # Optional: handle unexpected cases
            
            # Check if the trade result is 'Pending'
            if result == 'Pending':
                report += 'RECOVERY 👇🏻👇🏻👇🏻👇🏻\n'
            else:
                # Add trade details without extra line gaps
                report += '{} | {} | {} | {} | {}\n'.format(
                    direction_arrow,
                    trade['check_in'],
                    flags,
                    trade['currency'],
                    result
                )
        
        # Count wins and losses
        wins = sum(1 for trade in trade_results if trade['result'] == '✅')
        losses = sum(1 for trade in trade_results if trade['result'] == '💔')

        report += '\n✅ WINS {} × {} LOSS❌'.format(format_number_with_emojis(wins), format_number_with_emojis(losses))

        # If there are no trades, handle it gracefully
        if not trade_results:
            report = "No trades have been recorded yet."
        
        await event.respond(report)
        print(f"Generated Report:\n{report}")  # Log the report to terminal

    except Exception as e:
        print(f"Unexpected error in result command: {str(e)}")  # Log unexpected errors
        await event.respond("An unexpected error occurred while generating the report.")

# Event handler for /clear command
@client.on(events.NewMessage(pattern='/clear'))
async def clear_command_handler(event):
    try:
        trade_results.clear()  # Clear the trade results
        await event.respond("Trade results cleared! You can now start a new session.")
    except Exception as e:
        print(f"Unexpected error in clear command: {str(e)}")  # Log unexpected errors
        await event.respond("An unexpected error occurred while clearing the trade results.")

flask_thread = Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()

# Start the bot
print("Bot is running...")
client.run_until_disconnected()
