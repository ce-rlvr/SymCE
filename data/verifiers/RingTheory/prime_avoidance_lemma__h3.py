import sympy
import math

ZZ = sympy.ZZ
QQ = sympy.QQ

def is_ideal(n, P):
    if not P: return False
    P_set = {int(x) % n for x in P}
    for a in P_set:
        for b in P_set:
            if (a - b) % n not in P_set:
                return False
    for a in P_set:
        for r in range(n):
            if (a * r) % n not in P_set:
                return False
    return True

def is_prime_ideal(n, P):
    if not is_ideal(n, P): return False
    P_set = {int(x) % n for x in P}
    if len(P_set) == n: return False
    for a in range(n):
        for b in range(n):
            if (a * b) % n in P_set:
                if a not in P_set and b not in P_set:
                    return False
    return True

def parse_witness(witness):
    R, P_list, I_list = None, None, None
    try:
        if isinstance(witness, dict):
            R = witness.get('R', witness.get('n', None))
            P_list = witness.get('P_list', witness.get('P', witness.get('ideals', None)))
            I_list = witness.get('I_list', witness.get('I', witness.get('subset', None)))
        elif isinstance(witness, (tuple, list)) and len(witness) >= 3:
            R = witness[0]
            P_list = witness[1]
            I_list = witness[2]
    except Exception:
        pass

    if isinstance(I_list, int) or (hasattr(I_list, 'is_Integer') and I_list.is_Integer):
        I_list = [I_list]

    ring_type = None
    n = None

    try:
        if str(R) in ['ZZ', 'Z', 'Integers', 'S.Integers', 'Ring of Integers']:
            ring_type = 'ZZ'
        else:
            if isinstance(R, int):
                n = R
                ring_type = 'ZnZ'
            elif hasattr(R, 'is_Integer') and R.is_Integer:
                n = int(R)
                ring_type = 'ZnZ'
            elif isinstance(R, (set, list, tuple)):
                n = len(R)
                ring_type = 'ZnZ'
            else:
                try:
                    n = int(R)
                    ring_type = 'ZnZ'
                except Exception:
                    pass
    except Exception:
        pass

    return ring_type, n, P_list, I_list

def conditions(witness) -> list[bool]:
    ring_type, n, P_list, I_list = parse_witness(witness)
    
    if ring_type is None or P_list is None or I_list is None:
        return [False, False, False, False]

    if ring_type == 'ZZ':
        h1 = True
        
        try:
            parsed_P_list = []
            for P in P_list:
                if isinstance(P, (list, tuple, set)):
                    if len(P) == 1:
                        parsed_P_list.append(int(list(P)[0]))
                    else:
                        g = 0
                        for x in P:
                            g = math.gcd(g, int(x))
                        parsed_P_list.append(g)
                else:
                    parsed_P_list.append(int(P))
        except Exception:
            return [False, False, False, False]
            
        try:
            not_prime_count = 0
            for k in parsed_P_list:
                k = abs(k)
                if k != 0 and not sympy.isprime(k):
                    not_prime_count += 1
            h2 = (not_prime_count <= 2) and len(parsed_P_list) >= 1
        except Exception:
            h2 = False
            
        try:
            h3 = True
            for x in I_list:
                x = int(x)
                in_union = False
                for k in parsed_P_list:
                    k = abs(k)
                    if k == 0:
                        if x == 0:
                            in_union = True
                            break
                    else:
                        if x % k == 0:
                            in_union = True
                            break
                if not in_union:
                    h3 = False
                    break
        except Exception:
            h3 = False
            
        try:
            neg_q = True
            for k in parsed_P_list:
                k = abs(k)
                subset = True
                for x in I_list:
                    x = int(x)
                    if k == 0:
                        if x != 0:
                            subset = False
                            break
                    else:
                        if x % k != 0:
                            subset = False
                            break
                if subset:
                    neg_q = False
                    break
        except Exception:
            neg_q = False
            
        return [h1, h2, h3, neg_q]

    elif ring_type == 'ZnZ':
        try:
            h1 = (n >= 2)
            if n > 2000:
                return [False, False, False, False]
        except Exception:
            h1 = False
            
        try:
            parsed_P_list = []
            for P in P_list:
                if isinstance(P, int) or (hasattr(P, 'is_Integer') and P.is_Integer):
                    parsed_P_list.append([(int(P) * i) % n for i in range(n)])
                elif isinstance(P, (list, tuple, set)):
                    parsed_P_list.append(list(P))
                else:
                    raise ValueError
        except Exception:
            return [False, False, False, False]
            
        try:
            if len(parsed_P_list) < 1:
                h2 = False
            else:
                all_ideals = True
                not_prime_count = 0
                for P in parsed_P_list:
                    if not is_ideal(n, P):
                        all_ideals = False
                        break
                    if not is_prime_ideal(n, P):
                        not_prime_count += 1
                h2 = all_ideals and (not_prime_count <= 2)
        except Exception:
            h2 = False
            
        try:
            union_P = set()
            for P in parsed_P_list:
                union_P.update({int(x) % n for x in P})
            
            h3 = True
            for x in I_list:
                if (int(x) % n) not in union_P:
                    h3 = False
                    break
        except Exception:
            h3 = False
            
        try:
            I_set = {int(x) % n for x in I_list}
            neg_q = True
            for P in parsed_P_list:
                P_set = {int(x) % n for x in P}
                if I_set.issubset(P_set):
                    neg_q = False
                    break
        except Exception:
            neg_q = False
            
        return [h1, h2, h3, neg_q]

    return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: P_1, ..., P_n are ideals of R such that at most two of them are not prime ideals",
    "H_3: I is contained in the union of P_1, ..., P_n",
    "¬Q: I is not contained in any P_i"
]

N_HYP = 3
NEG_Q_INDEX = 3