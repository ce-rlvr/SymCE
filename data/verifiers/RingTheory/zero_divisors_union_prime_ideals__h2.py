import itertools
import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z

def get_ring_ops(R):
    if isinstance(R, int):
        elements = list(range(R))
        add = lambda a, b: (a + b) % R
        mul = lambda a, b: (a * b) % R
        zero = 0
        one = 1 % R
        return elements, add, mul, zero, one
    elif isinstance(R, tuple) and len(R) == 5:
        return R
    else:
        elements = list(R.elements)
        add = R.add
        mul = R.mul
        zero = R.zero
        one = R.one
        return elements, add, mul, zero, one

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, S = witness
        else:
            R = witness
            elements, add, mul, zero, one = get_ring_ops(R)
            S = set()
            for a in elements:
                for b in elements:
                    if b != zero and mul(a, b) == zero:
                        S.add(a)
                        break
    except Exception:
        return [False, False]
        
    try:
        elements, add, mul, zero, one = get_ring_ops(R)
    except Exception:
        return [False, False]
        
    # H_1: R is a commutative ring with identity
    try:
        h1 = True
        # check closure
        for a in elements:
            for b in elements:
                if add(a, b) not in elements: h1 = False
                if mul(a, b) not in elements: h1 = False
        if h1:
            # check commutativity
            for a in elements:
                for b in elements:
                    if add(a, b) != add(b, a): h1 = False
                    if mul(a, b) != mul(b, a): h1 = False
        if h1:
            # check associativity
            for a in elements:
                for b in elements:
                    for c in elements:
                        if add(add(a, b), c) != add(a, add(b, c)): h1 = False
                        if mul(mul(a, b), c) != mul(a, mul(b, c)): h1 = False
        if h1:
            # check distributivity
            for a in elements:
                for b in elements:
                    for c in elements:
                        if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): h1 = False
        if h1:
            # check identity
            for a in elements:
                if add(a, zero) != a: h1 = False
                if mul(a, one) != a: h1 = False
        if h1:
            # check inverses
            for a in elements:
                has_inv = False
                for b in elements:
                    if add(a, b) == zero:
                        has_inv = True
                        break
                if not has_inv: h1 = False
    except Exception:
        h1 = False

    # ¬Q: S is not a union of prime ideals of R
    try:
        # Generate all principal ideals
        principal_ideals = []
        for a in elements:
            ideal = set()
            for r in elements:
                ideal.add(mul(r, a))
            # Close under addition
            while True:
                added = False
                new_elements = list(ideal)
                for u in new_elements:
                    for v in new_elements:
                        s = add(u, v)
                        if s not in ideal:
                            ideal.add(s)
                            added = True
                if not added:
                    break
            principal_ideals.append(frozenset(ideal))
        
        # Generate all ideals by taking sums of principal ideals
        ideals = set(principal_ideals)
        while True:
            added = False
            new_ideals = set()
            for I in ideals:
                for J in principal_ideals:
                    sum_ideal = frozenset(add(u, v) for u in I for v in J)
                    if sum_ideal not in ideals and sum_ideal not in new_ideals:
                        new_ideals.add(sum_ideal)
                        added = True
            if not added:
                break
            ideals.update(new_ideals)
        
        # Filter for prime ideals
        prime_ideals = []
        for I in ideals:
            if len(I) == len(elements):
                continue  # Must be a proper ideal
            is_prime = True
            for a in elements:
                if a in I: continue
                for b in elements:
                    if b in I: continue
                    if mul(a, b) in I:
                        is_prime = False
                        break
                if not is_prime:
                    break
            if is_prime:
                prime_ideals.append(I)
                
        # Check if S is the union of some prime ideals
        S_set = set(S)
        union = set()
        for P in prime_ideals:
            if P.issubset(S_set):
                union.update(P)
        
        neg_q = (union != S_set)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "¬Q: S is not a union of prime ideals of R"
]

N_HYP = 1
NEG_Q_INDEX = 1