import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
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

def conditions(witness):
    # Parse witness
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            X, phi = witness
            X = tuple(X)
        elif isinstance(witness, dict):
            phi = witness
            elements = set()
            for k in phi.keys():
                elements.update(k)
            try:
                X = tuple(sorted(elements))
            except Exception:
                X = tuple(elements)
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: X is a non-empty set
    try:
        h1 = len(X) > 0 and len(set(X)) == len(X)
    except Exception:
        h1 = False

    # H2: Domain of phi is P(X)
    try:
        subsets = set()
        for r in range(len(X) + 1):
            for combo in itertools.combinations(X, r):
                subsets.add(frozenset(combo))
        
        if isinstance(phi, dict):
            h2 = set(phi.keys()) == subsets
        elif callable(phi):
            h2 = True
            for s in subsets:
                try:
                    _ = phi(s)
                except Exception:
                    h2 = False
                    break
        else:
            h2 = False
    except Exception:
        h2 = False

    # H3: Codomain of phi is F(X, Z_2)
    try:
        h3 = True
        for s in subsets:
            val = phi[s] if isinstance(phi, dict) else phi(s)
            if isinstance(val, tuple):
                if len(val) != len(X):
                    h3 = False
                    break
                if any(v not in (0, 1) for v in val):
                    h3 = False
                    break
            elif isinstance(val, dict):
                if set(val.keys()) != set(X):
                    h3 = False
                    break
                if any(v not in (0, 1) for v in val.values()):
                    h3 = False
                    break
            elif callable(val):
                for x in X:
                    try:
                        v = val(x)
                        if v not in (0, 1):
                            h3 = False
                            break
                    except Exception:
                        h3 = False
                        break
                if not h3:
                    break
            else:
                try:
                    val_tuple = tuple(val)
                    if len(val_tuple) != len(X):
                        h3 = False
                        break
                    if any(v not in (0, 1) for v in val_tuple):
                        h3 = False
                        break
                except Exception:
                    h3 = False
                    break
    except Exception:
        h3 = False

    # neg_Q: phi is NOT a ring isomorphism
    try:
        def normalize_val(v):
            if isinstance(v, dict):
                return tuple(v[x] for x in X)
            elif callable(v):
                return tuple(v(x) for x in X)
            elif isinstance(v, tuple):
                return v
            else:
                return tuple(v)

        is_iso = True
        
        # Check bijection
        vals = []
        for s in subsets:
            val = phi[s] if isinstance(phi, dict) else phi(s)
            vals.append(normalize_val(val))
        if len(set(vals)) != len(subsets):
            is_iso = False
            
        # Check addition and multiplication
        if is_iso:
            for A in subsets:
                for B in subsets:
                    valA = normalize_val(phi[A] if isinstance(phi, dict) else phi(A))
                    valB = normalize_val(phi[B] if isinstance(phi, dict) else phi(B))
                    
                    # Addition: symmetric difference
                    A_sym_B = A.symmetric_difference(B)
                    val_A_sym_B = normalize_val(phi[A_sym_B] if isinstance(phi, dict) else phi(A_sym_B))
                    expected_add = tuple((a + b) % 2 for a, b in zip(valA, valB))
                    if val_A_sym_B != expected_add:
                        is_iso = False
                        break
                        
                    # Multiplication: intersection
                    A_int_B = A.intersection(B)
                    val_A_int_B = normalize_val(phi[A_int_B] if isinstance(phi, dict) else phi(A_int_B))
                    expected_mul = tuple((a * b) % 2 for a, b in zip(valA, valB))
                    if val_A_int_B != expected_mul:
                        is_iso = False
                        break
                if not is_iso:
                    break
                    
        neg_q = not is_iso
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: X is a non-empty set",
    "H_2: P(X) is the Boolean ring of subsets of X (domain of phi is P(X))",
    "H_3: F(X, Z_2) is the Boolean ring of functions from X to Z_2 (codomain of phi is F(X, Z_2))",
    "¬Q: phi is not a ring isomorphism"
]

N_HYP = 3
NEG_Q_INDEX = 3