import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
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

def extract_witness(witness):
    """
    Extracts G, X, op, action, e from the witness.
    Supports multiple formats for ease of use.
    """
    # Format 1: 5-tuple (G, X, op, action, e)
    if isinstance(witness, tuple) and len(witness) == 5:
        return witness
    
    # Format 2: Object with attributes
    if hasattr(witness, 'G') and hasattr(witness, 'X') and hasattr(witness, 'op') and hasattr(witness, 'action') and hasattr(witness, 'e'):
        return witness.G, witness.X, witness.op, witness.action, witness.e
        
    # Format 3: SymPy PermutationGroup (X is implicitly the degree domain)
    if hasattr(witness, 'degree') and hasattr(witness, 'elements'):
        G = list(witness.elements)
        X = list(range(witness.degree))
        op = lambda g, h: g * h
        action = lambda g, x: g(x)
        e = witness.identity
        return G, X, op, action, e
        
    # Format 4: 2-tuple (PermutationGroup, X)
    if isinstance(witness, tuple) and len(witness) == 2:
        grp, X = witness
        if hasattr(grp, 'elements'):
            G = list(grp.elements)
            op = lambda g, h: g * h
            action = lambda g, x: g(x)
            e = grp.identity
            return G, list(X), op, action, e

    raise ValueError("Unknown witness format")

def conditions(witness) -> list[bool]:
    try:
        G, X, op, action, e = extract_witness(witness)
    except Exception:
        return [False, False, False]
        
    # H_1: G is a group
    try:
        h1 = True
        if e not in G:
            h1 = False
        else:
            for a in G:
                if op(a, e) != a or op(e, a) != a:
                    h1 = False
                    break
                has_inv = False
                for b in G:
                    if op(a, b) == e and op(b, a) == e:
                        has_inv = True
                        break
                if not has_inv:
                    h1 = False
                    break
                for b in G:
                    if op(a, b) not in G:
                        h1 = False
                        break
                    for c in G:
                        if op(a, op(b, c)) != op(op(a, b), c):
                            h1 = False
                            break
                    if not h1:
                        break
                if not h1:
                    break
    except Exception:
        h1 = False

    # H_2: G acts on X
    try:
        h2 = True
        for x in X:
            if action(e, x) != x:
                h2 = False
                break
            for g in G:
                gx = action(g, x)
                if gx not in X:
                    h2 = False
                    break
                for h in G:
                    if action(g, action(h, x)) != action(op(g, h), x):
                        h2 = False
                        break
                if not h2:
                    break
            if not h2:
                break
    except Exception:
        h2 = False

    # ¬Q: The conclusion fails at the witness.
    # Conclusion: The action is regular iff it is transitive and the stabilizer of every element is trivial.
    # We evaluate this under the two most common standard definitions of regular/transitive to catch the edge case (empty set).
    try:
        # 1. Vacuous transitivity: for all x, y in X, exists g in G such that g.x = y
        trans_vac = True
        for x in X:
            for y in X:
                if not any(action(g, x) == y for g in G):
                    trans_vac = False
                    break
            if not trans_vac:
                break
                
        # 2. Orbit transitivity: exactly one orbit
        if not X:
            trans_orb = False
        else:
            orbit = []
            for g in G:
                gx = action(g, X[0])
                if gx not in orbit:
                    orbit.append(gx)
            trans_orb = (len(orbit) == len(X))
            
        # Free action: stabilizer of every element is trivial
        free = True
        for x in X:
            for g in G:
                if action(g, x) == x and g != e:
                    free = False
                    break
            if not free:
                break
                
        # Regular definition A: Isomorphic to left regular action (|X| == |G| and transitive and free)
        reg_A = (len(X) == len(G)) and trans_vac and free
        
        # Regular definition B: Sharply 1-transitive
        reg_B = True
        for x in X:
            for y in X:
                count = sum(1 for g in G if action(g, x) == y)
                if count != 1:
                    reg_B = False
                    break
            if not reg_B:
                break
                
        # The conjecture is false if the equivalence fails under standard interpretations
        iff_A = (reg_A == (trans_vac and free))
        iff_B = (reg_B == (trans_orb and free))
        
        neg_q = (not iff_A) or (not iff_B)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: G acts on X",
    "¬Q: The equivalence between regular action and (transitive + free) fails"
]

N_HYP = 2
NEG_Q_INDEX = 2