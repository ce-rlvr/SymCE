import sympy
from sympy import symbols, S

# Top-level setup
x, y, z = symbols('x y z')
ZZ = S.Integers
QQ = S.Rationals

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            P_gen = witness.get('P', witness.get('P_gen'))
            Q_chain = witness.get('Q_chain', witness.get('chain'))
        elif isinstance(witness, tuple) or isinstance(witness, list):
            if len(witness) == 2:
                P_gen, Q_chain = witness
            elif len(witness) == 3:
                _, P_gen, Q_chain = witness
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
            
        if P_gen is None or Q_chain is None:
            return [False, False, False, False]
            
        Q_chain = list(Q_chain)
            
        # H1: R is a commutative ring
        h1 = True
        
        # Check if elements are integers
        try:
            is_int = isinstance(P_gen, (int, sympy.Integer)) and all(isinstance(q, (int, sympy.Integer)) for q in Q_chain)
        except Exception:
            is_int = False
            
        if is_int:
            P_gen = abs(int(P_gen))
            Q_chain = [abs(int(q)) for q in Q_chain]
            
            h2 = (P_gen == 0) or sympy.isprime(P_gen)
            
            h3 = True
            if len(Q_chain) == 0:
                h3 = False
            else:
                for i in range(len(Q_chain) - 1):
                    if Q_chain[i+1] == 0:
                        if Q_chain[i] != 0:
                            h3 = False
                            break
                    elif Q_chain[i] % Q_chain[i+1] != 0:
                        h3 = False
                        break
                        
            if not h3 or len(Q_chain) == 0:
                U_gen = 1
            else:
                U_gen = Q_chain[-1]
                
            if P_gen == 0:
                is_P_primary = (U_gen == 0)
            else:
                if U_gen == 0:
                    is_P_primary = False
                else:
                    factors = sympy.factorint(U_gen)
                    is_P_primary = (list(factors.keys()) == [P_gen])
                    
        else:
            # Polynomials
            P_gen = sympy.sympify(P_gen)
            Q_chain = [sympy.sympify(q) for q in Q_chain]
            
            if P_gen == 0:
                h2 = True
            else:
                factors = sympy.factor_list(P_gen)
                h2 = (len(factors[1]) == 1 and factors[1][0][1] == 1)
                
            h3 = True
            if len(Q_chain) == 0:
                h3 = False
            else:
                for i in range(len(Q_chain) - 1):
                    if Q_chain[i+1] == 0:
                        if Q_chain[i] != 0:
                            h3 = False
                            break
                    else:
                        ratio = sympy.cancel(Q_chain[i] / Q_chain[i+1])
                        if len(ratio.as_numer_denom()[1].free_symbols) > 0:
                            h3 = False
                            break
                            
            if not h3 or len(Q_chain) == 0:
                U_gen = sympy.S.One
            else:
                U_gen = Q_chain[-1]
                
            if P_gen == 0:
                is_P_primary = (U_gen == 0)
            else:
                if U_gen == 0:
                    is_P_primary = False
                else:
                    factors = sympy.factor_list(U_gen)
                    if len(factors[1]) == 1:
                        factor = factors[1][0][0]
                        q = sympy.cancel(factor / P_gen)
                        if len(q.free_symbols) == 0 and q != 0:
                            is_P_primary = True
                        else:
                            is_P_primary = False
                    else:
                        is_P_primary = False
                        
        neg_q = not is_P_primary
        
        return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: P is a prime ideal in R",
    "H_3: Q_1 \\subseteq Q_2 \\subseteq \\dots is an ascending chain of ideals in R",
    "¬Q: The union of Q_i is not a P-primary ideal"
]

N_HYP = 3
NEG_Q_INDEX = 3