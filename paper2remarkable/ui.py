# -*- coding: utf-8 -*-

"""Command line interface

Author: G.J.J. van den Burg
License: See LICENSE file
Copyright: 2019, G.J.J. van den Burg

"""

import argparse

from .providers import providers
from .utils import exception


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-b",
        "--blank",
        help="Add a blank page after every page of the PDF",
        action="store_true",
    )
    parser.add_argument(
        "-v", "--verbose", help="be verbose", action="store_true"
    )
    parser.add_argument(
        "-n",
        "--no-upload",
        help="don't upload to the reMarkable, save the output in current working dir",
        action="store_true",
    )
    parser.add_argument(
        "-d",
        "--debug",
        help="debug mode, doesn't upload to reMarkable",
        action="store_true",
    )
    parser.add_argument(
        "-c",
        "--center",
        help="Center the PDF on the page, instead of left align",
        action="store_true",
    )
    parser.add_argument(
        "--filename",
        help="Filename to use for the file on reMarkable",
        default=None,
    )
    parser.add_argument(
        "-p",
        "--remarkable-path",
        help="directory on reMarkable to put the file (created if missing)",
        dest="remarkable_dir",
        default="/",
    )
    parser.add_argument(
        "--rmapi", help="path to rmapi executable", default="rmapi"
    )
    parser.add_argument(
        "--pdfcrop", help="path to pdfcrop executable", default="pdfcrop"
    )
    parser.add_argument(
        "--pdftk", help="path to pdftk executable", default="pdftk"
    )
    parser.add_argument("--gs", help="path to gs executable", default="gs")
    parser.add_argument(
        "input", help="URL to a paper or the path of a local PDF file"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    provider = next((p for p in providers if p.validate(args.input)), None)
    if provider is None:
        exception("Input not valid, no provider can handle this source.")

    prov = provider(
        verbose=args.verbose,
        upload=not args.no_upload,
        debug=args.debug,
        center=args.center,
        blank=args.blank,
        remarkable_dir=args.remarkable_dir,
        rmapi_path=args.rmapi,
        pdfcrop_path=args.pdfcrop,
        pdftk_path=args.pdftk,
        gs_path=args.gs,
    )

    prov.run(args.input, filename=args.filename)