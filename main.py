from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle

import mysql.connector

class TuitionManager(App):

    def build(self):
        Window.clearcolor = (0.9, 0.9, 0.9, 1)  # Set background color to light gray

        scroll_view = ScrollView()
        layout = FloatLayout(size_hint=(None, None), size=(Window.width, Window.height))

        add_student_btn = Button(text='Add New Student', size_hint=(0.3, 0.1), pos_hint={'center_x': 0.5, 'top': 0.9}, background_color=(1, 0, 0, 1))
        add_student_btn.bind(on_press=self.add_student_popup)
        layout.add_widget(add_student_btn)

        update_payment_btn = Button(text='Update Payment Status', size_hint=(0.3, 0.1), pos_hint={'center_x': 0.5, 'top': 0.75}, background_color=(1, 0, 0, 1))
        update_payment_btn.bind(on_press=self.update_payment_popup)
        layout.add_widget(update_payment_btn)

        delete_student_btn = Button(text='Delete Student', size_hint=(0.3, 0.1), pos_hint={'center_x': 0.5, 'top': 0.6}, background_color=(1, 0, 0, 1))
        delete_student_btn.bind(on_press=self.delete_student_popup)
        layout.add_widget(delete_student_btn)

        sort_students_btn = Button(text='Display Student List', size_hint=(0.3, 0.1), pos_hint={'center_x': 0.5, 'top': 0.45}, background_color=(1, 0, 0, 1))
        sort_students_btn.bind(on_press=self.sort_students_popup)
        layout.add_widget(sort_students_btn)

        search_student_btn = Button(text='Search Student', size_hint=(0.3, 0.1), pos_hint={'center_x': 0.5, 'top': 0.3}, background_color=(1, 0, 0, 1))
        search_student_btn.bind(on_press=self.search_student_popup)
        layout.add_widget(search_student_btn)

        scroll_view.add_widget(layout)

        return scroll_view

    # اضافة الدوال الاخرى هنا...

    
   

    def delete_student_popup(self, instance):
        popup_layout = GridLayout(cols=2)

        student_id_input = TextInput(hint_text='Student ID')
        popup_layout.add_widget(Label(text='Student ID'))
        popup_layout.add_widget(student_id_input)

        submit_btn = Button(text='Submit')
        submit_btn.bind(on_press=lambda x: self.delete_student(student_id_input.text))
        popup_layout.add_widget(submit_btn)

        popup = Popup(title='Delete Student', content=popup_layout, size_hint=(None, None), size=(400, 200))
        popup.open()



    def delete_student(self, student_id):
        try:
            connection = mysql.connector.connect(host='localhost',
                                                database='tuition_manager',
                                                user='root',
                                                password='')
            cursor = connection.cursor()

            sql_query = "DELETE FROM students WHERE id = %s"
            cursor.execute(sql_query, (student_id,))
            connection.commit()

            popup = Popup(title='Success', content=Label(text='Student deleted successfully.'), size_hint=(None, None), size=(200, 200))
            popup.open()

        except mysql.connector.Error as error:
            print(f"Failed to delete record from MySQL table: {error}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()



    def search_student_popup(self, instance):
        popup_layout = GridLayout(cols=2)

        search_input = TextInput(hint_text='Search')
        popup_layout.add_widget(Label(text='Search'))
        popup_layout.add_widget(search_input)

        search_by_name_btn = Button(text='Search by Name')
        search_by_name_btn.bind(on_press=lambda x: self.search_student('name', search_input.text))
        popup_layout.add_widget(search_by_name_btn)

        search_by_university_id_btn = Button(text='Search by University ID')
        search_by_university_id_btn.bind(on_press=lambda x: self.search_student('university_id', search_input.text))
        popup_layout.add_widget(search_by_university_id_btn)

        popup = Popup(title='Search Student', content=popup_layout, size_hint=(None, None), size=(400, 200))
        popup.open()
    
    

    def search_student(self, search_by, search_term):
        try:
            connection = mysql.connector.connect(host='localhost',
                                                database='tuition_manager',
                                                user='root',
                                                password='')
            cursor = connection.cursor()

            sql_query = f"SELECT * FROM students WHERE {search_by} = %s"
            cursor.execute(sql_query, (search_term,))
            students = cursor.fetchall()

            popup_layout = GridLayout(cols=6, padding=10, spacing=10, size_hint=(0.8, 0.8))
            popup_layout.bind(minimum_height=popup_layout.setter('height'))

            popup_layout.add_widget(Label(text='ID', size_hint_x=None, width=100))
            popup_layout.add_widget(Label(text='Name', size_hint_x=None, width=150))
            popup_layout.add_widget(Label(text='University ID', size_hint_x=None, width=150))
            popup_layout.add_widget(Label(text='Payment Status', size_hint_x=None, width=150))
            popup_layout.add_widget(Label(text='Installment Date', size_hint_x=None, width=150))
            popup_layout.add_widget(Label(text='Installment Amount', size_hint_x=None, width=150))
            for student in students:
                for value in student:
                    popup_layout.add_widget(Label(text=str(value), size_hint_x=None, width=150))


            scroll_view = ScrollView(size_hint=(None, None), size=(800, 400))
            scroll_view.add_widget(popup_layout)


            popup = Popup(title='Search Result', content=scroll_view, size_hint=(None, None), size=(900, 500))
            popup.open()

        except mysql.connector.Error as error:
            print(f"Failed to fetch records from MySQL table: {error}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


    def add_student_popup(self, instance):
        popup_layout = GridLayout(cols=2)

        name_input = TextInput(hint_text='Name')
        popup_layout.add_widget(Label(text='Name'))
        popup_layout.add_widget(name_input)

        university_id_input = TextInput(hint_text='University ID')
        popup_layout.add_widget(Label(text='University ID'))
        popup_layout.add_widget(university_id_input)

        payment_status_input = TextInput(hint_text='Payment Status')
        popup_layout.add_widget(Label(text='Payment Status'))
        popup_layout.add_widget(payment_status_input)

        installment_date_input = TextInput(hint_text='Installment Date')
        popup_layout.add_widget(Label(text='Installment Date'))
        popup_layout.add_widget(installment_date_input)

        installment_amount_input = TextInput(hint_text='Installment Amount')
        popup_layout.add_widget(Label(text='Installment Amount'))
        popup_layout.add_widget(installment_amount_input)

        submit_btn = Button(text='Submit')
        submit_btn.bind(on_press=lambda x: self.add_student(name_input.text, university_id_input.text, payment_status_input.text, installment_date_input.text, installment_amount_input.text))
        popup_layout.add_widget(submit_btn)

        popup = Popup(title='Add New Student', content=popup_layout, size_hint=(None, None), size=(400, 400))
        popup.open()

    def add_student(self, name, university_id, payment_status, installment_date, installment_amount):
        try:
            connection = mysql.connector.connect(host='localhost',
                                                database='tuition_manager',
                                                user='root',
                                                password='')
            cursor = connection.cursor()

            sql_query = "INSERT INTO students (name, university_id, payment_status, installment_date, installment_amount) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql_query, (name, university_id, payment_status, installment_date, installment_amount))
            connection.commit()

            popup = Popup(title='Success', content=Label(text='Student added successfully.'), size_hint=(None, None), size=(200, 200))
            popup.open()

        except mysql.connector.Error as error:
            print(f"Failed to insert record into MySQL table: {error}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def sort_students_popup(self, instance):
        popup_layout = GridLayout(cols=1)

        sort_by_name_btn = Button(text='Sort by Name')
        sort_by_name_btn.bind(on_press=lambda x: self.sort_students('name'))
        popup_layout.add_widget(sort_by_name_btn)

        sort_by_payment_status_btn = Button(text='Sort by Payment Status')
        sort_by_payment_status_btn.bind(on_press=lambda x: self.sort_students('payment_status'))
        popup_layout.add_widget(sort_by_payment_status_btn)

        popup = Popup(title='Sort Students', content=popup_layout, size_hint=(None, None), size=(200, 200))
        popup.open()

    def sort_students(self, sort_by):
        try:
            connection = mysql.connector.connect(host='localhost',
                                                database='tuition_manager',
                                                user='root',
                                                password='')
            cursor = connection.cursor()

            sql_query = f"SELECT * FROM students ORDER BY {sort_by}"
            cursor.execute(sql_query)
            sorted_students = cursor.fetchall()

            popup_layout = GridLayout(cols=6, padding=10, spacing=10, size_hint=(0.8, 0.8))
            popup_layout.bind(minimum_height=popup_layout.setter('height'))


            popup_layout.add_widget(Label(text='ID', size_hint_x=None, width=100))
            popup_layout.add_widget(Label(text='Name', size_hint_x=None, width=150))
            popup_layout.add_widget(Label(text='University ID', size_hint_x=None, width=150))
            popup_layout.add_widget(Label(text='Payment Status', size_hint_x=None, width=150))
            popup_layout.add_widget(Label(text='Installment Date', size_hint_x=None, width=150))
            popup_layout.add_widget(Label(text='Installment Amount', size_hint_x=None, width=150))
            for student in sorted_students:
                for value in student:
                    popup_layout.add_widget(Label(text=str(value), size_hint_x=None, width=150))

            scroll_view = ScrollView(size_hint=(None, None), size=(800, 400))
            scroll_view.add_widget(popup_layout)

            popup = Popup(title='Student List', content=scroll_view, size_hint=(None, None), size=(900, 500))
            popup.open()

        except mysql.connector.Error as error:
            print(f"Failed to fetch records from MySQL table: {error}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    

    def update_payment(self, student_id, payment_status):
        try:
            connection = mysql.connector.connect(host='localhost',
                                                database='tuition_manager',
                                                user='root',
                                                password='')
            cursor = connection.cursor()

            sql_query = "UPDATE students SET payment_status = %s WHERE id = %s"
            cursor.execute(sql_query, (payment_status, student_id))
            connection.commit()

            popup = Popup(title='Success', content=Label(text='Payment status updated successfully.'), size_hint=(None, None), size=(200, 200))
            popup.open()

        except mysql.connector.Error as error:
            print(f"Failed to update record in MySQL table: {error}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


    def update_payment_popup(self, instance):
        popup_layout = GridLayout(cols=2)

        student_id_input = TextInput(hint_text='Student ID')
        popup_layout.add_widget(Label(text='Student ID'))
        popup_layout.add_widget(student_id_input)

        payment_status_input = TextInput(hint_text='Payment Status')
        popup_layout.add_widget(Label(text='Payment Status'))
        popup_layout.add_widget(payment_status_input)

        submit_btn = Button(text='Submit')
        submit_btn.bind(on_press=lambda x: self.update_payment(student_id_input.text, payment_status_input.text))
        popup_layout.add_widget(submit_btn)

        popup = Popup(title='Update Payment Status', content=popup_layout, size_hint=(None, None), size=(400, 200))
        popup.open()

    # Add other popup functions and database functions here...

if __name__ == '__main__':
    TuitionManager().run()

