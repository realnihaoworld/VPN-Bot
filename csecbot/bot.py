import discord
import responses
from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend
from dotenv import dotenv_values
# from io import BytesIO

import codecs
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
from cryptography.hazmat.primitives import serialization

from configparser import ConfigParser

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
        
        config = ConfigParser()
        config['Interface'] = {
            'PrivateKey': codecs.encode(bytes_, 'base64').decode('utf8').strip(),
            'Address': 'temp',
            'DNS': '172.29.1.1'
        }
        config['Peer'] = {
            'PublicKey': codecs.encode(pubkey, 'base64').decode('utf8').strip(),
            'AllowedIPs': 'temp',
            'Endpoint': 'temp'
        }

        with open('config.ini', 'w') as conf:
            config.write(conf)

        #public_key_file = BytesIO(config.ini)
        config_file = discord.File(fp='config.ini', filename="test.conf")
        await interaction.response.send_message(
            content=f"Here is your Config File!",
            ephemeral=True,
            file=config_file
            )
    
    client.run(TOKEN)