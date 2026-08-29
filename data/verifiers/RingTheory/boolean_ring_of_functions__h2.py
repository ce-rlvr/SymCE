import sympy
from sympy import ZZ, QQ, GF
import math
import itertools
import functools

# Top-level setup: named object bindings that the witness expression may reference.
# We provide common rings/fields that might be used as counterexamples.
Z2 = GF(2)
Z3 = GF(3)

CONDITION_LABELS = [
    "H_1: X is a non-empty set",
    "H_2: R^X is the set of all functions from X to R",
    "H_3: Addition and multiplication on R^X are defined pointwise",
    "¬Q: R^X is not a Boolean ring"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    # The witness is expected to be a tuple (X, R) where X is the set and R is the ring.
    # If only a ring is provided, we assume X is a singleton set (e.g., X = 1).
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            X, R = witness
        else:
            X = 1
            R = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: X is a non-empty set
    try:
        if isinstance(X, int):
            h1 = X > 0
        elif hasattr(X, '__len__'):
            h1 = len(X) > 0
        elif hasattr(X, '__iter__'):
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: R^X is the set of all functions from X to R
    # We verify that R is a valid domain/set that can be mapped into.
    try:
        h2 = hasattr(R, '__contains__') or hasattr(R, 'zero') or hasattr(R, 'is_Ring')
    except Exception:
        h2 = False

    # H_3: Addition and multiplication on R^X are defined pointwise
    # We verify that R supports addition and multiplication (i.e., it is a valid ring structure).
    try:
        if hasattr(R, 'zero') and hasattr(R, 'one'):
            z_el = R.zero
            o_el = R.one
        else:
            z_el = 0
            o_el = 1
            if not (hasattr(R, '__contains__') and z_el in R and o_el in R):
                raise ValueError("R does not contain 0 and 1")
        
        # Check closure for basic operations to ensure pointwise operations are well-defined
        s = z_el + o_el
        p = z_el * o_el
        s2 = o_el + o_el
        
        if hasattr(R, '__contains__'):
            if s not in R or p not in R or s2 not in R:
                h3 = False
            else:
                h3 = True
        else:
            h3 = True
    except Exception:
        h3 = False

    # ¬Q: R^X is not a Boolean ring
    # R^X is a Boolean ring iff R is a Boolean ring.
    # We check if R is NOT a Boolean ring by finding an element x where x^2 != x.
    try:
        is_boolean_ring = True
        if hasattr(R, 'is_Ring') and not R.is_Ring:
            is_boolean_ring = False
        else:
            elements = []
            if hasattr(R, 'zero'): elements.append(R.zero)
            elif hasattr(R, '__contains__') and 0 in R: elements.append(0)
            
            if hasattr(R, 'one'): elements.append(R.one)
            elif hasattr(R, '__contains__') and 1 in R: elements.append(1)
            
            try:
                if hasattr(R, '__call__'): elements.append(R(2))
                elif hasattr(R, '__contains__') and 2 in R: elements.append(2)
            except Exception: pass
            
            try:
                if hasattr(R, '__call__'): elements.append(R(-1))
                elif hasattr(R, '__contains__') and -1 in R: elements.append(-1)
            except Exception: pass
            
            if not elements:
                is_boolean_ring = False
            
            for e in elements:
                try:
                    if e * e != e:
                        is_boolean_ring = False
                        break
                except Exception:
                    is_boolean_ring = False
                    break
        neg_q = not is_boolean_ring
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]