import discord
from discord.ext import commands
import requests
import os

from model import get_class  # get_class fonksiyonunun model.py içinde tanımlı olduğunu varsayıyoruz

# Bot için gerekli izinleri (intents) ayarlıyoruz
intents = discord.Intents.default()
intents.message_content = True  

# Botu başlatıyoruz
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} ({bot.user.id})")
    print("------")

# Basit bir echo komutu (heh heh heh gibi)
@bot.command(name="anladım")
async def echo(ctx, *, count_heh: int = 5):
    await ctx.send("hee" * count_heh)
@bot.command(name="hello")
async def echo(ctx):
    await ctx.send("Hello, i am AIbob,What's your name?" )


# Rastgele ördek fotoğrafı getiren yardımcı fonksiyon
def get_duck_image_url():
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']

# !duck komutu: ördek fotoğrafı gönderir
@bot.command(name='duck')
async def duck(ctx):
    '''The duck command returns the photo of the duck'''
    image_url = get_duck_image_url()
    await ctx.send(image_url)

# !check komutu: resim yüklenmişse sınıflandırma yapar
@bot.command(name="check")
async def check(ctx):
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            try:
                file_path = f"./{attachment.filename}"
                await attachment.save(file_path)
                
                result = get_class(
                    model_path="./keras_model.h5",
                    label_path="./labels.txt",
                    img_path=file_path
                )
                
                await ctx.send(f"RESİMDEKİ NESNE: {result}")
            except Exception as e:
                await ctx.send(f"Error occurred: {e}")
    else:
        await ctx.send("You forgot to upload the image :(")





bot.run("MTQwOTk2MDI3MTYwNjQ1MjM0MA.G8VrDy.qJXB_uuv41XpftGzaaxxAUUcuUOdlZxdO2ULY8")
