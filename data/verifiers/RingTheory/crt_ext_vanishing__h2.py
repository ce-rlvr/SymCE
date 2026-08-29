import math
import itertools
import functools
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def conditions(witness):
    """
    witness is expected to be a dictionary with:
      'ring_size': int (number of elements N, elements are 0 to N-1)
      'add': list of lists (N x N addition table)
      'mult': list of lists (N x N multiplication table)
      'I': list of ints (elements of ideal I)
      'J': list of ints (elements of ideal J)
      'n': int (the integer n in Ext^n, must be 0 for this verifier)
    """
    try:
        if isinstance(witness, dict):
            N = witness['ring_size']
            add = witness['add']
            mult = witness['mult']
            I = witness['I']
            J = witness['J']
            n = witness['n']
        elif isinstance(witness, (list, tuple)) and len(witness) == 6:
            N, add, mult, I, J, n = witness
        else:
            N = witness.ring_size
            add = witness.add
            mult = witness.mult
            I = witness.I
            J = witness.J
            n = witness.n
    except Exception:
        return [False, False, False, False]

    # H1: R is a commutative ring (rng, identity not required)
    h1 = False
    try:
        if len(add) == N and all(len(row) == N for row in add) and \
           len(mult) == N and all(len(row) == N for row in mult):
            
            closure = True
            for i in range(N):
                for j in range(N):
                    if add[i][j] not in range(N) or mult[i][j] not in range(N):
                        closure = False
            
            if closure:
                comm = all(add[i][j] == add[j][i] and mult[i][j] == mult[j][i] 
                           for i in range(N) for j in range(N))
                
                assoc = all(add[add[i][j]][k] == add[i][add[j][k]] and 
                            mult[mult[i][j]][k] == mult[i][mult[j][k]]
                            for i in range(N) for j in range(N) for k in range(N))
                
                dist = all(mult[i][add[j][k]] == add[mult[i][j]][mult[i][k]]
                           for i in range(N) for j in range(N) for k in range(N))
                
                zeros_list = [i for i in range(N) if all(add[i][j] == j for j in range(N))]
                
                if comm and assoc and dist and len(zeros_list) == 1:
                    zero = zeros_list[0]
                    inv = all(any(add[i][j] == zero for j in range(N)) for i in range(N))
                    if inv:
                        h1 = True
    except Exception:
        h1 = False

    # H2: I and J are comaximal ideals
    h2 = False
    try:
        I_set = set(I)
        J_set = set(J)
        if I_set.issubset(range(N)) and J_set.issubset(range(N)):
            I_ideal = all(add[x][y] in I_set for x in I for y in I) and \
                      all(mult[r][x] in I_set for r in range(N) for x in I)
            J_ideal = all(add[x][y] in J_set for x in J for y in J) and \
                      all(mult[r][x] in J_set for r in range(N) for x in J)
            
            sums = set(add[x][y] for x in I for y in J)
            if I_ideal and J_ideal and sums == set(range(N)):
                h2 = True
    except Exception:
        h2 = False

    # H3: n >= 0 is an integer
    h3 = False
    try:
        if isinstance(n, int) and n >= 0:
            h3 = True
    except Exception:
        h3 = False

    # neg_Q: Ext^n_R(R/I, R/J) is NOT trivial
    neg_q = False
    try:
        # We only evaluate the counterexample for n = 0 (Hom_R(R/I, R/J))
        if n == 0 and h1 and h2:
            def get_cosets(ideal):
                cosets = []
                seen = set()
                for i in range(N):
                    if i not in seen:
                        coset = set(add[i][x] for x in ideal)
                        cosets.append(frozenset(coset))
                        seen.update(coset)
                return cosets

            RI_list = get_cosets(I)
            RJ_list = get_cosets(J)
            
            def add_cosets(A, B, coset_list):
                a = next(iter(A))
                b = next(iter(B))
                s = add[a][b]
                for i, C in enumerate(coset_list):
                    if s in C: return i
                return -1
                
            def mult_coset(r, A, coset_list):
                a = next(iter(A))
                p = mult[r][a]
                for i, C in enumerate(coset_list):
                    if p in C: return i
                return -1

            RI_add = [[add_cosets(A, B, RI_list) for B in RI_list] for A in RI_list]
            RJ_add = [[add_cosets(A, B, RJ_list) for B in RJ_list] for A in RJ_list]
            
            RI_mult = [[mult_coset(r, A, RI_list) for A in RI_list] for r in range(N)]
            RJ_mult = [[mult_coset(r, A, RJ_list) for A in RJ_list] for r in range(N)]
            
            hom_count = 0
            
            def search(idx, current_mapping):
                nonlocal hom_count
                if hom_count > 1:
                    return
                if idx == len(RI_list):
                    hom_count += 1
                    return
                
                for val in range(len(RJ_list)):
                    current_mapping.append(val)
                    valid = True
                    
                    for i in range(idx + 1):
                        for j in range(idx + 1):
                            k = RI_add[i][j]
                            if k <= idx:
                                if current_mapping[k] != RJ_add[current_mapping[i]][current_mapping[j]]:
                                    valid = False
                                    break
                        if not valid: break
                        
                    if valid:
                        for r in range(N):
                            for i in range(idx + 1):
                                k = RI_mult[r][i]
                                if k <= idx:
                                    if current_mapping[k] != RJ_mult[r][current_mapping[i]]:
                                        valid = False
                                        break
                            if not valid: break
                            
                    if valid:
                        search(idx + 1, current_mapping)
                        
                    current_mapping.pop()

            search(0, [])
            if hom_count > 1:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I and J are comaximal",
    "H_3: n >= 0 is an integer",
    "¬Q: Ext^n_R(R/I, R/J) is not the trivial group"
]

N_HYP = 3
NEG_Q_INDEX = 3