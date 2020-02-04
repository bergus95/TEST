l1 = 0
l2 = 0
l3 = 0
l4 = 0
l5 = 0
l6 = 0


def obliczWynik(k1, k2, k3, k4, k5):
    wynik = 0
    zlicz(k1, k2, k3, k4, k5)
    global l1, l2, l3, l4, l5, l6
    print("\n\n ilosc wystapien kosci kolejno:", l1, l2, l3, l4, l5, l6)
    # podejrzane mniej więcej z kurnika.pl/wiki  ^\(-.-)/^ wagi pozmieniałem na uczciwe według siebie
    # np +10 w karecie żeby nie była jak trójka i odjołem jesli nie ma
    if l1 == 5 or l2 == 5 or l3 == 5 or l4 == 5 or l5 == 5 or l6 == 5:
        print("generał")
        wynik += 70
    elif l1 == 4 or l2 == 4 or l3 == 4 or l4 == 4 or l5 == 4 or l6 == 4:
        print("kareta")
        wynik = l1 * 1 + l2 * 2 + l3 * 3 + l4 * 4 + l5 * 5 + l6 * 6 + 10
    elif (l2 == 1 and l3 == 1 and l4 == 1 and l5 == 1 and l6 == 1) or \
            (l2 == 1 and l3 == 1 and l4 == 1 and l5 == 1 and l1 == 1):
        print("duży strit")
        wynik += 60
    elif (l2 == 1 and l3 == 1 and l4 == 1 and l5 == 1) or \
            (l3 == 1 and l4 == 1 and l5 == 1 and l6 == 1) or \
            (l2 == 1 and l3 == 1 and l4 == 1 and l1 == 1):
        print("mały strit")
        wynik += 50
    elif (l1 == 3 and (l2 == 2 or l3 == 2 or l4 == 2 or l5 == 2 or l6 == 2)) \
            or (l2 == 3 and (l3 == 2 or l4 == 2 or l5 == 2 or l6 == 2 or l1 == 2)) \
            or (l3 == 3 and (l2 == 2 or l4 == 2 or l5 == 2 or l6 == 2 or l1 == 2)) \
            or (l4 == 3 and (l2 == 2 or l3 == 2 or l5 == 2 or l6 == 2 or l1 == 2)) \
            or (l5 == 3 and (l2 == 2 or l3 == 2 or l4 == 2 or l6 == 2 or l1 == 2)) \
            or (l6 == 3 and (l2 == 2 or l3 == 2 or l4 == 2 or l5 == 2 or l1 == 2)):
        print("full")
        wynik += 25
    elif l1 == 3 or l2 == 3 or l3 == 3 or l4 == 3 or l5 == 3 or l6 == 3:
        print("trójki")
        wynik = l1 * 1 + l2 * 2 + l3 * 3 + l4 * 4 + l5 * 5 + l6 * 6
    elif (l1 == 2 and (l2 == 2 or l3 == 2 or l4 == 2 or l5 == 2 or l6 == 2)) \
            or (l2 == 2 and (l1 == 2 or l3 == 2 or l4 == 2 or l5 == 2 or l6 == 2)) \
            or (l3 == 2 and (l2 == 2 or l1 == 2 or l4 == 2 or l5 == 2 or l6 == 2)) \
            or (l4 == 2 and (l2 == 2 or l3 == 2 or l1 == 2 or l5 == 2 or l6 == 2)) \
            or (l5 == 2 and (l2 == 2 or l3 == 2 or l4 == 2 or l1 == 2 or l6 == 2)) \
            or (l6 == 2 and (l2 == 2 or l3 == 2 or l4 == 2 or l5 == 2 or l6 == 2)):
        print("masz dwie dwójki")
        if l2 == 2:
            wynik += l2 * 2
        if l1 == 2:
            wynik += l1 * 1
        if l3 == 2:
            wynik += l3 * 3
        if l4 == 2:
            wynik += l4 * 4
        if l5 == 2:
            wynik += l5 * 5
        if l6 == 2:
            wynik += l6 * 6
    elif l2 == 2 or l3 == 2 or l4 == 2 or l5 == 2 or l6 == 2 or l1 == 2:
        print("masz dwójke")
        if l2 == 2:
            wynik += l2 * 2
        if l1 == 2:
            wynik += l1 * 1
        if l3 == 2:
            wynik += l3 * 3
        if l4 == 2:
            wynik += l4 * 4
        if l5 == 2:
            wynik += l5 * 5
        if l6 == 2:
            wynik += l6 * 6
    else:
        if l6 > 0:
            wynik += 6
        elif l5 > 0:
            wynik += 5
        elif l4 > 0:
            wynik += 4
        elif l3 > 0:
            wynik += 3
        elif l2 > 0:
            wynik += 2
        elif l1 > 0:
            wynik += 1

    print("\nWYNIK W LICZ: \n", wynik)
    return wynik


# wstyd i hańba ta funkcja i ten plik ... przepraszam .. taki niedoszły jednolinijkowiec :)
# to wymaga jednolinijkowca koniecznie i bezsprzecznie ^^
def zlicz(k1, k2, k3, k4, k5):
    global l1, l2, l3, l4, l5, l6

    l1 = 0
    l2 = 0
    l3 = 0
    l4 = 0
    l5 = 0
    l6 = 0

    # zliczanie 1
    if k1 == 1:
        l1 += 1
    if k2 == 1:
        l1 += 1
    if k3 == 1:
        l1 += 1
    if k4 == 1:
        l1 += 1
    if k5 == 1:
        l1 += 1

    # zliczanie 2
    if k1 == 2:
        l2 += 1
    if k2 == 2:
        l2 += 1
    if k3 == 2:
        l2 += 1
    if k4 == 2:
        l2 += 1
    if k5 == 2:
        l2 += 1

    # zliczanie 3
    if k1 == 3:
        l3 += 1
    if k2 == 3:
        l3 += 1
    if k3 == 3:
        l3 += 1
    if k4 == 3:
        l3 += 1
    if k5 == 3:
        l3 += 1

    # zliczanie 4
    if k1 == 4:
        l4 += 1
    if k2 == 4:
        l4 += 1
    if k3 == 4:
        l4 += 1
    if k4 == 4:
        l4 += 1
    if k5 == 4:
        l4 += 1

    # zliczanie 5
    if k1 == 5:
        l5 += 1
    if k2 == 5:
        l5 += 1
    if k3 == 5:
        l5 += 1
    if k4 == 5:
        l5 += 1
    if k5 == 5:
        l5 += 1

    # zlczanie 6
    if k1 == 6:
        l6 += 1
    if k2 == 6:
        l6 += 1
    if k3 == 6:
        l6 += 1
    if k4 == 6:
        l6 += 1
    if k5 == 6:
        l6 += 1
