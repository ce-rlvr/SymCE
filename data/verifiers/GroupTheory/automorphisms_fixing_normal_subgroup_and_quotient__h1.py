import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AbelianGroup(2, 2)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: N is an abelian normal subgroup of G",
    "H_2: A is the set of automorphisms fixing N and G/N",
    "¬Q: A is not an abelian subgroup of Aut(G)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def get_A(G, N):
    elements = list(G.generate())
    N_elems = list(N.generate())
    S = G.generators
    A = []
    
    ident = None
    for g in elements:
        if g.is_Identity:
            ident = g
            break
    if ident is None:
        ident = elements[0]**0

    for n_tuple in itertools.product(N_elems, repeat=len(S)):
        S_mapping = {s: s * n for s, n in zip(S, n_tuple)}
        alpha = {ident: ident}
        queue = [ident]
        valid = True
        
        while queue:
            curr = queue.pop(0)
            for s in S:
                nxt = curr * s
                mapped_nxt = alpha[curr] * S_mapping[s]
                if nxt not in alpha:
                    alpha[nxt] = mapped_nxt
                    queue.append(nxt)
                else:
                    if alpha[nxt] != mapped_nxt:
                        valid = False
                        break
            if not valid:
                break
                
        if not valid:
            continue
            
        for n in N_elems:
            if alpha[n] != n:
                valid = False
                break
                
        if valid:
            A.append(alpha)
            
    return A, elements

def conditions(witness):
    try:
        G, N = witness
    except Exception:
        return [False, False, False]
        
    # H1: N is an abelian normal subgroup of G
    try:
        h1 = True
        G_elems = set(G.generate())
        for n in N.generators:
            if n not in G_elems:
                h1 = False
                break
        if h1:
            N_elems = set(N.generate())
            for g in G.generators:
                for n in N.generators:
                    if g * n * (g**-1) not in N_elems:
                        h1 = False
                        break
        if h1:
            N_gens = N.generators
            for g1 in N_gens:
                for g2 in N_gens:
                    if g1 * g2 != g2 * g1:
                        h1 = False
                        break
    except Exception:
        h1 = False

    # H2: A is the set of automorphisms fixing N and G/N
    # This is true by definition of our construction of A
    h2 = True

    # neg_Q: A is NOT an abelian subgroup of Aut(G)
    try:
        A, elements = get_A(G, N)
        is_abelian_A = True
        for alpha in A:
            for beta in A:
                for x in elements:
                    if alpha[beta[x]] != beta[alpha[x]]:
                        is_abelian_A = False
                        break
                if not is_abelian_A:
                    break
            if not is_abelian_A:
                break
        neg_q = not is_abelian_A
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]