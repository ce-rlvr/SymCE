import sympy as sp

# Top-level setup: named object bindings that the witness expression may reference
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness satisfies the hypotheses and fails the conclusion.
    The conjecture states: The annihilator of the union is equal to the intersection of their individual annihilators.
    """
    try:
        n = None
        
        # Handle dictionary or tuple wrappers
        if isinstance(witness, dict):
            if 'V_dim' in witness:
                n = witness['V_dim']
            if 'subsets' in witness:
                witness = witness['subsets']
            elif 'S' in witness:
                witness = witness['S']
            else:
                return [False, False]
                
        if isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[0], int):
            n, witness = witness
            
        if not isinstance(witness, (list, tuple, set)):
            return [False, False]
            
        parsed_witness = []
        for subset in witness:
            if isinstance(subset, sp.Matrix):
                if n is None:
                    n = subset.cols
                elif subset.cols != n:
                    return [False, False]
                parsed_witness.append(subset.tolist())
            elif isinstance(subset, (list, tuple, set)):
                parsed_subset = []
                for vec in subset:
                    if isinstance(vec, sp.Matrix):
                        vec = list(vec)
                    if not isinstance(vec, (list, tuple)):
                        return [False, False]
                    if n is None:
                        n = len(vec)
                    elif len(vec) != n:
                        return [False, False]
                    parsed_subset.append(list(vec))
                parsed_witness.append(parsed_subset)
            else:
                return [False, False]
                
        if n is None:
            n = 1
            
        h1 = True
    except Exception:
        return [False, False]
        
    try:
        # Compute the annihilator of the union
        union_vecs = []
        for subset in parsed_witness:
            union_vecs.extend(subset)
            
        if not union_vecs:
            union_matrix = sp.zeros(1, n)
        else:
            union_matrix = sp.Matrix(union_vecs)
            
        union_annihilator_basis = union_matrix.nullspace()
        
        # Compute the intersection of the individual annihilators
        if not parsed_witness:
            intersection_basis = sp.eye(n).columnspace()
        else:
            intersection_basis = sp.eye(n).columnspace()
            for subset in parsed_witness:
                if not subset:
                    M_i = sp.zeros(1, n)
                else:
                    M_i = sp.Matrix(subset)
                
                if not intersection_basis:
                    break
                    
                B = sp.Matrix.hstack(*intersection_basis)
                M_int = M_i * B
                c_basis = M_int.nullspace()
                
                new_basis = []
                for c in c_basis:
                    new_basis.append(B * c)
                intersection_basis = new_basis
                
        # Compare the two subspaces
        dim1 = len(union_annihilator_basis)
        dim2 = len(intersection_basis)
        
        if dim1 != dim2:
            neg_q = True
        else:
            if dim1 == 0:
                neg_q = False
            else:
                B1 = sp.Matrix.hstack(*union_annihilator_basis)
                B2 = sp.Matrix.hstack(*intersection_basis)
                rank2 = B2.rank()
                rank_both = sp.Matrix.hstack(B2, B1).rank()
                neg_q = (rank2 != rank_both)
                
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Let V be a vector space over a field F",
    "¬Q: The annihilator of the union is NOT equal to the intersection of their individual annihilators"
]

N_HYP = 1
NEG_Q_INDEX = 1