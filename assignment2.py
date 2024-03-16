from enum import Enum
import keyword

class Token(Enum):
    INTEGER = 1
    FLOAT = 2
    ID = 3
    BITWISE_OR = 4
    LOGICAL_OR = 5
    BITWISE_AND = 6
    LOGICAL_AND = 7
    FOR = 8
    WHILE = 9
    IF = 10
    ELSE = 11
    ERROR = 12


class Lexeme:
    def __init__(self, token, index=None, integer_value=None, float_value=None, unrecognized_string=None):
        self.token = token
        self.index = index
        self.integer_value = integer_value
        self.float_value = float_value
        self.unrecognized_string = unrecognized_string


symbol_table = ["for", "while", "if", "else"]
next_index = 4
tokens = []
token_index = 0
num_tokens = 0

def show_symbol_table():
    print("Symbol Table:")
    for symbol in symbol_table:
        print(f"{symbol}  ", end="")

def is_integer(string):
    string = string.strip()
    
    if not string:
        return False
    
    if string[0] in ['+', '-']:
        string = string[1:]
    
    if string.isdigit():
        return True
    
    return False

def is_float(string):
    string = string.strip()
    
    if not string:
        return False
    
    if string.count('.') > 1:
        return False
    
    if all(char.isdigit() or (char == '.' and index != 0) or (char in ['+', '-'] and index == 0) for index, char in enumerate(string)):
        return True
    
    return False

def is_valid_variable_name(name):
    return name.isidentifier() and not keyword.iskeyword(name)


def lex(file_name):

    global next_index, tokens, token_index, symbol_table, num_tokens
    if len(tokens) == 0:
        with open(file_name, 'r') as file:
            text = file.read()
            tokens = text.strip().split()
            num_tokens = len(tokens)
            token_index = 0
            
    if(num_tokens == token_index):
        print("File finished. ")
        return
    token = tokens[token_index]
    token_index += 1

    if is_integer(token):
        yield Lexeme(Token.INTEGER.name, integer_value=int(token))
    elif is_float(token):
        yield Lexeme(Token.FLOAT.name, float_value=float(token))
    elif (token.lower() in symbol_table) and (symbol_table.index(token) < 4):
        yield Lexeme(token.upper())
    elif is_valid_variable_name(token):
        if token not in symbol_table:
                symbol_table.append(token)
        yield Lexeme(Token.ID.name, symbol_table.index(token))
    elif token == '|':
        yield Lexeme(Token.BITWISE_OR.name)
    elif token == '||':
        yield Lexeme(Token.LOGICAL_OR.name)
    elif token == '&':
        yield Lexeme(Token.BITWISE_AND.name)
    elif token == '&&':
        yield Lexeme(Token.LOGICAL_AND.name)
    else:
        yield Lexeme(Token.ERROR.name, unrecognized_string=token)

    

def main():
    global next_index, tokens, token_index, symbol_table, num_tokens

    file_name = input("Enter the name of the input file: ")
    
    while True:
        print("\nMenu:")
        print("1. Call lex()")
        print("2. Show symbol table")
        print("3. Exit")
        print("4. ReEnter file name")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            lexer = lex(file_name)
            for lexeme in lexer:
                print(f"<token={lexeme.token}, index={lexeme.index}, integer_value={lexeme.integer_value}, float_value={lexeme.float_value}, unrecognized_string={lexeme.unrecognized_string}>")
        elif choice == "2":
            show_symbol_table()
        elif choice == "3":
            print("Exiting...")
            break
        elif choice == "4":
            file_name = input("Enter the name of the input file: ")
            symbol_table = ["for", "while", "if", "else"]
            next_index = 4
            tokens = []
            token_index = 0
            num_tokens = 0
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()


    






