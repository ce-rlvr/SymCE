import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
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

def conditions(witness) -> list[bool]:
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness can be either (G, alpha, beta) or (G, Omega, alpha, beta).
    """
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                G, alpha, beta = witness
                if isinstance(G, PermutationGroup):
                    Omega = set(range(G.degree))
                else:
                    Omega = set()
            elif len(witness) == 4:
                G, Omega, alpha, beta = witness
                Omega = set(Omega)
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: G is a permutation group acting transitively on a set Omega
    try:
        if not isinstance(G, PermutationGroup):
            h1 = False
        elif not Omega:
            h1 = False
        else:
            orbit = G.orbit(list(Omega)[0])
            h1 = (set(orbit) == Omega)
    except Exception:
        h1 = False

    # H_2: alpha and beta are two arbitrary elements of Omega
    try:
        h2 = (alpha in Omega) and (beta in Omega)
    except Exception:
        h2 = False

    # neg_Q: G_alpha and G_beta are NOT conjugate subgroups in G
    try:
        if not isinstance(G, PermutationGroup):
            neg_q = False
        else:
            G_beta = G.stabilizer(beta)
            orbit_alpha = G.orbit(alpha)
            are_conjugate = False
            
            # Two stabilizers G_alpha and G_beta are conjugate in G if and only if 
            # G_beta is equal to G_x for some x in the orbit of alpha.
            for x in orbit_alpha:
                G_x = G.stabilizer(x)
                if G_x.order() == G_beta.order():
                    # Check if G_x is a subgroup of G_beta (and thus equal, since orders match)
                    if all(g in G_beta for g in G_x.generators):
                        are_conjugate = True
                        break
            
            neg_q = not are_conjugate
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a permutation group acting transitively on a set Omega",
    "H_2: alpha and beta are elements of Omega",
    "¬Q: G_alpha and G_beta are not conjugate subgroups in G"
]

N_HYP = 2
NEG_Q_INDEX = 2