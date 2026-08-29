import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def apply_phi(Phi, g, n):
    try:
        return Phi(g)(n)
    except Exception:
        pass
    try:
        return Phi[g][n]
    except Exception:
        pass
    return None

def conditions(witness):
    try:
        if len(witness) == 2:
            G, N = witness
            Phi = None
        elif len(witness) == 3:
            G, N, Phi = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H1: G is a group
    try:
        H1 = isinstance(G, PermutationGroup)
    except Exception:
        H1 = False
        
    # H2: \Phi: G \to Aut(N) is the homomorphism defined by \Phi(g)(n) = gng^{-1} for all g \in G and n \in N
    try:
        H2 = True
        if not isinstance(N, PermutationGroup):
            H2 = False
        else:
            for g in G.generate_dimino():
                for n in N.generate_dimino():
                    expected = g * n * g**-1
                    if expected not in N:
                        H2 = False
                        break
                    if Phi is not None:
                        actual = apply_phi(Phi, g, n)
                        if actual != expected:
                            H2 = False
                            break
                if not H2:
                    break
    except Exception:
        H2 = False
        
    # neg_Q: The kernel of \Phi is NOT the centralizer C_G(N)
    try:
        ker_Phi = set()
        for g in G.generate_dimino():
            is_in_ker = True
            for n in N.generate_dimino():
                if Phi is not None:
                    val = apply_phi(Phi, g, n)
                else:
                    val = g * n * g**-1
                if val != n:
                    is_in_ker = False
                    break
            if is_in_ker:
                ker_Phi.add(g)
                
        C_G_N = set()
        for g in G.generate_dimino():
            if all(g * n == n * g for n in N.generate_dimino()):
                C_G_N.add(g)
                
        neg_Q = ker_Phi != C_G_N
    except Exception:
        neg_Q = False
        
    return [H1, H2, neg_Q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: \\Phi: G \\to Aut(N) is the homomorphism defined by \\Phi(g)(n) = gng^{-1} for all g \\in G and n \\in N",
    "\\neg Q: The kernel of \\Phi is not the centralizer C_G(N)"
]

N_HYP = 2
NEG_Q_INDEX = 2