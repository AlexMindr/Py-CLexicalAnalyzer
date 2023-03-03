
import re

header = {'#include'}
delimiters = {'\t', ' ', '+', '-', '*', '/', ',', '<', '>', '?', '!', '=', ':', ';', '[', ']', '(', ')', '{', '}'}
operators = {'+', '-', '*', '/', '>', '<', '='}
operators2 = {'++', '--', '>>', '<<', '==', '>=', '<=', '!='}
identifiers = r'^[A-Za-z]+[a-zA-Z0-9_\.]*'
keywords = {'return', 'printf', 'while', 'for', 'if', 'else', 'main', 'do', 'break', 'continue', 'int', 'double',
            'float', 'bool', 'char', 'case', 'sizeof', 'switch', 'short', 'long', 'typedef', 'unsigned', 'void',
            'static', 'struct'}
integers = r'^(-|[0-9])*[0-9]+$'
decimals = r'^(-|[0-9]|\.)?([0-9]|\.)+$'
chars = r'^\'.?\'$'
string = r'^".*'

error = []
comms = []


def comments():
    file = open('InputProg.txt', 'r')
    elcomms = []
    fp = 0
    count = 1
    strin = ''
    comm = ''

    while True:

        char = file.read(1)
        fp += 1

        if char == '':
            # print('End Of File')
            break

        if char == '\n':
            count = count + 1

        if char == '/':
            strin += char
            char = file.read(1)
            fp += 1
            strin += char

            if strin == '//':
                elcomms.append(fp - 1)
                while char != '\n':
                    char = file.read(1)
                    fp += 1
                    comm += char
                    if char == '\n':
                        count = count + 1
                comm = comm.strip()
                print(comm, '----Comment line#', count - 1, '------\n')
                comm = ''
                strin = ''
                elcomms.append(fp)
                comms.append(elcomms)
                elcomms = []

            if strin == '/*':
                elcomms.append(fp - 1)
                c1 = file.read(1)
                fp += 1
                c2 = file.read(1)
                fp += 1
                print("-----Multi line comment start at line #", count, '-------')
                while c1 + c2 != '*/':
                    if c1 == '':
                        err = "Error, comment not closed at line #" + "{}".format(count)
                        error.append(err)
                        break
                    comm += c1 + c2
                    c2 = ''
                    c1 = file.read(1)
                    fp += 1
                    if c1 == '*':
                        c2 = file.read(1)
                        fp += 1
                    if c1 == '\n' or c2 == '\n':
                        count = count + 1
                comm = comm.strip()
                print(comm, '\n-----Multi line comm end at line #', count, '------\n')
                comm = ''
                strin = ''
                elcomms.append(fp)
                comms.append(elcomms)
                elcomms = []
    file.close()


def analyze():
    comments()
    file = open('InputProg.txt', 'r')
    fp = 0
    count = 1
    strin = ''

    while True:

        char = file.read(1)
        fp += 1

        for el in comms:
            if el[0] <= fp <= el[1]:
                while el[0] <= fp <= el[1]:
                    if char == '\n':
                        count = count + 1
                    char = file.read(1)
                    fp += 1

        if char == '':
            print('End Of File')
            break

        if char == '\n':
            count = count + 1

        if char == '"':
            strin += char
            char = file.read(1)
            strin += char
            while char != '"':
                char = file.read(1)
                fp += 1
                if char == '\n':
                    count = count + 1
                elif char == '"':
                    strin += char
                    print(strin, 'string, dim', len(strin), '-line #', count)
                    strin = ''
                else:
                    strin += char
            char = file.read(1)

        if char not in delimiters and char != '\n':
            strin += char
        auxstr = ''
        if char in delimiters:
            op2 = ''
            if char in operators:
                op2 += char
                ok = 1
                aux = file.read(1)
                while aux == ' ' or aux == '\t':
                    aux = file.read(1)
                    ok = 0

                if aux in operators and ok == 0:
                    print(char, 'operator, dim', len(char), '-line #', count)
                    print(aux, 'operator, dim', len(char), '-line #', count)
                    err = "Error at line #" + "{}".format(count) + "{}".format(aux)
                    error.append(err)
                elif aux in operators and ok == 1:
                    op2 += aux
                if op2 in operators2:
                    print(op2, 'operator2, dim', len(op2), '-line #', count)
                else:
                    auxstr += aux
                    print(char, 'operator, dim', len(char), '-line #', count)

            else:
                if char != ' ' and char != '\t' and char != '\r':
                    print(char, "delimiter, dim", len(char), '-line#', count)
                    # pass

            if strin in header:
                print(strin, 'keyword header, dim', len(strin), '-line #', count)
                strin = ''
                while char != '>':
                    if char == '\n':
                        count = count + 1
                    char = file.read(1)
                    fp += 1
                    if char == '<':
                        print(char, 'operator, dim', len(char), '-line #', count)
                    elif char == '>':
                        print(strin, 'lib, dim', len(strin), '-line #', count)
                        print(char, 'operator, dim', len(char), '-line #', count)
                        strin = ''
                    else:
                        strin += char

            elif strin in keywords:
                print(strin, 'keyword, dim', len(strin), '-line #', count)
                strin = ''
            elif re.search(integers, strin):
                print(strin, 'integer, dim', len(strin), '-line #', count)
                strin = ''
            elif re.search(decimals, strin):
                print(strin, 'decimal, dim', len(strin), '-line #', count)
                strin = ''
            elif re.search(chars, strin):
                out = '#emptychar#'
                if strin[1] != "'":
                    out = strin[1]
                print(out, 'character -line #', count)
                strin = ''
            elif re.search(identifiers, strin) and strin != '':
                print(strin, 'identifier, dim', len(strin), '-line #', count)
                strin = ''
            elif not re.search(identifiers, strin) and strin != '':
                print(strin, 'invalid token, dim', len(strin), '-line #', count)
                strin = ''
            strin += auxstr

    print('Errors are:', error)
    file.close()


def main():
    analyze()


if __name__ == "__main__":
    main()
