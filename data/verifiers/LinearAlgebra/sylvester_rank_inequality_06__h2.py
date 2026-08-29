import sympy as sp

# Top-level setup
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    Sylvester's rank inequality is unconditionally true for finite-dimensional vector spaces.
    The dropped hypothesis is that V is finite-dimensional. Thus, a valid counterexample
    must involve infinite-dimensional spaces where the arithmetic of ranks becomes undefined.
    
    The witness can be provided as:
      - A tuple of two sympy Matrices (S, T) [will always fail to be a counterexample]
      - A dictionary with keys 'rank_S', 'rank_T', 'rank_ST', 'dim_V'
      - A tuple of 4 values: (rank_S, rank_T, rank_ST, dim_V)
    """
    try:
        def is_valid(x):
            return x == sp.oo or (isinstance(x, (int, sp.Integer)) and x >= 0)

        # Parse witness
        if isinstance(witness, tuple) and len(witness) == 2 and hasattr(witness[0], 'rank'):
            S, T = witness
            rank_S = S.rank()
            rank_T = T.rank()
            rank_ST = (S * T).rank()
            dim_V = S.cols
            
            H1 = True
            H2 = True
            H3 = (S.cols == T.rows)
            
        elif isinstance(witness, dict):
            rank_S = witness.get('rank_S')
            rank_T = witness.get('rank_T')
            rank_ST = witness.get('rank_ST')
            dim_V = witness.get('dim_V')
            
            H1 = is_valid(dim_V)
            H2 = is_valid(rank_T)
            H3_a = is_valid(rank_S) and is_valid(rank_ST)
            H3_b = bool(rank_ST <= rank_S) and bool(rank_ST <= rank_T) if H3_a else False
            if dim_V != sp.oo and rank_S != sp.oo and rank_T != sp.oo:
                H3_c = bool(rank_ST >= rank_S + rank_T - dim_V)
            else:
                H3_c = True
            H3 = H3_a and H3_b and H3_c
            
        else:
            rank_S, rank_T, rank_ST, dim_V = witness
            
            H1 = is_valid(dim_V)
            H2 = is_valid(rank_T)
            H3_a = is_valid(rank_S) and is_valid(rank_ST)
            H3_b = bool(rank_ST <= rank_S) and bool(rank_ST <= rank_T) if H3_a else False
            # Enforce necessary existence conditions for finite-dimensional linear transformations
            if dim_V != sp.oo and rank_S != sp.oo and rank_T != sp.oo:
                H3_c = bool(rank_ST >= rank_S + rank_T - dim_V)
            else:
                H3_c = True
            H3 = H3_a and H3_b and H3_c

        # Evaluate the conclusion: rank(S ∘ T) >= rank(S) + rank(T) - dim(V)
        rhs = rank_S + rank_T - dim_V
        
        # If rhs evaluates to nan (e.g., oo + oo - oo), the inequality is undefined and thus fails.
        if rhs is sp.nan:
            neg_Q = True
        else:
            neg_Q = not bool(rank_ST >= rhs)

        return [bool(H1), bool(H2), bool(H3), bool(neg_Q)]
    
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: U, V, and W are vector spaces over a field F",
    "H_2: T: U -> V is a linear transformation",
    "H_3: S: V -> W is a linear transformation",
    "¬Q: rank(S ∘ T) < rank(S) + rank(T) - dim(V) or is undefined"
]

N_HYP = 3
NEG_Q_INDEX = 3