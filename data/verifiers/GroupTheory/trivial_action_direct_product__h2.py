import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
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

def _make_v4():
    deg_N = 2
    deg_H = 2
    gens = []
    for g in Z2.generators:
        arr = [g(i) for i in range(deg_N)]
        arr += list(range(deg_N, deg_N + deg_H))
        gens.append(Permutation(arr))
    for g in Z2.generators:
        arr = [g(i) for i in range(deg_H)]
        padded = list(range(deg_N)) + [x + deg_N for x in arr]
        gens.append(Permutation(padded))
    return PermutationGroup(*gens)

V4 = _make_v4()

CONDITION_LABELS = [
    "H_1: Let N and H be groups",
    "H_2: phi(h) is the identity automorphism of N for all h in H",
    "¬Q: The semidirect product N rtimes_phi H is NOT isomorphic to the direct product N x H"
]
N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    def direct_product(N, H):
        deg_N = N.degree
        deg_H = H.degree
        
        gens = []
        for g in N.generators:
            arr = [g(i) for i in range(deg_N)]
            arr += list(range(deg_N, deg_N + deg_H))
            gens.append(Permutation(arr))
            
        for g in H.generators:
            arr = [g(i) for i in range(deg_H)]
            padded = list(range(deg_N)) + [x + deg_N for x in arr]
            gens.append(Permutation(padded))
            
        if not gens:
            return PermutationGroup(Permutation(0))
        return PermutationGroup(*gens)

    h1 = False
    h2 = False
    neg_q = False

    interpretation = None
    if isinstance(witness, tuple):
        if len(witness) == 3 and all(isinstance(x, PermutationGroup) for x in witness):
            interpretation = 'internal'
        elif len(witness) == 4 and isinstance(witness[0], PermutationGroup) and isinstance(witness[1], PermutationGroup) and isinstance(witness[3], PermutationGroup):
            interpretation = 'external_S'
        elif len(witness) == 3 and isinstance(witness[0], PermutationGroup) and isinstance(witness[1], PermutationGroup):
            interpretation = 'external'

    if interpretation == 'internal':
        G, N, H = witness
        
        try:
            h1 = True
        except Exception:
            h1 = False
            
        try:
            h2 = True
            for h in H.elements:
                h_inv = h**-1
                for n in N.elements:
                    if h * n * h_inv != n:
                        h2 = False
                        break
                if not h2:
                    break
        except Exception:
            h2 = False
            
        try:
            DP = direct_product(N, H)
            neg_q = not G.is_isomorphic(DP)
        except Exception:
            neg_q = False

    elif interpretation == 'external_S':
        N, H, phi, S = witness
        
        try:
            h1 = True
        except Exception:
            h1 = False
            
        try:
            h2 = True
            for h in H.elements:
                aut = phi(h) if callable(phi) else phi[h]
                for n in N.elements:
                    val = aut(n) if callable(aut) else aut[n]
                    if val != n:
                        h2 = False
                        break
                if not h2:
                    break
        except Exception:
            h2 = False
            
        try:
            DP = direct_product(N, H)
            neg_q = not S.is_isomorphic(DP)
        except Exception:
            neg_q = False

    elif interpretation == 'external':
        N, H, phi = witness
        
        try:
            h1 = True
        except Exception:
            h1 = False
            
        try:
            h2 = True
            for h in H.elements:
                aut = phi(h) if callable(phi) else phi[h]
                for n in N.elements:
                    val = aut(n) if callable(aut) else aut[n]
                    if val != n:
                        h2 = False
                        break
                if not h2:
                    break
        except Exception:
            h2 = False
            
        try:
            neg_q = False
        except Exception:
            neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]