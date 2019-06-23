from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

def main():
    """
    Draw scale factors across HT and lep Pt and jet mult
    Returns: nothing

    """
    parser = ArgumentParser(description=__doc__, formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-f", "--inputLFN", help="Set era in 2017 to be checked")
    args = parser.parse_args()

    print(args.inputLFN)


if __name__=="__main__":
    main()
