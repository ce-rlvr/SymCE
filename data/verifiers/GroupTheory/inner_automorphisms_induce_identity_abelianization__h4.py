import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Standard group theory objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

# Standard linear algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: G' is the commutator subgroup of G",
    "H_3: \\phi is an inner automorphism of G",
    "¬Q: \\bar{\\phi} is not the identity map on G/G'"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    h1_ok = False
    h2_ok = False
    h3_ok = False
    neg_q_ok = False
    
    try:
        # Parse witness: can be (G, phi) or (G, G_prime, phi)
        # phi can be a dict, a callable, or an element g that induces the inner automorphism
        if len(witness) == 2:
            G, second = witness
            if isinstance(second, dict) or callable(second):
                phi = second
            else:
                g_elem = second
                phi = lambda x: g_elem * x * ~g_elem
        elif len(witness) == 3:
            G, G_prime_witness, third = witness
            if isinstance(third, dict) or callable(third):
                phi = third
            else:
                g_elem = third
                phi = lambda x: g_elem * x * ~g_elem
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: G' is the commutator subgroup of G
    try:
        if h1_ok:
            if len(witness) == 2:
                G_prime = G.derived_subgroup()
                h2_ok = True
            else:
                G_prime = G_prime_witness
                derived = G.derived_subgroup()
                h2_ok = G_prime.is_subgroup(derived) and derived.is_subgroup(G_prime)
    except Exception:
        h2_ok = False

    # H_3: \phi is an inner automorphism of G
    try:
        if h1_ok:
            elements = list(G.generate())
            is_inner = False
            for g in elements:
                match = True
                for x in elements:
                    px = phi[x] if isinstance(phi, dict) else phi(x)
                    if px != g * x * ~g:
                        match = False
                        break
                if match:
                    is_inner = True
                    break
            h3_ok = is_inner
    except Exception:
        h3_ok = False

    # ¬Q: \bar{\phi} is not the identity map on G/G'
    try:
        if h1_ok and h2_ok:
            elements = list(G.generate())
            q_holds = True
            for x in elements:
                px = phi[x] if isinstance(phi, dict) else phi(x)
                # \bar{\phi}(x G') = x G' iff x^{-1} \phi(x) \in G'
                # In sympy's left-to-right multiplication, this is ~x * px
                if (~x * px) not in G_prime:
                    q_holds = False
                    break
            neg_q_ok = not q_holds
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]