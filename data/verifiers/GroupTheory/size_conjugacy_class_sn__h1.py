import math
from sympy.combinatorics import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness):
    """
    Checks if the witness satisfies the hypotheses and falsifies the conclusion.
    Expected witness format: a dictionary {'C': list_of_permutations, 'n': int, 'm': dict_or_list}
    or a tuple (C, n, m).
    """
    try:
        if isinstance(witness, dict):
            C_raw = witness.get('C', [])
            n_raw = witness.get('n', 0)
            m = witness.get('m', {})
        else:
            C_raw, n_raw, m = witness
            
        C = list(C_raw)
        n = int(n_raw)
        
        if n < 1 or n > 1000:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    def check_h1():
        try:
            if not C:
                return False
            
            for p in C:
                if not isinstance(p, Permutation):
                    return False
                supp = p.support()
                if supp and max(supp) >= n:
                    return False
                    
            def full_cycle_type(p, n):
                c = {k: 0 for k in range(1, n+1)}
                elements_in_cycles = 0
                for cyc in p.cyclic_form:
                    c[len(cyc)] += 1
                    elements_in_cycles += len(cyc)
                c[1] += n - elements_in_cycles
                return c
                
            p0 = C[0]
            c0 = full_cycle_type(p0, n)
            
            for p in C:
                if full_cycle_type(p, n) != c0:
                    return False
                    
            denom = 1
            for k, count in c0.items():
                denom *= (k ** count) * math.factorial(count)
            expected_size = math.factorial(n) // denom
            
            if len(set(C)) != expected_size:
                return False
                
            return True
        except Exception:
            return False

    def check_h2():
        try:
            if isinstance(m, dict):
                get_m = lambda k: m.get(k, 0)
            else:
                get_m = lambda k: m[k-1]
                
            for p in C:
                actual_m = {k: 0 for k in range(1, n+1)}
                for cyc in p.cyclic_form:
                    if len(cyc) <= n:
                        actual_m[len(cyc)] += 1
                    else:
                        return False
                for k in range(1, n+1):
                    if int(get_m(k)) != actual_m[k]:
                        return False
            return True
        except Exception:
            return False

    def check_neg_q():
        try:
            if isinstance(m, dict):
                get_m = lambda k: m.get(k, 0)
            else:
                get_m = lambda k: m[k-1]
                
            denom = 1
            for k in range(1, n+1):
                mk = int(get_m(k))
                if mk < 0:
                    return False
                denom *= (k ** mk) * math.factorial(mk)
                
            expected_size = math.factorial(n) // denom
            return len(set(C)) != expected_size
        except Exception:
            return False

    return [check_h1(), check_h2(), check_neg_q()]

CONDITION_LABELS = [
    "H_1: C is a conjugacy class in the symmetric group S_n",
    "H_2: The elements of C have a disjoint cycle decomposition consisting of exactly m_k cycles of length k for each 1 <= k <= n",
    "¬Q: The number of elements in C is NOT n! / ∏_{k=1}^n (k^{m_k} * m_k!)"
]

N_HYP = 2
NEG_Q_INDEX = 2