from keep_alive import keep_alive
import discord
import google.generativeai as genai
import os

# --- CONFIGURATION ---
GEMINI_API_KEY = "AIzaSyC8ieqq6sLnKJXTErXSytKdsgjGIw8G0A8" 
DISCORD_TOKEN = "MTQ1MDE0NDQ1ODA0NDg2NjcxMQ.G5quKi.TFQTKqQbaLYvNqMkIp2wZ0wpvWqnv0yV9eYF5Y"
# REPLACE THIS WITH YOUR CHANNEL ID (It must be a number, not a string)
TARGET_CHANNEL_ID = 1450146914933932234

# 1. Configure Gemini
os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-2.5-flash')

# 2. Configure Discord Client
intents = discord.Intents.default()
intents.message_content = True 

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    print(f'Listening only in channel ID: {TARGET_CHANNEL_ID}')

@client.event
async def on_message(message):
    # 1. Stop the bot from replying to itself (Prevents infinite loops)
    if message.author == client.user:
        return

    # 2. Check if the message is in the specific channel
    if message.channel.id == TARGET_CHANNEL_ID:
        
        # (Optional) Ignore empty messages (like images without text)
        if not message.content:
            return

        print(f"Message received from {message.author}: {message.content}")

        async with message.channel.typing():
            try:
                # Send the user's message to Gemini
                response = await model.generate_content_async(message.content)
                response_text = response.text

                # Split message if longer than 2000 chars
                if len(response_text) > 2000:
                    chunks = [response_text[i:i+1900] for i in range(0, len(response_text), 1900)]
                    for chunk in chunks:
                        await message.channel.send(chunk)
                else:
                    await message.channel.send(response_text)

            except Exception as e:
                await message.channel.send(f"I encountered an error: {e}")
                print(f"Error: {e}")

# Run the bot
keep_alive()
client.run(DISCORD_TOKEN)
