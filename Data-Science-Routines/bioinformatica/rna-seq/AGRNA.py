#
# ANALISE GERAL DE RNA-SEQ
#  Este script realiza a analise geral do experimento de RNA-Seq com Illumina.
#  (!)Para utilizar ele e necessario ter instalado no servidor os seguintes programas:
#	** Trimmomatic 0.36 (http://www.usadellab.org/cms/?page=trimmomatic)
#	** Diamond 0.8.34 (https://github.com/bbuchfink/diamond)
#   ** Kronatools 2.4 (https://github.com/marbl/Krona/wiki)
#
#	(!)Deve-se ter realizado o download dos seguintes bancos de dados:
#	** NCBI NR (ftp://ftp.ncbi.nlm.nih.gov/blast/db/FASTA/nr.gz)

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
if(getparam("-h")!= False):
    print("Este script realiza a analise geral do experimento de RNA-Seq com Illumina.")
    print(" (!)Para utilizar ele e necessario ter instalado no servidor os seguintes programas:")
    print("     ** Trimmomatic 0.36 (http://www.usadellab.org/cms/?page=trimmomatic)")
    print("     ** Diamond 0.8.34 (https://github.com/bbuchfink/diamond)")
    print("     ** Kronatools 2.4 (https://github.com/marbl/Krona/wiki)")
    print("     ** Java 1.7")
    print("")
    print(" (!)Deve-se ter realizado o download dos seguintes bancos de dados:")
    print("     ** NCBI NR (ftp://ftp.ncbi.nlm.nih.gov/blast/db/FASTA/nr.gz)")
    print("")
    print("Alguns dos nossos parametros:")
    print(" python AGRNA.py -d -bd -trim -in -out ")
else:
    #Checa se todos os parametros obrigatorios estao preenchidos
    validateparam = True
    if (getparam("-d") == False):
        print("(!)Precisa selecionar a pasta do Diamond")
        validateparam = False
    elif (getparam("-bd") == False):
        print("(!)Precisa selecionar a base de dados formatada usando makedb do Diamond")
        validateparam = False
    elif(getparam("-trim") == False):
        print("(!)Precisa selecionar a pasta do Trimmomatic")
        validateparam = False
    elif(getparam("-in")== False):
        print("(!)Precisa selecionar a pasta com as sequencias de transcrito")
        validateparam = False

    #Se todos os parametros obrigatorios estiverem corretos, executa o pipeline
    if(validateparam):
        param_d = getparam("-d")
        param_bd = getparam("-bd")
        param_trim = getparam("-trim")
        param_in = getparam("-in")

        #Unifica todas as fitas de transcrito em uma foward e uma reverse
        os.system("cd " + param_in)
        os.system("cat " + param_in + "*R1* > "+ param_in+"merged_R1.fastq.gz")
        os.system("cat " + param_in + "*R2* > "+ param_in+"merged_R2.fastq.gz")
        os.system("gunzip -d -k "+ param_in+"merged_R*")

        #Executa o Trimmomatic paired
        os.system("java -jar "+param_trim+"trimmomatic-0.36.jar PE " +
                  "-threads 10 -phred33 "+ param_in+"merged_R1.fastq " + param_in+"merged_R2.fastq "+ param_in +
                                                    "output_trimmomatic_paired.fq.gz "
                  + param_in + "output_trimmomatic_unpaired.fq.gz  ILLUMINACLIP:TruSeq3-PE.fa:2:30:10 "
                               "LEADING:3 TRAILING:3")

        #Executa o Diamond
        os.system("gunzip -d -k "+ param_in+"output_trimmomatic_paired.fq.gz")
        os.system(param_d + "diamond blastx  -d " + param_bd +
                  " -q "+ param_in+"output_trimmomatic_paired.fq " +
                  "-o "+ param_in+"diamond_matches.m8")

        #Gera o Kronatools
        os.system("ktImportBLAST "+ param_in+"diamond_matches.m8 -o "+ param_in+"report.html ")

        #Concluido
        print("*******************  Processo concluido ! **************************")