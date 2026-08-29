import math
import itertools
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.abc as abc
from sympy import Rational, Integer

# Top-level setup for potential witness expressions
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
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness can be an integer `k` (representing the ring Z/kZ) or a tuple
    `(N, add_table, mul_table)` representing a finite ring of size N.
    """
    h1_ok = False
    neg_q_ok = False
    
    try:
        N = -1
        is_int_witness = False
        if isinstance(witness, int) or (hasattr(witness, 'is_Integer') and witness.is_Integer):
            N = int(witness)
            is_int_witness = True
        elif isinstance(witness, tuple) and len(witness) == 3:
            N_val = witness[0]
            if isinstance(N_val, int) or (hasattr(N_val, 'is_Integer') and N_val.is_Integer):
                N = int(N_val)
            elif isinstance(N_val, (list, tuple)):
                N = len(N_val)
                
        # H_1: The cardinality of R is 2^n for some integer n >= 1
        # We restrict N <= 64 to ensure the automorphism search completes quickly.
        if N > 1 and N <= 64 and (N & (N - 1)) == 0:
            n = N.bit_length() - 1
            h1_ok = True
        else:
            h1_ok = False
            n = -1
    except Exception:
        h1_ok = False
        n = -1

    try:
        if h1_ok:
            if is_int_witness:
                add_table = [[(x + y) % N for y in range(N)] for x in range(N)]
                mul_table = [[(x * y) % N for y in range(N)] for x in range(N)]
            else:
                N_val = witness[0]
                if isinstance(N_val, int) or (hasattr(N_val, 'is_Integer') and N_val.is_Integer):
                    elements = list(range(N))
                else:
                    elements = list(N_val)
                
                add_table = []
                mul_table = []
                valid_tables = True
                for x in range(N):
                    add_row = []
                    mul_row = []
                    for y in range(N):
                        a_val = witness[1][x][y]
                        m_val = witness[2][x][y]
                        if a_val in elements:
                            add_row.append(elements.index(a_val))
                        else:
                            valid_tables = False
                        if m_val in elements:
                            mul_row.append(elements.index(m_val))
                        else:
                            valid_tables = False
                    add_table.append(add_row)
                    mul_table.append(mul_row)
                
                if not valid_tables:
                    return [h1_ok, False]

            # Find all ring automorphisms using backtracking
            ans = []
            def backtrack(mapping, used):
                if len(ans) > math.factorial(n):
                    return
                if len(mapping) == N:
                    ans.append(mapping.copy())
                    return
                
                i = len(mapping)
                for j in range(N):
                    if j in used: continue
                    
                    valid = True
                    mapping.append(j)
                    
                    # Check consistency with already assigned mappings
                    for x in range(i + 1):
                        if not valid: break
                        for y in range(i + 1):
                            res_add = add_table[x][y]
                            if res_add <= i:
                                if mapping[res_add] != add_table[mapping[x]][mapping[y]]:
                                    valid = False
                                    break
                            res_mul = mul_table[x][y]
                            if res_mul <= i:
                                if mapping[res_mul] != mul_table[mapping[x]][mapping[y]]:
                                    valid = False
                                    break
                    
                    if valid:
                        used.add(j)
                        backtrack(mapping, used)
                        used.remove(j)
                    
                    mapping.pop()

            backtrack([], set())
            
            # neg_Q: The automorphism group of R is NOT isomorphic to the symmetric group S_n
            if len(ans) != math.factorial(n):
                neg_q_ok = True
            else:
                def gcd(a, b):
                    while b: a, b = b, a % b
                    return a

                def order_counts(group_elements):
                    counts = {}
                    for p in group_elements:
                        visited = [False] * len(p)
                        order = 1
                        for i in range(len(p)):
                            if not visited[i]:
                                cycle_len = 0
                                curr = i
                                while not visited[curr]:
                                    visited[curr] = True
                                    curr = p[curr]
                                    cycle_len += 1
                                if cycle_len > 0:
                                    order = (order * cycle_len) // gcd(order, cycle_len)
                        counts[order] = counts.get(order, 0) + 1
                    return counts
                
                counts_G = order_counts(ans)
                
                def generate_Sn(n):
                    return list(itertools.permutations(range(n)))
                
                counts_Sn = order_counts(generate_Sn(n))
                
                # If the distribution of element orders differs, the groups are not isomorphic
                if counts_G != counts_Sn:
                    neg_q_ok = True
                else:
                    neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: The cardinality of R is 2^n for some integer n >= 1",
    "¬Q: The automorphism group of R is NOT isomorphic to the symmetric group S_n"
]

N_HYP = 1
NEG_Q_INDEX = 1