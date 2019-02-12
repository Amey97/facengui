import sqlite3
from os import path, getcwd

db = path.join(getcwd(), 'database.db')


class Database:



    def __init__(self):
        self.connection = sqlite3.connect(db, check_same_thread=False)

    def insertUser(self, name_of_comp, reg_no, region, address_comp, ps_phone, hr_name, emp_id, hr_aadhar, hr_pan,hr_email, hr_mob_no, head_user_id, head_pass, head_pass2):
        cursor = self.connection.cursor()
        #con = sqlite3.connect("database.db")
        #cur = con.cursor()
        #cursor.execute("CREATE TABLE company_reg ( `name_of_comp` TEXT, `reg_no` INTEGER, `region` TEXT, `address_comp` TEXT, `ps_phone` INTEGER, `hr_name` TEXT, `emp_id` INTEGER, `hr_aadhar` INTEGER, `hr_pan` INTEGER, `hr_email` TEXT, `hr_mob_no` NUMERIC, `head_user_id` TEXT, `head_pass` TEXT, `head_pass2` TEXT )")
        cursor.execute( "INSERT INTO company_reg (name_of_comp, reg_no, region, address_comp, ps_phone, hr_name, emp_id, hr_aadhar, hr_pan, hr_email, hr_mob_no, head_user_id, head_pass, head_pass2) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(name_of_comp, reg_no, region, address_comp, ps_phone, hr_name, emp_id, hr_aadhar, hr_pan, hr_email, hr_mob_no, head_user_id, head_pass, head_pass2))

        self.connection.commit()
        cursor.close()


    def query(self, q, arg=()):
        cursor = self.connection.cursor()

        cursor.execute(q, arg)
        results = cursor.fetchall()
        cursor.close()

        return results

    def insert(self, q, arg=()):
        cursor = self.connection.cursor()

        cursor.execute(q, arg)

        self.connection.commit()
        result = cursor.lastrowid
        cursor.close()
        return result

    def select(self, q, arg=()):
        cursor = self.connection.cursor()

        return cursor.execute(q, arg)

    def delete(self, q, arg=()):
        cursor = self.connection.cursor()
        result = cursor.execute(q, arg)
        self.connection.commit()
        return result