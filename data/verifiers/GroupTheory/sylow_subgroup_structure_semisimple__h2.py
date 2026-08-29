import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import sympy.ntheory

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

def conditions(witness):
    try:
        G, S_list, P, p = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G is a semisimple finite group such that G = S_1 x ... x S_k, where each S_i is a non-abelian simple group
    try:
        h1 = False
        if isinstance(G, PermutationGroup) and isinstance(S_list, list) and len(S_list) > 0:
            h1_ok = True
            prod_order = 1
            for S in S_list:
                if not isinstance(S, PermutationGroup):
                    h1_ok = False
                    break
                
                # Check if S is a subgroup of G
                is_sub = True
                for gen in S.generators:
                    if not G.contains(gen):
                        is_sub = False
                        break
                if not is_sub:
                    h1_ok = False
                    break
                
                # Check non-abelian
                if S.is_abelian:
                    h1_ok = False
                    break
                
                # Check simple (exactly 2 normal subgroups: trivial and itself)
                ns = S.normal_subgroups()
                if len(ns) != 2:
                    h1_ok = False
                    break
                
                # Check if S is normal in G
                is_normal = True
                for g in G.generators:
                    for s in S.generators:
                        if not S.contains(g**-1 * s * g):
                            is_normal = False
                            break
                    if not is_normal:
                        break
                if not is_normal:
                    h1_ok = False
                    break
                
                prod_order *= S.order()
            
            # If the product of orders of normal subgroups equals the order of G,
            # and they generate G (implied by order), G is their internal direct product.
            if h1_ok and prod_order == G.order():
                h1 = True
    except Exception:
        h1 = False

    # H_2: P is a Sylow p-subgroup of G
    try:
        h2 = False
        if isinstance(P, PermutationGroup) and sympy.ntheory.isprime(p):
            is_sub = True
            for gen in P.generators:
                if not G.contains(gen):
                    is_sub = False
                    break
            
            if is_sub:
                order_P = P.order()
                if order_P == 1:
                    is_p_group = True
                else:
                    factors = sympy.ntheory.factorint(order_P)
                    is_p_group = (list(factors.keys()) == [p])
                
                if is_p_group:
                    order_G = G.order()
                    max_p_power = 1
                    temp = order_G
                    while temp % p == 0:
                        max_p_power *= p
                        temp //= p
                    
                    if order_P == max_p_power:
                        h2 = True
    except Exception:
        h2 = False

    # ¬Q: P CANNOT be uniquely expressed as P_1 x P_2 x ... x P_k, where each P_i is a Sylow p-subgroup of S_i
    try:
        neg_q = False
        if h1 and h2:
            P_elements = list(P.generate())
            can_be_expressed = True
            prod_P_i = 1
            
            for S in S_list:
                # P_i must be P \cap S_i for the expression to be valid and unique
                P_i_elems = [x for x in P_elements if S.contains(x)]
                order_P_i = len(P_i_elems)
                
                # Check if P_i is a Sylow p-subgroup of S_i
                max_p_power_S = 1
                temp = S.order()
                while temp % p == 0:
                    max_p_power_S *= p
                    temp //= p
                
                if order_P_i != max_p_power_S:
                    can_be_expressed = False
                    break
                
                prod_P_i *= order_P_i
            
            # The internal direct product of P_i must equal P
            if can_be_expressed and prod_P_i != P.order():
                can_be_expressed = False
            
            neg_q = not can_be_expressed
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a semisimple finite group such that G = S_1 x ... x S_k, where each S_i is a non-abelian simple group",
    "H_2: P is a Sylow p-subgroup of G",
    "¬Q: P CANNOT be uniquely expressed as P_1 x ... x P_k, where each P_i is a Sylow p-subgroup of S_i"
]

N_HYP = 2
NEG_Q_INDEX = 2