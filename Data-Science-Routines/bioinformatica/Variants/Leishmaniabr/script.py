#!/usr/bin/env python
#  -*- coding: utf-8 -*-
#
# AUTOMATIZAR O SCRIPT DE RAUL PARA SNPS
#  Este script automatiza o leishsnp.sh para que possa ser executado automaticamente em lote.
#
# (!)Para executar o script e necessario ter na mesma pasta de softwares com os seguintes programas
#  instalados:
#	** FastQC (https://www.bioinformatics.babraham.ac.uk/projects/download.html#fastqc)
#	** Trimmomatic 0.36 (http://www.usadellab.org/cms/?page=trimmomatic)
#	** Picard (https://github.com/broadinstitute/picard/releases/latest)
#   ** GATK (https://software.broadinstitute.org/gatk/download/)
#   ** bwa 0.7.15 (https://sourceforge.net/projects/bio-bwa/files/)
#   ** sratoolkit (https://github.com/ncbi/sra-tools/wiki/Downloads)
#

import os.path
import os
import sys

# Funcoes auxiliares
# Se existe um determinado path retorna TRUE senao retorna FALSE.
def exists_dir(path):
    try:
        return os.path.isdir(path)
    except:
        return False

# Se existe um determinado arquivo retorna TRUE senao returna FALSE.
def exists_file(path):
    try:
        return os.path.isfile(path)
    except:
        return False

# Essa funcao retorna o valor do parametro passado no script.
def get_a_param(param, name):
    next = False
    for obj in param:
        if next:
            return str(obj)
        if obj == name:
            next = True

# Rotina principal do script.
param = sys.argv[1:]
resultsfolder = get_a_param(param,"-resultsfolder")
genomename = get_a_param(param,"-genomename")
srafolder = get_a_param(param,"-srafolder")

# Verifica todas as pastas requeridas, caso nao exista o script informa ao usuario.
if(exists_dir(resultsfolder)!=True):
    #Caso a pasta resultados nao exista o script cria ela.
	os.mkdir((str(resultsfolder) + str("results")))
if(exists_dir(srafolder)!=True):
    print ("The sra folder not exists.")
    exit ();

# No caso de um arquivo SRA o script executara o fastq-dump para separar os arquivos.
print (os.system(str("softwares/sratoolkit/bin/fastq-dump ") +str(" --split-files ")+ srafolder +str("/") + genomename + str("/") +genomename +
          str(".sra --outdir ") + resultsfolder + str("/results")))

# Executando o script de raul leishsnp.sh
comandsnp = (str("perl leishsnp.sh ") + str(" -r ")+genomename +str("_1.fastq -r2 ") + genomename +str("_2.fastq -f ")+
     resultsfolder+str("/results -t 2"))

# Ao terminar a execucao do script em perl caso exista a pasta resultados o script renomeia ela e da a mensagem de
# complete.
if(exists_dir(resultsfolder + str("results"))!=False):
    os.rename((resultsfolder + str("results")), (resultsfolder+ str("results")).replace("results",genomename))
    print ("Complete the snp analises of " + str(genomename))
else:
	print ("[ERROR] The results folder not exist. Please execute the script again.")
	

