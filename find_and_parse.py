# coding: utf-8
# Copyright 2018-2020 @ Sarthak Vashisth
#Released under the GNU General Public License
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os,db_layer
import re
import time
from collections import defaultdict
from difflib import get_close_matches
from fuzzywuzzy import process,fuzz

import yaml

from ObjectState import ObjectState

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
            elif index == 'invoice_date' or index == 'due':
                self.parse_date(index,synonyms,data)
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
        for key in keys_to_find:
            result = process.extract(key, data)
            for str_data,index in result:
                pattern = re.compile(r'(total)(.)+(\d)')
                match = pattern.findall(str_data)
                if len(match) > 0 and "total" in str_data and "subtotal" not in str_data:
                    for w in str_data.split():
                        pattern_balance = re.compile(r'\d+\.\d+')
                        balance = pattern_balance.findall(w)
                        if len(balance) > 0:
                            self.json_data["total_balance"] = w

    def parse_date(self,index,keys_to_find,data):
        for key in keys_to_find:
            result = process.extract(key, data)
        if index == "invoice_date":
            for str_data, index in result:
                pattern = re.compile(r'.(date)')
                match = pattern.findall(str_data)
                if match:
                    self.convert_to_date_format(str_data);
        else:
            for str_data, index in result:
                pattern = re.compile(r'(due)+')
                match = pattern.findall(str_data)
                if match:
                    self.convert_to_date_format(str_data);

    def convert_to_date_format(self,str_data):
        if "invoice" in str_data:
            if ':' in str_data:
                invoice_date = str_data.split(':')[1].strip(' ');
                if ',' in invoice_date:
                    self.json_data['invoice_date'] = ''.join(invoice_date.split(','))
                else:
                    self.json_data['invoice_date'] =str_data.split(':')[1].strip(' ');
            else:
                self.json_data['invoice_date'] = 'NA';
        else:
            if ':' in str_data:
                due_date = str_data.split(':')[1].strip(' ');
                if ',' in due_date:
                    self.json_data['invoice_date'] = ''.join(due_date.split(','))
                else:
                    self.json_data['invoice_date'] = str_data.split(':')[1].strip(' ');
            else:
                self.json_data['due_date'] = 'NA';


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
    return ObjectState(docs)

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
    list_of_data_obj = [];
    final_list = [];
    for receipt_file in receipt_files:
        with open(receipt_file,'r+') as receipt:
            invoice = Invoice_parser(config,receipt.readlines());
            returned_json = invoice.parse_data(invoice.configuration,invoice.data);
            list_of_data_obj.append(returned_json)
    final_list = enhance_data_insert_db(list_of_data_obj);
    db_layer.insert_to_db(final_list)
    print(final_list)

def enhance_data_insert_db(image_list):
    local_obj={}
    return_final_list=[];
    for i in range(0,len(image_list)):
        local_obj = image_list[i]
        # if local_obj.get('image_id') == '' or local_obj.get('image_id') == None:
        #     local_obj['image_id'] = str(i)
        if local_obj.get('image') == '' or local_obj.get('image') == None:
            local_obj['image'] = 'NA'
        if local_obj.get('sender') == '' or local_obj.get('sender') == None:
            local_obj['sender'] = 'NA'
        if local_obj.get('receiver') == '' or local_obj.get('receiver') == None:
            local_obj['receiver'] = 'NA'
        if local_obj.get('invoice_date') == '' or local_obj.get('invoice_date') == None:
            local_obj['invoice_date'] = 'NA'
        if local_obj.get('due_date') == '' or local_obj.get('due_date') == None:
            local_obj['due_date'] = 'NA'
        if local_obj.get('invoice_no') == '' or local_obj.get('invoice_no') == None:
            local_obj['invoice_no'] = 'NA'
        if local_obj.get('total_balance') == '' or local_obj.get('total_balance') == None:
            local_obj['total_balance'] = 'NA'
        if local_obj.get('serial_label') == '' or local_obj.get('serial_label') == None:
            local_obj['serial_label'] = 'NA'
        if local_obj.get('order_label') == '' or local_obj.get('order_label') == None:
            local_obj['order_label'] = 'NA'
        return_final_list.append(local_obj)
    return return_final_list


def main():
    config = read_meta_file()
    receipt_files = get_files_in_folder(config.receipts_path)
    ocr_receipts(config, receipt_files)



if __name__ == "__main__":
    main()


