import discord
import responses
from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend
from dotenv import dotenv_values
from io import BytesIO

import codecs
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
from cryptography.hazmat.primitives import serialization

import configparser

config = dotenv_values(".env")

TOKEN = config["DISCORD_TOKEN"]

async def send_message(message, user_message):
    try:
        response = responses.handle_response(user_message)
        await message.channel.send(response)
    except Exception as e:
        print(e)


def run_discord_bot():

    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
    client.tree = discord.app_commands.CommandTree(client)

    # intents = discord.Intents.default()
    # client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        await client.tree.sync()
        print(f'{client.user} is now running!')
        
    @client.tree.command(name="hello")
    async def hello(interaction: discord.Interaction):
        await interaction.response.send_message(f"Hi, {interaction.user.mention}")

    @client.tree.command(name="generate")
    async def generate(interaction: discord.Interaction):
        # generate private key
        private_key = X25519PrivateKey.generate()
        bytes_ = private_key.private_bytes(  
            encoding=serialization.Encoding.Raw,  
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption()
        )
        print(codecs.encode(bytes_, 'base64').decode('utf8').strip())

        # derive public key
        pubkey = private_key.public_key().public_bytes(encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw)
        print(codecs.encode(pubkey, 'base64').decode('utf8').strip())
        
        config = configparser.ConfigParser()
        config['Interface'] = {'PrivateKey': codecs.encode(bytes_, 'base64').decode('utf8').strip(),
                               'Address': '10.20.1.x/24'}
        config['Peer'] = {'PublicKey': codecs.encode(pubkey, 'base64').decode('utf8').strip(),
                          'AllowedIPs': 'temp',
                          'Endpoint': 'temp'}
        

        public_key_file = BytesIO(pubkey)
        public_key_discord_file = discord.File(fp=public_key_file, filename="test.conf")
        await interaction.response.send_message(
            content=f"Here is your X25519 Public Key!",
            ephemeral=True,
            file=public_key_discord_file
            )
    
    
    
    # @client.event
    # async def on_message(message):
    #     # prevents the output of the bot from being used as an input
    #     if message.author == client.user:
    #         return

    #     username = str(message.author)
    #     user_message = str(message.content)
    #     channel = str(message.channel)

    #     # debugging
    #     print(f"{username} said: '{user_message}' in {channel}")

    #     if message.content:
    #         await send_message(message, user_message)

    
    client.run(TOKEN)