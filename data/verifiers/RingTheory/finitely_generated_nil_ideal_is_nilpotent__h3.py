import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z

# Top-level setup
# (No additional bindings needed beyond ZZ, QQ, x, y, z)

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        # Case 1: witness is an integer or SymPy Integer (assume R = ZZ, I = (witness))
        if isinstance(witness, int) or (hasattr(witness, 'is_Integer') and witness.is_Integer):
            h1 = True
            h2 = True
            neg_q = (witness != 0)
            return [h1, h2, neg_q]
            
        # Case 2: witness is a Symbol (assume R = ZZ[witness], I = (witness))
        if hasattr(witness, 'is_Symbol') and witness.is_Symbol:
            h1 = True
            h2 = True
            neg_q = True
            return [h1, h2, neg_q]
            
        # Case 3: witness is a list or tuple of integers (assume R = ZZ, I = (witness))
        if isinstance(witness, (list, tuple)) and all(isinstance(g, int) or (hasattr(g, 'is_Integer') and g.is_Integer) for g in witness):
            h1 = True
            h2 = True
            is_nilpotent = all(g == 0 for g in witness)
            neg_q = not is_nilpotent
            return [h1, h2, neg_q]
            
        # Case 4: witness is a tuple (R, I) or (R, gens)
        if isinstance(witness, tuple) and len(witness) == 2:
            R, I = witness
            
            # Check H1
            if hasattr(R, 'is_commutative'):
                h1 = bool(R.is_commutative)
            elif R in [sympy.ZZ, sympy.QQ, sympy.RR, sympy.CC]:
                h1 = True
            else:
                h1 = False
                
            # Check H2
            gens = []
            if hasattr(I, 'gens'):
                gens = list(I.gens)
                h2 = True
            elif isinstance(I, (list, tuple, set)):
                gens = list(I)
                h2 = True
            else:
                gens = [I]
                h2 = True
                
            # Check neg_Q
            if h1 and h2:
                is_nilpotent = True
                for g in gens:
                    g_is_nil = False
                    for n in range(1, 20):
                        try:
                            val = g**n
                            if val == 0:
                                g_is_nil = True
                                break
                            if hasattr(val, 'is_zero') and val.is_zero:
                                g_is_nil = True
                                break
                            if hasattr(R, 'zero') and val == R.zero:
                                g_is_nil = True
                                break
                            if hasattr(R, 'reduce') and R.reduce(val) == 0:
                                g_is_nil = True
                                break
                        except Exception:
                            pass
                    if not g_is_nil:
                        is_nilpotent = False
                        break
                neg_q = not is_nilpotent
                
            return [h1, h2, neg_q]
            
        # Case 5: witness is a SymPy Ideal object
        if hasattr(witness, 'ring') and hasattr(witness, 'gens'):
            R = witness.ring
            if hasattr(R, 'is_commutative'):
                h1 = bool(R.is_commutative)
            else:
                h1 = True
                
            h2 = True
            
            is_nilpotent = True
            for g in witness.gens:
                g_is_nil = False
                for n in range(1, 20):
                    try:
                        val = g**n
                        if val == 0:
                            g_is_nil = True
                            break
                        if hasattr(val, 'is_zero') and val.is_zero:
                            g_is_nil = True
                            break
                        if hasattr(R, 'zero') and val == R.zero:
                            g_is_nil = True
                            break
                        if hasattr(R, 'reduce') and R.reduce(val) == 0:
                            g_is_nil = True
                            break
                    except Exception:
                        pass
                if not g_is_nil:
                    is_nilpotent = False
                    break
            neg_q = not is_nilpotent
            
            return [h1, h2, neg_q]
            
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is a finitely generated ideal of R",
    "¬Q: I is not nilpotent (I^n != 0 for all n > 0)"
]

N_HYP = 2
NEG_Q_INDEX = 2