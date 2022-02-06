import sys
import os
import search
#script realiza a busca em arquivos gff por meio do name.
#voce precisa ter o arquivo gff no qual deseja realizar a busca.
def getParam(param_name):
	name = False
	for param in sys.argv:
		if(name):
			name = False
			return param
		if(param == param_name):
			name = True
	return False
	
#verifica todas as variaveis e armazena para o pipeline.
if(getParam("-h") != False):
	print("Esse script faz a busca em arquivos gff")
	print("(!)Para utilizar passe o diretorio, nome para o banco e o nome que quer pesquisar.")
else:
	#verifica se todos os parametros estao preenchidos.
	validateParam = True

	if(getParam("-dir") == False):
		print("selecione o diretorio do arquivo gff.")
		validateParam = False
	elif(getParam("-bd") == False):
		print("escolha um nome para o banco.")
		validateParam = False
	elif(getParam("-n") == False):
		print("escolha o nome que voce quer pesquisar")
		validateParam = False					
	#se estiver correto todos os parametros ele executa.
	if(validateParam):
		param_dir = getParam("-dir")
		param_bd = getParam("-bd")
		param_n = getParam("-n")
		#ele busca no diretorio passado e cria um banco com o nome escolhido.
		db = search.Gff(param_dir,param_bd)
		lista = db.search_for_name(param_n)
		for i in lista:
			print(i)
		db.save_file(lista,'dados')