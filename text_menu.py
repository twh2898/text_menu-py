
from typing import List, Callable, Optional, Union, Tuple
from collections.abc import Iterable
from simple_term_menu import TerminalMenu

__version__ = '0.1.1'

Default = Optional[Union[str, Callable[[], str]]]
IntDefault = Optional[Union[int, Callable[[], int]]]
Validator = Callable[[str], bool]
Options = Union[Iterable[str], Callable[[], Iterable[str]]]
Result = Union[str, bool, Tuple[int, str]]


def select_text(title: str, default: Default = None, validator: Validator = any) -> str:
    if callable(default):
        default = default()

    if default:
        title += '(default {})'.format(default)
    title += ': '

    while True:
        choice = input(title)

        if len(choice) == 0:
            if default is not None:
                choice = default
            else:
                continue

        if validator(choice):
            return choice


def select_bool(title: str, default: bool = False):
    if default:
        title += ' [Yn]: '
    else:
        title += ' [yN]: '

    while True:
        choice = input(title).lower()

        if len(choice) == 0:
            return default

        if choice in ['n', 'y']:
            return choice == 'y'


def select_choice(title: str, options: Options, allow_new: bool = False, default: IntDefault = 0, validator: Validator = any):
    if callable(options):
        options = options()

    if options is None:
        raise ValueError('options must not be None')
    options = list(options)

    if allow_new:
        options.append('New')

    if callable(default):
        default = default()

    tm = TerminalMenu(options, title=title, cursor_index=default, show_search_hint=True)
    entry = tm.show()

    if entry is None:
        raise KeyboardInterrupt()  # Get out, like ^C during text input
    elif isinstance(entry, tuple):  # Shouldn't be possible without multi select
        entry = entry[0]

    if allow_new:
        if entry == len(options) - 1:
            options[entry] = select_text(title, validator=validator)
        else:
            options.pop()

    return entry, options[entry]


class MenuItem:
    key: str
    title: str
    result: Optional[Result]

    def __init__(self, key: str, title: str):
        self.key = key
        self.title = title
        self.result = None

    def show(self) -> Result:
        raise NotImplementedError('Please implement show')


class SelectTextItem(MenuItem):
    def __init__(self, key: str, title: str, default: Default = None, validator: Validator = any):
        self.key = key
        self.title = title
        self.default = default
        self.validator = validator
        self.result = None

    def show(self) -> str:
        self.result = select_text(self.title, self.default, self.validator)
        return self.result


class SelectBoolItem(MenuItem):
    def __init__(self, key: str, title: str, default: bool = False):
        self.key = key
        self.title = title
        self.default = default
        self.result = None

    def show(self) -> bool:
        self.result = select_bool(self.title, self.default)
        return self.result


class SelectChoiceItem(MenuItem):
    def __init__(self, key: str, title: str, options: Options, allow_new: bool = False, default: IntDefault = 0, validator: Validator = any):
        self.key = key
        self.title = title
        self.options = options
        self.allow_new = allow_new
        self.default = default
        self.validator = validator
        self.result = None

    def show(self) -> Tuple[int, str]:
        self.result = select_choice(
            self.title, self.options, self.allow_new, self.default, self.validator)
        print(self.title + ':', self.result[1])
        return self.result


class Menu:
    def __init__(self, title: str):
        self.title = title
        self.menu: List[MenuItem] = []

    def add_text(self, key: str, title: str, default: Default = None, validator: Validator = any):
        item = SelectTextItem(key, title, default, validator)
        self.menu.append(item)
        return item

    def add_bool(self, key: str, title: str, default: bool = False):
        item = SelectBoolItem(key, title, default)
        self.menu.append(item)
        return item

    def add_choice(self, key: str, title: str, options: Options, allow_new: bool = False, default: IntDefault = 0, validator: Validator = any):
        item = SelectChoiceItem(key, title, options,
                                allow_new, default, validator)
        self.menu.append(item)
        return item

    def add_nested_choice(self, key: str, title: str, options: Options, allow_new: bool = False, default: IntDefault = 0, validator: Validator = any):
        raise NotADirectoryError('Please implement add_nested_choice')

    def show(self):
        res = {}
        for item in self.menu:
            res[item.key] = item.show()
        return res
