import sympy
from sympy.abc import x, y, z

# Top-level setup
# No specific named objects required for this general ring theory property.
# The witness is expected to define its own ring elements and membership test.

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample.
    The witness must be an object representing a ring and an infinite chain of elements.
    It should provide:
      - is_in_ring(expr) -> bool: checks if an expression belongs to the ring R
      - chain_element(n) -> expr: returns the generator a_n of the n-th principal ideal
    """
    try:
        is_in_ring = witness.is_in_ring
        chain_element = witness.chain_element
        
        neg_q = True
        # We check the first few elements to verify it forms a strictly ascending chain
        for n in range(6):
            a_n = chain_element(n)
            a_next = chain_element(n+1)
            
            # Both generators must be in the ring
            if not is_in_ring(a_n) or not is_in_ring(a_next):
                neg_q = False
                break
                
            # Check if <a_n> is a subset of <a_next>
            # This means a_n must be a multiple of a_next in the ring.
            q = sympy.simplify(a_n / a_next)
            if not is_in_ring(q):
                neg_q = False
                break
                
            # Check if the inclusion is strict: <a_n> != <a_next>
            # This means a_next is NOT a multiple of a_n in the ring.
            p = sympy.simplify(a_next / a_n)
            if is_in_ring(p):
                neg_q = False
                break
                
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: R contains a strictly ascending chain of principal ideals"
]

N_HYP = 0
NEG_Q_INDEX = 0