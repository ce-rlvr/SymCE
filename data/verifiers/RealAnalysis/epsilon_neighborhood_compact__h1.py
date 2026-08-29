import sympy
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: K is a compact subset of X",
    "H_2: U is an open subset of X",
    "H_3: K is a subset of U",
    "¬Q: For all epsilon > 0, the epsilon-neighborhood of K is not contained in U"
]

N_HYP = 3
NEG_Q_INDEX = 3

def get_attr(witness, attr, default=None):
    if isinstance(witness, dict) and attr in witness:
        return witness[attr]
    elif hasattr(witness, attr):
        return getattr(witness, attr)
    return default

def is_finite_collection(obj):
    if isinstance(obj, sympy.FiniteSet):
        return True
    if isinstance(obj, sympy.Set):
        return False
    if isinstance(obj, (list, set, tuple, frozenset)):
        return True
    return False

def conditions(witness):
    H1 = False
    H2 = False
    H3 = False
    neg_Q = False
    
    try:
        X = get_attr(witness, 'X')
        K = get_attr(witness, 'K')
        U = get_attr(witness, 'U')
        d = get_attr(witness, 'd')
        
        if X is None or K is None or U is None or d is None:
            return [False, False, False, False]
            
        def is_subset(A, B):
            if B == sympy.S.Reals:
                try:
                    return all(isinstance(a, (int, float)) or getattr(a, 'is_real', False) for a in A)
                except Exception:
                    return False
            try:
                if hasattr(A, 'issubset') and isinstance(B, sympy.Set):
                    return A.issubset(B)
            except Exception:
                pass
            try:
                if not isinstance(B, (set, frozenset)):
                    B = set(B)
                return all(a in B for a in A)
            except Exception:
                return False
                
        # H1 & H2
        is_compact = get_attr(witness, 'is_compact')
        compact_sets = get_attr(witness, 'compact_sets')
        is_open = get_attr(witness, 'is_open')
        open_sets = get_attr(witness, 'open_sets')
        topology = get_attr(witness, 'topology')
        
        # Evaluate H1
        if is_compact is not None:
            H1 = is_compact(K)
        elif compact_sets is not None:
            H1 = any(set(K) == set(c) for c in compact_sets)
        else:
            if is_finite_collection(X):
                H1 = is_subset(K, X)
            elif X == sympy.S.Reals:
                if topology == 'discrete':
                    H1 = is_finite_collection(K)
                    
        # Evaluate H2
        if is_open is not None:
            H2 = is_open(U)
        elif open_sets is not None:
            H2 = any(set(U) == set(o) for o in open_sets)
        elif isinstance(topology, (list, set, tuple)):
            H2 = any(set(U) == set(o) for o in topology)
        else:
            if is_finite_collection(X):
                if topology == 'discrete' or topology is None:
                    H2 = is_subset(U, X)
            elif X == sympy.S.Reals:
                if topology == 'discrete':
                    H2 = is_subset(U, X)
                    
        # Evaluate H3
        H3 = is_subset(K, U)
        
        # Evaluate neg_Q
        check_conclusion = get_attr(witness, 'check_conclusion')
        if check_conclusion is not None:
            neg_Q = not check_conclusion()
        elif is_finite_collection(X):
            conclusion_holds = False
            distances = set()
            for x in X:
                for k in K:
                    try:
                        distances.add(float(d(x, k)))
                    except Exception:
                        pass
            
            distances = sorted(list(distances))
            eps_to_check = [0.0001, 0.5, 1.0]
            for dist in distances:
                if dist >= 0:
                    eps_to_check.append(dist + 0.0001)
                    eps_to_check.append(dist + 1.0)
                    
            for eps in eps_to_check:
                if eps <= 0: continue
                N_eps = set()
                for x in X:
                    try:
                        if any(float(d(x, k)) < eps for k in K):
                            N_eps.add(x)
                    except Exception:
                        pass
                if is_subset(N_eps, U):
                    conclusion_holds = True
                    break
            neg_Q = not conclusion_holds
        elif X == sympy.S.Reals:
            if is_finite_collection(K) and is_finite_collection(U):
                if len(K) == 0:
                    neg_Q = False
                else:
                    conclusion_holds = False
                    eps_to_check = [1.0, 0.1, 0.01, 0.001, 0.0001]
                    for eps in eps_to_check:
                        subset_holds = True
                        for k in K:
                            try:
                                k_val = float(k)
                            except Exception:
                                continue
                            samples = [k_val, k_val + eps/2, k_val - eps/2, k_val + eps/10, k_val - eps/10, k_val + 10, k_val - 10]
                            for x in samples:
                                try:
                                    if any(float(d(x, k2)) < eps for k2 in K):
                                        if not any(abs(x - float(u)) < 1e-9 for u in U):
                                            subset_holds = False
                                            break
                                except Exception:
                                    pass
                            if not subset_holds:
                                break
                        if subset_holds:
                            conclusion_holds = True
                            break
                    neg_Q = not conclusion_holds
                    
    except Exception:
        pass
        
    return [bool(H1), bool(H2), bool(H3), bool(neg_Q)]