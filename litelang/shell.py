from .lexer import Lexer
from .parser import Parser

##################################
# RUN
##################################


def run(filename, text):
    # Generate tokens
    lexer = Lexer(filename, text)
    tokens, error = lexer.make_tokens()

    # print('🚨', tokens)
    # print('🚨', error)
    if error:
        return None, error

    # Generate AST
    parser = Parser(tokens)
    ast = parser.parse()

    return ast.node, ast.error


def shell():
    filename = '<stdin>'
    while True:
        try:
            text = input('Lite> ')
            ast, error = run(filename, text)
            if error:
                print(error.__class__.__name__)
                print(error.as_string())
            else:
                print(ast)

        except KeyboardInterrupt:
            print('\nKeyboardInterrupt')
        except EOFError:
            print('\n👋')
            exit()
