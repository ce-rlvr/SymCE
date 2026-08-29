import itertools

# Top-level setup for potential witness expressions
# (No specific named objects are required for this ring theory domain, 
# but we provide basic imports that might be used to construct rings)
from sympy import symbols, Rational

def get_ops(witness):
    """
    Extracts elements, addition, and multiplication operations from the witness.
    Supports:
    - tuple: (elements, add_table, mul_table)
    - object with .elements, .add, .mul
    - list/set/tuple of elements that support + and * operators
    """
    if isinstance(witness, tuple) and len(witness) == 3:
        elements, add_table, mul_table = witness
        if isinstance(add_table, dict):
            add = lambda x, y: add_table[(x, y)]
            mul = lambda x, y: mul_table[(x, y)]
        else:
            idx = {e: i for i, e in enumerate(elements)}
            def add(x, y):
                res = add_table[idx[x]][idx[y]]
                if res not in elements and isinstance(res, int) and 0 <= res < len(elements):
                    return elements[res]
                return res
            def mul(x, y):
                res = mul_table[idx[x]][idx[y]]
                if res not in elements and isinstance(res, int) and 0 <= res < len(elements):
                    return elements[res]
                return res
        return elements, add, mul
    elif hasattr(witness, 'elements') and hasattr(witness, 'add') and hasattr(witness, 'mul'):
        return witness.elements, witness.add, witness.mul
    elif isinstance(witness, (list, set, tuple)):
        elements = list(witness)
        add = lambda x, y: x + y
        mul = lambda x, y: x * y
        return elements, add, mul
    else:
        raise ValueError("Unknown witness format")

def conditions(witness) -> list[bool]:
    try:
        elements, add, mul = get_ops(witness)
        elements = list(elements)
        if not elements:
            return [False, False]
    except Exception:
        return [False, False]
    
    # H_1: R is a Boolean ring (non-associative ring with x^2 = x)
    h1 = False
    try:
        is_ring = True
        
        # Check closure
        for i in elements:
            for j in elements:
                if add(i, j) not in elements: is_ring = False
                if mul(i, j) not in elements: is_ring = False
        
        if is_ring:
            # Check abelian group for addition: Associativity
            for i in elements:
                for j in elements:
                    for k in elements:
                        if add(i, add(j, k)) != add(add(i, j), k):
                            is_ring = False
                            break
                    if not is_ring: break
                if not is_ring: break
        
        if is_ring:
            # Commutativity of addition
            for i in elements:
                for j in elements:
                    if add(i, j) != add(j, i):
                        is_ring = False
                        break
                if not is_ring: break

        if is_ring:
            # Identity of addition
            id_elem = None
            for e in elements:
                if all(add(e, x) == x for x in elements):
                    id_elem = e
                    break
            if id_elem is None:
                is_ring = False
            else:
                # Inverse of addition
                for x in elements:
                    if not any(add(x, y) == id_elem for y in elements):
                        is_ring = False
                        break

        if is_ring:
            # Distributivity of multiplication over addition
            for i in elements:
                for j in elements:
                    for k in elements:
                        if mul(i, add(j, k)) != add(mul(i, j), mul(i, k)):
                            is_ring = False
                            break
                        if mul(add(i, j), k) != add(mul(i, k), mul(j, k)):
                            is_ring = False
                            break
                    if not is_ring: break
                if not is_ring: break

        if is_ring:
            # Idempotency of multiplication (x^2 = x)
            for x in elements:
                if mul(x, x) != x:
                    is_ring = False
                    break
        
        h1 = is_ring
    except Exception:
        h1 = False

    # neg_Q: The left-multiplication operator L_a does NOT satisfy L_a o L_a = L_a for some a
    # i.e., there exists a, x in R such that a * (a * x) != a * x
    neg_q = False
    try:
        for a in elements:
            for x in elements:
                if mul(a, mul(a, x)) != mul(a, x):
                    neg_q = True
                    break
            if neg_q:
                break
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "¬Q: The left-multiplication operator L_a does not satisfy L_a o L_a = L_a for some a"
]

N_HYP = 1
NEG_Q_INDEX = 1