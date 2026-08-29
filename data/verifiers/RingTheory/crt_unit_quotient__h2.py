import sympy
from sympy import *
from sympy.abc import *
from sympy.combinatorics.named_groups import CyclicGroup, SymmetricGroup
import itertools
import functools

# Top-level setup
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
S3 = SymmetricGroup(3)

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: a is an element of R",
    "H_3: the image of a in the quotient ring R/I is a unit",
    "¬Q: The ideal I and the principal ideal (a) are not comaximal in R"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    """
    # Duck-typing for pre-evaluated witness
    try:
        if hasattr(witness, 'H1') and hasattr(witness, 'H2') and hasattr(witness, 'H3') and hasattr(witness, 'neg_Q'):
            return [bool(witness.H1()), bool(witness.H2()), bool(witness.H3()), bool(witness.neg_Q())]
    except Exception:
        pass

    # Fallback to explicit ring evaluation
    try:
        if isinstance(witness, tuple) and len(witness) == 6:
            elements, add, mul, zero, I, a = witness
        else:
            elements = witness.elements
            add = witness.add
            mul = witness.mul
            zero = witness.zero
            I = witness.I
            a = witness.a
            
        elements = list(elements)
        I = list(I)
    except Exception:
        return [False, False, False, False]

    def neg(x):
        for y in elements:
            if add(x, y) == zero:
                return y
        return None

    # H1: R is a commutative ring
    h1 = True
    try:
        for x in elements:
            if add(x, zero) != x: h1 = False
            if add(zero, x) != x: h1 = False
            if neg(x) is None: h1 = False
            for y in elements:
                if add(x, y) != add(y, x): h1 = False
                if mul(x, y) != mul(y, x): h1 = False
                for z in elements:
                    if add(add(x, y), z) != add(x, add(y, z)): h1 = False
                    if mul(mul(x, y), z) != mul(x, mul(y, z)): h1 = False
                    if mul(x, add(y, z)) != add(mul(x, y), mul(x, z)): h1 = False
    except Exception:
        h1 = False

    # H2: a is an element of R
    try:
        h2 = a in elements
    except Exception:
        h2 = False

    # H3: the image of a in R/I is a unit
    h3 = False
    try:
        # Check if I is an ideal
        is_ideal = True
        for i in I:
            for j in I:
                if add(i, j) not in I: is_ideal = False
            for x in elements:
                if mul(x, i) not in I: is_ideal = False
        
        if is_ideal:
            # Find identities in R/I
            # e is an identity in R/I if for all x in R, e*x - x in I
            identities_RI = []
            for e in elements:
                is_id = True
                for x in elements:
                    if add(mul(e, x), neg(x)) not in I:
                        is_id = False
                        break
                if is_id:
                    identities_RI.append(e)
            
            # Check if a is a unit in R/I
            # a is a unit if there exists b in R such that a*b - e in I for some identity e in R/I
            if identities_RI:
                for e in identities_RI:
                    for b in elements:
                        if add(mul(a, b), neg(e)) in I:
                            h3 = True
                            break
                    if h3:
                        break
    except Exception:
        h3 = False

    # neg_Q: I and (a) are NOT comaximal in R
    neg_q = False
    try:
        # Generate principal ideal (a)
        # In a general commutative ring (possibly without identity),
        # (a) = { r*a + n*a | r in R, n in Z }
        principal_a = set()
        for r in elements:
            principal_a.add(mul(r, a))
        
        # Add integer multiples of a
        curr = a
        while curr not in principal_a:
            principal_a.add(curr)
            curr = add(curr, a)
        principal_a.add(zero)
        
        # Compute I + (a)
        sum_ideal = set()
        for i in I:
            for pa in principal_a:
                sum_ideal.add(add(i, pa))
        
        # They are comaximal if sum_ideal == elements
        is_comaximal = (len(sum_ideal) == len(elements))
        neg_q = not is_comaximal
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]