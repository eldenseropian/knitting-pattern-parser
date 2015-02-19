import pattern_tree
import os

def parse(pattern):
    pattern = pattern.splitlines()
    lines = [pattern_tree.Annotation(line) for line in pattern if line]
    section = pattern_tree.Section(lines)
    pattern = pattern_tree.PatternTree([section])
    return pattern

def unroll():
    pass

def expand_reference():
    pass

if __name__ == '__main__':
    pat = open('../scarf-beginner.txt', 'r')
    pat_lines = pat.read()
    pat.close()
    parse(pat_lines)