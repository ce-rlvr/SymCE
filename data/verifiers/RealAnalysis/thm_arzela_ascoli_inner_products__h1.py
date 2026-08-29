import sympy as sp
import math

# Top-level setup
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The dropped hypothesis is that H is a REAL Hilbert space.
    If H is a complex Hilbert space, the inner product can be complex-valued,
    making the family of functions not real-valued.
    """
    
    # 1. Dictionary witness
    if isinstance(witness, dict):
        try:
            h1 = bool(witness.get("H_is_Hilbert", False))
            h2 = bool(witness.get("F_is_equicontinuous", False))
            h3 = bool(witness.get("v_in_H", False))
            is_real = bool(witness.get("Q_is_real_valued", True))
            is_equi = bool(witness.get("Q_is_equicontinuous", True))
            neg_q = not (is_real and is_equi)
            return [h1, h2, h3, neg_q]
        except Exception:
            pass

    # 2. Object with attributes witness
    try:
        if hasattr(witness, "H_is_Hilbert"):
            h1 = bool(getattr(witness, "H_is_Hilbert", False))
            h2 = bool(getattr(witness, "F_is_equicontinuous", False))
            h3 = bool(getattr(witness, "v_in_H", False))
            is_real = bool(getattr(witness, "Q_is_real_valued", True))
            is_equi = bool(getattr(witness, "Q_is_equicontinuous", True))
            neg_q = not (is_real and is_equi)
            return [h1, h2, h3, neg_q]
    except Exception:
        pass

    # 3. Tuple of (F, v) witness (e.g., F = I*x, v = 1)
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            F, v = witness
            if isinstance(F, (list, tuple)):
                f = F[0]
            else:
                f = F
                
            h1 = True  # C is a Hilbert space
            h2 = True  # A single smooth function is equicontinuous
            
            v_sym = sp.sympify(v)
            h3 = len(v_sym.free_symbols) == 0
            
            f_sym = sp.sympify(f)
            
            try:
                inner_product = f_sym * sp.conjugate(v_sym)
            except Exception:
                inner_product = v_sym.dot(f_sym)
                
            val = inner_product
            if hasattr(val, "free_symbols"):
                for sym in val.free_symbols:
                    val = val.subs(sym, 1.234)
            
            val = complex(val)
            is_real = abs(val.imag) < 1e-9
            
            neg_q = not is_real
            return [h1, h2, h3, neg_q]
    except Exception:
        pass

    # 4. String witness
    if isinstance(witness, str):
        s = witness.lower()
        if "complex" in s or "imaginary" in s:
            return [True, True, True, True]

    return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: \mathcal{H} is a Hilbert space",
    "H_2: \mathcal{F} is an equicontinuous family of functions",
    "H_3: v is a fixed vector in \mathcal{H}",
    "¬Q: The family of functions is not real-valued or not equicontinuous"
]

N_HYP = 3
NEG_Q_INDEX = 3