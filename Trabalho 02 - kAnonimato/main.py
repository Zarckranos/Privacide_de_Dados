import sys

from optparse import OptionParser

BEGIN_DATE = ['ano', 'decada', 'seculo']
REGION = ['cidade', 'pais', 'sub-regiao', 'regiao']

def k_anonimato(options, args, k):
    # Open datafile
    try:
        datafile = open(args[0], 'r')
    except IOError as exc:
        print(exc)
        sys.exit(1)
    except IndexError as exc:
        print(">> Lembre de passar o nome do arquivo. Ex:")
        print("usage: python %prog [options] <datafile>")
        sys.exit(1)
    


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