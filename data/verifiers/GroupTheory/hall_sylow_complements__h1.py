import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime

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
A5 = AlternatingGroup(5)
S5 = SymmetricGroup(5)

def has_subgroup_of_order(G, target_order):
    """
    Checks if the permutation group G has at least one subgroup of the exact target_order.
    Uses a bottom-up generation approach, pruning any subgroup that exceeds target_order.
    """
    if target_order == 1:
        return True
    if target_order == G.order():
        return True
        
    elements = list(G.generate_dimino())
    
    # Base case: find all cyclic subgroups
    cyclic_subgroups = set()
    for g in elements:
        cg = []
        cg_set = set()
        curr = g
        while curr not in cg_set:
            cg.append(curr)
            cg_set.add(curr)
            curr = curr * g
        cyclic_subgroups.add(frozenset(cg_set))
        
    if any(len(cg) == target_order for cg in cyclic_subgroups):
        return True
        
    subgroups = set(cyclic_subgroups)
    queue = list(cyclic_subgroups)
    
    # BFS to find all subgroups up to target_order
    while queue:
        H = queue.pop(0)
        for C in cyclic_subgroups:
            if not C.issubset(H):
                # Generate the join of H and C
                closure = list(H)
                closure_set = set(H)
                for c in C:
                    if c not in closure_set:
                        closure.append(c)
                        closure_set.add(c)
                
                i = 0
                too_big = False
                while i < len(closure):
                    x = closure[i]
                    i += 1
                    for j in range(i):
                        y = closure[j]
                        
                        xy = x * y
                        if xy not in closure_set:
                            closure.append(xy)
                            closure_set.add(xy)
                            
                        yx = y * x
                        if yx not in closure_set:
                            closure.append(yx)
                            closure_set.add(yx)
                            
                    xx = x * x
                    if xx not in closure_set:
                        closure.append(xx)
                        closure_set.add(xx)
                        
                    # Prune early if the generated subgroup exceeds the target order
                    if len(closure_set) > target_order:
                        too_big = True
                        break
                        
                if not too_big:
                    join_fs = frozenset(closure_set)
                    if join_fs not in subgroups:
                        if len(join_fs) == target_order:
                            return True
                        subgroups.add(join_fs)
                        queue.append(join_fs)
                        
    return False

def conditions(witness) -> list[bool]:
    try:
        G, p = witness
    except Exception:
        return [False, False, False]
        
    # H_1: p is a prime number
    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False
        
    # H_2: p divides the order of G
    try:
        order_G = G.order()
        if not isinstance(order_G, (int, sympy.Integer)):
            h2 = False
        else:
            h2 = bool(order_G % p == 0)
    except Exception:
        h2 = False
        
    # ¬Q: G does NOT contain a Sylow p-complement
    # A Sylow p-complement is a subgroup of index equal to the highest power of p dividing |G|.
    try:
        if p <= 1:
            neg_q = False
        else:
            order_G = G.order()
            if not isinstance(order_G, (int, sympy.Integer)):
                neg_q = False
            else:
                p_k = 1
                temp = order_G
                while temp % p == 0:
                    p_k *= p
                    temp //= p
                    
                target_order = order_G // p_k
                
                has_complement = has_subgroup_of_order(G, target_order)
                neg_q = not has_complement
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: p divides the order of G",
    "¬Q: G does not contain a Sylow p-complement"
]

N_HYP = 2
NEG_Q_INDEX = 2
