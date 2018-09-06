#!/usr/bin/python

import os
import sys
import argparse
import logging

import calc

__author__ = 'jmrodriguezc'

def main(args):
    ''' Main function'''

    logging.info('create calculator object')
    w = calc.calculate(args.infile, args.sheetname, args.method)

    logging.info('calculate the correlation: '+args.method)
    w.correlation()

    logging.info('print the correlation file')
    w.to_csv(args.outfile)

    logging.info('create heatmap')
    w.create_heatmap(args.outgraphfile)

if __name__ == "__main__":
    # parse arguments
    parser = argparse.ArgumentParser(
        description='Gets the correlation values for the proteins in multiple patients',
        epilog='''
        Example:
            get_correlation.py -i data/tablas_figuras_correlaciones.xlsx -s fig1 -o data/tablas.corr_pearson.csv
        ''')
    parser.add_argument('-i',  '--infile', required=True, help='Excel file with the Zq for proteins/patients')
    parser.add_argument('-s',  '--sheetname',    required=True, help='The name of Excel sheet')    
    parser.add_argument('-m',  '--method', default='pearson', choices=['pearson', 'kendall', 'spearman'], help='Excel file with the Zq for proteins/patients')
    parser.add_argument('-o',  '--outfile', required=True, help='Output file with the correlation values in CSV format')
    parser.add_argument('-g',  '--outgraphfile', required=True, help='Output file with the correlation values in CSV format')
    parser.add_argument('-v', dest='verbose', action='store_true', help="Increase output verbosity")
    args = parser.parse_args()

    # logging debug level. By default, info level
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')
    else:
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')

    logging.info('start '+os.path.basename(__file__))
    main(args)
    logging.info('end '+os.path.basename(__file__))