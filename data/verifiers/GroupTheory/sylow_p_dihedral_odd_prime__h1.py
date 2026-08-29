import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
    Given a witness, checks if it is a valid counterexample to the false conjecture.
    The witness should be a tuple (p, n, G) or (p, n), or a dictionary with these keys.
    """
    try:
        if isinstance(witness, dict):
            p = witness.get('p')
            n = witness.get('n')
            G = witness.get('G')
            if G is None and n is not None:
                G = DihedralGroup(n)
        elif isinstance(witness, tuple):
            if len(witness) == 3:
                p, n, G = witness
            elif len(witness) == 2:
                p, n = witness
                G = DihedralGroup(n)
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: p is an odd prime dividing n
    try:
        h1 = sympy.isprime(p) and (p % 2 != 0) and (n % p == 0)
    except Exception:
        h1 = False

    # H_2: G is the dihedral group of order 2n
    try:
        if hasattr(G, 'order'):
            order = G.order() if callable(G.order) else G.order
            if order == 2 * n:
                if n > 2:
                    h2 = not G.is_abelian
                else:
                    h2 = bool(G.is_abelian)
            else:
                h2 = False
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: It is NOT the case that every Sylow p-subgroup of G is cyclic and normal in G
    try:
        if not h2:
            neg_q = False
        else:
            # Find a Sylow p-subgroup
            P = G.sylow_subgroup(p)
            
            # Check if P is cyclic
            is_cyclic = bool(P.is_cyclic)
            
            # Check if P is normal in G
            is_normal = True
            for g in G.generators:
                g_inv = ~g
                for h in P.generators:
                    # Check closure under conjugation by generators of G
                    if not P.contains(g * h * g_inv):
                        is_normal = False
                        break
                    if not P.contains(g_inv * h * g):
                        is_normal = False
                        break
                if not is_normal:
                    break
            
            # The conclusion fails if the Sylow p-subgroup is either not cyclic or not normal
            neg_q = not (is_cyclic and is_normal)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: p is an odd prime dividing n",
    "H_2: G is the dihedral group of order 2n",
    "¬Q: There exists a Sylow p-subgroup of G that is not cyclic or not normal in G"
]

N_HYP = 2
NEG_Q_INDEX = 2