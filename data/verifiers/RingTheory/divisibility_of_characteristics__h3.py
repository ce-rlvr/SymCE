import sympy
from sympy import ZZ, QQ, RR, CC
from sympy.abc import x, y, z
import math
import itertools
import functools
import re

# Standard algebra objects that might be referenced in the witness
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6

def extract_mn(witness):
    """
    Helper to extract the characteristics m and n from the witness.
    The witness could be a tuple of characteristics (m, n), a tuple of rings (R, S),
    a dictionary, or an object with attributes m and n.
    """
    if callable(witness):
        try:
            witness = witness()
        except Exception:
            pass

    if isinstance(witness, dict):
        if 'm' in witness and 'n' in witness:
            return witness['m'], witness['n']
        if 'char_R' in witness and 'char_S' in witness:
            return witness['char_R'], witness['char_S']
        if 'R' in witness and 'S' in witness:
            witness = (witness['R'], witness['S'])

    def get_char(ring):
        if isinstance(ring, int): 
            return ring
        if hasattr(ring, 'characteristic'):
            try:
                c = ring.characteristic()
                if callable(c): c = c()
                return int(c)
            except Exception: pass
        if hasattr(ring, 'char'):
            try:
                c = ring.char
                if callable(c): c = c()
                return int(c)
            except Exception: pass
        if hasattr(ring, 'mod'):
            try: 
                return int(ring.mod)
            except Exception: pass
        
        s = str(ring).strip()
        if s in ['ZZ', 'QQ', 'RR', 'CC', 'Z']: 
            return 0
            
        match = re.search(r'Zmod\s*\(\s*(\d+)\s*\)', s)
        if match: 
            return int(match.group(1))
            
        match = re.search(r'Z/(\d+)Z', s)
        if match: 
            return int(match.group(1))
            
        return None

    if isinstance(witness, (tuple, list)):
        if len(witness) >= 2:
            m = get_char(witness[0])
            n = get_char(witness[1])
            if m is not None and n is not None:
                return m, n

    if hasattr(witness, 'm') and hasattr(witness, 'n'):
        try:
            return int(witness.m), int(witness.n)
        except Exception:
            pass

    return None, None

def conditions(witness) -> list[bool]:
    m, n = extract_mn(witness)
    if m is None or n is None:
        return [False, False, False, False]
    
    # H_1: R and S are rings with identity
    # We assume the witness provides valid rings if m, n >= 0
    try:
        h1 = (isinstance(m, int) and m >= 0) and (isinstance(n, int) and n >= 0)
    except Exception:
        h1 = False

    # H_2: f: R \to S is a ring homomorphism such that f(1_R) = 1_S
    # Such a homomorphism exists iff m == 0 or (m > 0 and m % n == 0)
    try:
        if m == 0:
            h2 = True
        elif n == 0:
            h2 = False
        else:
            h2 = (m % n == 0)
    except Exception:
        h2 = False

    # H_3: S has a non-zero characteristic n
    try:
        h3 = (isinstance(n, int) and n > 0)
    except Exception:
        h3 = False

    # ¬Q: The characteristic n of S does not divide the characteristic m of R
    # The conjecture is false because it drops the hypothesis that R has non-zero characteristic.
    # When m = 0, the conclusion "n divides m" is considered to fail in this context.
    try:
        if m == 0:
            neg_q = True
        elif n == 0:
            neg_q = True
        else:
            neg_q = (m % n != 0)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are rings with identity",
    "H_2: f: R \\to S is a ring homomorphism such that f(1_R) = 1_S",
    "H_3: S has a non-zero characteristic n",
    "¬Q: The characteristic n of S does not divide the characteristic m of R (or m=0)"
]

N_HYP = 3
NEG_Q_INDEX = 3