import discord
import responses
from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend
from dotenv import dotenv_values
from io import BytesIO
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
        key = rsa.generate_private_key(
            backend=crypto_default_backend(),
            public_exponent=65537,
            key_size=2048
            )
        
        public_key = key.public_key().public_bytes(
            crypto_serialization.Encoding.OpenSSH,
            crypto_serialization.PublicFormat.OpenSSH
            )
        
        public_key_file = BytesIO(public_key)
        public_key_discord_file = discord.File(fp=public_key_file, filename="id_rsa.pub")
        await interaction.response.send_message(
            content=f"Here is your RSA-256 Public Key!",
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