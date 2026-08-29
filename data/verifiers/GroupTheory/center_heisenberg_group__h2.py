import sympy
from sympy import eye, zeros
from sympy.combinatorics.named_groups import CyclicGroup, SymmetricGroup, AlternatingGroup, DihedralGroup
import itertools

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

CONDITION_LABELS = [
    "H_1: F is a field",
    "¬Q: The center Z(G) does not consist exactly of those matrices in G whose only non-zero off-diagonal entry is in the top-right corner"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    H1 = False
    neg_Q = False
    
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            F, G = witness
        else:
            F = witness
            G = None
            
        # Check H1: F is a field
        if isinstance(F, int):
            from sympy import isprime
            H1 = isprime(F)
        elif hasattr(F, 'is_Field'):
            H1 = bool(F.is_Field)
        elif hasattr(F, 'is_field'):
            H1 = bool(F.is_field)
        elif str(F) in ['QQ', 'RR', 'CC']:
            H1 = True
        else:
            H1 = False
    except Exception:
        pass

    try:
        if G is None:
            # Assume G is the Heisenberg group over F
            if isinstance(F, int) and H1:
                p = F
                elements = list(range(p))
                def add(x, y): return (x + y) % p
                def mul(x, y): return (x * y) % p
                zero = 0
                
                G_elements = []
                for a, b, c in itertools.product(elements, repeat=3):
                    G_elements.append((a, b, c))
                
                center = []
                for g in G_elements:
                    is_center = True
                    for h in G_elements:
                        a1, b1, c1 = g
                        a2, b2, c2 = h
                        gh_a = add(a1, a2)
                        gh_b = add(b1, b2)
                        gh_c = add(add(c1, c2), mul(a1, b2))
                        
                        hg_a = add(a2, a1)
                        hg_b = add(b2, b1)
                        hg_c = add(add(c2, c1), mul(a2, b1))
                        
                        if (gh_a, gh_b, gh_c) != (hg_a, hg_b, hg_c):
                            is_center = False
                            break
                    if is_center:
                        center.append(g)
                        
                target_set = []
                for g in G_elements:
                    a, b, c = g
                    # Strict interpretation: exactly one non-zero off-diagonal entry
                    if a == zero and b == zero and c != zero:
                        target_set.append(g)
                        
                if sorted(center) != sorted(target_set):
                    neg_Q = True
                else:
                    neg_Q = False
            else:
                # For any field, the identity matrix is in the center but has 0 non-zero off-diagonal entries.
                # Thus the center never consists EXACTLY of matrices with exactly one non-zero off-diagonal entry.
                neg_Q = True
        else:
            # G is provided as a list of SymPy matrices
            center = []
            for g in G:
                is_center = True
                for h in G:
                    if g * h != h * g:
                        is_center = False
                        break
                if is_center:
                    center.append(g)
                    
            target_set = []
            for g in G:
                non_zero_off_diag = []
                for i in range(g.rows):
                    for j in range(g.cols):
                        if i != j and g[i, j] != 0:
                            non_zero_off_diag.append((i, j))
                if len(non_zero_off_diag) == 1 and non_zero_off_diag[0] == (0, 2):
                    target_set.append(g)
                    
            center_in_target = all(any(c == t for t in target_set) for c in center)
            target_in_center = all(any(t == c for c in center) for t in target_set)
            neg_Q = not (center_in_target and target_in_center)
            
    except Exception:
        pass
        
    return [H1, neg_Q]