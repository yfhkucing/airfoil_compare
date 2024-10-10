def AtmosPropStd(Href, PropertyID):
    #from Gudmundsson's book, translated into python
    # This function calculates an atmospheric property based on the variable
    # PropertyID at the given altitude H in ft, where:
    # If PropertyID = 0 then return Temperature ratio
    # If PropertyID = 1 then return Pressure ratio
    # If PropertyID = 2 then return Density ratio
    # If PropertyID = 10 then return Temperature
    # If PropertyID = 11 then return Pressure
    # If PropertyID = 12 then return Density
    # If PropertyID = 13 then return Dynamics Vicosity
    # If PropertyID = 14 then return Gravity
    # If PropertyID = 15 then return Speed of Sound

    # 1994 ATMOSPHERIC MODELING

    # Calculation
    R = 1 - 0.000022558 * Href
    TempRatio = R
    PressRatio = R ** 5.2561
    DensRatio = R ** 4.2561

    TempInt = 288.15 * TempRatio
    PressInt = 101325 * PressRatio
    DensInt = 1.225 * DensRatio

    RatioDynVisco = (TempRatio ** 1.5) * ((288.15 + 110) / (TempInt + 110))
    DynVisco = 0.00001789 * RatioDynVisco

    GravityInt = (9.807 * (6371000 ** 2)) / ((6371000 + Href) ** 2)

    SpeedSoundInt = 340.3 * ((TempInt / 288.15) ** 0.5)

    # Output
    if PropertyID == 0:
        return TempRatio
    elif PropertyID == 1:
        return PressRatio
    elif PropertyID == 2:
        return DensRatio
    elif PropertyID == 10:
        return TempInt - 273.15
    elif PropertyID == 11:
        return PressInt
    elif PropertyID == 12:
        return DensInt
    elif PropertyID == 13:
        return DynVisco
    elif PropertyID == 14:
        return GravityInt
    elif PropertyID == 15:
        return SpeedSoundInt