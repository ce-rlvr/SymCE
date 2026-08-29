import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.ntheory import isprime
from itertools import combinations

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

def conditions(witness):
    try:
        G, n, d = witness
    except Exception:
        return [False] * 5

    def get_order(obj):
        if callable(obj.order):
            return obj.order()
        return obj.order

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: the order of G is n
    try:
        h2 = get_order(G) == n
    except Exception:
        h2 = False

    # H_3: d is a positive integer
    try:
        h3 = type(d) is int and d > 0
    except Exception:
        h3 = False

    # H_4: d divides n
    try:
        h4 = (n % d == 0)
    except Exception:
        h4 = False

    # ¬Q: G does not contain exactly one subgroup of order d
    try:
        if not (h1 and h2 and h3 and h4):
            neg_q = False
        else:
            elements = list(G.elements)
            
            if isprime(d):
                # For prime d, subgroups of order d intersect trivially.
                count_elements = sum(1 for e in elements if get_order(e) == d)
                count = count_elements // (d - 1)
            else:
                # Find the identity element
                id_elem = None
                for e in elements:
                    if e * e == e:
                        id_elem = e
                        break
                
                # By Lagrange's theorem, elements in a subgroup of order d must have orders dividing d
                valid_elements = [e for e in elements if e != id_elem and d % get_order(e) == 0]
                
                if len(valid_elements) < d - 1:
                    count = 0
                else:
                    count = 0
                    # Check all subsets of size d-1
                    for subset in combinations(valid_elements, d - 1):
                        subset_set = set(subset)
                        subset_set.add(id_elem)
                        
                        is_subgroup = True
                        # For finite subsets, closure under multiplication implies it's a subgroup
                        for a in subset:
                            for b in subset:
                                if a * b not in subset_set:
                                    is_subgroup = False
                                    break
                            if not is_subgroup:
                                break
                        
                        if is_subgroup:
                            count += 1
                            
            neg_q = (count != 1)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: the order of G is n",
    "H_3: d is a positive integer",
    "H_4: d divides n",
    "¬Q: G does not contain exactly one subgroup of order d"
]

N_HYP = 4
NEG_Q_INDEX = 4