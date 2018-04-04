import os
import re
import time
from collections import defaultdict
from difflib import get_close_matches

import yaml

from objectview import ObjectView

THIS_FOLDER = os.getcwd()


class Invoice_parser:
    def __init__(self,configuration,invoice_file_data_list):
        self.configuration = configuration;
        self.data_with_emptyspace = invoice_file_data_list;
        self.truncate_empty_lines()


    def parse_data(self,curr_conf,data):
        for index, spellings in curr_conf.data.items():
            for spelling in spellings:
                line_matched = self.find_in_data(spelling,data);
                if line_matched:
                    print("Line matching is :: ",line_matched)

    def find_in_data(self,key,data):
        for each_line in data:
            words = each_line.split()
            # Get the single best match in line
            matches = get_close_matches(key, words, 1)
            if matches:
                return each_line

    def truncate_empty_lines(self):
        self.data = [line.lower() for line in self.data_with_emptyspace if line.strip()]



def read_meta_file(file="configuration.yaml"):
    stream = open(os.path.join(THIS_FOLDER, file), "r")
    docs = yaml.safe_load(stream)
    return ObjectView(docs)

def get_files_in_folder(folder, include_hidden=False):
    files = os.listdir(folder)
    if not include_hidden:
        files = [
            f for f in files if not f.startswith(".")
        ]

    files = [
        os.path.join(folder, f) for f in files
    ]
    return [
        f for f in files if os.path.isfile(f)
    ]


def ocr_receipts(config, receipt_files):
    for receipt_file in receipt_files:
        with open(receipt_file,'r+') as receipt:
            invoice = Invoice_parser(config,receipt.readlines());
            returned_json = invoice.parse_data(invoice.configuration,invoice.data);
            break;



def main():
    config = read_meta_file()
    receipt_files = get_files_in_folder(config.receipts_path)
    ocr_receipts(config, receipt_files)



if __name__ == "__main__":
    main()


