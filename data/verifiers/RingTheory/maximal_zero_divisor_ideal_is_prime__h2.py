import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    
    The witness must provide:
      - R: an iterable of elements in the ring
      - add: a function for ring addition
      - mul: a function for ring multiplication
      - zero: the additive identity
      - one: the multiplicative identity
      - I: an iterable of elements in the ideal I
      - Z: an iterable (or callable) representing the set Z
    """
    try:
        R = witness.R
        add = witness.add
        mul = witness.mul
        zero = witness.zero
        one = witness.one
        I = witness.I
        Z = witness.Z
    except Exception:
        return [False, False, False, False]

    def in_Z(elem, Z_obj):
        if callable(Z_obj):
            return Z_obj(elem)
        return elem in Z_obj

    # H_1: R is a commutative ring with identity
    h1 = False
    try:
        h1 = True
        if zero not in R or one not in R:
            h1 = False
        if h1:
            for a in R:
                if add(a, zero) != a or add(zero, a) != a:
                    h1 = False
                    break
                if mul(a, one) != a or mul(one, a) != a:
                    h1 = False
                    break
                has_inv = False
                for b in R:
                    if add(a, b) == zero:
                        has_inv = True
                        break
                if not has_inv:
                    h1 = False
                    break
                for b in R:
                    if add(a, b) != add(b, a):
                        h1 = False
                        break
                    if mul(a, b) != mul(b, a):
                        h1 = False
                        break
                if not h1:
                    break
        if h1:
            for a in R:
                for b in R:
                    for c in R:
                        if add(add(a, b), c) != add(a, add(b, c)):
                            h1 = False
                            break
                        if mul(mul(a, b), c) != mul(a, mul(b, c)):
                            h1 = False
                            break
                        if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)):
                            h1 = False
                            break
                    if not h1: break
                if not h1: break
    except Exception:
        h1 = False

    # H_2: I is an ideal of R such that I is a subset of Z
    h2 = False
    try:
        h2 = True
        if not all(x in R for x in I):
            h2 = False
        if not all(in_Z(x, Z) for x in I):
            h2 = False
        if zero not in I:
            h2 = False
        if h2:
            for i in I:
                for j in I:
                    if add(i, j) not in I:
                        h2 = False
                        break
                for r in R:
                    if mul(r, i) not in I:
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    # H_3: For any ideal J of R strictly containing I, J is not a subset of Z
    h3 = False
    try:
        h3 = True
        for x in R:
            if x in I:
                continue
            
            # Generate the ideal I + (x)
            ideal_x = []
            for i in I:
                for r in R:
                    val = add(i, mul(r, x))
                    if val not in ideal_x:
                        ideal_x.append(val)
            
            # If there is an ideal strictly containing I that is a subset of Z, H_3 fails
            if all(in_Z(elem, Z) for elem in ideal_x):
                h3 = False
                break
    except Exception:
        h3 = False

    # ¬Q: I is not a prime ideal of R
    neg_q = False
    try:
        # A prime ideal must be a proper ideal
        if all(x in I for x in R) and all(x in R for x in I):
            neg_q = True
        else:
            for a in R:
                if a in I: continue
                for b in R:
                    if b in I: continue
                    if mul(a, b) in I:
                        neg_q = True
                        break
                if neg_q:
                    break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: I is an ideal of R such that I is a subset of Z",
    "H_3: For any ideal J of R strictly containing I, J is not a subset of Z",
    "¬Q: I is not a prime ideal of R"
]

N_HYP = 3
NEG_Q_INDEX = 3