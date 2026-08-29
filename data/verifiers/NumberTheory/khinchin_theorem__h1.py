import sympy as sp
import math

# Top-level setup for potential witness expressions
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def get_sequence(witness, max_terms=1000):
    # Way A: Function taking index n
    try:
        t = witness(1)
        try:
            ft = float(t)
            return [witness(n) for n in range(1, max_terms + 1)]
        except Exception:
            pass
    except Exception:
        pass
        
    # Way B: Generator function
    try:
        it = iter(witness())
        res = []
        for _ in range(max_terms):
            res.append(next(it))
        return res
    except Exception:
        pass
        
    # Way C: Iterable (list, tuple, generator object)
    try:
        it = iter(witness)
        res = []
        for _ in range(max_terms):
            res.append(next(it))
        return res
    except Exception:
        pass
        
    # Way D: A number (compute continued fraction)
    try:
        it = sp.continued_fraction_iterator(witness)
        res = []
        a0 = next(it) # skip a0 (integer part)
        for _ in range(max_terms):
            res.append(next(it))
        return res
    except Exception:
        pass
        
    return []

def conditions(witness):
    try:
        terms = get_sequence(witness, max_terms=1000)
        
        if not terms:
            return [False]
            
        float_terms = []
        for t in terms:
            try:
                ft = float(t)
            except OverflowError:
                return [True]
            except Exception:
                return [False]
                
            if ft <= 0:
                return [True]
            float_terms.append(ft)
            
        if len(float_terms) < 50:
            # Finite sequence, limit doesn't exist
            return [True]
            
        K0 = 2.685452001065306
        
        # Check for periodicity
        n = len(float_terms)
        tail = float_terms[n // 2:]
        max_p = len(tail) // 2
        exact_limit = None
        
        for p in range(1, max_p + 1):
            is_periodic = True
            for i in range(len(tail) - p):
                if abs(tail[i] - tail[i+p]) > 1e-9:
                    is_periodic = False
                    break
            if is_periodic:
                period_terms = tail[:p]
                log_sum = sum(math.log(t) for t in period_terms)
                try:
                    exact_limit = math.exp(log_sum / p)
                except OverflowError:
                    return [True]
                break
                
        if exact_limit is not None:
            if abs(exact_limit - K0) > 1e-3:
                return [True]
            else:
                return [False]
        else:
            # Not periodic. Check geometric mean of all terms.
            log_sum = sum(math.log(t) for t in float_terms)
            try:
                geom_mean = math.exp(log_sum / len(float_terms))
            except OverflowError:
                return [True]
            
            if abs(geom_mean - K0) > 0.1:
                return [True]
            else:
                return [False]
                
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: The limit of the geometric mean of the sequence does not equal Khinchin's constant"
]
N_HYP = 0
NEG_Q_INDEX = 0