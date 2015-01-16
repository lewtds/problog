#! /usr/bin/env python

from __future__ import print_function

import os, sys, subprocess, traceback, json

sys.setrecursionlimit(10000)

sys.path.insert(0, os.path.abspath( os.path.join(os.path.dirname(__file__), '../')))

from problog.program import PrologFile, PrologFactory
from problog.core import process_error

from learning import lfi

# from problog.sdd_formula import SDD
            
def print_result( d, output, precision=8 ) :
    success, d = d
    if success :
        score, weights, names, iterations = d
        
        conv = lambda t : str(t.withProbability())
        
        results = { 'score' : score, 'iterations' : iterations, 'weights': dict(zip(map(conv,names),weights)) }
        results['success'] = True
        print (200, 'application/json', json.dumps(results), file=output)
    else :
        d['success'] = False
        #print (400, 'application/json', json.dumps(d), file=output)
        print (200, 'application/json', json.dumps(d), file=output)
    return 0 
    

def main(filename, examplefile) :
    try :
        examples = list(lfi.read_examples( examplefile ))
        program = PrologFile(filename)
    
        result = lfi.run_lfi( program, examples)
        return True, result
    except Exception as err :
        return False, {'err':process_error(err)}
    
        
if __name__ == '__main__' :
    import argparse
        
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', metavar='MODEL')
    parser.add_argument('examples', metavar='EXAMPLES')
    parser.add_argument('output', metavar='OUTPUT')
    
    args = parser.parse_args()

    result = main(args.filename, args.examples)
    with open(args.output, 'w') as output :        
        retcode = print_result( result , output )

    # Always exit with code 0
