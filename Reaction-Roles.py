import discord
from discord.ext import commands
import json

TOKEN = "" # Token hier einfügen 
SERVER_ID = 000000000000000000
reactionroles = {
    "MessageID": {
        "Emoji": {
            "roles": []
        }
    },
    "955221797551353857": { # Nachrichten ID
        "😎": { # Emoji 
            "roles": [000000000000000000] # Rollen ID
        },
        "😎": { # Emoji 
            "roles": [000000000000000000] # Rollen ID
        }
    },
    "956988191586541608": { # Nachrichten ID
        "✅": { # Emoji 
            "roles": [000000000000000000] # Rollen ID 
        }
    }
}

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command("help")

@bot.event
async def on_ready():
    print("Reaction Role ready!")

async def manage_reaction(payload: discord.RawReactionActionEvent, type=None):
    try:
        if str(payload.message_id) in reactionroles.keys():
            if str(payload.emoji) in reactionroles[str(payload.message_id)].keys():
                guild = bot.get_guild(SERVER_ID)
                member = guild.get_member(payload.user_id)
                if member.bot:
                    return
                for r in reactionroles[str(payload.message_id)][str(payload.emoji)]["roles"]:
                    role = guild.get_role(int(r))
                    if not role:
                        print(f"Rolle {r} nicht gefunden!")
                        continue
                    if type == "add":
                        await member.add_roles(role, reason="Reaction Role")
                    elif type == "remove":
                        await member.remove_roles(role, reason="Reaction Role")
    except Exception as e:
        print(f"Fehler aufgetreten:\nAchte darauf, dass die die Json-Datei richtig formatiert ist und die Emojis bzw Rollen ID´s korrekt sind!\nError:\n{e}")

@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    if payload.guild_id == SERVER_ID:
        await manage_reaction(payload, "add")

@bot.event
async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent):
    if payload.guild_id == SERVER_ID:
        await manage_reaction(payload, "remove")

@commands.has_permissions(administrator=True)
@bot.command()
async def react(ctx, message: discord.Message):
    await ctx.message.delete()
    if not str(message.id) in reactionroles.keys():
        return await ctx.send("Diese Nachricht wurde nicht konfiguriert.", delete_after=5)
    else:
        for emoji in reactionroles[str(message.id)].keys():
            await message.add_reaction(emoji)
        await ctx.send("Erledigt!", delete_after=5)

bot.run(TOKEN)