import sympy
from sympy.combinatorics import PermutationGroup
from sympy.ntheory import factorint

# Top-level setup
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

N_HYP = 4
NEG_Q_INDEX = 4

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: either n >= 3, or both n = 2 and |F| > 3",
    "H_3: GL_n(F) is the general linear group of degree n over F",
    "H_4: SL_n(F) is the special linear group of degree n over F",
    "¬Q: The commutator subgroup of GL_n(F) is not SL_n(F)"
]

def conditions(witness):
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            F = witness.get('F')
            G = witness.get('G')
            S = witness.get('S')
        elif hasattr(witness, 'n') and hasattr(witness, 'F'):
            n = witness.n
            F = witness.F
            G = witness.G
            S = witness.S
        else:
            n, F, G, S = witness
    except Exception:
        return [False] * 5
        
    # H1: F is a field
    try:
        if isinstance(F, int):
            h1 = (F > 1) and (len(factorint(F)) == 1)
        else:
            h1 = getattr(F, 'is_Field', False) or getattr(F, 'is_field', False) or (F in ['R', 'C', 'Q'])
    except Exception:
        h1 = False
        
    # H2: n >= 3 or (n == 2 and |F| > 3)
    try:
        if isinstance(F, int):
            q = F
        else:
            try:
                q = F.order
            except AttributeError:
                q = float('inf')
        h2 = (n >= 3) or (n == 2 and q > 3)
    except Exception:
        h2 = False
        
    # H3: G is GL_n(F)
    try:
        if isinstance(F, int):
            q = F
            order = 1
            for i in range(n):
                order *= (q**n - q**i)
            h3 = (G.order() == order)
        else:
            h3 = hasattr(G, 'order') and hasattr(G, 'derived_subgroup')
    except Exception:
        h3 = False
        
    # H4: S is SL_n(F)
    try:
        if isinstance(F, int):
            q = F
            if q <= 1:
                h4 = False
            else:
                order = 1
                for i in range(n):
                    order *= (q**n - q**i)
                sl_ord = order // (q - 1)
                h4 = (S.order() == sl_ord) and S.is_subgroup(G)
        else:
            h4 = hasattr(S, 'order') and hasattr(S, 'is_subgroup')
    except Exception:
        h4 = False
        
    # neg_Q: commutator of G is not S
    try:
        if hasattr(G, 'derived_subgroup'):
            D = G.derived_subgroup()
            neg_q = (D != S)
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]