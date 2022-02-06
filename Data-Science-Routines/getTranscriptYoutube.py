from socialmidia.youtube import Youtubefunctions
from functions import Basics

id = Basics.getparam("-id")
lang = Basics.getparam("-lang")

try:
    video = Youtubefunctions.getSubtitle(id, languages=[lang])
    # Percorrendo o dicionario do video e mostrando a legenda.
    for key in video: print(key["text"])
except:
    try:
        video = Youtubefunctions.getSubtitle(id)
        # Percorrendo o dicionario do video e mostrando a legenda.
        for key in video: print(key["text"])
    except:
        print(" O video nao possui legenda disponivel.")


