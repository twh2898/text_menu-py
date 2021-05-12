
def select_path(msg, default=None):
    if default is not None:
        msg += '({}): '.format(default)
    else:
        msg += '(): '
    while 1:
        choice = input(msg)
        if len(choice) == 0 and default is not None:
            return default

        if choice:
            return choice


def select_bool(msg, default=False):
    if default:
        msg += ' (Yn): '
    else:
        msg += ' (yN): '
    while 1:
        choice = input(msg).lower()
        if len(choice) == 0:
            return default
        elif choice in ['n', 'y']:
            return choice == 'y'


def select_numeric_choice(msg, options, default=None):
    if default is not None:
        msg += ' ({}): '.format(default)
    else:
        msg += ' (): '
    while 1:
        for i, k in enumerate(options):
            print(' {}) {}'.format(i, k))

        choice = input(msg)
        if len(choice) == 0 and default is not None:
            return default

        try:
            choice = int(choice)
            if choice >= 0 and choice < len(options):
                return choice
        except ValueError:
            pass


def select_text_choice(msg, options, default=None):
    if default is not None:
        msg += ' ({}): '.format(default)
    else:
        msg += ' (): '
    while 1:
        for k in options:
            print(' ', k)
        choice = input(msg)
        if len(choice) > 0 and choice in options:
            return choice
        elif default is not None:
            return default


def select_choice(msg, options, default=None, use_numeric=True):
    if use_numeric:
        return select_numeric_choice(msg, options, default)
    else:
        return select_text_choice(msg, options, default)
