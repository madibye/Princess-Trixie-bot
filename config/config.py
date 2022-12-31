import os
from dataclasses import dataclass
from typing import List, Optional

from dotenv import load_dotenv


@dataclass
class RolePickerInfo:
    channel_id: Optional[int] = 0
    embed_name: Optional[str] = "👋 Hey there! What are your pronouns?"
    embed_desc: Optional[str] = "Use the buttons below to select what pronouns you'd like us to display for you."
    role_ids: Optional[List[int]] = None
    max_row_length: Optional[int] = 5
    message_data: Optional[dict] = None

    def __post_init__(self):
        # We should instantiate a default list & dict for these two
        if not self.role_ids:
            self.role_ids = []
        if not self.message_data:
            self.message_data = {'channel_id': 0, 'message_id': 0}


load_dotenv()

_true = ["true", "True", "t", "T", "1", "yes", "Yes", "YES"]

guild_id = 991518170542260336

mongo_url = os.environ.get("MONGO_URL", "mongodb://mongo/")

activity_text = "hi hi :)"
command_prefixes = ['!']

# Roles
ccgse_notif_role = 996963548959871069
minecraft_notif_role = 1007714356189991083
club_notif_role = 1007714385642393655

ccgse_channel = 993962449717960836
minecraft_channel = 1009699321651925022
club_channel = 991544912556339241

remindme_ignore_words = ["this"]
remindme_remove_words = ["in", "and", "on", "at", "@"]

discord_token = os.environ.get("PRINCESS_TRIXIE_TOKEN")
bot_application_id = 925087331915022377
discord_cogs = [
    "cogs.reminders",
    "cogs.type",
    "cogs.threads",
    "cogs.roles",
    "cogs.notifications",
    "cogs.role_picker",
]

default_role_picker_info = {}
