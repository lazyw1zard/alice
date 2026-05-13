# Alice

Alice is a small console utility for browsing, searching, editing, and running shell aliases.



## Installation

Just clone or download this repo. 

Put this lines into your shell rc file

*bash*

```shell
if [ -f ~/.zsh_aliases ]; then
    . ~/.zsh_aliases
fi
```

*zsh*

```shell
if [ -f ~/.zsh_aliases ]; then
    . ~/.zsh_aliases
fi
```



## Usage

Modern CLI mode:

```shell
alice list
alice list --names
alice search git
alice show gs
alice run gs
alice edit
alice path
```

Run without arguments to open the interactive curses menu:

```shell
alice
```

`alice run <name>` executes the alias command in a child shell. Commands that change shell state, such as `cd`, affect only that child shell.

## Legacy usage

You can wrap this script in a function in your command shell rc file as sample:


*bash example*

```shell
alice() {
    python3 ~/path/to/alice-py/alice $@
    source ~/.bashrc
}
```

*or for zsh*

```shell
alice() {
    python3 ~/path/to/alice-py/alice $@
    source ~/.zshrc
}
```


## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Make sure to add or update tests as appropriate.

## [Changelog](CHANGELOG.md)

## License

[MIT](https://choosealicense.com/licenses/mit/)
