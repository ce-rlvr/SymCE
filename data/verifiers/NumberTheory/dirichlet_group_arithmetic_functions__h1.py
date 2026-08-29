import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: For all f in S, f(1) != 0",
    "¬Q: S does not form an abelian group under Dirichlet convolution"
]

N_HYP = 1
NEG_Q_INDEX = 1

def to_tuple(f, N=10):
    if isinstance(f, (tuple, list)):
        res = list(f)
        if len(res) < N:
            res += [0] * (N - len(res))
        return tuple(res[:N])
    elif callable(f):
        return tuple(f(n) for n in range(1, N + 1))
    else:
        raise ValueError("Unknown function format")

def dirichlet_conv(f, g):
    N = len(f)
    h = [0] * N
    for n in range(1, N + 1):
        val = 0
        for d in sympy.ntheory.divisors(n):
            val += f[d - 1] * g[n // d - 1]
        try:
            if hasattr(val, 'expand'):
                val = val.expand()
        except Exception:
            pass
        h[n - 1] = val
    return tuple(h)

def conditions(witness):
    try:
        # Allow single function or single tuple as witness
        if callable(witness):
            witness = [witness]
        elif isinstance(witness, (tuple, list)) and len(witness) > 0:
            if not isinstance(witness[0], (tuple, list)) and not callable(witness[0]):
                witness = [witness]
                
        N = 10
        S = []
        for i, f in enumerate(witness):
            if i >= 100:  # Limit size to ensure fast execution
                break
            S.append(to_tuple(f, N))
    except Exception:
        return [False, False]
        
    # H_1: For all f in S, f(1) != 0
    try:
        h1 = bool(S) and all(f[0] != 0 for f in S)
    except Exception:
        h1 = False
        
    # ¬Q: S does NOT form an abelian group under Dirichlet convolution
    try:
        q = True
        if not S:
            q = False
        else:
            S_set = set(S)
            
            # Check Closure
            for f in S_set:
                for g in S_set:
                    if dirichlet_conv(f, g) not in S_set:
                        q = False
                        break
                if not q:
                    break
                    
            if q:
                # Check Identity
                identities = []
                for e in S_set:
                    if all(dirichlet_conv(e, f) == f for f in S_set):
                        identities.append(e)
                if not identities:
                    q = False
                else:
                    e = identities[0]
                    # Check Inverses
                    for f in S_set:
                        has_inverse = False
                        for g in S_set:
                            if dirichlet_conv(f, g) == e:
                                has_inverse = True
                                break
                        if not has_inverse:
                            q = False
                            break
                            
                    if q:
                        # Check Abelian property
                        for f in S_set:
                            for g in S_set:
                                if dirichlet_conv(f, g) != dirichlet_conv(g, f):
                                    q = False
                                    break
                            if not q:
                                break
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, neg_q]