import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should be a tuple: (G, alpha, beta)
    where G is a PermutationGroup, and alpha, beta are integers representing points in the domain.
    """
    try:
        G, alpha, beta = witness
    except Exception:
        return [False, False, False]
    
    # H_1: alpha and beta are elements of the domain Omega of G
    try:
        if isinstance(G, PermutationGroup) and isinstance(alpha, (int, sympy.Integer)) and isinstance(beta, (int, sympy.Integer)):
            degree = G.degree() if callable(G.degree) else G.degree
            h1 = bool(0 <= alpha < degree and 0 <= beta < degree)
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: G_alpha and G_beta are the stabilizers of alpha and beta in G
    try:
        if h1:
            G_alpha = G.stabilizer(alpha)
            G_beta = G.stabilizer(beta)
            h2 = isinstance(G_alpha, PermutationGroup) and isinstance(G_beta, PermutationGroup)
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: G_alpha and G_beta are NOT conjugate subgroups in G
    try:
        if h1 and h2:
            are_conjugate = False
            order_alpha = G_alpha.order() if callable(G_alpha.order) else G_alpha.order
            order_beta = G_beta.order() if callable(G_beta.order) else G_beta.order
            
            # If orders are different, they cannot be conjugate
            if order_alpha == order_beta:
                beta_elements = set(G_beta.generate())
                # Check if there exists g in G such that g * G_alpha * g^-1 == G_beta
                for g in G.generate():
                    # Since orders are equal, we only need to check if generators of G_alpha 
                    # conjugated by g are all in G_beta.
                    if all((g * h * ~g) in beta_elements for h in G_alpha.generators):
                        are_conjugate = True
                        break
            neg_q = not are_conjugate
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: alpha and beta are elements of the domain Omega of G",
    "H_2: G_alpha and G_beta are the stabilizers of alpha and beta in G",
    "¬Q: G_alpha and G_beta are not conjugate subgroups in G"
]

N_HYP = 2
NEG_Q_INDEX = 2