import sympy
from sympy import Rational, Integer
import itertools
import functools
import math

# Top-level setup for potential witness expressions
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6

def parse_witness(witness):
    """
    Parses the witness into a modulus n (representing the ring Z_n) 
    and a list of subsets of Z_n.
    """
    if isinstance(witness, dict):
        if 'n' in witness:
            R = witness['n']
        elif 'R' in witness:
            R = witness['R']
        else:
            R = len(witness.get('elements', []))
        I_list = witness['I_list']
    elif isinstance(witness, tuple) and len(witness) == 2:
        R, I_list = witness[0], witness[1]
    elif isinstance(witness, list) and all(isinstance(x, (list, set, tuple)) for x in witness):
        I_list = witness
        max_elem = -1
        for I in I_list:
            for x in I:
                if int(x) > max_elem:
                    max_elem = int(x)
        R = max_elem + 1
    else:
        R, I_list = witness.R, witness.I_list

    if isinstance(R, int):
        n = R
    elif hasattr(R, '__len__'):
        n = len(R)
    else:
        n = int(R)
        
    parsed_I_list = []
    for I in I_list:
        parsed_I_list.append(set(int(x) for x in I))
    return n, parsed_I_list

def conditions(witness) -> list[bool]:
    # H_1: R is a commutative ring with identity
    try:
        n, I_list = parse_witness(witness)
        # Z_n is a commutative ring with identity for any n >= 1
        h1_ok = isinstance(n, int) and n >= 1
    except Exception:
        h1_ok = False

    # H_2: I_i + I_j = R for all i != j
    try:
        n, I_list = parse_witness(witness)
        R = set(range(n))
        h2_ok = True
        for i in range(len(I_list)):
            for j in range(len(I_list)):
                if i != j:
                    add_set = set(((a + b) % n) for a in I_list[i] for b in I_list[j])
                    if add_set != R:
                        h2_ok = False
                        break
            if not h2_ok:
                break
    except Exception:
        h2_ok = False

    # ¬Q: The intersection of I_k is NOT equal to their product
    try:
        n, I_list = parse_witness(witness)
        if not I_list:
            neg_q_ok = False
        else:
            # Compute Intersection
            inter = set(I_list[0])
            for I in I_list[1:]:
                inter = inter.intersection(I)
                
            # Compute Product (additive closure of element-wise products)
            if len(I_list) == 1:
                closure = set(I_list[0])
            else:
                prods = set(I_list[0])
                for I in I_list[1:]:
                    prods = set(((a * b) % n) for a in prods for b in I)
                    
                closure = set(prods)
                if not closure:
                    closure.add(0)
                
                queue = list(prods)
                while queue:
                    curr = queue.pop(0)
                    for x in prods:
                        nxt = (curr + x) % n
                        if nxt not in closure:
                            closure.add(nxt)
                            queue.append(nxt)
                            
            neg_q_ok = (inter != closure)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: I_i + I_j = R for all i != j",
    "¬Q: Intersection of I_k is not equal to their product"
]

N_HYP = 2
NEG_Q_INDEX = 2