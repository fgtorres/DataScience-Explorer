import gffutils
#Classe responsavel por manipular arquivos GFF.
class Gff(object):
#A isntancia da classe precisa do nome do arquivo gff e um nome para o banco que pode ser qualquer um.
    def __init__(self,gff,nome_banco):
        self.gff = gff
        self.nome_banco = nome_banco
#Essa funcao connection_gff recebe o nome do gff e retorna o caminho completo do arquivo.
    def connection_gff(self,nome_gff):
        fn = gffutils.example_filename(nome_gff)
        return fn
#O create_bank_gff epga o caminho do arquivo e gera um banco para o gff.
    def create_bank_gff(self):
        fn = self.connection_gff(self.gff)
        gffutils.create_db(fn, dbfn=self.nome_banco,force=True, keep_order=True, merge_strategy='merge',sort_attribute_values=True)
        db = gffutils.FeatureDB(self.nome_banco, keep_order=True)
        return db
#O search_featuretype e responsavel por pesquisar o gene desejado no gff passando o banco, tipo desejado e o id e o seu retorno e uma lista com os resultados.
    def search_featuretype(self,banco,type,id):
        result = []
        gene = banco[id]
        for i in banco.children(gene,featuretype=type, order_by="start"):
            result.append(i)
        return result
#essa funcao ela pesquisa por coordenadas no aquivo gff
    def search_for_coordinates(self,banco,seqid,start,end):
        result = list(banco.region(region=(seqid,start,end), completely_within=True))
        return result
#essa funcao permite uma busca pelo name no arquivo gff que em alguns arquivos e a terceira coluna
    def search_for_name(self,name):
        result = []
        fn = self.connection_gff(self.gff)
        db = gffutils.create_db(fn, dbfn=self.nome_banco, force=True, keep_order=True, merge_strategy='merge', sort_attribute_values=True, id_spec=['ID', 'Name'])
        for i in db.features_of_type(name, order_by='start'):
            result.append(i)
        return result
    def save_file(self,result,name):
        with open(name + ".txt","w") as arquivo:
            for info in result :
                    info = str(info)
                    arquivo.write(info + "\n")
    

if(__name__ == "__main__"):

#Ao instanciar a classe passe o nome do arquivo gff e do banco que voce quer criar.
    #db = Gff("gff/LeishDB.gff","test2.db")
    #banco = db2.create_bank_gff()
#Nesse exemplo criei o banco e passei ele junto com o gene que eu quero buscar e o id.
    #lista = db.search_featuretype(banco,"mRNA","7881")
#O resultado posso verificar atraves de um for.
    #for result in lista:
        #print(result)
#Um exemplo de como buscar por cordenadas        
    #result = db.search_for_coordinates(banco,'chr1',1,1500)
    #for teste in result:
        #print(teste)

