import math
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, CyclicGroup, AlternatingGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
from sympy import Integer

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

def conditions(witness) -> list[bool]:
    try:
        G, n, k, f = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: G is a finite cyclic group
    try:
        if isinstance(G, PermutationGroup):
            cyclic_attr = getattr(G, "is_cyclic", False)
            is_cyclic = cyclic_attr() if callable(cyclic_attr) else cyclic_attr
            h1 = bool(is_cyclic)
        else:
            h1 = False
    except Exception:
        h1 = False
        
    # H2: The order of G is n
    try:
        if isinstance(G, PermutationGroup):
            order_attr = getattr(G, "order")
            order_val = order_attr() if callable(order_attr) else order_attr
            h2 = (order_val == n)
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # H3: k is an integer
    try:
        h3 = isinstance(k, (int, Integer))
    except Exception:
        h3 = False
        
    # neg_Q: f is a group automorphism of G if and only if gcd(k, n) = 1
    try:
        elements = list(G.generate())
        
        def evaluate_f(func, x):
            if isinstance(func, dict):
                return func[x]
            elif isinstance(func, (list, tuple)):
                for k_item, v_item in func:
                    if k_item == x:
                        return v_item
                raise ValueError("Not found")
            return func(x)
            
        is_aut = True
        mapped = []
        for x in elements:
            try:
                fx = evaluate_f(f, x)
            except Exception:
                is_aut = False
                break
            if fx not in elements:
                is_aut = False
                break
            mapped.append(fx)
            
        if is_aut:
            if len(set(mapped)) != len(elements):
                is_aut = False
            else:
                for x in elements:
                    for y in elements:
                        try:
                            xy = x * y
                            f_xy = evaluate_f(f, xy)
                            fx = evaluate_f(f, x)
                            fy = evaluate_f(f, y)
                            if f_xy != fx * fy:
                                is_aut = False
                                break
                        except Exception:
                            is_aut = False
                            break
                    if not is_aut:
                        break
                        
        gcd_cond = (math.gcd(int(k), int(n)) == 1)
        
        q = (is_aut == gcd_cond)
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite cyclic group",
    "H_2: The order of G is n",
    "H_3: k is an integer",
    "¬Q: (f is a group automorphism of G) is not equivalent to (gcd(k, n) == 1)"
]

N_HYP = 3
NEG_Q_INDEX = 3