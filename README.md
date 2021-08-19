# Alice
Alice is console utilite which helps you manage and define your aliases easy.



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