
#JIA YI HE

import flet as ft
def main(page: ft.Page):
    def on_open_file_result(e):
        if e.files:
            with open(e.files.path, "r") as f:
                content = f.read()
                txt_editor.value = content
                update_word_count()

    def on_save_click(e):
        with open("output.txt", "w") as f:
            f.write(txt_editor.value)

    def on_create_click(e):
        txt_editor.value = ""
        update_word_count()

    def update_word_count():
        words = txt_editor.value.split()
        word_count = len(words) if words[0] != '' else 0  
        lbl_word_count.value = f"Word count: {word_count}"
        page.update()

    def on_text_change(e):
        update_word_count()

    txt_editor = ft.TextField(value="", multiline=True, on_change=on_text_change, expand=True)
    btn_open = ft.FilePicker(on_result=on_open_file_result)
    btn_save = ft.ElevatedButton(text="Save", on_click=on_save_click)
    btn_create = ft.ElevatedButton(text="Create", on_click=on_create_click)
    lbl_word_count = ft.Text(value="Word count: 0")
    page.add(ft.Row([btn_create, btn_open, btn_save, lbl_word_count]), txt_editor)

ft.app(target=main)
