from config.parameters import desktop_systems, server_typenames


def is_desktop_name(name: str) -> bool:
    if len(name) < 4:
        return False

    return name[-4:].isdigit()


def is_desktop_os(os: str) -> bool:

    for desktop_system in desktop_systems:
        if desktop_system in os:
            return True

    return False


def asset_is_desktop(asset) -> bool:
    if asset["operating_system"]:
        return is_desktop_os(asset["operating_system"])
    return False


def asset_is_server(asset) -> bool:
    type = asset["typename"]
    os = asset["operating_system"]
    name = asset["name"]

    if not (type in server_typenames):
        return False

    if type == "Windows" and not os and is_desktop_name(name):
        return False
    if os and is_desktop_os(os):
        return False

    return True
