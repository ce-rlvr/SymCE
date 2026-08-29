import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        G, c, i = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a nilpotent group of nilpotency class c
    try:
        if not hasattr(G, 'lower_central_series'):
            h1 = False
        else:
            if not (isinstance(c, int) or (hasattr(c, 'is_integer') and c.is_integer)):
                h1 = False
            else:
                lcs = G.lower_central_series()
                is_nilpotent = (len(list(lcs[-1].generate())) == 1)
                actual_c = len(lcs) - 1
                c_val = int(c)
                h1 = is_nilpotent and (actual_c == c_val)
    except Exception:
        h1 = False

    # H_2: Z_j(G) denotes the j-th term of the upper central series of G
    try:
        # Definitional hypothesis; verify G is a valid group by accessing its identity
        _ = G.identity
        h2 = True
    except Exception:
        h2 = False

    # H_3: i is an integer such that 1 <= i <= c + 1
    try:
        if not (isinstance(i, int) or (hasattr(i, 'is_integer') and i.is_integer)):
            h3 = False
        else:
            c_val = int(c)
            i_val = int(i)
            h3 = (1 <= i_val <= c_val + 1)
    except Exception:
        h3 = False

    # ¬Q: \gamma_i(G) is not a subgroup of Z_{c-i+1}(G)
    try:
        if not h1 or not h3:
            neg_q = False
        else:
            c_val = int(c)
            i_val = int(i)
            lcs = G.lower_central_series()
            
            # \gamma_i(G) is the i-th term of the lower central series (1-indexed)
            gamma_i = lcs[i_val - 1]
            
            # Z_{c-i+1}(G)
            Z_idx = c_val - i_val + 1
            
            if Z_idx <= 0:
                Z_set = {G.identity}
            else:
                elements = list(G.generate())
                Z_prev = {G.identity}
                for _ in range(Z_idx):
                    Z_curr = set()
                    for x in elements:
                        is_in_Z = True
                        for g in elements:
                            # Commutator [x, g] = x^-1 g^-1 x g
                            comm = (~x) * (~g) * x * g
                            if comm not in Z_prev:
                                is_in_Z = False
                                break
                        if is_in_Z:
                            Z_curr.add(x)
                    Z_prev = Z_curr
                    if len(Z_prev) == len(elements):
                        break
                Z_set = Z_prev
                
            gamma_i_elements = list(gamma_i.generate())
            is_subgroup = all(g in Z_set for g in gamma_i_elements)
            
            neg_q = not is_subgroup
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a nilpotent group of nilpotency class c",
    "H_2: Z_j(G) denotes the j-th term of the upper central series of G",
    "H_3: i is an integer such that 1 <= i <= c + 1",
    "¬Q: \\gamma_i(G) is not a subgroup of Z_{c-i+1}(G)"
]

N_HYP = 3
NEG_Q_INDEX = 3