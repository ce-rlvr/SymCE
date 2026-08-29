import sympy
from sympy import symbols, Rational, Integer
import itertools

# Top-level setup
x, y, z = symbols('x y z')
n = symbols('n', integer=True, positive=True)

def conditions(witness) -> list[bool]:
    H1, H2, neg_Q = False, False, False
    
    # 1. Callable representing d(n) or generator x_n**d_n
    if callable(witness):
        try:
            count = 0
            valid = True
            for i in range(1, 201):
                val = witness(i)
                deg = None
                if hasattr(val, 'is_Pow') and val.is_Pow:
                    deg = float(val.exp)
                elif hasattr(val, 'is_Symbol') and val.is_Symbol:
                    deg = 1.0
                else:
                    deg = float(val)
                    
                if deg < 1:
                    valid = False
                if deg >= 2 and deg < float('inf'):
                    count += 1
            if valid:
                H1 = True
                H2 = True
                if count >= 100:
                    neg_Q = True
        except Exception:
            pass

    # 2. Iterable representing d_n or generators x_n**d_n
    if not H1 and hasattr(witness, '__iter__') and not isinstance(witness, (str, dict)):
        try:
            count = 0
            valid = True
            for val in itertools.islice(witness, 200):
                deg = None
                if hasattr(val, 'is_Pow') and val.is_Pow:
                    deg = float(val.exp)
                elif hasattr(val, 'is_Symbol') and val.is_Symbol:
                    deg = 1.0
                else:
                    deg = float(val)
                    
                if deg < 1:
                    valid = False
                if deg >= 2 and deg < float('inf'):
                    count += 1
            if valid:
                H1 = True
                H2 = True
                if count >= 100:
                    neg_Q = True
        except Exception:
            pass

    # 3. SymPy expression
    if not H1 and hasattr(witness, 'free_symbols'):
        try:
            count = 0
            valid = True
            if len(witness.free_symbols) == 1:
                sym = list(witness.free_symbols)[0]
                for i in range(1, 201):
                    val = witness.subs(sym, i)
                    deg = None
                    if hasattr(val, 'is_Pow') and val.is_Pow:
                        deg = float(val.exp)
                    elif hasattr(val, 'is_Symbol') and val.is_Symbol:
                        deg = 1.0
                    else:
                        deg = float(val)
                        
                    if deg < 1:
                        valid = False
                    if deg >= 2 and deg < float('inf'):
                        count += 1
            elif len(witness.free_symbols) == 0:
                val = witness
                deg = None
                if hasattr(val, 'is_Pow') and val.is_Pow:
                    deg = float(val.exp)
                elif hasattr(val, 'is_Symbol') and val.is_Symbol:
                    deg = 1.0
                else:
                    deg = float(val)
                    
                if deg < 1:
                    valid = False
                if deg >= 2 and deg < float('inf'):
                    count = 200
            else:
                valid = False
                
            if valid:
                H1 = True
                H2 = True
                if count >= 100:
                    neg_Q = True
        except Exception:
            pass

    # 4. Dictionary
    if not H1 and isinstance(witness, dict):
        try:
            if witness.get('is_commutative_ring') and witness.get('is_ideal'):
                H1 = True
                H2 = True
                if 'radical_power_contained' in witness:
                    neg_Q = not bool(witness['radical_power_contained'])
                elif witness.get('is_counterexample'):
                    neg_Q = True
        except Exception:
            pass

    # 5. Object with attributes
    if not H1 and hasattr(witness, 'is_commutative_ring'):
        try:
            if getattr(witness, 'is_commutative_ring') and getattr(witness, 'is_ideal', False):
                H1 = True
                H2 = True
                if hasattr(witness, 'radical_power_contained'):
                    neg_Q = not bool(getattr(witness, 'radical_power_contained'))
                elif getattr(witness, 'is_counterexample', False):
                    neg_Q = True
        except Exception:
            pass

    # 6. Tuple (R, I)
    if not H1 and isinstance(witness, tuple) and len(witness) == 2:
        try:
            R, I = witness
            r_ok = False
            if hasattr(R, 'is_commutative_ring') and getattr(R, 'is_commutative_ring'):
                r_ok = True
            elif isinstance(R, dict) and R.get('is_commutative_ring'):
                r_ok = True
            elif hasattr(R, 'is_commutative') and getattr(R, 'is_commutative'):
                r_ok = True
                
            i_ok = False
            if hasattr(I, 'is_ideal') and getattr(I, 'is_ideal'):
                i_ok = True
            elif isinstance(I, dict) and I.get('is_ideal'):
                i_ok = True
            elif hasattr(I, 'ring'):
                i_ok = True
                
            if r_ok and i_ok:
                H1 = True
                H2 = True
                if hasattr(I, 'radical_power_contained'):
                    neg_Q = not bool(getattr(I, 'radical_power_contained'))
                elif isinstance(I, dict) and 'radical_power_contained' in I:
                    neg_Q = not bool(I['radical_power_contained'])
                elif hasattr(R, 'radical_power_contained'):
                    neg_Q = not bool(getattr(R, 'radical_power_contained'))
                elif isinstance(R, dict) and 'radical_power_contained' in R:
                    neg_Q = not bool(R['radical_power_contained'])
                elif getattr(I, 'is_counterexample', False) or getattr(R, 'is_counterexample', False):
                    neg_Q = True
        except Exception:
            pass

    # 7. String (fallback)
    if not H1 and isinstance(witness, str):
        try:
            s = witness.lower()
            if 'ring' in s and 'ideal' in s:
                H1 = True
                H2 = True
                if ('radical' in s or 'sqrt' in s) and ('not' in s or 'never' in s or 'no ' in s or 'unbounded' in s):
                    if 'infinit' in s or '...' in s or 'x_n' in s:
                        neg_Q = True
        except Exception:
            pass

    return [H1, H2, neg_Q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is an ideal of R",
    "¬Q: There is no positive integer k such that (\\sqrt{I})^k \\subseteq I"
]

N_HYP = 2
NEG_Q_INDEX = 2