#
# Esse script transforma arquivo GFF em GTF
#  Este script realiza a analise geral do experimento de RNA-Seq com Illumina.

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

#Verifica variaveis e armazena para o pipeline.
#Checa se todos os parametros obrigatorios estao preenchidos
validateparam = True
if (getparam("-in") == False):
    print("(!)Precisa selecionar o arquivo de entrada")
    validateparam = False
elif (getparam("-out") == False):
    print("(!)Precisa selecionar o arquivo de saida.")
    validateparam = False

if(validateparam):
    if(getparam("-h")!= False):
        print("Este script transforma o arquivo GFF para GTF.")
        print(" (!)Para utilizar ele e necessario ter instalado no servidor os seguintes programas:")
        print("     ** AWK")
        print("")
        print("Alguns dos nossos parametros:")
        print(" python gff2gtf.py -in <Arquivo.GFF> -out <Arquivo.GTF>)
    else:
        filegff=getparam("-in")
        filegtf=getparam("-out")
        os.system(" awk -f gff2gtf.awk " + filegff + " > " + filegtf )