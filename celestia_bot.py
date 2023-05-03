import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


import requests

# API token Celestia API URL
TELEGRAM_API_TOKEN = '-'
CELESTIA_API_URL = '-'

def start(update: Update, context: CallbackContext):
    update.message.reply_text('Hello, I am the Telegram Explorer bot for Celestia Blockspacerace-0. Currently, I can only perform block number queries and I am still in the development stage. Please send me the block number you would like to search for.')

def search_block_or_tx(update: Update, context: CallbackContext):
    query = update.message.text.strip()

    try:
        response = requests.get(f'{CELESTIA_API_URL}/block?height={query}')
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            try:
                response = requests.get(f'{CELESTIA_API_URL}/tx?hash={query}')
                response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                update.message.reply_text('Im sorry, but no results were found. Please try another query.')
                return
        else:
            update.message.reply_text('An error has occurred. Please try again.')
            return

    data = response.json()

    if 'result' in data:
        result = format_data(data['result'])
        update.message.reply_text(result)
    else:
        update.message.reply_text('Im sorry, but no results were found. Please try another query.')

def status(update: Update, context: CallbackContext):
    try:
        response = requests.get(f'{CELESTIA_API_URL}/status?')
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        update.message.reply_text('An error has occurred. Please try again.')
        return

    data = response.json()
    result = format_status_data(data)
    update.message.reply_text(result)

def format_status_data(data):
    
    result = ""

    node_info = data['result']['node_info']
    result += f"Node ID: {node_info['id']}\n"
    result += f"Node Version: {node_info['version']}\n"
    result += f"Node Network: {node_info['network']}\n"
    result += f"Node Listen Address: {node_info['listen_addr']}\n"
    result += f"Node Moniker: {node_info['moniker']}\n"

    sync_info = data['result']['sync_info']
    result += f"Latest Block Hash: {sync_info['latest_block_hash']}\n"
    result += f"Latest App Hash: {sync_info['latest_app_hash']}\n"
    result += f"Latest Block Height: {sync_info['latest_block_height']}\n"
    result += f"Latest Block Time: {sync_info['latest_block_time']}\n"
    result += f"Earliest Block Hash: {sync_info['earliest_block_hash']}\n"
    result += f"Earliest App Hash: {sync_info['earliest_app_hash']}\n"
    result += f"Earliest Block Height: {sync_info['earliest_block_height']}\n"
    result += f"Earliest Block Time: {sync_info['earliest_block_time']}\n"
    result += f"Catching Up: {sync_info['catching_up']}\n"

    validator_info = data['result']['validator_info']
    result += f"Validator Address: {validator_info['address']}\n"
    result += f"Validator Public Key: {validator_info['pub_key']['value']}\n"
    result += f"Validator Voting Power: {validator_info['voting_power']}\n"

    return result



def format_data(data):
    
    result = ""

    if 'block' in data:
        block = data['block']
        header = block['header']
        height = int(header['height'])
        success = "Successful" if height > 0 else "Unsuccessful"

        result += f"Block Height: {height}\n"
        result += f"Block Hash: {data['block_id']['hash']}\n"
        result += f"Timestamp: {header['time']}\n"
        result += f"Chain ID: {header['chain_id']}\n"
        result += f"Validators Hash: {header['validators_hash']}\n"
        result += f"Next Validators Hash: {header['next_validators_hash']}\n"
        result += f"Consensus Hash: {header['consensus_hash']}\n"
        result += f"App Hash: {header['app_hash']}\n"
        result += f"Status: {success}\n"
        result += f"\nMintscan URL: https://testnet.mintscan.io/celestia-incentivized-testnet/blocks/{height}\n"
    else:
        result = "I'm sorry, but no results were found."

    return result
    
def explorer(update: Update, context: CallbackContext):
    update.message.reply_text("If you would like to examine your wallet address and other transactions in detail, you can do so on the original explorer website. Here is the Explorer website: https://testnet.mintscan.io/celestia-incentivized-testnet")

def itntasks(update: Update, context: CallbackContext):
    update.message.reply_text("You can access the tasks of the incentivized network from this link. Visit the website, scroll down to the bottom of the page, and start examining the details and performing the tasks. https://docs.celestia.org/nodes/blockspace-race/")
    
def docs(update: Update, context: CallbackContext):
    update.message.reply_text("You can access Celestia Network's articles to obtain more detailed information about the network. This way, you can have a better understanding of Celestia Network. https://docs.celestia.org/")

def website(update: Update, context: CallbackContext):
    update.message.reply_text("The first modular blockchain network https://celestia.org/")
    
def termsofservice(update: Update, context: CallbackContext):
    update.message.reply_text("A link to Celestia’s Incentivized Testnet Supplemental Terms can be found here. Those incorporate our website Terms of Service by reference. We encourage you to review and familiarise yourself with all relevant terms. https://celestia.org/tos/ https://docs.celestia.org/nodes/blockspace-race/")

def privacy(update: Update, context: CallbackContext):
    update.message.reply_text("A link to our Privacy Policy can be found here. https://celestia.org/privacy/")
    
def main():
    updater = Updater(TELEGRAM_API_TOKEN)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("status", status))
    dp.add_handler(CommandHandler("explorer", explorer))
    dp.add_handler(CommandHandler("itntasks", itntasks))
    dp.add_handler(CommandHandler("docs", docs))
    dp.add_handler(CommandHandler("website", website))
    dp.add_handler(CommandHandler("termsofservice", termsofservice))
    dp.add_handler(CommandHandler("privacy", privacy))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, search_block_or_tx))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
