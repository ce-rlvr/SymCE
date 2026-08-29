import sympy
import sympy.ntheory as nt
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: N is an abelian normal p-subgroup of G",
    "H_3: P is a Sylow p-subgroup of G",
    "H_4: There exists a complement of N in P",
    "¬Q: N does not have a complement in G"
]

N_HYP = 4
NEG_Q_INDEX = 4

def is_abelian(group):
    if hasattr(group, 'is_abelian'):
        val = group.is_abelian
        return val() if callable(val) else val
    return False

def is_normal(subgroup, group):
    if hasattr(subgroup, 'is_normal'):
        val = subgroup.is_normal(group)
        return val() if callable(val) else val
    if hasattr(group, 'is_normal'):
        val = group.is_normal(subgroup)
        return val() if callable(val) else val
    return False

def is_p_group(group, p):
    if hasattr(group, 'is_p_group'):
        val = group.is_p_group(p)
        return val() if callable(val) else val
    if hasattr(group, 'order'):
        order = group.order()
        if order == 1: return True
        factors = nt.factorint(order)
        return list(factors.keys()) == [p]
    return False

def is_sylow(subgroup, p, group):
    if hasattr(subgroup, 'is_sylow'):
        val = subgroup.is_sylow(p, group)
        return val() if callable(val) else val
    if hasattr(group, 'is_sylow'):
        val = group.is_sylow(subgroup, p)
        return val() if callable(val) else val
    if hasattr(group, 'order') and hasattr(subgroup, 'order'):
        g_order = group.order()
        s_order = subgroup.order()
        if s_order == 1:
            return p not in nt.factorint(g_order)
        factors = nt.factorint(s_order)
        if list(factors.keys()) != [p]: return False
        return (g_order // s_order) % p != 0
    return False

def check_complement(P, N, H_P):
    if hasattr(P, 'is_complement'):
        val = P.is_complement(N, H_P)
        return val() if callable(val) else val
    
    is_sub = False
    if hasattr(H_P, 'is_subgroup'):
        val = H_P.is_subgroup(P)
        is_sub = val() if callable(val) else val
    else:
        is_sub = True
        
    inter_trivial = False
    if hasattr(N, 'intersect'):
        inter = N.intersect(H_P)
        if hasattr(inter, 'order'):
            inter_trivial = (inter.order() == 1)
        elif hasattr(inter, 'is_trivial'):
            val = inter.is_trivial
            inter_trivial = val() if callable(val) else val
    elif hasattr(N, 'intersection'):
        inter = N.intersection(H_P)
        if hasattr(inter, 'order'):
            inter_trivial = (inter.order() == 1)
        elif hasattr(inter, 'is_trivial'):
            val = inter.is_trivial
            inter_trivial = val() if callable(val) else val
    elif hasattr(N, 'elements') and hasattr(H_P, 'elements'):
        inter_trivial = len(set(N.elements).intersection(set(H_P.elements))) == 1
        
    generates = False
    if hasattr(N, 'order') and hasattr(H_P, 'order') and hasattr(P, 'order'):
        generates = (N.order() * H_P.order() == P.order())
    elif hasattr(P, 'is_generated_by'):
        val = P.is_generated_by(N, H_P)
        generates = val() if callable(val) else val
        
    return is_sub and inter_trivial and generates

def extract(witness):
    if isinstance(witness, dict):
        return witness.get('G'), witness.get('N'), witness.get('p'), witness.get('P'), witness.get('H_P')
    elif isinstance(witness, tuple) or isinstance(witness, list):
        if len(witness) == 4:
            return witness[0], witness[1], witness[2], witness[3], None
        elif len(witness) >= 5:
            return witness[0], witness[1], witness[2], witness[3], witness[4]
    else:
        return getattr(witness, 'G', None), getattr(witness, 'N', None), getattr(witness, 'p', None), getattr(witness, 'P', None), getattr(witness, 'H_P', None)

def conditions(witness):
    try:
        G, N, p, P, H_P = extract(witness)
    except Exception:
        return [False, False, False, False, False]

    # H1
    try:
        h1 = bool(nt.isprime(p))
    except Exception:
        h1 = False

    # H2
    try:
        h2 = False
        if G is not None and N is not None:
            is_sub = False
            if hasattr(N, 'is_subgroup'):
                val = N.is_subgroup(G)
                is_sub = val() if callable(val) else val
            else:
                is_sub = True
            
            if is_sub:
                is_ab = is_abelian(N)
                is_norm = is_normal(N, G)
                is_p = is_p_group(N, p)
                h2 = bool(is_ab and is_norm and is_p)
    except Exception:
        h2 = False

    # H3
    try:
        h3 = False
        if G is not None and P is not None:
            h3 = bool(is_sylow(P, p, G))
    except Exception:
        h3 = False

    # H4
    try:
        h4 = False
        if P is not None and N is not None:
            if H_P is not None:
                h4 = bool(check_complement(P, N, H_P))
            else:
                if hasattr(P, 'has_complement'):
                    val = P.has_complement(N)
                    h4 = bool(val() if callable(val) else val)
    except Exception:
        h4 = False

    # neg_Q
    try:
        neg_q = False
        if G is not None and N is not None:
            if hasattr(G, 'has_complement'):
                val = G.has_complement(N)
                has_comp = val() if callable(val) else val
                neg_q = not has_comp
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]