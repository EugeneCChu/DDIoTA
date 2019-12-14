from .synonym_acronym import handle_syn_acr

command_device = {
    "TV": ["set", "change", "turn"],
    "AC": ["set"],
    "light": ["turn"],
    "tank": ["fill"],
    "door": ["open", "close"],
    "drone": ["take off", "land", "set"],
}

parameter_device = {
    "TV": ["channel", "volume", "brightness"],
    "AC": ["temperature"],
    "drone": ["speed", "altitude"],
}


def final_device(command):
    i = 1

    for item in parameter_device.keys():
        if command[i] in parameter_device[item]:
            command[i] = item
            return command

    if command[i] not in command_device.keys():
        syn, acr = handle_syn_acr(command[i])
        if syn:
            for item in syn:
                if item in command_device.keys():
                    command[i] = item
                    return command
        elif acr:
            if acr[0] in command_device.keys():
                command[i] = acr[0]
                return command
    return command


def final_action(command):
    i = 0
    if command[1] not in command_device.keys():
        return command

    if command[i] not in command_device[command[1]]:
        syn, acr = handle_syn_acr(command[i])
        if syn:
            for item in syn:
                if item in command_device[command[1]]:
                    command[0] = item
                    return command
        elif acr:
            if acr[0] in command_device[command[1]]:
                command[0] = item
                return command
    return command
