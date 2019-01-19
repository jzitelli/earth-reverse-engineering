import argparse
import pathlib
import logging
import PIL.Image as Image
_logger = logging.getLogger('convert_to_png')


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory', dest='directory', default=".",
                        help='directory to convert')
    parser.add_argument('-r', '--recursive', action='store_false',
                        help='convert directory recursively')
    return parser.parse_args()


def convert_dir(directory, recursive=True):
    for p in (p for p in pathlib.Path(directory).iterdir()
              if p.name.endswith('.bmp')):
        image = Image.open(p)
        outpath = p.with_name(p.name[:-3] + 'png')
        image.save(outpath)
        _logger.info('saved "%s"', outpath)
    for p in (p for p in pathlib.Path(directory).iterdir()
              if p.name.endswith('.mtl')):
        p.write_text(p.read_text().replace('.bmp', '.png', -1))
        _logger.info('saved "%s"', p)
    if recursive:
        for p in (p for p in pathlib.Path(directory).iterdir()
                  if p.is_dir()):
            convert_dir(p, recursive=True)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    args = parse_args()
    convert_dir(args.directory, recursive=args.recursive)
