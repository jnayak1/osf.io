from framework.transactions.context import TokuTransaction
import sys

def main(dev=False, _db=None):
	pass

if __name__ == '__main__':
    dry_run = 'dry' in sys.argv
    dev = 'dev' in sys.argv
    with TokuTransaction():
        main(dev=dev)
        if dry_run:
            raise RuntimeError('Dry run, rolling back transaction.')