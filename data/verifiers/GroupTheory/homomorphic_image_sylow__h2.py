import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.ntheory as nt

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

def get_elements(G):
    if hasattr(G, 'generate') and callable(G.generate):
        raw = []
        for i, x in enumerate(G.generate()):
            if i >= 2000:
                raise ValueError("Group too large")
            raw.append(x)
    elif hasattr(G, 'elements'):
        raw = list(G.elements)
        if len(raw) > 2000:
            raise ValueError("Group too large")
    else:
        raw = list(G)
        if len(raw) > 2000:
            raise ValueError("Group too large")
            
    try:
        res = list(set(raw))
    except TypeError:
        if len(raw) > 200:
            raise ValueError("Group too large for unhashable elements")
        res = []
        for x in raw:
            if x not in res:
                res.append(x)
    return res

def evaluate_f(f, g):
    if callable(f):
        return f(g)
    elif isinstance(f, dict):
        return f[g]
    else:
        for k, v in f:
            if k == g:
                return v
    raise ValueError("Cannot evaluate f")

def check_finite_group(G):
    try:
        if hasattr(G, 'is_group') and not G.is_group:
            return False
        elems = get_elements(G)
        if len(elems) == 0:
            return False
        
        try:
            elems_set = set(elems)
            for x in elems:
                for y in elems:
                    if (x * y) not in elems_set:
                        return False
        except TypeError:
            for x in elems:
                for y in elems:
                    if (x * y) not in elems:
                        return False
                        
        has_identity = False
        for e in elems:
            is_id = True
            for x in elems:
                if (e * x) != x or (x * e) != x:
                    is_id = False
                    break
            if is_id:
                has_identity = True
                identity = e
                break
                
        if not has_identity:
            return False
            
        for x in elems:
            has_inv = False
            for y in elems:
                if (x * y) == identity and (y * x) == identity:
                    has_inv = True
                    break
            if not has_inv:
                return False
                
        return True
    except Exception:
        return False

def check_surjective_homomorphism(G, H, f):
    G_elems = get_elements(G)
    H_elems = get_elements(H)
    
    try:
        f_map = {}
        for g in G_elems:
            fg = evaluate_f(f, g)
            if fg not in H_elems:
                return False
            f_map[g] = fg
            
        unique_f_vals = set(f_map.values())
        if len(unique_f_vals) != len(H_elems):
            return False
            
        for x in G_elems:
            for y in G_elems:
                xy = x * y
                if f_map[xy] != f_map[x] * f_map[y]:
                    return False
        return True
    except TypeError:
        if len(G_elems) > 100:
            raise ValueError("Group too large for unhashable elements")
        f_vals = []
        for g in G_elems:
            fg = evaluate_f(f, g)
            if fg not in H_elems:
                return False
            f_vals.append(fg)
            
        unique_f_vals = []
        for fg in f_vals:
            if fg not in unique_f_vals:
                unique_f_vals.append(fg)
                
        if len(unique_f_vals) != len(H_elems):
            return False
            
        for x in G_elems:
            for y in G_elems:
                xy = x * y
                f_xy = evaluate_f(f, xy)
                f_x = evaluate_f(f, x)
                f_y = evaluate_f(f, y)
                if f_xy != f_x * f_y:
                    return False
        return True

def check_sylow_p_subgroup(P, G, p):
    if not nt.isprime(p):
        return False
        
    G_elems = get_elements(G)
    P_elems = get_elements(P)
    
    n = len(G_elems)
    k = 0
    while n % p == 0:
        k += 1
        n //= p
        
    expected_order = p ** k
    
    if len(P_elems) != expected_order:
        return False
        
    try:
        G_set = set(G_elems)
        P_set = set(P_elems)
        if not P_set.issubset(G_set):
            return False
        for x in P_elems:
            for y in P_elems:
                if (x * y) not in P_set:
                    return False
    except TypeError:
        for x in P_elems:
            if x not in G_elems:
                return False
        for x in P_elems:
            for y in P_elems:
                if (x * y) not in P_elems:
                    return False
                    
    return True

def check_conclusion(P, H, f, p):
    P_elems = get_elements(P)
    H_elems = get_elements(H)
    
    try:
        f_P = set()
        for g in P_elems:
            f_P.add(evaluate_f(f, g))
            
        n = len(H_elems)
        k = 0
        while n % p == 0:
            k += 1
            n //= p
            
        expected_order = p ** k
        
        if len(f_P) != expected_order:
            return False
            
        for x in f_P:
            for y in f_P:
                if (x * y) not in f_P:
                    return False
    except TypeError:
        f_P = []
        for g in P_elems:
            fg = evaluate_f(f, g)
            if fg not in f_P:
                f_P.append(fg)
                
        n = len(H_elems)
        k = 0
        while n % p == 0:
            k += 1
            n //= p
            
        expected_order = p ** k
        
        if len(f_P) != expected_order:
            return False
            
        for x in f_P:
            for y in f_P:
                if (x * y) not in f_P:
                    return False
                    
    return True

def conditions(witness):
    try:
        G = witness['G']
        H = witness['H']
        f = witness['f']
        P = witness['P']
        p = witness['p']
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = check_finite_group(G) and check_finite_group(H)
    except Exception:
        h1 = False
        
    try:
        h2 = check_surjective_homomorphism(G, H, f)
    except Exception:
        h2 = False
        
    try:
        h3 = check_sylow_p_subgroup(P, G, p)
    except Exception:
        h3 = False
        
    try:
        q = check_conclusion(P, H, f, p)
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are finite groups",
    "H_2: f is a surjective group homomorphism",
    "H_3: P is a Sylow p-subgroup of G",
    "¬Q: f(P) is not a Sylow p-subgroup of H"
]

N_HYP = 3
NEG_Q_INDEX = 3