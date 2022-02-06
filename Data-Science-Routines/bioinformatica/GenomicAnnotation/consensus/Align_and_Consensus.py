#
# SCRIPT PARA ALINHAR SEQUENCIA COM REFERENCIA E EXTRAIR A CONSENSUS

import os
import sys

def getparam(param_name):
    name = False
    for param in sys.argv :
        if (name):
            name = False
            return param
        if (param == param_name):
            name = True
    return False

#Verifica variaveis para o pipeline.
if(getparam("-h")!= False):
    print("Este script realiza a formatacao do GFF para ter na coluna atributos apenas o GenbankID.")
    print(" (!)Para utilizar ele e necessario ter instalado no servidor os seguintes programas:")
    print("     ** GFF Utils: pip install gffutils")
    print("")
    print("Alguns dos nossos parametros:")
    print(" python Align_Consensus.py -gff <GFF file> -a <Label> -o <Output file> ")
else: