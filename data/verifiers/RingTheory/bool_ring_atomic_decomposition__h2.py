import itertools
import functools
import math
import sympy
from sympy import symbols, Rational, Integer

# Top-level setup
x, y, z = symbols('x y z')

def extract_ring_and_x(witness):
    """
    Extracts the elements, addition function, multiplication function, and the element x
    from various possible witness formats.
    """
    # Format 1: Tuple of (elements, add_table/func, mul_table/func, x)
    if isinstance(witness, tuple) and len(witness) == 4:
        elements, add_obj, mul_obj, x_val = witness
        
        if isinstance(add_obj, dict):
            add = lambda a, b: add_obj[(a, b)]
        elif isinstance(add_obj, list):
            add = lambda a, b: add_obj[elements.index(a)][elements.index(b)]
        else:
            add = add_obj
            
        if isinstance(mul_obj, dict):
            mul = lambda a, b: mul_obj[(a, b)]
        elif isinstance(mul_obj, list):
            mul = lambda a, b: mul_obj[elements.index(a)][elements.index(b)]
        else:
            mul = mul_obj
            
        return list(elements), add, mul, x_val
        
    # Format 2: Dictionary with keys
    if isinstance(witness, dict) and all(k in witness for k in ('elements', 'add', 'mul', 'x')):
        return list(witness['elements']), witness['add'], witness['mul'], witness['x']
        
    # Format 3: Object with attributes
    if hasattr(witness, 'elements') and hasattr(witness, 'add') and hasattr(witness, 'mul') and hasattr(witness, 'x'):
        return list(witness.elements), witness.add, witness.mul, witness.x
        
    # Format 4: Tuple (n, x) where n is an int, representing the power set ring of {0, ..., n-1}
    if isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[0], int):
        n, x_val = witness
        elements = []
        base_set = list(range(n))
        for r in range(n + 1):
            for combo in itertools.combinations(base_set, r):
                elements.append(frozenset(combo))
        add = lambda a, b: a ^ b
        mul = lambda a, b: a & b
        if not isinstance(x_val, frozenset):
            try:
                x_val = frozenset(x_val)
            except Exception:
                pass
        return elements, add, mul, x_val
        
    # Default fallback: assume witness is just the element x in the Boolean ring Z_2
    elements = [0, 1]
    add = lambda a, b: (a + b) % 2
    mul = lambda a, b: (a * b) % 2
    return elements, add, mul, witness

def conditions(witness) -> list[bool]:
    try:
        elements, add, mul, x_val = extract_ring_and_x(witness)
    except Exception:
        return [False, False]
        
    # Check H_1: R is a finite Boolean ring and x is in R
    h1 = False
    try:
        if elements and x_val in elements:
            is_ring = True
            
            # Check closure
            for a in elements:
                for b in elements:
                    if add(a, b) not in elements: is_ring = False
                    if mul(a, b) not in elements: is_ring = False
            
            if is_ring:
                # Check commutativity and associativity of addition
                for a in elements:
                    for b in elements:
                        if add(a, b) != add(b, a): is_ring = False
                        for c in elements:
                            if add(add(a, b), c) != add(a, add(b, c)): is_ring = False
            
            if is_ring:
                # Check for additive identity (zero)
                zeros = [z for z in elements if all(add(z, a) == a for a in elements)]
                if len(zeros) != 1:
                    is_ring = False
                else:
                    zero = zeros[0]
                    # Check for additive inverses
                    for a in elements:
                        if not any(add(a, b) == zero for b in elements):
                            is_ring = False
            
            if is_ring:
                # Check associativity of multiplication and distributivity
                for a in elements:
                    for b in elements:
                        for c in elements:
                            if mul(mul(a, b), c) != mul(a, mul(b, c)): is_ring = False
                            if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): is_ring = False
                            if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): is_ring = False
            
            if is_ring:
                # Check Boolean property (x^2 = x)
                for a in elements:
                    if mul(a, a) != a: is_ring = False
                    
            h1 = is_ring
    except Exception:
        h1 = False

    # Check neg_Q: x cannot be expressed as a non-empty sum of mutually orthogonal atoms of R
    neg_q = False
    try:
        if h1:
            zero = next(z for z in elements if all(add(z, a) == a for a in elements))
            
            # Find all atoms in the Boolean ring
            atoms = []
            for a in elements:
                if a == zero: continue
                is_atom = True
                for y in elements:
                    prod = mul(y, a)
                    if prod != zero and prod != a:
                        is_atom = False
                        break
                if is_atom:
                    atoms.append(a)
                    
            # Check if x_val is the sum of any non-empty subset of mutually orthogonal atoms
            is_sum = False
            for r in range(1, len(atoms) + 1):
                for subset in itertools.combinations(atoms, r):
                    orthogonal = True
                    # Verify mutual orthogonality
                    for i in range(len(subset)):
                        for j in range(i+1, len(subset)):
                            if mul(subset[i], subset[j]) != zero:
                                orthogonal = False
                                break
                        if not orthogonal:
                            break
                            
                    if orthogonal:
                        s = subset[0]
                        for item in subset[1:]:
                            s = add(s, item)
                        if s == x_val:
                            is_sum = True
                            break
                if is_sum:
                    break
                    
            neg_q = not is_sum
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a finite Boolean ring and x is in R",
    "¬Q: x cannot be expressed as a non-empty sum of mutually orthogonal atoms of R"
]

N_HYP = 1
NEG_Q_INDEX = 1