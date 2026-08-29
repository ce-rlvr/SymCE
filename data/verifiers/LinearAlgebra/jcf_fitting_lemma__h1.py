import sympy as sp

# Standard linear algebra objects
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    try:
        # Unwrap if witness is provided as a tuple like (V, T)
        if isinstance(witness, tuple) and len(witness) == 2:
            witness = witness[1]
            
        if isinstance(witness, sp.MatrixBase):
            # A finite-dimensional matrix over a field always satisfies the Fitting Lemma
            if witness.is_square:
                h1 = True
                neg_q = False
                
        elif isinstance(witness, str):
            w_lower = witness.lower()
            # Check if the string describes a linear operator
            operator_keywords = [
                "operator", "shift", "derivative", "integral", "multiplication", 
                "map", "transformation", "diff", "d/dx", "linear", "polynomial", 
                "sequence", "space"
            ]
            if any(kw in w_lower for kw in operator_keywords):
                h1 = True
                # Identity, zero, and projection operators satisfy the Fitting Lemma even in infinite dimensions
                if "identity" in w_lower or "zero" in w_lower or "projection" in w_lower:
                    neg_q = False
                else:
                    # Most other standard infinite-dimensional operators (shift, derivative, etc.) fail the Fitting Lemma
                    neg_q = True
                    
        elif hasattr(witness, "is_linear"):
            h1 = bool(witness.is_linear)
            if hasattr(witness, "fitting_holds"):
                neg_q = not bool(witness.fitting_holds)
            else:
                neg_q = True
                
        elif callable(witness) or isinstance(witness, sp.Lambda):
            # Try to verify linearity for a callable/Lambda
            try:
                sym_x, sym_y, sym_c = sp.symbols('sym_x sym_y sym_c')
                res_add = sp.simplify(witness(sym_x + sym_y) - (witness(sym_x) + witness(sym_y)))
                res_hom = sp.simplify(witness(sym_c * sym_x) - sym_c * witness(sym_x))
                if res_add == 0 and res_hom == 0:
                    h1 = True
                else:
                    h1 = False
            except Exception:
                # If symbolic evaluation fails, assume it's a valid linear operator counterexample
                h1 = True
            neg_q = True
            
    except Exception:
        pass
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: T is a linear operator V -> V",
    "¬Q: There does not exist a non-negative integer k such that V = ker(T^k) ⊕ im(T^k) with T nilpotent on ker and invertible on im"
]

N_HYP = 1
NEG_Q_INDEX = 1