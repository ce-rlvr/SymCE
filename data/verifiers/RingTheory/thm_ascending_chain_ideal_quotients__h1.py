import sympy
from sympy import *
import sympy.combinatorics
from sympy.combinatorics.named_groups import *
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import *
from sympy.ntheory import *
from sympy.abc import *
from sympy.polys import *
import z3
import math
import itertools
import functools

# Top-level setup
QQ = sympy.QQ
ZZ = sympy.ZZ

def conditions(witness) -> list[bool]:
    h1, h2, neg_q = False, False, False

    # 1. Try to unpack as (R, I, x) where R has methods
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            R, I, x_elem = witness
            if hasattr(R, 'is_ideal') or hasattr(R, 'chain_stabilizes'):
                h1 = bool(R.is_ideal(I) if callable(getattr(R, 'is_ideal', None)) else getattr(R, 'is_ideal', True))
                h2 = bool(R.is_element(x_elem) if callable(getattr(R, 'is_element', None)) else getattr(R, 'is_element', True))
                stab = R.chain_stabilizes(I, x_elem) if callable(getattr(R, 'chain_stabilizes', None)) else getattr(R, 'chain_stabilizes', False)
                neg_q = not bool(stab)
                return [h1, h2, neg_q]
    except Exception:
        pass

    # 2. Try to unpack as (I, x, chain) or (R, I, x, chain)
    try:
        if isinstance(witness, tuple):
            chain = None
            if len(witness) == 3 and isinstance(witness[2], (list, tuple)):
                # Check if witness[2] looks like a chain of ideals (list of lists/sets)
                if len(witness[2]) > 0 and isinstance(witness[2][0], (list, set, tuple)):
                    chain = witness[2]
            elif len(witness) == 4 and isinstance(witness[3], (list, tuple)):
                if len(witness[3]) > 0 and isinstance(witness[3][0], (list, set, tuple)):
                    chain = witness[3]
            elif len(witness) == 2 and isinstance(witness[1], (list, tuple)):
                if len(witness[1]) > 0 and isinstance(witness[1][0], (list, set, tuple)):
                    chain = witness[1]
                
            if chain is not None and len(chain) > 1:
                h1 = True
                h2 = True
                strictly_ascending = True
                for i in range(len(chain) - 1):
                    set_i = set(chain[i]) if isinstance(chain[i], (list, set, tuple)) else {chain[i]}
                    set_next = set(chain[i+1]) if isinstance(chain[i+1], (list, set, tuple)) else {chain[i+1]}
                    if not (set_i < set_next):
                        strictly_ascending = False
                        break
                neg_q = strictly_ascending
                return [h1, h2, neg_q]
    except Exception:
        pass

    # 3. Try if witness is a dictionary
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_ideal', True))
            h2 = bool(witness.get('is_element', True))
            if 'chain_stabilizes' in witness:
                neg_q = not bool(witness['chain_stabilizes'])
            elif 'stabilizes' in witness:
                neg_q = not bool(witness['stabilizes'])
            else:
                neg_q = True
            return [h1, h2, neg_q]
    except Exception:
        pass

    # 4. Try if witness is an object with methods
    try:
        if hasattr(witness, 'is_ideal') or hasattr(witness, 'chain_stabilizes'):
            h1 = bool(witness.is_ideal() if callable(getattr(witness, 'is_ideal', None)) else getattr(witness, 'is_ideal', True))
            h2 = bool(witness.is_element() if callable(getattr(witness, 'is_element', None)) else getattr(witness, 'is_element', True))
            stab = witness.chain_stabilizes() if callable(getattr(witness, 'chain_stabilizes', None)) else getattr(witness, 'chain_stabilizes', False)
            neg_q = not bool(stab)
            return [h1, h2, neg_q]
    except Exception:
        pass

    # 5. Try if witness is a list of sets/lists (the chain itself)
    try:
        if isinstance(witness, list) and len(witness) > 1:
            h1 = True
            h2 = True
            strictly_ascending = True
            for i in range(len(witness) - 1):
                set_i = set(witness[i]) if isinstance(witness[i], (list, set, tuple)) else {witness[i]}
                set_next = set(witness[i+1]) if isinstance(witness[i+1], (list, set, tuple)) else {witness[i+1]}
                if not (set_i < set_next):
                    strictly_ascending = False
                    break
            neg_q = strictly_ascending
            return [h1, h2, neg_q]
    except Exception:
        pass

    # 6. Try if witness is a callable
    try:
        if callable(witness):
            h1 = True
            h2 = True
            strictly_ascending = True
            for i in range(1, 10):
                val_i = witness(i)
                val_next = witness(i+1)
                set_i = set(val_i) if isinstance(val_i, (list, set, tuple)) else {val_i}
                set_next = set(val_next) if isinstance(val_next, (list, set, tuple)) else {val_next}
                if not (set_i < set_next):
                    strictly_ascending = False
                    break
            neg_q = strictly_ascending
            return [h1, h2, neg_q]
    except Exception:
        pass

    return [False, False, False]

CONDITION_LABELS = [
    "H_1: I is an ideal of R",
    "H_2: x is an element of R",
    "¬Q: The ascending chain of ideal quotients (I : x^n) does not stabilize"
]

N_HYP = 2
NEG_Q_INDEX = 2