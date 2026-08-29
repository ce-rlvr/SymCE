import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.perm_groups import PermutationGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if not isinstance(witness, PermutationGroup):
            return [False, False]
    except Exception:
        return [False, False]
        
    # H_1: G contains a cyclic normal subgroup N such that G/N is cyclic
    try:
        order_attr = witness.order
        target_order = order_attr() if callable(order_attr) else order_attr
        
        # Limit order to prevent timeouts on unreasonably large witnesses
        if target_order > 2048:
            h1 = False
        else:
            elements = list(witness.elements)
            generators_G = list(witness.generators)
            
            # Find the identity element
            identity = next(g for g in elements if (g.order() if callable(g.order) else g.order) == 1)
            
            h1 = False
            for g in elements:
                # Generate N = <g>
                N_elements = set()
                curr = identity
                while True:
                    N_elements.add(curr)
                    curr = curr * g
                    if curr == identity:
                        break
                        
                # Check normality: x * g * x^-1 must be in N for all generators x of G
                is_normal = True
                for x in generators_G:
                    conj = x * g * (~x)
                    if conj not in N_elements:
                        is_normal = False
                        break
                
                if not is_normal:
                    continue
                    
                # Check if G/N is cyclic
                # G/N is cyclic iff there exists h in G such that <h, g> = G
                quotient_order = target_order // len(N_elements)
                is_quotient_cyclic = False
                for h in elements:
                    h_order_attr = h.order
                    h_order = h_order_attr() if callable(h_order_attr) else h_order_attr
                    
                    # The order of h must be a multiple of the quotient order
                    if h_order % quotient_order != 0:
                        continue
                        
                    H = PermutationGroup([h, g])
                    H_order_attr = H.order
                    H_order = H_order_attr() if callable(H_order_attr) else H_order_attr
                    
                    if H_order == target_order:
                        is_quotient_cyclic = True
                        break
                        
                if is_quotient_cyclic:
                    h1 = True
                    break
    except Exception:
        h1 = False
        
    # ¬Q: G is not solvable
    try:
        solvable_attr = witness.is_solvable
        if callable(solvable_attr):
            neg_q = not solvable_attr()
        else:
            neg_q = not bool(solvable_attr)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G contains a cyclic normal subgroup N such that G/N is cyclic",
    "¬Q: G is not solvable"
]

N_HYP = 1
NEG_Q_INDEX = 1