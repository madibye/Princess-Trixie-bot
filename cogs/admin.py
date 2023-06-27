from discord import Guild, TextChannel
from discord.ext import commands

import config
from config.live_config import lc
from handlers import database, embedding
from main import Amelia


class Admin(commands.Cog, name="admin"):
    def __init__(self, bot):
        self.bot: Amelia = bot
        self.leadership_channel: TextChannel | None = None
        self.guild: Guild | None = None

    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = self.bot.get_guild(config.guild_id)

    @commands.has_role("alpha koala")
    @commands.command(name="viewconfig", aliases=["vc"])
    async def view_all_config(self, ctx):
        key_list = [item for item in lc.__slots__ if type(getattr(lc, item)) in [str, int, bool, float]]
        text_list = []
        for key in key_list:
            text_list.append(f"{key}: {getattr(lc, key)}")
            if description := database.get_config_description(key):
                text_list[-1] += f"  # {description}"
        await embedding.create_info_list_embed(
            ctx=ctx,
            title="Config List",
            description=f"{len(key_list)} total config values",
            field_name="The current config values are:",
            value_list=text_list,
            send_after=True,
            error_msg="Couldn't find any config entries in the db!"
        )

    @commands.has_role("alpha koala")
    @commands.command(name="setconfigvalue", aliases=["scv"])
    async def set_config_value(self, ctx, key: str, new_value: str):
        if config.scv_blocked.get(key):
            return await ctx.send(f"This is a blocked key! Use `{config.scv_blocked[key]}` instead.", reference=ctx.message)
        if key not in lc.__slots__:
            await ctx.message.add_reaction("❌")
            return await ctx.send(
                f"The specified key is not in the list of config entries that can be changed using this command, sorry!",
                reference=ctx.message
            )
        attr = getattr(lc, key)
        try:
            if type(attr) == int:
                new_value = int(new_value)
            elif type(attr) == float:
                new_value = float(new_value)
            elif type(attr) == bool:
                new_value = new_value in ['true', 'True', 't', 'T', '1', 'yes', 'Yes', 'YES']
        except ValueError:
            await ctx.message.add_reaction("❌")
            return await ctx.send(
                f"You must specify a new value of the correct datatype.",
                reference=ctx.message
            )
        lc.set(key, new_value)
        await ctx.message.add_reaction("✅")

    @commands.has_role("alpha koala")
    @commands.command(name="setconfigdescription", aliases=["scd"])
    async def set_config_description(self, ctx, key: str, *args):
        if not args:
            await ctx.message.add_reaction("❌")
            return await ctx.send(f"Please specify a description to be set!", reference=ctx.message)
        new_description = " ".join(args)
        key_list = [item for item in lc.__slots__ if type(getattr(lc, item)) in [str, int, bool, float]]
        if key not in key_list:
            await ctx.message.add_reaction("❌")
            return await ctx.send(
                f"The specified key is not in the list of config entries that can be changed using this command, sorry!",
                reference=ctx.message)
        database.set_config_description(key, new_description)
        await ctx.message.add_reaction("✅")


async def setup(client):
    await client.add_cog(Admin(client))
