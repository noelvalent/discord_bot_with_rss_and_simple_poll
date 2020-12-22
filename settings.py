from get_from_xml import get_startup, get_command_xml


COMMANDS = get_command_xml()
DISCORD_TOKEN = get_startup()['discord_token']
PREFIX = get_startup()['prefix']
UPDATE_TIME = get_startup()['update_time']