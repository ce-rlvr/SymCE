import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_frobenius_group(G):
    try:
        if not hasattr(G, 'elements'):
            return False
        
        elements = []
        for i, e in enumerate(G.elements):
            if i > 1000:  # Prevent hanging on infinite or overly large groups
                return False
            elements.append(e)
            
        n = len(elements)
        if n <= 1:
            return False
        
        id_elem = None
        for e in elements:
            if e * e == e:
                id_elem = e
                break
        if id_elem is None:
            return False
        
        classes = []
        seen = set()
        for g in elements:
            if g in seen:
                continue
            cls = set()
            for x in elements:
                conj = x * g * (x**-1)
                cls.add(conj)
                seen.add(conj)
            classes.append(list(cls))
            
        def normal_closure(subset):
            closure = set(subset)
            closure.add(id_elem)
            while True:
                new_elements = set()
                for a in closure:
                    for b in subset:
                        prod = a * b
                        if prod not in closure:
                            new_elements.add(prod)
                if not new_elements:
                    break
                closure.update(new_elements)
            return frozenset(closure)

        known_normals = [frozenset([id_elem])]
        for cls in classes:
            if id_elem in cls:
                continue
            new_normals = []
            for N in known_normals:
                gen = N.union(cls)
                K = normal_closure(gen)
                if K not in known_normals and K not in new_normals:
                    new_normals.append(K)
            known_normals.extend(new_normals)
            
        for K_set in known_normals:
            if len(K_set) == 1 or len(K_set) == n:
                continue
            is_kernel = True
            for k in K_set:
                if k == id_elem:
                    continue
                for g in elements:
                    if g * k == k * g:
                        if g not in K_set:
                            is_kernel = False
                            break
                if not is_kernel:
                    break
            if is_kernel:
                return True
                
        return False
    except Exception:
        return False

def are_conjugate_subgroups(G, H, K):
    try:
        if not hasattr(H, 'elements') or not hasattr(K, 'elements') or not hasattr(G, 'elements'):
            return False
            
        H_elems = set()
        for i, e in enumerate(H.elements):
            if i > 1000: return False
            H_elems.add(e)
            
        K_elems = set()
        for i, e in enumerate(K.elements):
            if i > 1000: return False
            K_elems.add(e)
            
        G_elems = set()
        for i, e in enumerate(G.elements):
            if i > 1000: return False
            G_elems.add(e)
            
        if not H_elems.issubset(G_elems):
            return False
        if not K_elems.issubset(G_elems):
            return False
            
        if len(H_elems) != len(K_elems):
            return False
            
        for g in G_elems:
            conj_H = set(g * h * (g**-1) for h in H_elems)
            if conj_H == K_elems:
                return True
                
        return False
    except Exception:
        return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
            K = witness.get('K')
        else:
            G, H, K = witness
    except Exception:
        return [False, False]
        
    try:
        h1 = is_frobenius_group(G)
    except Exception:
        h1 = False
        
    try:
        neg_q = not are_conjugate_subgroups(G, H, K)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite Frobenius group",
    "¬Q: H and K are not conjugate subgroups in G"
]

N_HYP = 1
NEG_Q_INDEX = 1