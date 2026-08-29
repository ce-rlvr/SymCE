import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def U_structure(k):
    """
    Returns a sorted tuple of prime-power elementary divisors for the group U(k).
    This uniquely identifies the isomorphism class of the abelian group U(k).
    """
    if not isinstance(k, (int, sympy.Integer)) or k <= 0:
        raise ValueError("k must be a positive integer")
    if k == 1:
        return ()
    
    factors = factorint(k)
    cyclic_components = []
    
    for p, e in factors.items():
        if p == 2:
            if e == 1:
                pass
            elif e == 2:
                cyclic_components.append(2)
            else:
                cyclic_components.append(2)
                cyclic_components.append(2**(e-2))
        else:
            cyclic_components.append((p**(e-1)) * (p - 1))
    
    prime_powers = []
    for m in cyclic_components:
        if m == 1: 
            continue
        fm = factorint(m)
        for q, f in fm.items():
            prime_powers.append(q**f)
            
    prime_powers.sort()
    return tuple(prime_powers)

def conditions(witness) -> list[bool]:
    # The witness is expected to provide both the group G and the integer n.
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            n = witness.get('n')
        else:
            G, n = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup) or getattr(G, 'is_group', False)
    except Exception:
        h1 = False

    # H_2: G is a cyclic group
    try:
        h2 = bool(G.is_cyclic)
    except Exception:
        h2 = False

    # ¬Q: Aut(G) is not isomorphic to U(n)
    try:
        if not isinstance(n, (int, sympy.Integer)) or n <= 0:
            neg_q = False
        else:
            if not h2:
                # If G is not cyclic, we bypass computing Aut(G) to avoid complexity,
                # as it cannot be a valid counterexample anyway.
                neg_q = False
            else:
                # For a finite cyclic group G, Aut(G) is isomorphic to U(|G|).
                # We check if U(|G|) is isomorphic to U(n) by comparing their elementary divisors.
                aut_G_struct = U_structure(G.order())
                U_n_struct = U_structure(n)
                neg_q = (aut_G_struct != U_n_struct)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G is a cyclic group",
    "¬Q: Aut(G) is not isomorphic to U(n)"
]

N_HYP = 2
NEG_Q_INDEX = 2