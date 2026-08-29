import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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

def conditions(witness):
    try:
        G, H, K = witness
    except Exception:
        return [False, False, False]
    
    def get_elems(obj):
        if hasattr(obj, 'elements'):
            val = obj.elements
            if callable(val):
                elems = list(val())
            else:
                elems = list(val)
        elif hasattr(obj, 'generate') and callable(obj.generate):
            elems = list(obj.generate())
        else:
            elems = list(obj)
            
        res = []
        for e in elems:
            if e not in res:
                res.append(e)
        return res

    def is_subset(sub, super_set):
        for item in sub:
            if item not in super_set:
                return False
        return True

    def is_group_set(S):
        if not S: 
            return False
        # Check closure
        for a in S:
            for b in S:
                try:
                    if (a * b) not in S:
                        return False
                except Exception:
                    return False
        # Find identity
        identities = []
        for e in S:
            try:
                if all((e * a) == a and (a * e) == a for a in S):
                    identities.append(e)
            except Exception:
                pass
        if len(identities) != 1:
            return False
        e = identities[0]
        # Check inverses
        for a in S:
            has_inv = False
            for b in S:
                try:
                    if (a * b) == e and (b * a) == e:
                        has_inv = True
                        break
                except Exception:
                    pass
            if not has_inv:
                return False
        return True

    def check_subgroup(sub, group):
        try:
            if hasattr(sub, 'is_subgroup') and hasattr(group, 'is_group') and group.is_group:
                return sub.is_subgroup(group)
        except Exception:
            pass
        
        try:
            elems_sub = get_elems(sub)
            elems_group = get_elems(group)
            if not is_subset(elems_sub, elems_group):
                return False
            return is_group_set(elems_sub)
        except Exception:
            return False

    try:
        h1 = check_subgroup(H, G)
    except Exception:
        h1 = False

    try:
        h2 = check_subgroup(K, G)
    except Exception:
        h2 = False

    try:
        elems_H = get_elems(H)
        elems_K = get_elems(K)
        elems_G = get_elems(G)
        
        HK_list = []
        for h in elems_H:
            for k in elems_K:
                prod = h * k
                if prod not in HK_list:
                    HK_list.append(prod)
                    
        KH_list = []
        for k in elems_K:
            for h in elems_H:
                prod = k * h
                if prod not in KH_list:
                    KH_list.append(prod)
                    
        hk_eq_kh = is_subset(HK_list, KH_list) and is_subset(KH_list, HK_list)
        
        is_sub = is_subset(HK_list, elems_G) and is_group_set(HK_list)
                    
        neg_q = (is_sub != hk_eq_kh)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "H_2: K is a subgroup of G",
    "¬Q: HK is a subgroup of G is not equivalent to HK = KH"
]

N_HYP = 2
NEG_Q_INDEX = 2