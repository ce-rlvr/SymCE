import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the false Orbit Partition Theorem conjecture.
    The witness is expected to provide the group G, the set X, the action `act(g, x)`, 
    and optionally the group multiplication `mult(g1, g2)`.
    """
    try:
        if isinstance(witness, dict):
            G = list(witness['G'])
            X = list(witness['X'])
            act = witness['act']
            if 'mult' in witness:
                mult = witness['mult']
            else:
                mult = lambda a, b: a * b
        elif isinstance(witness, tuple):
            if len(witness) == 4:
                G, mult, X, act = witness
                G = list(G)
                X = list(X)
            elif len(witness) == 3:
                G, X, act = witness
                G = list(G)
                X = list(X)
                mult = lambda a, b: a * b
            else:
                return [False, False, False, False]
        else:
            G = list(witness.G)
            X = list(witness.X)
            act = witness.act
            if hasattr(witness, 'mult'):
                mult = witness.mult
            else:
                mult = lambda a, b: a * b
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group
    h1 = True
    try:
        if not G:
            h1 = False
        else:
            # Check closure
            for a in G:
                for b in G:
                    if mult(a, b) not in G:
                        h1 = False
            # Check associativity
            if h1:
                for a in G:
                    for b in G:
                        for c in G:
                            if mult(mult(a, b), c) != mult(a, mult(b, c)):
                                h1 = False
            # Check identity
            identities = []
            if h1:
                for e in G:
                    if all(mult(e, a) == a and mult(a, e) == a for a in G):
                        identities.append(e)
                if len(identities) != 1:
                    h1 = False
                else:
                    e = identities[0]
                    # Check inverses
                    for a in G:
                        has_inv = False
                        for b in G:
                            if mult(a, b) == e and mult(b, a) == e:
                                has_inv = True
                                break
                        if not has_inv:
                            h1 = False
    except Exception:
        h1 = False

    # H_2: G acts on X (there is a map G x X -> X)
    h2 = True
    try:
        for g in G:
            for x in X:
                if act(g, x) not in X:
                    h2 = False
    except Exception:
        h2 = False

    # H_3: For x, y \in X, a relation \sim is defined such that x \sim y if there exists g \in G such that g \cdot x = y
    # This is a definition, so it holds by construction in our verification.
    h3 = True

    # ¬Q: The relation \sim is NOT an equivalence relation on X, or its equivalence classes are NOT exactly the orbits.
    # Note: If \sim is an equivalence relation, its equivalence classes are exactly the orbits by definition of \sim.
    # Thus, the conclusion fails if and only if \sim is not an equivalence relation.
    neg_q = False
    try:
        def sim(x, y):
            for g in G:
                if act(g, x) == y:
                    return True
            return False
        
        is_equiv = True
        
        # Check reflexive
        for x in X:
            if not sim(x, x):
                is_equiv = False
                break
        
        # Check symmetric
        if is_equiv:
            for x in X:
                for y in X:
                    if sim(x, y) and not sim(y, x):
                        is_equiv = False
                        break
                if not is_equiv:
                    break
        
        # Check transitive
        if is_equiv:
            for x in X:
                for y in X:
                    for z in X:
                        if sim(x, y) and sim(y, z) and not sim(x, z):
                            is_equiv = False
                            break
                    if not is_equiv:
                        break
                if not is_equiv:
                    break
                    
        neg_q = not is_equiv
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: G acts on X",
    "H_3: For x, y in X, a relation ~ is defined such that x ~ y if there exists g in G such that g.x = y",
    "¬Q: The relation ~ is not an equivalence relation on X, or its equivalence classes are not exactly the orbits of G on X"
]

N_HYP = 3
NEG_Q_INDEX = 3