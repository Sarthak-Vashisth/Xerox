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

import pymysql

def insert_to_db(final_list_to_db):
    query = """INSERT INTO Xerox.image_ocr_data(image,sender,
                receiver,invoice_date,due_date,invoice_no,total_balance,serial_label,order_label)
                values(%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
    try:
        conn = pymysql.connect(host='localhost',user='root',passwd='root',port=3306,database='Xerox')
        curr = conn.cursor()
        curr.execute("Select * from Xerox.image_ocr_data");
        for i in range(0,len(final_list_to_db)):
            obj_to_db = final_list_to_db[i]
            args=(obj_to_db['image'],obj_to_db['sender'],obj_to_db['receiver'],
                  obj_to_db['invoice_date'],obj_to_db['due_date'],obj_to_db['invoice_no'],obj_to_db['total_balance'],
                  obj_to_db['serial_label'],obj_to_db['order_label'])
            curr.execute(query,args);
            conn.commit()
    except Exception as e:
        print(e)
