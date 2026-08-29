import sympy
from sympy.matrices import Matrix
from sympy import Integer

# Top-level setup
# (No specific named objects needed for this domain)

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 3:
            return [False]
        
        a, b, c = witness
        
        # Check if they are integers
        if not all(isinstance(x, (int, Integer)) for x in witness):
            return [False]
            
        # Any triple generated from (3, 4, 5) by Barning's matrices must be a Pythagorean triple.
        # If it's not, it cannot be generated.
        if a**2 + b**2 != c**2:
            return [True]
            
        v = Matrix(3, 1, [a, b, c])
        
        # Barning's three specific 3x3 unimodular matrices
        A = Matrix([[1, -2, 2], [2, -1, 2], [2, -2, 3]])
        B = Matrix([[1, 2, 2], [2, 1, 2], [2, 2, 3]])
        C = Matrix([[-1, 2, 2], [-2, 1, 2], [-2, 2, 3]])
        
        A_inv = A.inv()
        B_inv = B.inv()
        C_inv = C.inv()
        
        seen = set()
        can_gen = False
        
        # Backward search: if it can be generated, we can uniquely trace it back to (3, 4, 5)
        # by repeatedly applying the inverse matrix that yields a smaller positive triple.
        while True:
            tup = (v[0], v[1], v[2])
            if tup == (3, 4, 5):
                can_gen = True
                break
            if tup in seen:
                can_gen = False
                break
            seen.add(tup)
            
            next_v = None
            for M_inv in (A_inv, B_inv, C_inv):
                cand = M_inv * v
                # The correct parent in the tree of positive primitive Pythagorean triples
                # must have strictly positive entries and a strictly smaller hypotenuse.
                if cand[0] > 0 and cand[1] > 0 and cand[2] > 0 and cand[2] < v[2]:
                    next_v = cand
                    break
            
            if next_v is None:
                can_gen = False
                break
            v = next_v
            
        neg_q = not can_gen
        return [neg_q]
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: The triple cannot be generated from (3, 4, 5) by Barning's matrices"
]

N_HYP = 0
NEG_Q_INDEX = 0