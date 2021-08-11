from tkinter import ttk
from tkinter import *

import sqlite3

class Product:
    database = 'app.db'

    def __init__(self, window):
        
        self.wind = window
        self.wind.title('Products aplication')

        # creating a Frame container
        frame = LabelFrame(self.wind, text="regitra un nuevo producto")
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)
        

        #name input
        Label(frame, text='Name:  ').grid(row = 1, column = 0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row = 1, column= 1)

        #price input
        Label(frame, text="price:  ", activebackground='red').grid(row = 2, column = 0)
        self.price = Entry(frame)
        self.price.grid(row = 2, column = 1)

        #button add product
        ttk.Button(frame, text= 'Save Product',command=self.add_products).grid(row = 3, columnspan= 2, sticky = W + E)

        # Output Messages
        self.message = Label(text='', fg='red')
        self.message.grid(row = 3, column=0, columnspan=2, sticky= W + E)

        # table
        self.tree = ttk.Treeview(height=10, columns=2)
        self.tree.grid(row=4, column=0, columnspan=5)
        self.tree.heading('#0', text='Name')
        self.tree.heading('#1', text='Price')

        #Buttons:
        ttk.Button(text='DELETE', command=self.delete_product).grid(row=5, column=0,  sticky = W + E)
        ttk.Button(text='EDIT', command=self.update_product).grid(row=5, column=1,  sticky = W + E )

        #excute

        self.get_products()

    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.database) as conn:
            cursor = conn.cursor()
            result =cursor.execute(query, parameters)
            conn.commit()
        return result

    def get_products(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)

        QUERY = 'SELECT * FROM product ORDER BY name DESC'
        db_rows = self.run_query(QUERY)
        
        for row in db_rows:
            self.tree.insert('', 0, text=row[1], values= row[2])

    def validation(self):
        return len(self.name.get()) != 0 and len(self.price.get()) != 0

    def add_products(self):
        if self.validation():
            QUERY = 'INSERT INTO product VALUES(NULL, ?, ?)'
            PARAMETERS = (self.name.get(), self.price.get())
            self.run_query(QUERY, PARAMETERS)
            self.message['text'] = 'Product {}  added successfully'.format(self.name.get())
            self.name.delete(0, END)
            self.price.delete(0, END)
        else:
            self.message['text'] = 'Name and Price are required'
            
        self.get_products()

    def delete_product(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Please select a record, error: {}'.format(e)
            return
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM product WHERE name = ?'
        self.run_query(query, (name, ))
        self.message['text'] = 'Record {} deleted successfully'.format(name)
        self.get_products()

    def update_product(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Please select a record, error: {}'.format(e)
            return
        
        name = self.tree.item(self.tree.selection())['text']
        old_price = self.tree.item(self.tree.selection())['values'][0]

        self.edi_wid = Toplevel()
        self.edi_wid.title = 'Edit Proudct'

        # old Name
        Label(self.edi_wid, text='Old Name: ').grid(row=0,column=1)
        Entry(self.edi_wid, textvariable= StringVar(self.edi_wid, value=name), state='readonly').grid(row=0, column=2)
        #new name
        Label(self.edi_wid, text='New Name: ').grid(row=1,column=1)
        new_name = Entry(self.edi_wid)
        new_name.grid(row=1, column=2)

        # old Price
        Label(self.edi_wid, text='Old Price: ').grid(row=2,column=1)
        Entry(self.edi_wid, textvariable= StringVar(self.edi_wid, value=old_price), state='readonly').grid(row=2, column=2)
        #new Price
        Label(self.edi_wid, text='New Price: ').grid(row=3,column=1)
        new_price = Entry(self.edi_wid)
        new_price.grid(row=3, column=2)

        Button(self.edi_wid, text= 'update', command=lambda: self.edit_records(new_name.get(), new_price.get(), name, old_price)).grid(row=4, column=2, sticky= W )

    def edit_records(self, new_name, new_price, name, old_price):
        query = 'UPDATE product SET name = ?, price = ? WHERE name = ? AND price = ?'
        parameters = (new_name,new_price, name, old_price)
        self.run_query(query, parameters)
        self.edi_wid.destroy()
        self.message['text'] = 'record {} updated successfuly '.format(name)

        self.get_products()


if __name__ == '__main__':
    window = Tk()
    aplication = Product(window)
    window.mainloop()