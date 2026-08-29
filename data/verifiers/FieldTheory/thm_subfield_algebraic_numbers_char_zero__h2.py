import sympy
from sympy import *
import re

# Top-level setup
CC = sympy.S.Complexes
QQ = sympy.S.Rationals
RR = sympy.S.Reals
ZZ = sympy.S.Integers

def conditions(witness) -> list[bool]:
    try:
        h1_ok = False
        if hasattr(witness, 'is_algebraically_closed') and callable(witness.is_algebraically_closed):
            h1_ok = bool(witness.is_algebraically_closed())
        elif hasattr(witness, 'is_AlgebraicallyClosed'):
            h1_ok = bool(witness.is_AlgebraicallyClosed)
        else:
            s = str(witness).lower()
            if s in ['cc', 'c', 'complexes', 'complexfield', 'complex']: 
                h1_ok = True
            elif s in ['qq_bar', 'q_bar', 'algebraicnumbers', 'algebraic_numbers']: 
                h1_ok = True
            elif s in ['qq', 'q', 'rationals', 'rationalfield', 'rational']: 
                h1_ok = False
            elif s in ['rr', 'r', 'reals', 'realfield', 'real']: 
                h1_ok = False
            elif s in ['zz', 'z', 'integers', 'integerring']: 
                h1_ok = False
            elif 'bar' in s or 'alg_closure' in s or 'algebraicclosure' in s or 'algebraicallyclosed' in s or 'closure' in s:
                h1_ok = True
    except Exception:
        h1_ok = False

    try:
        char = 0
        if hasattr(witness, 'characteristic'):
            if callable(witness.characteristic):
                char = witness.characteristic()
            else:
                char = witness.characteristic
        elif hasattr(witness, 'char'):
            if callable(witness.char):
                char = witness.char()
            else:
                char = witness.char
        else:
            s = str(witness).lower()
            if s in ['cc', 'c', 'complexes', 'complexfield', 'complex', 
                     'qq_bar', 'q_bar', 'algebraicnumbers', 'algebraic_numbers', 
                     'qq', 'q', 'rationals', 'rationalfield', 'rational',
                     'rr', 'r', 'reals', 'realfield', 'real',
                     'zz', 'z', 'integers', 'integerring']: 
                char = 0
            else:
                m = re.search(r'(?:f|gf|z|z_|z/|f_)\s*\(?\s*(\d+)', s)
                if m: 
                    char = int(m.group(1))
                elif 'p' in s and not '0' in s:
                    char = 2
                else:
                    char = 0
        
        if char != 0:
            contains_qq_bar = False
        else:
            s = str(witness).lower()
            if s in ['cc', 'c', 'complexes', 'complexfield', 'complex', 'qq_bar', 'q_bar', 'algebraicnumbers', 'algebraic_numbers']:
                contains_qq_bar = True
            elif h1_ok:
                contains_qq_bar = True
            elif 'bar' in s or 'alg_closure' in s or 'algebraicclosure' in s or 'algebraicallyclosed' in s or 'closure' in s:
                contains_qq_bar = True
            else:
                contains_qq_bar = False
                
        neg_q_ok = not contains_qq_bar
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field",
    "¬Q: K does not contain a unique subfield isomorphic to the field of algebraic numbers"
]

N_HYP = 1
NEG_Q_INDEX = 1