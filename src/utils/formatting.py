def get_pretty_small_float(number, max, decimal_places):
    assert 0 <= decimal_places <= 1

    if max >= 10 and abs(round(number, decimal_places)) < 10:
        prepend = " "
    else:
        prepend = ""

    full_str = prepend + str(round(number, decimal_places))

    if full_str.count(".") == 1 and decimal_places == 0:
        return full_str[0:-2]
    elif full_str.endswith(".0") and decimal_places == 1:
        return full_str[0:-2] + "  "
    elif full_str.count(".") == 0 and decimal_places == 1:
        return full_str + "  "
    else:
        return full_str

def get_pretty_large_integer(number):
    return "{:,}".format(round(number))




#print("<<" + get_pretty_number_(9.9999, 30, 0) + ">>")
#print("<<" + get_pretty_number_(10, 30, 0) + ">>")
#print("<<" + get_pretty_number_(10.001, 30, 0) + ">>")

#print("<<" + get_pretty_number_(9.9999, 30, 1) + ">>")
#print("<<" + get_pretty_number_(10, 30, 1) + ">>")
#print("<<" + get_pretty_number_(10.001, 30, 1) + ">>")
#print("<<" + get_pretty_number_(10.101, 30, 1) + ">>")


#print(round(20, 3))