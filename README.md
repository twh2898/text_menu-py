# text_menu-py

A set of console menu functions.


## Usage

```py
from text_menu import select_text, select_bool, select_choice

t = select_text('Add a name or path')
b = select_bool('Message here', default=True)
tc = select_choice('Choice of text', ['One', 'Two'], use_numeric=False)
nc = select_choice('Choice of index', ['One', 'Two'], use_numeric=True)
```

## Installing

```sh
$ pip install https://gitlab.com/twh2898/text_menu-py
```
