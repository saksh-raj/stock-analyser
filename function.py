def CAGR(PV, FV, YEARS):
    if PV == 0:
        raise ValueError("PV cannot be zero.")
    if YEARS <=0:
        raise ValueError("Number of years must be a positive value.")
    
    return (FV/PV) ** (1/YEARS) - 1
