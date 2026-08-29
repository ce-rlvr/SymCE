import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.matrices import eye, zeros
import itertools

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_cyclic(G):
    try:
        if not G.is_abelian:
            return False
        order = G.order()
        for g in G.elements:
            if g.order() == order:
                return True
        return False
    except Exception:
        return False

def exactly_one_subgroup_of_order(G, d):
    try:
        elements = list(G.elements)
        n_elements = len(elements)
        if d > n_elements:
            return False
        if d == 1:
            return True
        
        if is_cyclic(G):
            return bool(n_elements % int(d) == 0)
            
        if n_elements > 20:
            return False
            
        identity = G.identity
        count = 0
        for subset in itertools.combinations(elements, d):
            if identity not in subset:
                continue
            subset_set = set(subset)
            is_subgroup = True
            for a in subset:
                for b in subset:
                    if a * b not in subset_set:
                        is_subgroup = False
                        break
                if not is_subgroup:
                    break
            if is_subgroup:
                count += 1
                if count > 1:
                    return False
        return count == 1
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            d = witness.get('d')
            n = witness.get('n')
        else:
            G, d, n = witness
    except Exception:
        return [False] * 4 + [False]
        
    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2: G is a cyclic group
    try:
        h2 = is_cyclic(G)
    except Exception:
        h2 = False
        
    # H3: d is a positive integer
    try:
        h3 = (int(d) == d) and (d > 0)
    except Exception:
        h3 = False
        
    # H4: d divides n
    try:
        h4 = (int(n) == n) and (int(d) == d) and (d != 0) and (n % d == 0)
    except Exception:
        h4 = False
        
    # neg_Q: G does NOT contain exactly one subgroup of order d
    try:
        if not ((int(d) == d) and (d > 0)):
            neg_q = True
        else:
            has_exactly_one = exactly_one_subgroup_of_order(G, int(d))
            neg_q = not has_exactly_one
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G is a cyclic group",
    "H_3: d is a positive integer",
    "H_4: d divides n",
    "¬Q: G does not contain exactly one subgroup of order d"
]

N_HYP = 4
NEG_Q_INDEX = 4