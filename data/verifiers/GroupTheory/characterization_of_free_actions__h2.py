import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def parse_witness(witness):
    """
    Parses the witness into a group G, a domain X, and an action function.
    Supports various formats for convenience.
    """
    if isinstance(witness, PermutationGroup):
        G = witness
        X = list(range(G.degree))
        action = lambda g, x: g(x)
        return G, X, action
    if isinstance(witness, Permutation):
        G = PermutationGroup(witness)
        X = list(range(G.degree))
        action = lambda g, x: g(x)
        return G, X, action
    if isinstance(witness, (list, tuple)):
        if len(witness) > 0 and all(isinstance(w, Permutation) for w in witness):
            G = PermutationGroup(*witness)
            X = list(range(G.degree))
            action = lambda g, x: g(x)
            return G, X, action
        if len(witness) == 2:
            G, X = witness
            if isinstance(G, PermutationGroup) and isinstance(X, (list, tuple, set)):
                action = lambda g, x: g(x)
                return G, list(X), action
        if len(witness) == 3:
            G, X, action = witness
            if isinstance(G, PermutationGroup) and isinstance(X, (list, tuple, set)) and callable(action):
                return G, list(X), action
    return None, None, None

def conditions(witness) -> list[bool]:
    try:
        G, X, action = parse_witness(witness)
        if G is None:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # Prevent hanging on extremely large groups
    try:
        if int(G.order()) > 1000:
            return [h1, False, False]
        elements = list(G.elements)
    except Exception:
        return [h1, False, False]

    # H_2: G acts on X
    try:
        if not X:
            h2 = True
        else:
            h2 = True
            # Check identity acts trivially
            for x in X:
                if action(G.identity, x) != x:
                    h2 = False
                    break
            # Check closure of the action
            if h2:
                for g in elements:
                    for x in X:
                        if action(g, x) not in X:
                            h2 = False
                            break
                    if not h2:
                        break
    except Exception:
        h2 = False

    # neg_Q: The conclusion fails
    try:
        if not X:
            is_free = True
            every_trivial = True
            some_trivial = False
        else:
            # An action is free if no non-identity element has a fixed point
            is_free = True
            for g in elements:
                if not g.is_Identity:
                    if any(action(g, x) == x for x in X):
                        is_free = False
                        break
            
            every_trivial = True
            some_trivial = False
            for x in X:
                stab_is_trivial = True
                for g in elements:
                    if action(g, x) == x and not g.is_Identity:
                        stab_is_trivial = False
                        break
                if stab_is_trivial:
                    some_trivial = True
                else:
                    every_trivial = False

        # The prompt's text "every element" makes the equivalence a tautology.
        # We check both the literal translation and the likely intended "some element" 
        # translation (which corresponds to dropping the transitivity hypothesis).
        text_fails = not (is_free == every_trivial)
        intended_fails = not (is_free == some_trivial)
        
        neg_q = text_fails or intended_fails
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: G acts on X",
    "¬Q: The equivalence between free action and trivial stabilizers fails"
]

N_HYP = 2
NEG_Q_INDEX = 2