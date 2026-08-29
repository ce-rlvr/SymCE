import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime
import math
import itertools
import functools

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

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    
    The theorem is true for finite groups, so the counterexample must be an infinite group.
    This verifier explicitly supports G = Z (the integers) as an infinite group.
    
    To use the infinite group Z, the witness must provide:
      witness.G = "Z"
      witness.H = m (an integer representing the finite group Z_m)
      witness.phi = callable (int -> int)
      witness.P = [0] (the unique Sylow p-subgroup of Z)
      witness.p = a prime integer
      
    The verifier also includes duck-typed checks for finite groups just in case.
    """
    try:
        p = witness.p
        G = witness.G
        H = witness.H
        phi = witness.phi
        P = witness.P
    except Exception:
        return [False, False, False]
        
    try:
        if not isprime(p):
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # Case 1: Infinite group Z
    if G == "Z":
        try:
            m = int(H)
            if m <= 0:
                return [False, False, False]
                
            # Check if P is a Sylow p-subgroup of Z
            # In Z, the only element of finite order is 0.
            # So the unique Sylow p-subgroup is {0}.
            is_sylow_G = (set(P) == {0})
            
            # Check if phi is a surjective homomorphism from Z to Z_m
            is_hom = True
            for x in range(-20, 20):
                for y in range(-20, 20):
                    if phi(x + y) % m != (phi(x) + phi(y)) % m:
                        is_hom = False
                        break
                        
            images = set(phi(x) % m for x in range(-m*2, m*2))
            is_surj = (images == set(range(m)))
            is_surj_hom = is_hom and is_surj
            
            # Check if phi(P) is a Sylow p-subgroup of Z_m
            phi_P = set(phi(x) % m for x in P)
            
            highest_power = 1
            temp = m
            while temp % p == 0:
                highest_power *= p
                temp //= p
                
            is_sylow_H = (len(phi_P) == highest_power)
            if is_sylow_H:
                is_subgroup = True
                for x in phi_P:
                    for y in phi_P:
                        if (x + y) % m not in phi_P:
                            is_subgroup = False
                is_sylow_H = is_sylow_H and is_subgroup
                
            neg_Q = not is_sylow_H
            
            return [bool(is_surj_hom), bool(is_sylow_G), bool(neg_Q)]
        except Exception:
            return [False, False, False]

    # Case 2: SymPy PermutationGroup
    if isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup):
        try:
            G_elements = list(G.elements)
            H_elements = list(H.elements)
            
            is_hom = True
            for x in G_elements:
                for y in G_elements:
                    if phi(x * y) != phi(x) * phi(y):
                        is_hom = False
                        break
                        
            images = set(phi(x) for x in G_elements)
            is_surj = (images == set(H_elements))
            is_surj_hom = is_hom and is_surj
            
            def is_p_group_perm(elements, p_val):
                for x in elements:
                    order = x.order()
                    if order == 1:
                        continue
                    temp = order
                    while temp % p_val == 0:
                        temp //= p_val
                    if temp != 1:
                        return False
                return True
                
            def is_subgroup_perm(elements):
                if not elements:
                    return False
                for x in elements:
                    if x**-1 not in elements:
                        return False
                    for y in elements:
                        if x * y not in elements:
                            return False
                return True

            P_set = set(P)
            if not is_subgroup_perm(P_set):
                is_sylow_G = False
            elif not is_p_group_perm(P_set, p):
                is_sylow_G = False
            else:
                order_G = G.order()
                highest_power = 1
                temp = order_G
                while temp % p == 0:
                    highest_power *= p
                    temp //= p
                is_sylow_G = (len(P_set) == highest_power)
                
            phi_P = set(phi(x) for x in P_set)
            if not is_subgroup_perm(phi_P):
                is_sylow_H = False
            elif not is_p_group_perm(phi_P, p):
                is_sylow_H = False
            else:
                order_H = H.order()
                highest_power_H = 1
                temp = order_H
                while temp % p == 0:
                    highest_power_H *= p
                    temp //= p
                is_sylow_H = (len(phi_P) == highest_power_H)
                
            neg_Q = not is_sylow_H
            
            return [bool(is_surj_hom), bool(is_sylow_G), bool(neg_Q)]
        except Exception:
            pass

    # Case 3: Finite group (duck-typed)
    try:
        G_elements = list(G.elements)
        H_elements = list(H.elements)
        
        is_hom = True
        for x in G_elements:
            for y in G_elements:
                if phi(G.op(x, y)) != H.op(phi(x), phi(y)):
                    is_hom = False
                    break
                    
        images = set(phi(x) for x in G_elements)
        is_surj = (images == set(H_elements))
        is_surj_hom = is_hom and is_surj
        
        def get_order(x, identity, op):
            if x == identity: return 1
            curr = x
            order = 1
            while curr != identity and order < 10000:
                curr = op(curr, x)
                order += 1
            return order

        def is_p_group(elements, p_val, identity, op):
            for x in elements:
                order = get_order(x, identity, op)
                if order == 1:
                    continue
                temp = order
                while temp % p_val == 0:
                    temp //= p_val
                if temp != 1:
                    return False
            return True
            
        def is_subgroup(elements, identity, op):
            if not elements:
                return False
            if identity not in elements:
                return False
            for x in elements:
                for y in elements:
                    if op(x, y) not in elements:
                        return False
            return True

        P_set = set(P)
        if not is_subgroup(P_set, G.identity, G.op):
            is_sylow_G = False
        elif not is_p_group(P_set, p, G.identity, G.op):
            is_sylow_G = False
        else:
            order_G = len(G_elements)
            highest_power = 1
            temp = order_G
            while temp % p == 0:
                highest_power *= p
                temp //= p
            is_sylow_G = (len(P_set) == highest_power)
            
        phi_P = set(phi(x) for x in P_set)
        if not is_subgroup(phi_P, H.identity, H.op):
            is_sylow_H = False
        elif not is_p_group(phi_P, p, H.identity, H.op):
            is_sylow_H = False
        else:
            order_H = len(H_elements)
            highest_power_H = 1
            temp = order_H
            while temp % p == 0:
                highest_power_H *= p
                temp //= p
            is_sylow_H = (len(phi_P) == highest_power_H)
            
        neg_Q = not is_sylow_H
        
        return [bool(is_surj_hom), bool(is_sylow_G), bool(neg_Q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: phi is a surjective group homomorphism from G to H",
    "H_2: P is a Sylow p-subgroup of G",
    "not Q: phi(P) is not a Sylow p-subgroup of H"
]

N_HYP = 2
NEG_Q_INDEX = 2