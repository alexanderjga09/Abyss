max_rank: int = 8000

ranks_mph = max_rank / 5
ranks_proe = (max_rank / 5) * 0.1


def Mph(mph):
    if mph >= ranks_mph * 5:
        return (5, "S")
    if mph >= ranks_mph * 4:
        return (4, "A")
    if mph >= ranks_mph * 3:
        return (3, "B")
    if mph >= ranks_mph * 2:
        return (2, "C")
    if mph >= ranks_mph:
        return (1, "D")
    if mph >= 0:
        return (0, "E")


def PriceRoe(pr):
    if pr >= ranks_proe * 5:
        return (5, "S")
    if pr >= ranks_proe * 4:
        return (4, "A")
    if pr >= ranks_proe * 3:
        return (3, "B")
    if pr >= ranks_proe * 2:
        return (2, "C")
    if pr >= ranks_proe:
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
