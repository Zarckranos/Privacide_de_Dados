import sys
import pandas as pd
import matplotlib.pyplot as plt

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
Recebe uma entrada referente ao ano e generaliza o dado de acordo com o nível passado.
'''
def generalize_begindate(year, level):
    if BEGIN_DATE[level] == 'Decada':
        return (year // 10) * 10
    elif BEGIN_DATE[level] == 'Seculo':
        return (year - 1) // 100 + 1
    
    return year


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
    anonymized_data = pd.DataFrame()
    # Generalizando Region referente ao nível de hierarquia passado
    anonymized_data['Region'] = datafile['Region'].apply(lambda x: get_region(x, options.region))

    # Generalizando BeginDate referente ao nível de hierarquia
    anonymized_data['BeginDate'] = datafile['BeginDate'].apply(lambda x: generalize_begindate(x, options.begindate))

    # Calcular o tamanho classes de equivalência
    class_sizes = anonymized_data.groupby(['BeginDate', 'Region']).size()

    # Filtrar as classes que não satisfazem k
    filtered_classes = class_sizes[class_sizes < k]
    
    # Calcular min e max apenas para as classes que não satisfazem k
    if not filtered_classes.empty:
        min_begin_date = filtered_classes.index.get_level_values(0).min()
        max_begin_date = filtered_classes.index.get_level_values(0).max()

        # Generalizar classes que não satisfazem k
        for (begin_date, region), count in class_sizes.items():
            if count < k:
                anonymized_data.loc[(anonymized_data['BeginDate'] == begin_date) & (anonymized_data['Region'] == region), 'Region'] = 'World'
                anonymized_data.loc[(anonymized_data['BeginDate'] == begin_date) & (anonymized_data['Region'] == "World"), 'BeginDate'] = f'{min_begin_date}-{max_begin_date}'

    # Recalcular o tamanho médio das classes de equivalência
    class_sizes = anonymized_data.groupby(['BeginDate', 'Region']).size()
    mean_class_size = class_sizes.mean()

    # Calcular a precisão
    precision = len(class_sizes[class_sizes >= k]) / len(class_sizes)
    anonymized_data['Income ($)'] = datafile['Income ($)']
    
    # Fim do modelo ================================================================

    # Criar e salvar arquivo de saída csv [kAnonArtists.csv]
    anonymized_data.to_csv(f"{k}AnonArtists.csv", index=False)
    return  anonymized_data, mean_class_size, precision

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
        anon_data, mean_class_size, precision = k_anonimato(options, args, k)
        print(f'Anonimização concluída para k={k}, BeginDate={BEGIN_DATE[options.begindate]}, Region={REGION[options.region]}')
        print(f'Tamanho médio das classes de equivalência: {mean_class_size:.2f}')
        print(f'Precisão: {precision:.2f}')

        # Plotar histograma das classes de equivalência
        plt.hist(anon_data.groupby(['BeginDate', 'Region']).size(), bins=20)
        plt.xlabel('Tamanho das classes de equivalência')
        plt.ylabel('Número de classes de equivalência')
        plt.title(f'k={k}, BeginDate={BEGIN_DATE[options.begindate]}, Region={REGION[options.region]}')
        plt.show()

main()