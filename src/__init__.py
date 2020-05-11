import argparse
from decode import decoder
from trie import Trie
from sufxArr import SA
from kmer import kmer_maker
from mapper import mapper
from reporter import reporter


parser = argparse.ArgumentParser()
parser.add_argument("-m", default=1, help="Which method to use? 1:trie 2:suffi\
x array 3: bwd")
parser.add_argument("-r", default="", help="Reference file path")
parser.add_argument("-s", default="", help="Sequence reads file path")
parser.add_argument("-k", default=13, help="k-mer size")
parser.add_argument("-b", default=-1, help="Batch size")
parser.add_argument("-c", default=10, help="Min allowed count of matching\
 kmers")
parser.add_argument("-p", default=70, help="Min allowed matching similarity\
 percentage")
parser.add_argument("-o", default="", help="Output file prefix path")
args = parser.parse_args()


def run():
    reference = decoder(args.r)
    sequence = decoder(args.s)
    refKmer = kmer_maker(int(args.k), reference, True)
    seqKmer = kmer_maker(int(args.k), sequence, False)
    if int(args.m) == 1:  # mapping through Suffix Trie
        reference_trie = Trie()
        sternum = mapper(refKmer, seqKmer, reference_trie, int(args.b))
        sternum.filter_matching(int(args.c), int(args.p))
        reporter(sternum, args.o)
    elif int(args.m) == 2:  # mapping through Suffix Array
        reference_sa = SA(reference)
