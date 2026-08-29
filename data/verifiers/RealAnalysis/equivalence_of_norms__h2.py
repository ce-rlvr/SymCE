import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def extract_witness(witness):
    if isinstance(witness, tuple) and len(witness) == 3:
        return witness
    elif hasattr(witness, 'n') and hasattr(witness, 'norm1') and hasattr(witness, 'norm2'):
        return witness.n, witness.norm1, witness.norm2
    elif isinstance(witness, dict) and 'n' in witness and 'norm1' in witness and 'norm2' in witness:
        return witness['n'], witness['norm1'], witness['norm2']
    raise ValueError("Invalid witness format")

def conditions(witness) -> list[bool]:
    # H_1: V is a finite-dimensional vector space over R
    try:
        n, norm1, norm2 = extract_witness(witness)
        h1_ok = isinstance(n, int) and n > 0
    except Exception:
        h1_ok = False

    # neg_Q: The conclusion fails (the functions are not equivalent)
    neg_q_ok = False
    try:
        n, norm1, norm2 = extract_witness(witness)
        if isinstance(n, int) and n > 0 and callable(norm1) and callable(norm2):
            points = []
            points.append([0.0] * n)
            
            for i in range(min(n, 100)):
                v = [0.0] * n
                v[i] = 1.0
                points.append(v)
                
            seed = 12345
            def lcg():
                nonlocal seed
                seed = (1103515245 * seed + 12345) % (2**31)
                return seed / (2**31 - 1)
                
            for _ in range(1000):
                v = []
                for _ in range(n):
                    r = lcg()
                    if r < 0.33:
                        v.append(-1.0)
                    elif r < 0.66:
                        v.append(0.0)
                    else:
                        v.append(1.0)
                if any(x != 0 for x in v):
                    points.append(v)
                    
            scaled_points = []
            for p in points:
                for scale in [1e-6, 1e-3, 1.0, 1e3, 1e6]:
                    scaled_points.append([x * scale for x in p])
                    
            pos_ratios = []
            neg_ratios = []
            
            for x in scaled_points:
                try:
                    n1 = float(norm1(x))
                    n2 = float(norm2(x))
                except Exception:
                    continue
                    
                if n1 == 0 and n2 == 0:
                    continue
                if n1 == 0 and n2 != 0:
                    neg_q_ok = True
                    break
                if n1 != 0 and n2 == 0:
                    neg_q_ok = True
                    break
                    
                if n1 > 0 and n2 < 0:
                    neg_q_ok = True
                    break
                if n1 < 0 and n2 > 0:
                    neg_q_ok = True
                    break
                    
                if n1 > 0 and n2 > 0:
                    pos_ratios.append(n2 / n1)
                elif n1 < 0 and n2 < 0:
                    neg_ratios.append(n2 / n1)
                    
            if not neg_q_ok:
                if pos_ratios:
                    max_pos = max(pos_ratios)
                    min_pos = min(pos_ratios)
                    if max_pos / min_pos > 1e5:
                        neg_q_ok = True
                        
                if neg_ratios and not neg_q_ok:
                    max_neg = max(neg_ratios)
                    min_neg = min(neg_ratios)
                    if max_neg / min_neg > 1e5:
                        neg_q_ok = True
                        
                if pos_ratios and neg_ratios and not neg_q_ok:
                    if max(neg_ratios) > min(pos_ratios) + 1e-9:
                        neg_q_ok = True
                    if max(pos_ratios) > min(neg_ratios) + 1e-9:
                        neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over R",
    "¬Q: The functions are not equivalent norms"
]

N_HYP = 1
NEG_Q_INDEX = 1