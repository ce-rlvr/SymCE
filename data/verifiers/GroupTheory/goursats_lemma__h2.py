import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings that the witness expression may reference.
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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: S is a subgroup of G × H",
    "¬Q: The conclusion of Goursat's Lemma fails (e.g., H is not a group)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def get_unique(items):
    res = []
    for item in items:
        if not any(item == r for r in res):
            res.append(item)
    return res

def in_S(g, h, S):
    for sg, sh in S:
        if sg == g and sh == h:
            return True
    return False

def extract_magma(obj):
    if hasattr(obj, 'generate') and callable(obj.generate):
        elements = list(obj.generate())
        op = lambda a, b: a * b
        return elements, op
    elif hasattr(obj, 'elements'):
        elements = list(obj.elements)
        op = lambda a, b: a * b
        return elements, op
    elif isinstance(obj, tuple) and len(obj) == 2:
        return list(obj[0]), obj[1]
    else:
        raise ValueError("Invalid magma format")

def is_group(elements, op):
    if not elements: 
        return False
    elements = list(elements)
    
    # Check closure
    for a in elements:
        for b in elements:
            try:
                c = op(a, b)
                if not any(c == e for e in elements): 
                    return False
            except Exception:
                return False
                
    # Check associativity
    for a in elements:
        for b in elements:
            for c in elements:
                try:
                    if op(op(a, b), c) != op(a, op(b, c)): 
                        return False
                except Exception:
                    return False
                
    # Check identity
    identity = None
    for e in elements:
        try:
            if all(op(e, a) == a and op(a, e) == a for a in elements):
                identity = e
                break
        except Exception:
            return False
            
    if identity is None: 
        return False
    
    # Check inverses
    for a in elements:
        has_inv = False
        for b in elements:
            try:
                if op(a, b) == identity and op(b, a) == identity:
                    has_inv = True
                    break
            except Exception:
                pass
        if not has_inv: 
            return False
        
    return True

def is_subgroup(sub_elems, super_elems, op):
    for x in sub_elems:
        if not any(x == se for se in super_elems): 
            return False
    return is_group(sub_elems, op)

def conditions(witness):
    try:
        G, H, S = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G is a group
    try:
        G_elems, G_op = extract_magma(G)
        h1 = is_group(G_elems, G_op)
    except Exception:
        h1 = False
        
    # H_2: S is a subgroup of G x H
    try:
        G_elems, G_op = extract_magma(G)
        H_elems, H_op = extract_magma(H)
        
        subset = True
        for g, h in S:
            if not any(g == ge for ge in G_elems) or not any(h == he for he in H_elems):
                subset = False
                break
                
        if subset:
            def S_op(x, y):
                return (G_op(x[0], y[0]), H_op(x[1], y[1]))
            h2 = is_group(S, S_op)
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # ¬Q: The conclusion fails
    try:
        def check_conc():
            # The conclusion requires B <= B' <= H. If H is not a group, this is false.
            if not is_group(H_elems, H_op): 
                return False
            if not is_group(G_elems, G_op): 
                return False
            
            A_prime = get_unique([g for g, h in S])
            B_prime = get_unique([h for g, h in S])
            
            if not is_subgroup(A_prime, G_elems, G_op): return False
            if not is_subgroup(B_prime, H_elems, H_op): return False
            
            e_A = None
            for e in A_prime:
                if all(G_op(e, a) == a and G_op(a, e) == a for a in A_prime):
                    e_A = e
                    break
            e_B = None
            for e in B_prime:
                if all(H_op(e, b) == b and H_op(b, e) == b for b in B_prime):
                    e_B = e
                    break
                    
            A = get_unique([g for g in A_prime if in_S(g, e_B, S)])
            B = get_unique([h for h in B_prime if in_S(e_A, h, S)])
            
            if not is_subgroup(A, A_prime, G_op): return False
            if not is_subgroup(B, B_prime, H_op): return False
            
            def is_normal(sub, sup, op):
                for x in sup:
                    for s in sub:
                        left = op(x, s)
                        if not any(op(s_prime, x) == left for s_prime in sub):
                            return False
                return True
                
            if not is_normal(A, A_prime, G_op): return False
            if not is_normal(B, B_prime, H_op): return False
            
            # Check if S is exactly the set of pairs satisfying the isomorphism
            for g, h in S:
                for a in A:
                    for b in B:
                        if not in_S(G_op(g, a), H_op(h, b), S):
                            return False
                            
            if len(S) != len(A_prime) * len(B): return False
            if len(S) != len(B_prime) * len(A): return False
            
            return True
            
        neg_q = not check_conc()
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]