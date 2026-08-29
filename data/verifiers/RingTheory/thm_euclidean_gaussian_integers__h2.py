import sympy
import math
import itertools
import functools

# Top-level setup
I = sympy.I

def conditions(witness):
    N = witness
    if isinstance(witness, tuple) and len(witness) > 0:
        N = witness[-1]
        
    h1 = True
    neg_q = False
    
    try:
        if not callable(N):
            h1 = False
        else:
            use_sympy = False
            try:
                val = N(complex(1, 1))
                _ = float(val)
            except Exception:
                try:
                    val = N(1 + I)
                    _ = float(val)
                    use_sympy = True
                except Exception:
                    h1 = False
            
            if h1:
                if use_sympy:
                    grid_ab = [sympy.Integer(x) + sympy.Integer(y)*I for x in range(-2, 3) for y in range(-2, 3)]
                    grid_q = [sympy.Integer(x) + sympy.Integer(y)*I for x in range(-15, 16) for y in range(-15, 16)]
                    test_elements = [
                        sympy.Integer(1), sympy.Integer(-1), I, -I,
                        1 + I, 1 - I, -1 + I, -1 - I,
                        sympy.Integer(2), 2*I
                    ]
                else:
                    grid_ab = [complex(x, y) for x in range(-2, 3) for y in range(-2, 3)]
                    grid_q = [complex(x, y) for x in range(-15, 16) for y in range(-15, 16)]
                    test_elements = [
                        complex(1, 0), complex(-1, 0), complex(0, 1), complex(0, -1),
                        complex(1, 1), complex(1, -1), complex(-1, 1), complex(-1, -1),
                        complex(2, 0), complex(0, 2)
                    ]
                
                for x in test_elements:
                    try:
                        val = N(x)
                        if float(val) < 0:
                            neg_q = True
                            break
                    except Exception:
                        h1 = False
                        break
                
                if h1 and not neg_q:
                    for a in grid_ab:
                        for b in grid_ab:
                            if b == 0:
                                continue
                            
                            try:
                                nb = float(N(b))
                            except Exception:
                                continue
                                
                            any_q_works = False
                            for q in grid_q:
                                r = a - b * q
                                if r == 0:
                                    any_q_works = True
                                    break
                                try:
                                    nr = float(N(r))
                                    if nr < nb:
                                        any_q_works = True
                                        break
                                except Exception:
                                    pass
                            
                            if not any_q_works:
                                neg_q = True
                                break
                        if neg_q:
                            break
    except Exception:
        h1 = False
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Let R be the ring of Gaussian integers",
    "¬Q: R is not a Euclidean domain with Euclidean function N"
]

N_HYP = 1
NEG_Q_INDEX = 1