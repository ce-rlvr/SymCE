import sympy
from sympy import S, Matrix, eye, zeros
from sympy.matrices.normalforms import smith_normal_form

# Top-level setup for potential witness expressions
Z = sympy.Symbol('Z')
Integers = S.Integers

def conditions(witness):
    """
    Checks if the witness is a counterexample to the false conjecture:
    "If R is a PID and M is a finitely generated module over R, 
    then Ann(M) is a non-zero principal ideal in R."
    
    A valid counterexample is a finitely generated module that is NOT torsion 
    (e.g., has a free component), so its annihilator is the zero ideal, 
    which is not a *non-zero* principal ideal.
    """
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        # Unwrap tuple or dict representations (e.g., (R, M) or {'R': Z, 'M': [0]})
        if isinstance(witness, tuple) and len(witness) == 2:
            _, witness = witness
        if isinstance(witness, dict) and 'M' in witness:
            witness = witness['M']

        # Representation 1: List of invariant factors (integers) for a module over Z
        if isinstance(witness, list) and all(isinstance(x, (int, sympy.Integer)) for x in witness):
            h1 = True  # Z is a PID
            h2 = True  # Finite list of cyclic modules is finitely generated
            if len(witness) == 0:
                neg_q = False
            elif any(x == 0 for x in witness):
                # A free component exists, so Ann(M) = {0}, which is not a non-zero principal ideal
                neg_q = True
            else:
                neg_q = False

        # Representation 2: Presentation matrix for a module over Z
        elif isinstance(witness, sympy.Matrix):
            h1 = True
            h2 = True
            m, n = witness.shape
            if m < n:
                # Fewer relations than generators implies a free component
                neg_q = True
            else:
                snf = smith_normal_form(witness)
                has_zero = False
                for i in range(n):
                    if snf[i, i] == 0:
                        has_zero = True
                        break
                neg_q = has_zero

        # Representation 3: The free module Z itself
        elif witness == Z or witness == Integers or str(witness) in ('Z', 'Integers'):
            h1 = True
            h2 = True
            neg_q = True

    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: M is a finitely generated module over R",
    "¬Q: Ann(M) is not a non-zero principal ideal in R"
]

N_HYP = 2
NEG_Q_INDEX = 2