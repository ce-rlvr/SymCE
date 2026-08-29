import math
from itertools import combinations
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            p = witness.get('p')
            n = witness.get('n')
            m = witness.get('m')
            n_p = witness.get('n_p')
        else:
            G, p, n, m, n_p = witness
    except Exception:
        return [False] * 4 + [False]

    # H1: G is a finite group
    try:
        h1 = hasattr(G, 'order') and (hasattr(G, 'elements') or hasattr(G, 'generate'))
        if h1:
            order_G = G.order() if callable(G.order) else G.order
            h1 = isinstance(order_G, int) and order_G > 0
    except Exception:
        h1 = False

    # H2: The order of G is p^n * m
    try:
        h2 = (order_G == (p**n) * m)
    except Exception:
        h2 = False

    # H3: p does not divide m
    try:
        h3 = (m % p != 0)
    except Exception:
        h3 = False

    # H4: n_p is the number of distinct Sylow p-subgroups of G
    # (Interpreted as subgroups of order p^n since p might not be prime)
    try:
        target_order_float = p**n
        if target_order_float != int(target_order_float):
            h4 = False
        else:
            target_order = int(target_order_float)
            
            if hasattr(G, 'subgroups') and callable(G.subgroups):
                count = sum(1 for H in G.subgroups() if H.order() == target_order)
            else:
                if hasattr(G, 'elements'):
                    elements = list(G.elements)
                elif hasattr(G, 'generate') and callable(G.generate):
                    elements = list(G.generate())
                else:
                    elements = []
                    
                n_elements = len(elements)
                if target_order > n_elements:
                    count = 0
                elif target_order == n_elements:
                    count = 1
                elif target_order == 1:
                    count = 1
                else:
                    if hasattr(G, 'identity'):
                        id_elem = G.identity
                    else:
                        id_elem = None
                        for e in elements:
                            if e * e == e:
                                id_elem = e
                                break
                    
                    if id_elem in elements:
                        elements.remove(id_elem)
                    
                    def get_order(e):
                        if hasattr(e, 'order'):
                            if callable(e.order):
                                return e.order()
                            else:
                                return e.order
                        curr = e
                        ord = 1
                        while curr != id_elem:
                            curr = curr * e
                            ord += 1
                            if ord > n_elements:
                                break
                        return ord

                    valid_elements = [e for e in elements if target_order % get_order(e) == 0]
                    
                    if math.comb(len(valid_elements), target_order - 1) > 200000:
                        count = -2 # Force failure to avoid timeout
                    else:
                        count = 0
                        for subset in combinations(valid_elements, target_order - 1):
                            subgroup = set(subset)
                            subgroup.add(id_elem)
                            is_subgroup = True
                            for a in subset:
                                for b in subset:
                                    if a * b not in subgroup:
                                        is_subgroup = False
                                        break
                                if not is_subgroup:
                                    break
                            if is_subgroup:
                                count += 1
                                
            h4 = (count >= 0) and (n_p == count)
    except Exception:
        h4 = False

    # Conclusion: n_p divides m and n_p is congruent to 1 modulo p
    try:
        if n_p == 0:
            q = False
        else:
            q = (m % n_p == 0) and (n_p % p == 1)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: The order of G is p^n * m",
    "H_3: p does not divide m",
    "H_4: n_p is the number of distinct Sylow p-subgroups of G",
    "¬Q: n_p does not divide m or n_p is not congruent to 1 modulo p"
]

N_HYP = 4
NEG_Q_INDEX = 4