def Mph(mph):
    if mph >= 4000:
        return (5, "S")
    if mph >= 3200:
        return (4, "A")
    if mph >= 2400:
        return (3, "B")
    if mph >= 1600:
        return (2, "C")
    if mph >= 800:
        return (1, "D")
    if mph >= 0:
        return (0, "E")


def PriceRoe(pr):
    if pr >= 400:
        return (5, "S")
    if pr >= 320:
        return (4, "A")
    if pr >= 240:
        return (3, "B")
    if pr >= 160:
        return (2, "C")
    if pr >= 80:
        return (1, "D")
    if pr >= 0:
        return (0, "E")


def KgRoe(kr):
    if kr >= 40:
        return (0, "E")
    if kr >= 32:
        return (1, "D")
    if kr >= 24:
        return (2, "C")
    if kr >= 16:
        return (3, "B")
    if kr >= 8:
        return (4, "A")
    if kr >= 0:
        return (5, "S")


def Mut(pr):
    if pr >= 8.5:
        return (5, "S")
    if pr >= 6.8:
        return (4, "A")
    if pr >= 5.1:
        return (3, "B")
    if pr >= 3.4:
        return (2, "C")
    if pr >= 1.7:
        return (1, "D")
    if pr >= 0:
        return (0, "E")
