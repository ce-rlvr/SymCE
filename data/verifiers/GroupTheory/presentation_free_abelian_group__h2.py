import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for standard algebra objects
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
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            X = witness.get('X')
            R = witness.get('R')
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                n, X, R = witness
            elif len(witness) == 2:
                n, X = witness
                R = None
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: n is a positive integer
    try:
        h1 = isinstance(n, int) and 0 < n <= 1000
    except Exception:
        h1 = False

    # H2: R = {x_i x_j x_i^{-1} x_j^{-1} | 1 <= i < j <= n}
    try:
        if not (isinstance(n, int) and 0 < n <= 1000):
            h2 = False
        else:
            expected_R = set()
            for i in range(1, n + 1):
                for j in range(i + 1, n + 1):
                    expected_R.add((f'x{i}', f'x{j}', f'-x{i}', f'-x{j}'))
            
            parsed_R = set()
            if R is not None:
                if isinstance(R, str):
                    R_list = [R]
                else:
                    R_list = R
                    
                for rel in R_list:
                    if isinstance(rel, str):
                        rel_str = rel.replace('*', ' ')
                        rel_tuple = tuple(rel_str.split())
                    elif hasattr(rel, 'group') or hasattr(rel, 'free_group'):
                        rel_tuple = tuple(str(rel).replace(' ', '').split('*'))
                    else:
                        rel_tuple = tuple(str(x) for x in rel)
                    
                    normalized_rel = []
                    for symbol in rel_tuple:
                        if symbol.endswith('^-1'):
                            normalized_rel.append('-' + symbol[:-3])
                        elif symbol.endswith('**-1'):
                            normalized_rel.append('-' + symbol[:-5])
                        elif symbol.startswith('~'):
                            normalized_rel.append('-' + symbol[1:])
                        else:
                            normalized_rel.append(symbol)
                    parsed_R.add(tuple(normalized_rel))
                
                h2 = (parsed_R == expected_R)
            else:
                if n == 1:
                    h2 = True
                else:
                    h2 = False
    except Exception:
        h2 = False

    # neg_Q: The group <X | R> is not isomorphic to the free abelian group of rank n
    try:
        if not isinstance(n, int):
            neg_q = False
        else:
            parsed_X = set()
            if isinstance(X, int):
                if X <= 1000:
                    parsed_X = set(f'x{i}' for i in range(1, X + 1))
            elif isinstance(X, str):
                parsed_X = set(X.replace(',', ' ').split())
            else:
                for x in X:
                    parsed_X.add(str(x))
                    if len(parsed_X) > 1000:
                        break
                    
            valid_presentation = True
            # parsed_R is computed in H2 block, but if H2 failed it might be incomplete.
            # We re-evaluate valid_presentation based on whatever parsed_R is.
            # If R was None, parsed_R is empty, which is trivially valid over any X.
            for rel in parsed_R:
                for symbol in rel:
                    base_symbol = symbol[1:] if symbol.startswith('-') else symbol
                    if base_symbol not in parsed_X:
                        valid_presentation = False
                        break
                        
            if not valid_presentation:
                neg_q = True
            else:
                neg_q = (len(parsed_X) != n)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: R is the set of commutators {x_i x_j x_i^{-1} x_j^{-1} | 1 <= i < j <= n}",
    "¬Q: The group <X | R> is not isomorphic to the free abelian group of rank n"
]

N_HYP = 2
NEG_Q_INDEX = 2