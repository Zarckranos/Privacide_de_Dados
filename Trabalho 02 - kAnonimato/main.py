import sys
import pandas as pd

from optparse import OptionParser

BEGIN_DATE = ['Ano', 'Decada', 'Seculo']
REGION = ['Cidade', 'Pais', 'Sub-regiao', 'Regiao']

'''
Ler um registro Region e retorna o valor referente a região de interesse [Cidade, País, Sub-Região, Região]
  :param region: um elemento de Region
  :param i: nível de hierarquia passado no momento de chamada do programa
'''
def get_region(region, i):
    register = region.split('; ')
    return register[i]

'''
Recebe uma entrada de ano e retorna a decada correspondente
'''
def get_decada(year):
    decada = (year // 10) * 10
    return decada

'''
Recebe uma entrada de ano e retorna o seculo correspondente
'''
def get_seculo(year):
    seculo = (year - 1) // 100 + 1
    return seculo

def k_anonimato(options, args, k):
    # Open datafile
    try:
        datafile = pd.read_csv(args[0])
    except IOError as exc:
        print(exc)
        sys.exit(1)
    except IndexError as exc:
        print(">> Lembre de passar o nome do arquivo. Ex:")
        print("usage: python %prog [options] <datafile>")
        sys.exit(1)
    
    # Passo do modelo ==============================================================
    new_datafile = pd.DataFrame()
    # Generalizando Region referente ao nível de hierarquia passado
    new_datafile['Region'] = datafile['Region'].apply(lambda x: get_region(x, options.region))

    # Generalizando BeginDate referente ao nível de hierarquia
    if options.begindate == 0:
        # Precisa alterar algo (?)
        ...
    elif options.begindate == 1:
        new_datafile['BeginDate'] = datafile['BeginDate'].apply(get_decada)
    else:
        new_datafile['BeginDate'] = datafile['BeginDate'].apply(get_seculo)

    # Minha ideia:
    # Depois de ter feito a generalização de todo o dataset, tentar montar as classes de equivalência
    # a partir do campo do ano. Se para determinada classe tivermos seu tamanho < k, buscamos por por outra
    # classe de equivalência que (tenha o campo de region igual)² e tamanho < k e generaliza o campo BeginDate
    # para incluir o intervalor dessas duas classes [Ex: 'Brazil', '1930 - 1960'].

    # Então primeiro, após a generalização, seria interessante varrer todo o dataset e adicionar uma nova 
    # coluna para catalogar quantos outros registro um registro tem igual a ele

    # Problemas:
    # 1. Estou assumindo que devemos começar generalizando todo o dataset.
    # 2. Com certeza deve ter algum caso que vai falhar a ideia²
    # 3. Deve existir ideias melhores

    # > agora que paro pra pensar acho que deveria ter escrito isso tudo num README...
    
    # Fim do modelo ================================================================

    # Criar e salvar arquivo de saída csv [kAnonArtists.csv]
    new_datafile.to_csv(f"{k}AnonArtists.csv", index=False)

def main():
    K = [2, 4, 8]

    # INPUT VALUES =================================================================
    parser = OptionParser(usage="usage: python %prog [options] <datafile>")

    # Definir alguns valores padrão
    parser.set_defaults(
        begindate = 0,
        region    = 0
    )

    parser.add_option("-b", "--begindate", dest="begindate",
        type="int",
        metavar="NUM",
        help="Nível de generalização para o atributo BeginDate. [0 - Ano; 1 - Década; 2 - Século]"
    )
    parser.add_option("-r", "--region", dest="region",
        type="int",
        metavar="NUM",
        help="Nível de generalização para o atributo Region. [0 - Cidade; 1 - País; 2 - Sub-região; 3 - Região]"
    )

    (options, args) = parser.parse_args()
    # ==============================================================================
    # Tratar entradas erradas do usuário
    if(options.begindate > 2 or options.region > 3):
        parser.print_help()
        sys.exit(1)

    # Executar modelo k-Anonimato...
    for k in K:
        k_anonimato(options, args, k)

main()