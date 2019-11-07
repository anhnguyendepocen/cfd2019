#!/usr/bin/env python

import os
import os.path as op
import sys
from argparse import ArgumentParser
import re

from rmdex.exerciser import (make_exercise, make_solution, write_utf8,
                             read_utf8)


HERE = op.abspath(op.dirname(__file__))
sys.path.append(HERE)

import build_exercise as b_e


TEMPLATE_RE = re.compile('_template\.Rmd$')


def process_dir(path, out_path, execute=False):
    templates = [fn for fn in os.listdir(path) if TEMPLATE_RE.search(fn)]
    if len(templates) == 0:
        raise RuntimeError('No _template.Rmd in directory')
    if len(templates) > 1:
        raise RuntimeError('More than one _template.Rmd in directory')
    template_fname = op.join(path, templates[0])
    if execute:
        nb = b_e.read_nb(template_fname)
        b_e.execute_nb(nb, b_e.path_of(template_fname))
    template = read_utf8(template_fname)
    exercise_fname = TEMPLATE_RE.sub('.Rmd', template_fname)
    write_utf8(exercise_fname, make_exercise(template))
    solution_fname = TEMPLATE_RE.sub('_solution.Rmd', template_fname)
    write_utf8(solution_fname, make_solution(template))
    b_e.process_nb(exercise_fname, execute=False, out_path=out_path)


def main():
    parser = ArgumentParser()
    parser.add_argument('dir', help="Directory of exercise")
    parser.add_argument('--execute', action='store_true',
                        help='If specified, execute template notebook')
    parser.add_argument('--out-path',
                        help='Output path for zipped exercise')
    args = parser.parse_args()
    if args.out_path is None:
        args.out_path = op.join(HERE, '..', 'exercises')
    process_dir(args.dir, args.out_path, args.execute)


if __name__ == '__main__':
    main()
