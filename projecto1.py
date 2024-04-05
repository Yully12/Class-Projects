import flet as ft

def app(page: ft.Page):
    page.title = "Rastreador de Participación de Clase"
    
    # Elementos de UI para la selección de grado
    grade_dropdown = ft.Dropdown(
        label="Selecciona el Grado",
        hint_text="Elige el grado del estudiante",
        options=[
            ft.dropdown.Option("I"),
            ft.dropdown.Option("II"),
            ft.dropdown.Option("III"),
            ft.dropdown.Option("IV"),
        ],
        autofocus=True
    )

    # Elementos de UI para la gestión de estudiantes
    student_input = ft.TextField(label="Introduce el nombre del estudiante", hint_text="Escribe el nombre aquí")
    student_list = ft.ListView()
    add_student_btn = ft.Button(text="Añadir Estudiante")

    # Manejadores de eventos
    def add_student(e):
        selected_grade = grade_dropdown.value
        student_name = student_input.value.strip()

        if not student_name:
            # Manejar entrada vacía
            page.dialog("Advertencia", "Por favor, introduce el nombre del estudiante.")
            return

        # Añadir estudiante a la lista con el grado
        student_list.items.append(ft.ListTile(
            title=f"{selected_grade} - {student_name}",
            leading=ft.Checkbox()
        ))
        student_input.value = ""  # Limpiar el campo de nombre del estudiante después de añadir
        page.update()

    # Vincular manejadores de eventos a los botones
    add_student_btn.on_click = add_student

    # Añadir elementos de UI a la página
    page.add(grade_dropdown, student_input, add_student_btn, student_list)

ft.app(target=app)
