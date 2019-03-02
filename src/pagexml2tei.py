#!/usr/bin/env python3

import argparse
import logging


logging.basicConfig(level=logging.DEBUG,
                    filename="pagexml2tei.log",
                    filemode="w")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="pagexml2tei-parser",
                                     description="CLI tool to parse PAGE XML files"
                                                 "and convert them to TEI.")
    parser.add_argument("--path", "-p", help="Path to the PAGE XML files.")
    parser.add_argument("--output", "-o", help="Path to output directory.")

    args = parser.parse_args()
