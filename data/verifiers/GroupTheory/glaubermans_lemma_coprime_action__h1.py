import math
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import gcd

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

CONDITION_LABELS = [
    "H_1: A acts on G by automorphisms",
    "H_2: The orders |A| and |G| are coprime",
    "H_3: A leaves a conjugacy class C of G invariant",
    "¬Q: No element in C is fixed by the action of A"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        G, A, action, C = witness
    except Exception:
        return [False, False, False, False]

    try:
        G_elems = list(G.elements) if hasattr(G, 'elements') else list(G)
        A_elems = list(A.elements) if hasattr(A, 'elements') else list(A)
        C_elems = list(C)
    except Exception:
        return [False, False, False, False]

    try:
        if callable(action):
            act = action
        else:
            act = lambda a, g: action[a][g]
    except Exception:
        return [False, False, False, False]

    # H_1: A acts on G by automorphisms
    try:
        h1 = True
        # Find identity of A
        if hasattr(A, 'identity'):
            e_A = A.identity
        else:
            e_A = None
            for e in A_elems:
                if all(e * a == a for a in A_elems):
                    e_A = e
                    break
        
        if e_A is None:
            h1 = False
        else:
            # Check identity action
            for g in G_elems:
                if act(e_A, g) != g:
                    h1 = False
                    break
            
            # Check homomorphism property: act(a, act(b, g)) == act(a*b, g)
            if h1:
                for a in A_elems:
                    for b in A_elems:
                        ab = a * b
                        for g in G_elems:
                            if act(a, act(b, g)) != act(ab, g):
                                h1 = False
                                break
                        if not h1: break
                    if not h1: break
            
            # Check automorphism property: act(a, g*h) == act(a, g) * act(a, h)
            if h1:
                for a in A_elems:
                    for g in G_elems:
                        for h in G_elems:
                            gh = g * h
                            if act(a, gh) != act(a, g) * act(a, h):
                                h1 = False
                                break
                        if not h1: break
                    if not h1: break
            
            # Check closure
            if h1:
                for a in A_elems:
                    for g in G_elems:
                        if act(a, g) not in G_elems:
                            h1 = False
                            break
                    if not h1: break
    except Exception:
        h1 = False

    # H_2: The orders |A| and |G| are coprime
    try:
        h2 = math.gcd(len(A_elems), len(G_elems)) == 1
    except Exception:
        h2 = False

    # H_3: A leaves a conjugacy class C of G invariant
    try:
        h3 = True
        if not C_elems:
            h3 = False
        else:
            # Check C is a subset of G
            for c in C_elems:
                if c not in G_elems:
                    h3 = False
                    break
            
            if h3:
                # Check C is exactly one conjugacy class
                c0 = C_elems[0]
                gen_C = []
                for g in G_elems:
                    try:
                        g_inv = g**-1
                    except Exception:
                        g_inv = ~g
                    conj = g * c0 * g_inv
                    if conj not in gen_C:
                        gen_C.append(conj)
                
                if len(gen_C) != len(C_elems):
                    h3 = False
                else:
                    for c in gen_C:
                        if c not in C_elems:
                            h3 = False
                            break
            
            if h3:
                # Check A leaves C invariant
                for a in A_elems:
                    for c in C_elems:
                        if act(a, c) not in C_elems:
                            h3 = False
                            break
                    if not h3: break
    except Exception:
        h3 = False

    # ¬Q: No element in C is fixed by the action of A
    try:
        neg_q = True
        for c in C_elems:
            fixed = True
            for a in A_elems:
                if act(a, c) != c:
                    fixed = False
                    break
            if fixed:
                neg_q = False
                break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]