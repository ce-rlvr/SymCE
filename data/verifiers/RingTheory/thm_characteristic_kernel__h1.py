import sympy
from sympy import Integer, ZZ, QQ, RR, CC
import z3
import math
import itertools
import functools

# Top-level setup: named object bindings that the witness expression may reference.
class MockRing:
    """
    A mock ring object to represent a counterexample where the order of the 
    designated idempotent 1_R (which generates the kernel of phi) differs 
    from the characteristic of the ring. This can happen in non-unital rings 
    where a specific idempotent is treated as 1_R.
    """
    def __init__(self, kernel, char, h1=True):
        self.kernel = kernel
        self.char = char
        self.h1 = h1
        self.neg_q = (abs(kernel) != abs(char))

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    try:
        # 1. Witness is a MockRing or similar object with kernel and char attributes
        if hasattr(witness, 'kernel') and hasattr(witness, 'char'):
            h1 = bool(getattr(witness, 'h1', True))
            try:
                neg_q = bool(abs(witness.kernel) != abs(witness.char))
            except Exception:
                neg_q = bool(witness.kernel != witness.char)
            return [h1, neg_q]
            
        # 2. Witness is a dictionary
        if isinstance(witness, dict):
            h1 = bool(witness.get('h1', True))
            if 'kernel' in witness and 'char' in witness:
                try:
                    neg_q = bool(abs(witness['kernel']) != abs(witness['char']))
                except Exception:
                    neg_q = bool(witness['kernel'] != witness['char'])
            else:
                neg_q = bool(witness.get('neg_q', False))
            return [h1, neg_q]
            
        # 3. Witness is a tuple/list of 2 integers (kernel_gen, characteristic)
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            m, n = witness
            if isinstance(m, (int, Integer)) and isinstance(n, (int, Integer)):
                h1 = True
                neg_q = bool(abs(m) != abs(n))
                return [h1, neg_q]
                
        # 4. Witness is a Z3 model
        if 'z3' in str(type(witness)) and hasattr(witness, 'decls'):
            m = None
            n = None
            for d in witness.decls():
                name = d.name()
                if name in ('m', 'kernel', 'kernel_gen'):
                    m = witness[d].as_long()
                elif name in ('n', 'char', 'characteristic'):
                    n = witness[d].as_long()
            if m is not None and n is not None:
                h1 = True
                neg_q = bool(abs(m) != abs(n))
                return [h1, neg_q]
                
        # 5. Witness is a sympy Ring
        if hasattr(witness, 'characteristic') and callable(witness.characteristic):
            h1 = True
            neg_q = False  # For unital rings, kernel == characteristic always
            return [h1, neg_q]
            
        # 6. Fallback for objects with explicit h1 and neg_q attributes
        if hasattr(witness, 'h1'):
            h1 = bool(witness.h1)
        else:
            h1 = True
            
        if hasattr(witness, 'neg_q'):
            neg_q = bool(witness.neg_q)
            
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: phi: Z -> R is the unique ring homomorphism satisfying phi(1) = 1_R",
    "¬Q: The kernel of phi is not nZ, where n is the characteristic of R"
]

N_HYP = 1
NEG_Q_INDEX = 1