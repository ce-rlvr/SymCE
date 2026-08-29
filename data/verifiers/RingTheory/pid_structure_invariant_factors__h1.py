import sympy
from sympy import Matrix, groebner
import itertools

# Top-level setup
x, y, z = sympy.symbols('x y z')

def conditions(witness) -> list[bool]:
    try:
        h1 = False
        neg_q = False
        
        # Extract witness from dictionary if necessary
        if isinstance(witness, dict):
            if 'matrix' in witness:
                witness = witness['matrix']
            elif 'ideal_gens' in witness:
                witness = witness['ideal_gens']
            elif 'gens' in witness:
                witness = witness['gens']
                
        # Wrap single expressions in a list
        if hasattr(witness, 'free_symbols') and not isinstance(witness, Matrix):
            witness = [witness]
            
        # Convert list of lists to Matrix
        if isinstance(witness, (list, tuple)) and len(witness) > 0 and isinstance(witness[0], (list, tuple)):
            try:
                witness = Matrix(witness)
            except Exception:
                pass
                
        if isinstance(witness, Matrix):
            h1 = True
            n = witness.cols
            m = witness.rows
            
            # Prevent excessively large matrices from hanging the verifier
            if n > 6 or m > 6:
                return [False, False]
            
            free_symbols = set()
            for element in witness:
                if hasattr(element, 'free_symbols'):
                    free_symbols.update(element.free_symbols)
                
            if not free_symbols:
                # Over a field or Z (PIDs), the theorem holds, so negated conclusion is False
                return [h1, False]
                
            vars_list = list(free_symbols)
            
            # Check Fitting ideals. If any Fitting ideal is not principal, 
            # the module cannot be decomposed into invariant factors.
            for i in range(n):
                k = n - i
                if k > m or k <= 0:
                    continue
                
                row_indices = list(itertools.combinations(range(m), k))
                col_indices = list(itertools.combinations(range(n), k))
                minors = []
                for r_idx in row_indices:
                    for c_idx in col_indices:
                        sub_matrix = witness.extract(r_idx, c_idx)
                        minors.append(sub_matrix.det())
                
                minors = [m_val for m_val in minors if m_val != 0]
                if not minors:
                    continue
                    
                # An ideal is principal iff its reduced Groebner basis has size <= 1
                gb = groebner(minors, *vars_list)
                if len(list(gb)) > 1:
                    neg_q = True
                    break
            return [h1, neg_q]
            
        elif isinstance(witness, (list, tuple)):
            # Treat as a list of generators for an ideal
            if len(witness) > 0 and hasattr(witness[0], 'free_symbols'):
                h1 = True
                free_symbols = set()
                for e in witness:
                    if hasattr(e, 'free_symbols'):
                        free_symbols.update(e.free_symbols)
                
                if not free_symbols:
                    return [h1, False]
                    
                vars_list = list(free_symbols)
                gens = [e for e in witness if e != 0]
                if not gens:
                    return [h1, False]
                    
                # An ideal is isomorphic to R^r + ... iff it is principal
                gb = groebner(gens, *vars_list)
                if len(list(gb)) > 1:
                    neg_q = True
                else:
                    neg_q = False
                return [h1, neg_q]
                
    except Exception:
        pass
        
    return [False, False]

CONDITION_LABELS = [
    "H_1: M is a finitely generated R-module",
    "¬Q: M is not isomorphic to a direct sum of cyclic modules with invariant factors"
]
N_HYP = 1
NEG_Q_INDEX = 1