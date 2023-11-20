from utils.colors import colors


def color_input(prompt):
    return input(f"{colors.OKGREEN}{prompt}{colors.ENDC}")
