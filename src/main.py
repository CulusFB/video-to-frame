from function.cut_frame import frame_cut
import flet as ft
from function import globals as gl


def main(page: ft.Page):
    def on_save_path_result(e: ft.FilePickerResultEvent):
        if e.path is None:
            return 0
        gl.save_path = e.path
        check_icon.name = ft.Icons.CHECK
        check_icon.color = ft.Colors.GREEN
        page.update()

    def open_error_diag():
        page.dialog = error_dialog
        error_dialog.open = True
        page.update()

    def frame_cutting(e):
        if gl.path != '' and gl.save_path != '' and gl.filename != 'Файл не выбран' and gl.save_path is not None:
            btn_run.disabled = True
            done_txt.visible = False
            prb.visible = True
            page.update()
            done_txt.value = 'Файл успешно обработан'

            try:
                frame_cut(int(txt_number.value), prb, page)


            except Exception as exp:
                done_txt.value = f'Произошла непредвиденная ошибка {exp}'
                prb.visible = False
                btn_run.disabled = False
                done_txt.visible = True
                page.update()

            done_icon.name = ft.Icons.CHECK
            done_icon.color = ft.Colors.GREEN
            prb.visible = False

            btn_run.disabled = False

            done_txt.visible = True
            page.update()
        else:
            open_error_diag()

    page.title = "Video cut"
    page.window.min_width = 400
    page.window.min_height = 300
    page.window.width = 450
    page.window.height = 300
    page.vertical_alignment = ft.MainAxisAlignment.START
    txt_number = ft.TextField(value="5", text_align=ft.TextAlign.CENTER, width=100)
    page.theme_mode = ft.ThemeMode.LIGHT
    btn_run = ft.ElevatedButton("Обработать файл",
                                on_click=frame_cutting)

    filename_txt = ft.Text(str(f'Ваш файл: {gl.filename}'), )
    done_txt = ft.Text('', )
    done_txt.visible = False
    save_path = ft.FilePicker(on_result=on_save_path_result)
    page.overlay.append(save_path)
    check_icon = ft.Icon(name=ft.Icons.CLOSE, color=ft.Colors.RED)
    done_icon = ft.Icon(name=ft.Icons.CLOSE, color=ft.Colors.RED)
    error_dialog = ft.AlertDialog(
        title=ft.Text("Ошибка", color=ft.Colors.RED),
        content=ft.Text("Заполните все данные")
    )

    def on_dialog_result(e: ft.FilePickerResultEvent):
        if len(e.files) == 1:
            gl.filename = [e.files[0].name]
            gl.path = [e.files[0].path]
        else:
            gl.filename = [name.name for name in e.files]
            gl.path = [path.path for path in e.files]
        filename_txt.value = str(f'Ваш файл: {gl.filename}')
        page.update()

    pick_file = ft.FilePicker(on_result=on_dialog_result)
    page.overlay.append(pick_file)
    prb = ft.ProgressBar(width=400, color=ft.Colors.ORANGE, visible=False)
    page.update()
    page.add(ft.Row(alignment=ft.MainAxisAlignment.START, controls=[
        ft.Column(alignment=ft.MainAxisAlignment.START, controls=[
            ft.Row(
                [
                    txt_number,
                    ft.Text('Вырезать каждый n кадр', )
                ],
                alignment=ft.MainAxisAlignment.START
            ),
            ft.Row([
                ft.ElevatedButton("Выберите файл",
                                  on_click=lambda _: pick_file.pick_files(allow_multiple=True)),
                filename_txt,
            ],
                alignment=ft.MainAxisAlignment.START
            ),
            ft.Row([
                ft.ElevatedButton('Выберите место сохранения',
                                  on_click=lambda _: save_path.get_directory_path()),
                check_icon
            ]),
            ft.Row(
                [btn_run,
                 done_icon
                 ]),
            ft.Row([
                prb,
                done_txt
            ]),
        ]), ])
             )


if __name__ == "__main__":
    ft.app(target=main)
