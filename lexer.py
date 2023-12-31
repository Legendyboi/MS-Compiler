# Lexer.py
from Token import *
import sys


class Lexer:
    def __init__(self, source_code):
        self.source = source_code + '\n'
        self.curChar = ''
        self.curPos = -1
        self.nextChar()

    def nextChar(self):
        self.curPos += 1
        if self.curPos >= len(self.source):
            self.curChar = '\0'  # EOF
        else:
            self.curChar = self.source[self.curPos]

    def peek(self):
        if self.curPos + 1 >= len(self.source):
            return '\0'
        return self.source[self.curPos + 1]

    def abort(self, message):
        sys.exit("LEXICAL ERROR: " + message)

    def skipWhitespace(self):
        while self.curChar == ' ' or self.curChar == '\t' or self.curChar == '\r':
            print("Skipping whitespace:", self.curChar)
            self.nextChar()

    def skipComment(self):
        if self.curChar == '//':
            while self.curChar != '\n':
                self.nextChar()

    # Return the next token.
    def getToken(self):
        self.skipWhitespace()
        self.skipComment()
        token = None

        # Check the first character of this token to see if we can decide what it is. If it is a multiple character
        # operator (e.g., !=), number, identifier, or keyword then we will process the rest.
        if self.curChar == '\0':
            # End of input
            token = Token(self.curChar, TokenType.EOF)
        elif self.curChar == '+':
            token = Token(self.curChar, TokenType.PLUS)
        elif self.curChar == '-':
            token = Token(self.curChar, TokenType.MINUS)
        elif self.curChar == '*':
            token = Token(self.curChar, TokenType.ASTERISK)
        elif self.curChar == '/':
            token = Token(self.curChar, TokenType.SLASH)
        elif self.curChar == '=':
            # Check whether this token is = or ==
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.EQUAL_EQUAL)
            else:
                token = Token(self.curChar, TokenType.EQUAL)
        elif self.curChar == '>':
            # Check whether this is token is > or >=
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.GREATER_THAN_EQUAL)
            else:
                token = Token(self.curChar, TokenType.GREATER_THAN)
        elif self.curChar == '<':
            # Check whether this is token is < or <=
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.LESSER_THAN_EQUAL)
            else:
                token = Token(self.curChar, TokenType.LESSER_THAN)
        elif self.curChar == '!':
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.NOT_EQUAL)
            else:
                self.abort("Expected !=, got !" + self.peek())
        elif self.curChar == '\"':
            # Get characters between quotations.
            self.nextChar()
            startPos = self.curPos

            while self.curChar != '\"':
                # Don't allow special characters in the string. No escape characters, newlines, tabs, or %.
                # We will be using C's printf on this string.
                if self.curChar == '\r' or self.curChar == '\n' or self.curChar == '\t' or self.curChar == '\\' \
                        or self.curChar == '%':
                    self.abort("Illegal character in string.")
                self.nextChar()

            tokText = self.source[startPos: self.curPos]  # Get the substring.
            token = Token(tokText, TokenType.STRING)
        elif self.curChar.isdigit():
            # Leading character is a digit, so this must be a number.
            # Get all consecutive digits and decimal if there is one.
            startPos = self.curPos
            while self.peek().isdigit():
                self.nextChar()
            if self.peek() == '.':  # Decimal!
                self.nextChar()

                # Must have at least one digit after decimal.
                if not self.peek().isdigit():
                    # Error!
                    self.abort("Illegal character in number.")
                while self.peek().isdigit():
                    self.nextChar()

            tokText = self.source[startPos: self.curPos + 1]  # Get the substring.
            token = Token(tokText, TokenType.NUMBER)
        elif self.curChar.isalpha():
            # Leading character is a letter, so this must be an identifier or a keyword.
            # Get all consecutive alphanumeric characters.
            startPos = self.curPos
            while self.peek().isalnum():
                self.nextChar()

            # Check if the token is in the list of keywords.
            tokText = self.source[startPos: self.curPos + 1]  # Get the substring.
            keyword = Token.checkIfKeyword(tokText)
            if keyword is None:  # Identifier
                token = Token(tokText, TokenType.IDENTIFIER)
            else:  # Keyword
                token = Token(tokText, keyword)
        elif self.curChar == '\n':
            token = Token(self.curChar, TokenType.NEW_LINE)
        elif self.curChar == '{':
            token = Token(self.curChar, TokenType.LBRACE_START)
        elif self.curChar == '}':
            token = Token(self.curChar, TokenType.RBRACE_END)
        elif self.curChar == '\0':
            token = Token('', TokenType.EOF)
        else:
            # Unknown token!
            self.abort("Unknown token: " + self.curChar)

        self.nextChar()
        return token
