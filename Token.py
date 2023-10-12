# Token.py
import enum
from enum import Enum


class Token:
    def __init__(self, tokenName, tokenKind):
        self.text = tokenName
        self.kind = tokenKind

    @staticmethod
    def checkIfKeyword(tokenText):
        for kind in TokenType:
            # Relies on all keyword enum values being 1XX.
            if kind.name == tokenText and 100 <= kind.value < 200:
                return kind
        return None


class TokenType(enum.Enum):
    EOF = -1  # End of Line
    NEW_LINE = 0  # New Line
    NUMBER = 1
    IDENTIFIER = 2
    STRING = 3

    # Keywords
    fn = 101
    Print = 102
    Input = 103
    If = 104
    Else = 105
    For = 106
    While = 107
    LBRACE_START = 108
    RBRACE_END = 109
    Var = 111
    END = 112

    # Operators
    EQUAL = 201
    EQUAL_EQUAL = 202
    NOT_EQUAL = 203
    LESSER_THAN = 204
    LESSER_THAN_EQUAL = 205
    GREATER_THAN = 206
    GREATER_THAN_EQUAL = 207
    PLUS = 210
    MINUS = 211
    ASTERISK = 212
    SLASH = 213
    MODULUS = 214
