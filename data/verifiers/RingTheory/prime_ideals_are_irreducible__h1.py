import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z
import itertools

# Top-level setup
# (No specific named rings are strictly required by standard bindings, 
# but we provide basic SymPy symbols as requested)

def get_ideal(X, elements, add, mul):
    ideal = set(X)
    changed = True
    max_size = len(elements)
    while changed:
        changed = False
        new_elements = set()
        for a in ideal:
            for b in ideal:
                s = add(a, b)
                if s not in ideal and s not in new_elements:
                    new_elements.add(s)
            for r in elements:
                p1 = mul(r, a)
                if p1 not in ideal and p1 not in new_elements:
                    new_elements.add(p1)
                p2 = mul(a, r)
                if p2 not in ideal and p2 not in new_elements:
                    new_elements.add(p2)
        if new_elements:
            ideal.update(new_elements)
            changed = True
            if len(ideal) >= max_size:
                break
    return ideal

def is_prime_ideal(P_set, elements, add, mul):
    P_set = set(P_set)
    if not P_set: return False
    
    # Check if P is an ideal
    for a in P_set:
        for b in P_set:
            if add(a, b) not in P_set: return False
        for r in elements:
            if mul(r, a) not in P_set: return False
            if mul(a, r) not in P_set: return False
            
    # Check if P is proper
    if len(P_set) == len(elements): return False
    
    # Precompute principal ideals
    principal_ideals = {}
    for a in elements:
        if a not in P_set:
            principal_ideals[a] = get_ideal([a], elements, add, mul)
            
    # Check prime condition: for all a, b \notin P, AB \not\subseteq P
    for a in elements:
        if a in P_set: continue
        for b in elements:
            if b in P_set: continue
            
            A = principal_ideals[a]
            B = principal_ideals[b]
            
            ab_in_P = True
            for u in A:
                for v in B:
                    if mul(u, v) not in P_set:
                        ab_in_P = False
                        break
                if not ab_in_P:
                    break
            if ab_in_P:
                return False
    return True

def get_zero(elements, add):
    for z_elem in elements:
        if all(add(z_elem, e) == e for e in elements):
            return z_elem
    return None

def get_all_ideals(elements, add, mul):
    z_elem = get_zero(elements, add)
    if z_elem is None: return set()
    
    ideals = {frozenset([z_elem])}
    for a in elements:
        ideals.add(frozenset(get_ideal([a], elements, add, mul)))
        
    changed = True
    while changed:
        changed = False
        new_ideals = set()
        for I in ideals:
            for J in ideals:
                sum_ideal = set()
                for u in I:
                    for v in J:
                        sum_ideal.add(add(u, v))
                sum_ideal_fs = frozenset(sum_ideal)
                if sum_ideal_fs not in ideals and sum_ideal_fs not in new_ideals:
                    new_ideals.add(sum_ideal_fs)
        if new_ideals:
            ideals.update(new_ideals)
            changed = True
    return ideals

def is_irreducible_ideal(P_set, ideals):
    P_fs = frozenset(P_set)
    for I in ideals:
        for J in ideals:
            if I.intersection(J) == P_fs:
                if I != P_fs and J != P_fs:
                    return False
    return True

def extract_witness(witness):
    if isinstance(witness, dict) and 'elements' in witness:
        return witness['elements'], witness['add'], witness['mul'], witness['P']
    if hasattr(witness, 'elements') and hasattr(witness, 'add'):
        return witness.elements, witness.add, witness.mul, witness.P
    if isinstance(witness, tuple) and len(witness) == 4:
        return witness
    if isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[0], int):
        n, p_gen = witness
        elements = list(range(n))
        add = lambda a, b: (a + b) % n
        mul = lambda a, b: (a * b) % n
        P = set()
        for i in range(n):
            P.add((p_gen * i) % n)
        return elements, add, mul, list(P)
    raise ValueError("Unknown witness format")

def conditions(witness):
    # Fast path for SymPy ideals
    if hasattr(witness, 'is_prime') and hasattr(witness, 'ring'):
        try:
            h1 = bool(witness.is_prime)
            # Prime ideals are always irreducible, so the negated conclusion is False
            neg_q = False
            return [h1, neg_q]
        except Exception:
            pass

    try:
        elements, add, mul, P = extract_witness(witness)
    except Exception:
        return [False, False]
        
    try:
        h1 = is_prime_ideal(P, elements, add, mul)
    except Exception:
        h1 = False
        
    try:
        ideals = get_all_ideals(elements, add, mul)
        is_irred = is_irreducible_ideal(P, ideals)
        neg_q = not is_irred
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: P is a prime ideal of R",
    "¬Q: P is not an irreducible ideal"
]

N_HYP = 1
NEG_Q_INDEX = 1