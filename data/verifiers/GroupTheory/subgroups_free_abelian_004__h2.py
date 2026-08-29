import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_free_abelian_rank(G):
    """
    Helper function to determine the rank of a free abelian group.
    Returns the rank (int) if G is a free abelian group of finite rank, else None.
    """
    if isinstance(G, int) and G >= 0:
        return G
    if isinstance(G, str):
        s = G.strip().replace(' ', '')
        if s == 'Z':
            return 1
        if s.startswith('Z^'):
            try:
                return int(s[2:])
            except ValueError:
                pass
        if s in ('0', '{0}', 'trivial'):
            return 0
    try:
        if hasattr(G, 'order') and G.order() == 1:
            return 0
    except Exception:
        pass
    try:
        if type(G).__name__ == 'FreeGroup':
            if len(G.generators) <= 1:
                return len(G.generators)
    except Exception:
        pass
    return None

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            F = witness.get('F')
            H = witness.get('H')
        elif isinstance(witness, (list, tuple)) and len(witness) >= 2:
            F = witness[0]
            H = witness[1]
        else:
            return [False, False]
    except Exception:
        return [False, False]

    # H_1: Let F be a free abelian group of finite rank n
    try:
        n = get_free_abelian_rank(F)
        h1 = (n is not None)
    except Exception:
        h1 = False

    # Conclusion: H is a free abelian group of rank m, where m <= n
    try:
        m = get_free_abelian_rank(H)
        if m is None or n is None:
            q = False
        else:
            q = (m <= n)
    except Exception:
        q = False

    neg_q = not q

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free abelian group of finite rank n",
    "¬Q: H is not a free abelian group of rank m with m <= n"
]

N_HYP = 1
NEG_Q_INDEX = 1