#
# SCRIPT PARA FORMATAR O GFF
#  Este script realiza a formatacao do GFF para ter na coluna atributos apenas o GenbankID
#  (!)Para utilizar ele e necessario ter instalado no servidor os seguintes programas:
#	** GFF Utils: pip install gffutils

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
    print(" python GFFformat.py -gff <GFF file> -a <Label> -o <Output file> ")
else:
    # # Checa se todos os parametros obrigatorios estao preenchidos
    # validateparam = True
    # if (getparam("-gff") == False):
    #     print("(!)Precisa informar qual o arquivo GFF sera utilizado.")
    #     validateparam = False
    # elif (getparam("-a") == False):
    #     print("(!)Precisa informar qual label aparecera na ultima coluna.")
    #     validateparam = False
    # elif (getparam("-o") == False):
    #     print("(!)Precisa selecionar o arquivo de saida do GFF format.")
    #     validateparam = False

    #Se todos os parametros obrigatorios estiverem corretos, executa o pipeline
    # if(validateparam):

    # Ler o arquivo gff e carregar em memoria na variavel content.
    sourcefile = open("genomeLbr2904.gff", 'r')
    gffcontent = sourcefile.readlines()

    for line in gffcontent:
        if "#" in line:
            print(line)

        else:
            contentarray = line.split("\t")
            if "UniProtKB/TrEMBL:" in contentarray[8]:
                uniprotid = contentarray[8].split("UniProtKB/TrEMBL:")[1].split(",")[0]

                newline = contentarray[0] + "\t" + contentarray[1] + "\t" + contentarray[2] + "\t" + \
                          contentarray[3] + "\t" + contentarray[4] + "\t" + contentarray[5] + "\t" + \
                          contentarray[6] + "\t" + contentarray[7] + "\t" + "ID=" + uniprotid

                print(newline)

