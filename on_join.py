import discord
import asyncio
from ledger import Ledger

client = discord.Client()

ledger = Ledger()
@client.event
async def on_member_join(member):
    ledger.add_user(userid=member.id, clientid=member.name)

client.run('clientid')
