from argparse import ArgumentParser, FileType

parser = ArgumentParser()

parser.add_argument(
    '--script',
    type = FileType('rb', 0)
)

args = parser.parse_args()

print(args.script)