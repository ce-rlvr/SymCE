import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion
    of the modified Glauberman's Lemma on Coprime Action.
    
    Witness is expected to be a tuple: (A, G, action, C)
    where:
      - A and G are PermutationGroup objects.
      - action is a callable action(a, g) returning an element of G.
      - C is an iterable of elements of G representing a conjugacy class.
    """
    try:
        A, G, action, C_iter = witness
        C = list(C_iter)
    except Exception:
        return [False, False, False, False]

    # H1: A and G are finite groups
    try:
        h1 = isinstance(A, PermutationGroup) and isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: A acts on G by automorphisms
    try:
        h2 = True
        if h1 and callable(action):
            A_elems = list(A.elements)
            G_elems = list(G.elements)
            
            try:
                id_A = A.identity
            except AttributeError:
                id_A = A_elems[0]**0
                
            # Check closure of action
            for a in A_elems:
                for g in G_elems:
                    if action(a, g) not in G_elems:
                        h2 = False
                        break
                if not h2: break
                
            # Check identity action
            if h2:
                for g in G_elems:
                    if action(id_A, g) != g:
                        h2 = False
                        break
            
            # Check homomorphism property: action(a1 * a2, g) == action(a1, action(a2, g))
            if h2:
                for a1 in A_elems:
                    for a2 in A_elems:
                        a12 = a1 * a2
                        for g in G_elems:
                            if action(a12, g) != action(a1, action(a2, g)):
                                h2 = False
                                break
                        if not h2: break
                    if not h2: break
            
            # Check automorphism property: action(a, g1 * g2) == action(a, g1) * action(a, g2)
            if h2:
                for a in A_elems:
                    for g1 in G_elems:
                        for g2 in G_elems:
                            if action(a, g1 * g2) != action(a, g1) * action(a, g2):
                                h2 = False
                                break
                        if not h2: break
                    if not h2: break
        else:
            h2 = False
    except Exception:
        h2 = False

    # H3: A leaves a conjugacy class C of G invariant
    try:
        h3 = True
        if h1 and callable(action):
            if not C:
                h3 = False
            else:
                G_elems = list(G.elements)
                # Check C is a subset of G
                for c in C:
                    if c not in G_elems:
                        h3 = False
                        break
                
                # Check C is exactly one conjugacy class
                if h3:
                    c0 = C[0]
                    orbit = set()
                    for g in G_elems:
                        orbit.add(g * c0 * g**-1)
                    
                    if set(C) != orbit:
                        h3 = False
                
                # Check A leaves C invariant
                if h3:
                    A_elems = list(A.elements)
                    for a in A_elems:
                        for c in C:
                            if action(a, c) not in C:
                                h3 = False
                                break
                        if not h3: break
        else:
            h3 = False
    except Exception:
        h3 = False

    # Negated Conclusion: C contains NO element fixed by A
    try:
        neg_q = True
        if h1 and callable(action):
            A_elems = list(A.elements)
            for c in C:
                fixed = True
                for a in A_elems:
                    if action(a, c) != c:
                        fixed = False
                        break
                if fixed:
                    neg_q = False
                    break
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: A and G are finite groups",
    "H_2: A acts on G by automorphisms",
    "H_3: A leaves a conjugacy class C of G invariant",
    "¬Q: The conjugacy class C contains NO element fixed by the action of A"
]

N_HYP = 3
NEG_Q_INDEX = 3