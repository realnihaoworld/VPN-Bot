import discord
import responses


async def send_message(message, user_message):
    try:
        response = responses.handle_response(user_message)
        await message.channel.send(response)
    except Exception as e:
        print(e)


def run_discord_bot():
    TOKEN = 'MTE2Mzk0NzI2OTU3NDM3NzU4NQ.G7Vf0X.4qFthX-TpzPFXT_qhCqy6NRLlXgzMHVsJcfg2U'

    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    # intents = discord.Intents.default()
    # client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        # prevents the output of the bot from being used as an input
        if message.author == client.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        # debugging
        print(f"{username} said: '{user_message}' in {channel}")

        if message.content:
            await send_message(message, user_message)

    client.run(TOKEN)