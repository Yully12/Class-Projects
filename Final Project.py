
#XIE YING FENG, JIA YI HE AND DIANA NG

import csv
import flet as ft
import os
import json
from fpdf import FPDF


def app(page: ft.Page):
    page.title = "Rastreador de Participación de Clase"

    global students
    students = {
        "id": 0,
        "listado": []
    }
    global filename
    filename = None

    file_picker = ft.FilePicker()
    page.add(file_picker)

    dlg_save = ft.AlertDialog(
        title=ft.Row([ft.Icon(ft.icons.SYNC), ft.Text("Guardando listado")]),
        modal=True
    )

    def save_students_to_file(filepath):
        global students
        dlg_save.open = True
        page.dialog = dlg_save
        page.update()
        with open(filepath, 'w') as file:
            json.dump(students, file)
        dlg_save.open = False
        page.update()

    def save_as_studends_file(e):
        file_picker.save_file(allowed_extensions=["json"])

    save_as_button = ft.MenuItemButton(
        content=ft.Text("Guardar como..."),
        on_click=save_as_studends_file
    )
    save_as_button.disabled = True

    dlg_load = ft.AlertDialog(
        title=ft.Row([ft.Icon(ft.icons.SYNC), ft.Text("Cargando listado")]),
        modal=True
    )

    def file_event(e: ft.FilePickerResultEvent):
        global students
        global filename
        if e.path is not None:
            local_filename = e.path
            if not local_filename.endswith(".json"):
                local_filename += ".json"
            save_students_to_file(local_filename)
            filename = local_filename
            save_as_button.disabled = False
        elif e.files is not None:
            filename = e.files[0].path
            dlg_load.open = True
            page.dialog = dlg_load
            page.update()
            with open(filename, 'r') as file:
                students = json.load(file)
            dlg_load.open = False
            save_as_button.disabled = False
            fill_table()
        if filename is not None:
            page.title = "Rastreador de Participación de Clase ["+filename+"]"
        page.update()

    file_picker.on_result = file_event

    def save_studends_file(e):
        global filename
        if filename is None:
            file_picker.save_file(file_name='students.json',
                                  allowed_extensions=["json"])
        else:
            save_students_to_file(filename)

    def open_studends_file(e):
        file_picker.pick_files(allow_multiple=False,
                               allowed_extensions=["json"])

    register_dlg_text = ft.Text(size=25)
    register_dlg = None

    def close_register_dlg(e):
        if register_dlg in stack_controls:
            stack_controls.remove(register_dlg)
        page.update()

    table = ft.DataTable(columns=[
        ft.DataColumn(ft.Text("ID")),
        ft.DataColumn(ft.Text("Nombres")),
        ft.DataColumn(ft.Text("Apellidos")),
        ft.DataColumn(ft.Text("Curso")),
        ft.DataColumn(ft.Text("Sección")),
        ft.DataColumn(ft.Text("Nota")),
        ft.DataColumn(ft.Text("")),
        ft.DataColumn(ft.Text(""))
    ], expand=True)

    options = ft.Column([])
    stack_controls = []
    stack = ft.Stack(stack_controls, expand=True)

    input_id = ft.TextField(label="ID", read_only=True,
                            text_align=ft.TextAlign.RIGHT)
    input_nombres = ft.TextField(label="Nombres")
    input_apellidos = ft.TextField(label="Apellidos")
    input_curso = ft.Dropdown(
        label="Curso",
        options=[
            ft.dropdown.Option("9no"),
            ft.dropdown.Option("10mo"),
            ft.dropdown.Option("11vo"),
            ft.dropdown.Option("12vo")
        ]
    )
    input_seccion = ft.Dropdown(
        label="Sección",
        options=[
            ft.dropdown.Option("I"),
            ft.dropdown.Option("II"),
            ft.dropdown.Option("III")
        ]
    )
    input_nota = ft.TextField(
        label="Nota",
        keyboard_type=ft.KeyboardType.NUMBER,
        input_filter=ft.InputFilter(
            allow=True, regex_string=r"[0-9]", replacement_string=""),
        max_length=3
    )
    register_dlg_content = ft.Column()

    warning_banner = None

    def close_banner(e):
        warning_banner.open = False
        page.update()

    warning_text = ft.Text(color=ft.colors.DEEP_ORANGE)
    warning_banner = ft.Banner(
        bgcolor=ft.colors.AMBER_100,
        leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED,
                        color=ft.colors.AMBER, size=40),
        content=warning_text,
        actions=[
            ft.TextButton("Ok", on_click=close_banner),
        ],
    )
    page.banner = warning_banner

    def show_warning(msg):
        warning_banner.open = True
        warning_text.value = msg
        page.update()

    def open_register_dlg(e):
        if len(input_id.value) == 0:
            register_dlg_text.value = 'Registrar Estudiante'
            input_nombres.value = ""
            input_apellidos.value = ""
            input_curso.value = "9no"
            input_seccion.value = "I"
            input_nota.value = ""
            register_dlg_content.controls = [
                input_nombres,
                input_apellidos,
                input_curso,
                input_seccion,
                input_nota
            ]
        else:
            register_dlg_text.value = 'Modificar Estudiante'
            register_dlg_content.controls = [
                input_id,
                input_nombres,
                input_apellidos,
                input_curso,
                input_seccion,
                input_nota
            ]
        if register_dlg not in stack_controls:
            stack_controls.append(register_dlg)
        page.update()

    global delete_target
    delete_target = None

    dlg_delete = None

    def close_dlg_delete(e):
        dlg_delete.open = False
        page.update()

    def delete_student(e):
        if delete_target is None:
            return
        students["listado"].remove(delete_target)
        fill_table()
        close_dlg_delete(e)

    dlg_delete_title = ft.Text("")
    dlg_delete_content = ft.Text("")
    dlg_delete = ft.AlertDialog(
        title=dlg_delete_title,
        content=dlg_delete_content,
        actions_alignment=ft.MainAxisAlignment.END,
        actions=[
            ft.TextButton("Ok", style=ft.ButtonStyle(
                color=ft.colors.GREEN), on_click=delete_student),
            ft.TextButton("Cancelar", style=ft.ButtonStyle(
                color=ft.colors.RED), on_click=close_dlg_delete)
        ],
        modal=True
    )

    def ask_delete_student(student):
        global delete_target
        delete_target = student
        dlg_delete_title.value = "Eliminar Estudiante"
        dlg_delete_content.value = "¿Deseas eliminar el estudiante #" + \
            str(student["id"])+" "+str(student["nombres"]) + \
            " "+str(student["apellidos"])+"?"
        dlg_delete.open = True
        page.dialog = dlg_delete
        page.update()

    def edit_student(e):
        student = e.control.data
        input_id.value = str(student["id"])
        input_nombres.value = student["nombres"]
        input_apellidos.value = student["apellidos"]
        input_curso.value = student["curso"]
        input_seccion.value = student["seccion"]
        input_nota.value = str(student["nota"])
        open_register_dlg(e)

    def ask_to_delete(e):
        ask_delete_student(e.control.data)

    def fill_table():
        # global students
        rows = []
        for student in students["listado"]:
            rows.append(ft.DataRow([
                ft.DataCell(ft.Text(student["id"])),
                ft.DataCell(ft.Text(student["nombres"])),
                ft.DataCell(ft.Text(student["apellidos"])),
                ft.DataCell(
                    ft.Text(student["curso"], text_align=ft.TextAlign.CENTER)),
                ft.DataCell(
                    ft.Text(student["seccion"], text_align=ft.TextAlign.CENTER)),
                ft.DataCell(
                    ft.Text(student["nota"], text_align=ft.TextAlign.RIGHT)),
                ft.DataCell(
                    ft.Icon(ft.icons.EDIT, color=ft.colors.GREEN), on_tap=edit_student, data=student),
                ft.DataCell(ft.Icon(ft.icons.DELETE,
                            color=ft.colors.RED), on_tap=ask_to_delete, data=student)
            ]))
        table.rows = rows
        page.update()

    def register_student(e):
        global students
        close_banner(e)
        if len(input_id.value) == 0:
            id = students["id"]+1
            nombres = input_nombres.value.strip()
            apellidos = input_apellidos.value.strip()
            curso = input_curso.value
            seccion = input_seccion.value
            nota = input_nota.value.strip()
            if len(nombres) == 0:
                show_warning("El campo \"Nombres\" esta vacío.")
                return
            if len(apellidos) == 0:
                show_warning("El campo \"Apellidos\" esta vacío.")
                return
            if len(nota) == 0:
                show_warning("El campo \"Nota\" esta vacío.")
                return
            nota = int(nota)
            if nota > 100:
                show_warning("El campo \"Nota\" no puede ser mayor que 100.")
                return
            new_student = {
                "id": id,
                "nombres": nombres,
                "apellidos": apellidos,
                "curso": curso,
                "seccion": seccion,
                "nota": nota
            }
            students["id"] = id
            students["listado"].append(new_student)
        else:
            id = int(input_id.value)
            nombres = input_nombres.value.strip()
            apellidos = input_apellidos.value.strip()
            curso = input_curso.value
            seccion = input_seccion.value
            nota = input_nota.value.strip()
            for student in students["listado"]:
                if student["id"] == id:
                    student["id"] = id
                    student["nombres"] = nombres
                    student["apellidos"] = apellidos
                    student["curso"] = curso
                    student["seccion"] = seccion
                    student["nota"] = nota
                    break
        close_register_dlg(e)
        fill_table()
        page.update()

    save_student_button = ft.TextButton('Registrar', style=ft.ButtonStyle(
                                        color=ft.colors.GREEN), on_click=register_student)

    register_dlg_body = ft.Container(
        content=ft.Row([
            ft.Container(
                ft.Column(
                    controls=[
                        register_dlg_text,
                        ft.Column([
                            register_dlg_content,
                            ft.Container(
                                ft.Row([
                                    save_student_button,
                                    ft.TextButton('Cancelar', style=ft.ButtonStyle(
                                        color=ft.colors.RED), on_click=close_register_dlg)
                                ]),
                                alignment=ft.alignment.center_right
                            )
                        ], horizontal_alignment=ft.CrossAxisAlignment.END)
                    ],
                )
            )
        ]),
        padding=ft.padding.symmetric(10, 20),
        bgcolor=ft.colors.BACKGROUND,
        border_radius=ft.border_radius.all(10)
    )

    spacing = ft.Container(expand=True)
    register_dlg = ft.Container(

        content=ft.Container(ft.Row(
            [spacing,
             ft.Column([spacing, register_dlg_body, spacing]),
                spacing])),
        expand=True,
        bgcolor=ft.colors.with_opacity(
            0.4, ft.colors.ON_BACKGROUND)
    )

    def clear_list(e):
        global students
        global filename
        filename = None
        students = {
            "id": 0,
            "listado": []
        }
        page.title = "Rastreador de Participación de Clase"
        fill_table()
        page.update()

    def open_register_dlg_new(e):
        input_id.value = ""
        open_register_dlg(e)

    def export_text(e):
        if e.path is not None:
            local_filename = e.path
            if not local_filename.endswith(".txt") and not local_filename.endswith(".csv"):
                local_filename += ".txt"
            with open(local_filename, 'w') as file:
                writer = csv.writer(file)

                writer.writerow([
                    "ID",
                    "Nombres",
                    "Apellidos",
                    "Curso",
                    "Sección",
                    "Nota"
                ])
                for student in students["listado"]:
                    writer.writerow([
                        student["id"],
                        student["nombres"],
                        student["apellidos"],
                        student["curso"],
                        student["seccion"],
                        student["nota"]
                    ])

    def export_pdf(e):# https://py-pdf.github.io/fpdf2/Tables.html
        if e.path is not None:
            local_filename = e.path
            if not local_filename.endswith(".pdf"):
                local_filename += ".pdf"
            with open(local_filename, 'wb') as file:
                table_data = [("ID",
                                 "Nombres",
                                 "Apellidos",
                                 "Curso",
                                 "Sección",
                                 "Nota")]
                for student in students["listado"]:
                    table_data.append((
                        str(student["id"]),
                        student["nombres"],
                        student["apellidos"],
                        student["curso"],
                        student["seccion"],
                        str(student["nota"])
                    ))
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Times", size=16)
                with pdf.table() as table:
                    for data_row in table_data:
                        row = table.row()
                        for datum in data_row:
                            row.cell(datum)
                pdf.output(file)

    file_export_text = ft.FilePicker()
    page.add(file_export_text)

    def export_as_text(e):
        file_export_text.save_file(allowed_extensions=["txt", "csv"])
    file_export_text.on_result = export_text

    file_export_pdf = ft.FilePicker()
    page.add(file_export_pdf)

    def export_as_pdf(e):
        file_export_pdf.save_file(allowed_extensions=["pdf"])
    file_export_pdf.on_result = export_pdf

    menu = ft.MenuBar(
        controls=[
            ft.SubmenuButton(
                content=ft.Text("Estudiantes"),
                controls=[
                    ft.MenuItemButton(
                        content=ft.Text("Registrar"),
                        on_click=open_register_dlg_new
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Abrir listado"),
                        on_click=open_studends_file
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Nuevo listado"),
                        on_click=clear_list
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Guardar listado"),
                        on_click=save_studends_file
                    ),
                    save_as_button
                ]
            ),
            ft.SubmenuButton(
                content=ft.Text("Exportar"),
                controls=[
                    ft.MenuItemButton(
                        content=ft.Text("A PDF"),
                        on_click=export_as_pdf
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("A archivo de texto"),
                        on_click=export_as_text
                    )
                ]
            )
        ]
    )
    stack_controls.append(ft.Container(
        ft.Column([
            menu,
            ft.ListView(controls=[table], expand=1, spacing=10, padding=20)
        ], expand=True, alignment=ft.MainAxisAlignment.START),
        expand=True
    ))

    page.add(stack)


ft.app(target=app)
