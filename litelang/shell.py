from .lexer import Lexer
from .parser import Parser

##################################
# RUN
##################################


def run(filename, text):
    # Generate tokens
    lexer = Lexer(filename, text)
    tokens, error = lexer.make_tokens()

    return tokens, error


def shell():
    filename = '<stdin>'
    while True:
        try:
            text = input('Lite> ')
            tokens, error = run(filename, text)
            if error:
                print(error.as_string())
            else:
                print(tokens)

        except KeyboardInterrupt:
            print('\nKeyboardInterrupt')
        except EOFError:
            print('\n👋')
            exit()
