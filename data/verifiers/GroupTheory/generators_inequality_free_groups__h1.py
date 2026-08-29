import sympy
from sympy.combinatorics.free_groups import FreeGroup
from sympy.combinatorics.fp_groups import FpGroup
from sympy import Matrix
import itertools
import math
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

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

def get_exponent_vector(w, F):
    if isinstance(F, FreeGroup):
        n = F.rank
        gens = F.generators
    elif isinstance(F, FpGroup):
        n = len(F.generators)
        gens = F.generators
    else:
        n = 0
        gens = []
        
    vec = [0] * n
    
    gen_to_idx = {}
    for i, g in enumerate(gens):
        gen_to_idx[g] = i
        if hasattr(g, 'word'):
            gw = g.word
            if hasattr(gw, 'array_form') and len(gw.array_form) > 0:
                gen_to_idx[gw.array_form[0][0]] = i
        elif hasattr(g, 'array_form') and len(g.array_form) > 0:
            gen_to_idx[g.array_form[0][0]] = i
            
    if hasattr(w, 'word'):
        w_to_use = w.word
    else:
        w_to_use = w
        
    if hasattr(w_to_use, 'array_form'):
        for item in w_to_use.array_form:
            gen, exp = item
            if gen in gen_to_idx:
                vec[gen_to_idx[gen]] += exp
            elif isinstance(gen, int) and 0 <= gen < n:
                vec[gen] += exp
    return vec

def generates_Zn(M_rows, n):
    if n == 0:
        return True
    if len(M_rows) < n:
        return False
    
    M = Matrix(M_rows)
    if M.rank() < n:
        return False
    
    try:
        from sympy.matrices.normalforms import smith_normal_form
        snf = smith_normal_form(M)
        for i in range(n):
            if snf[i, i] != 1 and snf[i, i] != -1:
                return False
        return True
    except Exception:
        pass

    current_gcd = 0
    count = 0
    for rows in itertools.combinations(range(len(M_rows)), n):
        sub_M = M.extract(list(rows), list(range(n)))
        det = sub_M.det()
        current_gcd = math.gcd(current_gcd, abs(int(det)))
        if current_gcd == 1:
            return True
        count += 1
        if count > 1000:
            break
    return current_gcd == 1

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            F = witness.get('F')
            S = witness.get('S')
            n = witness.get('n')
        elif isinstance(witness, tuple) and len(witness) == 3:
            F, S, n = witness
        else:
            F = getattr(witness, 'F', None)
            S = getattr(witness, 'S', None)
            n = getattr(witness, 'n', None)
    except Exception:
        return [False, False, False]

    if F is None or S is None or n is None:
        return [False, False, False]

    try:
        S = list(S)
    except Exception:
        return [False, False, False]

    # H_1: F is a free group of rank n
    try:
        h1 = False
        if isinstance(F, FreeGroup):
            h1 = (F.rank == n)
        elif isinstance(F, FpGroup) and len(F.relators) == 0:
            h1 = (len(F.generators) == n)
    except Exception:
        h1 = False

    # H_2: S is a generating set for F
    try:
        if not h1:
            h2 = False
        else:
            M_rows = []
            for w in S:
                vec = get_exponent_vector(w, F)
                M_rows.append(vec)
            h2 = generates_Zn(M_rows, n)
    except Exception:
        h2 = False

    # ¬Q: The cardinality of S is less than n
    try:
        neg_q = len(S) < n
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group of rank n",
    "H_2: S is a generating set for F",
    "¬Q: The cardinality of S is less than n"
]

N_HYP = 2
NEG_Q_INDEX = 2