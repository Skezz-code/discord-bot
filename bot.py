import discord
from discord.ext import commands
import asyncio
import os
from datetime import datetime, timedelta

# =========================
# INTENTS
# =========================
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# =========================
# START
# =========================
@bot.event
async def on_ready():
    print(f"БОТ ОНЛАЙН: {bot.user}")

# =========================
# FORMAT TIME
# =========================
def parse_duration_to_seconds(text: str):
    text = text.lower().strip()
    parts = text.split()

    if len(parts) == 1:
        if "навсегда" in text:
            return None
        return None

    try:
        number = int(parts[0])
    except:
        return None

    unit = parts[1]

    if "д" in unit:
        return number * 86400
    elif "м" in unit:
        return number * 2592000
    else:
        return None


def format_duration(text: str):
    text = text.lower().strip()
    parts = text.split()

    if len(parts) == 1:
        if "навсегда" in text:
            return "Навсегда"
        return text

    number = parts[0]
    unit = parts[1]

    if "д" in unit:
        return f"{number} дней"
    elif "м" in unit:
        return f"{number} месяцев"

    return text


# =========================
# AUTO REMOVE ROLE
# =========================
async def auto_remove_role(member, role, seconds, log_channel):
    await asyncio.sleep(seconds)

    try:
        await member.remove_roles(role)

        if log_channel:
            await log_channel.send(
                f"⏳ Срок закончился — роль {role.mention} снята с {member.mention}"
            )
    except:
        pass


# =========================
# COMMAND
# =========================
@bot.command(name="audit")
async def audit(ctx, member: discord.Member, role: discord.Role, duration: str, *, reason: str):

    # удаляем команду
    try:
        await ctx.message.delete()
    except:
        pass

    seconds = parse_duration_to_seconds(duration)

    # выдача роли
    await member.add_roles(role)

    # время окончания
    if seconds is None:
        expires = "Навсегда"
    else:
        expires = format_seconds(seconds)

    # embed
    embed = discord.Embed(
        title="📋 КАДРОВЫЙ АУДИТ",
        color=discord.Color.blue()
    )

    embed.add_field(name="👤 Сотрудник", value=member.mention, inline=False)
    embed.add_field(name="⬆️ Должность", value=role.mention, inline=False)
    embed.add_field(name="⏳ Срок", value=expires, inline=False)
    embed.add_field(name="📝 Причина", value=reason, inline=False)

    await ctx.send(embed=embed)

    # авто-снятие роли
    if seconds:
        asyncio.create_task(auto_remove_role(member, role, seconds, ctx.channel))

    # авто-снятие роли
    if seconds:
        asyncio.create_task(auto_remove_role(member, role, seconds, ctx.channel))

# =========================
# RUN (RAILWAY READY)
# =========================
bot.run(os.getenv("DISCORD_TOKEN"))
