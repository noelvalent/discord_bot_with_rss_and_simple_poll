import xml.etree.ElementTree as elemTree


def get_command_xml():
    def get_cmd_and_desc(root):
        cmd = root.find('command').text
        desc = root.find('description').text
        return {'command': cmd, 'description': desc}

    tree = elemTree.parse('./command.xml')
    return {
        'poll': get_cmd_and_desc(tree.find('poll')),
        'rss_add': get_cmd_and_desc(tree.find('rss-add')),
        'rss_del': get_cmd_and_desc(tree.find('rss-del')),
        'rss_list': get_cmd_and_desc(tree.find('rss-list')),
        'rss_update': get_cmd_and_desc(tree.find('rss-update')),
    }


def get_startup():
    tree = elemTree.parse('./command.xml')
    settings = tree.find('setting')
    rss = settings.find('rss')
    return {
        'prefix': settings.find('prefix').text,
        'discord_token': settings.find('discord_token').text,
        'db_name': settings.find('db_name').text,
        'update_time': rss.find('update_time').text,
    }
