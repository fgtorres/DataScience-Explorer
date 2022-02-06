#!/usr/bin/env python
#  -*- coding: utf-8 -*-

#
# PIPELINE PARA EXECUTAR EM LOTE O SCRIPT DO RAUL PARA ANALISE DE SNPS EM LEISHMANIA
#  Este script executa diversas vezes o script de analise de SNPs em leishmania.

import os.path
import os
import sys


def main():
	# Essa e a lista de comandos para executar em lote.
	comandsnp = ("python script.py -srafolder ./ -resultsfolder /home/fgtorres/ -genomename ERR877268")
	os.system(comandsnp)

# Funcao principal
main();
