# Texas Holdem Environment
Texas Hold'em environment based on OpenAI gym package.  

## Install

Dependencies:
- python@3.9
- pipenv

The package uses pipenv as virtual environment but a `Makefile` is provided for simplify the installation process.

The `Makefile` calls follows the usage:

`make [ARG]`

with 

``` 
[ARG] 
    install - to setup the environment
    format - to run PEP8 checking and format
    lint - to run the linting on the code
    test - to run the tests
```
