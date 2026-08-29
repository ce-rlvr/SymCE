import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime

# Top-level setup: named object bindings that the witness expression may reference.
# In Galois theory, the witness is typically the Galois group of the extension E/F and the prime p.
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z5 = CyclicGroup(5)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    # Extract the Galois group G and prime p from the witness
    try:
        if isinstance(witness, dict):
            G = witness.get('G') or witness.get('GaloisGroup') or witness.get('E')
            p = witness.get('p')
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 2:
                G, p = witness
            elif len(witness) == 3:
                _, G, p = witness
            else:
                G, p = None, None
        else:
            G, p = None, None
    except Exception:
        G, p = None, None

    # H_1: F is a field
    # Represented by the existence of a valid Galois group for the extension
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: E is a finite Galois extension of F
    # Represented by the Galois group being finite
    try:
        if h1:
            try:
                g_order = G.order()
            except TypeError:
                g_order = G.order
            h2 = g_order > 0
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: p is a prime number
    try:
        h3 = isprime(p)
    except Exception:
        h3 = False

    # ¬Q: There is NO intermediate field K between F and E such that K/F is a Galois extension of degree p.
    # By the Fundamental Theorem of Galois Theory, this is equivalent to saying that G has NO normal subgroup
    # of index p. Since p is prime, any quotient group of order p is abelian. Thus, a normal subgroup of index p
    # exists if and only if p divides the order of the abelianization G/G' (where G' is the derived subgroup).
    try:
        neg_q = False
        if h2 and h3:
            try:
                derived = G.derived_subgroup()
                try:
                    g_order = G.order()
                except TypeError:
                    g_order = G.order
                try:
                    d_order = derived.order()
                except TypeError:
                    d_order = derived.order
                
                index = g_order // d_order
                neg_q = (index % p != 0)
            except Exception:
                # Fallback: iterate over all normal subgroups
                has_index_p = False
                for N in G.normal_subgroups():
                    try:
                        g_order = G.order()
                    except TypeError:
                        g_order = G.order
                    try:
                        n_order = N.order()
                    except TypeError:
                        n_order = N.order
                        
                    if g_order == p * n_order:
                        has_index_p = True
                        break
                neg_q = not has_index_p
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: E is a finite Galois extension of F",
    "H_3: p is a prime number",
    "¬Q: There is no intermediate field K between F and E such that K/F is a Galois extension of degree p"
]

N_HYP = 3
NEG_Q_INDEX = 3