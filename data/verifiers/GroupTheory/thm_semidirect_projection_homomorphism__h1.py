import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import functools

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

def get_witness_elements(witness):
    if isinstance(witness, dict):
        N = witness['N']
        H = witness['H']
        N_op = witness['N_op']
        H_op = witness['H_op']
        G_op = witness['G_op']
    elif isinstance(witness, tuple) and len(witness) == 5:
        N, H, N_op, H_op, G_op = witness
    else:
        N = witness.N
        H = witness.H
        N_op = witness.N_op
        H_op = witness.H_op
        G_op = witness.G_op
        
    def make_callable(op):
        if isinstance(op, dict):
            return lambda a, b: op[(a, b)]
        return op
        
    return list(N), list(H), make_callable(N_op), make_callable(H_op), make_callable(G_op)

def is_group(elements, op):
    try:
        elements = list(elements)
        if not elements: return False
        
        # Closure
        for a in elements:
            for b in elements:
                if op(a, b) not in elements:
                    return False
                    
        # Identity
        id_elem = None
        for e in elements:
            is_id = True
            for a in elements:
                if op(e, a) != a or op(a, e) != a:
                    is_id = False
                    break
            if is_id:
                id_elem = e
                break
        if id_elem is None:
            return False
            
        # Inverse
        for a in elements:
            has_inv = False
            for b in elements:
                if op(a, b) == id_elem and op(b, a) == id_elem:
                    has_inv = True
                    break
            if not has_inv:
                return False

        # Associativity
        for a in elements:
            for b in elements:
                ab = op(a, b)
                for c in elements:
                    if op(ab, c) != op(a, op(b, c)):
                        return False
                        
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        N, H, N_op, H_op, G_op = get_witness_elements(witness)
    except Exception:
        return [False, False]
        
    # H_1: G is a group on N x H, N and H are groups, pi((n,h))=h
    try:
        h1_ok = False
        if is_group(N, N_op) and is_group(H, H_op):
            G_elements = [(n, h) for n in N for h in H]
            if is_group(G_elements, G_op):
                h1_ok = True
    except Exception:
        h1_ok = False
        
    # neg_Q: Conclusion fails
    try:
        neg_q = False
        if h1_ok:
            G_elements = [(n, h) for n in N for h in H]
            
            # Find identity of H
            id_H = None
            for e in H:
                if all(H_op(e, a) == a and H_op(a, e) == a for a in H):
                    id_H = e
                    break
                    
            # pi is defined as pi((n, h)) = h
            def pi(g):
                return g[1]
                
            is_hom = True
            for g1 in G_elements:
                for g2 in G_elements:
                    if pi(G_op(g1, g2)) != H_op(pi(g1), pi(g2)):
                        is_hom = False
                        break
                if not is_hom: break
                
            image = []
            for g in G_elements:
                p = pi(g)
                if p not in image:
                    image.append(p)
            
            is_surj = True
            for h in H:
                if h not in image:
                    is_surj = False
                    break
            
            kernel = [g for g in G_elements if pi(g) == id_H]
            expected_kernel = [(n, id_H) for n in N]
            
            is_ker_correct = True
            for k in kernel:
                if k not in expected_kernel:
                    is_ker_correct = False
                    break
            for k in expected_kernel:
                if k not in kernel:
                    is_ker_correct = False
                    break
            
            is_iso = False
            if is_ker_correct:
                natural_valid = True
                for n1 in N:
                    for n2 in N:
                        if G_op((n1, id_H), (n2, id_H)) != (N_op(n1, n2), id_H):
                            natural_valid = False
                            break
                    if not natural_valid: break
                if natural_valid:
                    is_iso = True
                else:
                    if len(N) <= 7:
                        for p in itertools.permutations(expected_kernel):
                            mapping_pairs = list(zip(N, p))
                            valid = True
                            for n1 in N:
                                for n2 in N:
                                    mapped_n1 = next(v for k, v in mapping_pairs if k == n1)
                                    mapped_n2 = next(v for k, v in mapping_pairs if k == n2)
                                    mapped_n1n2 = next(v for k, v in mapping_pairs if k == N_op(n1, n2))
                                    if mapped_n1n2 != G_op(mapped_n1, mapped_n2):
                                        valid = False
                                        break
                                if not valid: break
                            if valid:
                                is_iso = True
                                break
                        
            conclusion_holds = is_hom and is_surj and is_ker_correct and is_iso
            neg_q = not conclusion_holds
    except Exception:
        neg_q = False
        
    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group on N x H, N and H are groups, and π((n,h))=h",
    "¬Q: π is not a surjective homomorphism, or its kernel is not N x {1_H}, or the kernel is not isomorphic to N"
]

N_HYP = 1
NEG_Q_INDEX = 1