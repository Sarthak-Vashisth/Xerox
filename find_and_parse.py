import os
import re
import time
from collections import defaultdict
from difflib import get_close_matches
from fuzzywuzzy import process,fuzz

import yaml

from objectview import ObjectView

THIS_FOLDER = os.getcwd()


class Invoice_parser:
    def __init__(self,configuration,invoice_file_data_list):
        self.configuration = configuration;
        self.data_with_emptyspace = invoice_file_data_list;
        self.truncate_empty_lines()
        self.json_data={}


    def parse_data(self,curr_conf,data):
        for index,synonyms in curr_conf.data.items():
            if index == 'invoice_no':
                self.parse_invoice_number(synonyms,data)
            elif index == 'total':
                self.parse_balance(synonyms,data)
            # elif index == 'invoice_date' or index == 'due':
            #     self.parse_date(synonyms,data)
            # elif index == 'sender':
            #     self.parse_sender(synonyms, data)
            # elif index == 'receiver':
            #     self.parse_receiver(synonyms, data)
        return self.json_data

    def parse_invoice_number(self,keys_to_find,data):
        for key in keys_to_find:
            result = get_close_matches(key, data)
            for data_str in result:
                if ':' in data_str:
                    self.json_data['invoice_no'] = data_str.split(':')[1].strip(' ');

    def parse_balance(self,keys_to_find,data):
        list_of_balance = []
        for key in keys_to_find:
            result = process.extract(key, data)
            for str_data,index in result:
                pattern = re.compile(r'(total)(.)+(\d)')
                match = pattern.findall(str_data)
                print(match)
                if len(match) > 0:
                    print(str_data)
                    for s in str_data.split():
                        if s.isdigit():
                            list_of_balance.append(int(s))
                            print(list_of_balance)




    def find_in_data(self,key,data):
        result = process.extract(key, data)
        print(result)
        #for each_line in data:
            # words = each_line.split()
            # # Get the single best match in line
            # matches = self.fuzzy_wuzzy_match(key, words)
            # if matches:
            #     return each_line

    def truncate_empty_lines(self):
        self.data = [line.lower().strip('\n') for line in self.data_with_emptyspace if line.strip()]


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
            print(returned_json)
            break;



def main():
    config = read_meta_file()
    receipt_files = get_files_in_folder(config.receipts_path)
    ocr_receipts(config, receipt_files)



if __name__ == "__main__":
    main()


