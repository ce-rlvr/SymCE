import sympy
import itertools
from sympy import Symbol, Expr
from sympy.polys.domains import QQ, ZZ

# Top-level setup
# (No specific named bindings required for this ring theory conjecture,
# but QQ and ZZ are provided for convenience)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "Let S be a non-empty set of ideals of R. Then S contains a maximal element."
    
    A valid counterexample is an infinite strictly ascending chain of ideals
    in a non-Noetherian ring (e.g., k[x_1, x_2, ...]).
    """
    h1 = False
    neg_q = False
    try:
        # Check if the witness is a finite collection
        is_finite = False
        if hasattr(witness, '__len__'):
            try:
                if witness.__len__() != sympy.oo:
                    is_finite = True
            except Exception:
                is_finite = True
                
        # The witness should be a callable or an iterator yielding ideals
        if callable(witness):
            def get_ideal(n): return witness(n)
            start_idx = 1
            try:
                # Test if it's 1-indexed
                _ = get_ideal(1)
            except Exception:
                start_idx = 0
        elif hasattr(witness, '__iter__'):
            iterator = iter(witness)
            def get_ideal(n): return next(iterator)
            start_idx = 0
        else:
            return [False, False]
            
        # Extract the first 20 ideals to verify the ascending chain property
        ideals = []
        for i in range(20):
            try:
                val = get_ideal(start_idx + i)
                if hasattr(val, 'gens'):
                    ideals.append(list(val.gens))
                else:
                    ideals.append(list(val))
            except StopIteration:
                break
            except Exception:
                break
                
        # H_1: S is a non-empty set of ideals of R
        if len(ideals) > 0:
            all_valid = True
            for I in ideals:
                if not isinstance(I, (list, tuple, set)):
                    all_valid = False
                    break
                for elem in I:
                    mod = type(elem).__module__
                    # Elements should be SymPy objects or strings representing variables
                    if not (mod and mod.startswith('sympy') or isinstance(elem, str)):
                        all_valid = False
                        break
            if all_valid:
                h1 = True
            
        # ¬Q: S does not contain a maximal element
        # We verify this by checking if the first 20 ideals form a strictly ascending chain
        # with independent generators (which guarantees strict inclusion in free rings).
        if h1 and len(ideals) == 20 and not is_finite:
            is_strictly_ascending = True
            for i in range(19):
                I_n = set(ideals[i])
                I_n1 = set(ideals[i+1])
                
                if not I_n.issubset(I_n1):
                    is_strictly_ascending = False
                    break
                if I_n == I_n1:
                    is_strictly_ascending = False
                    break
                    
                new_elements = I_n1 - I_n
                for elem in new_elements:
                    if isinstance(elem, Symbol):
                        continue
                    s = str(elem)
                    if not s:
                        is_strictly_ascending = False
                        break
                    # Ensure the new generator is a simple variable (e.g., 'x_3'), 
                    # not a composite expression (e.g., 'x**2' or '2*x')
                    if not (s[0].isalpha() or s[0] == '_'):
                        is_strictly_ascending = False
                        break
                    valid_var = True
                    for char in s[1:]:
                        if not (char.isalnum() or char == '_'):
                            valid_var = False
                            break
                    if not valid_var:
                        is_strictly_ascending = False
                        break
                        
                if not is_strictly_ascending:
                    break
                    
            if is_strictly_ascending:
                neg_q = True
                
    except Exception:
        pass
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: S is a non-empty set of ideals of R",
    "¬Q: S does not contain a maximal element"
]

N_HYP = 1
NEG_Q_INDEX = 1