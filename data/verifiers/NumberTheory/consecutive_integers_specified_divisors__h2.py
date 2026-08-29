import sympy

def conditions(witness):
    try:
        if isinstance(witness, dict):
            if 'p' in witness and 'e' in witness:
                ps = witness['p']
                es = witness['e']
                if len(ps) == len(es):
                    witness = list(zip(ps, es))
                else:
                    return [False, False]
            else:
                return [False, False]
                
        if not isinstance(witness, (list, tuple)):
            return [False, False]
            
        if len(witness) > 0 and all(isinstance(x, (int, sympy.Integer)) for x in witness):
            h1 = True
            for p in witness:
                if not sympy.isprime(p):
                    h1 = False
            if len(set(witness)) != len(witness):
                h1 = False
            return [h1, True]
            
        h1 = True
        primes = []
        for item in witness:
            if not isinstance(item, (list, tuple)) or len(item) != 2:
                h1 = False
                break
            p, e = item
            if not sympy.isprime(p):
                h1 = False
            primes.append(p)
            
        if h1 and len(set(primes)) != len(primes):
            h1 = False
            
        q_holds = True
        for i, item in enumerate(witness):
            if not h1:
                break
            p, e = item
            if isinstance(e, float) and e.is_integer():
                e = int(e)
            if not isinstance(e, (int, sympy.Integer)):
                q_holds = False
                break
            if e < 0:
                q_holds = False
                break
                
        neg_q = not q_holds
        
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: p_1, ..., p_k are distinct prime numbers",
    "¬Q: There does not exist a positive integer x such that x + i is divisible by p_i^{e_i} for all 1 <= i <= k"
]
N_HYP = 1
NEG_Q_INDEX = 1