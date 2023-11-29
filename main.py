from function.cut_frame import frame_cut
import flet as ft
from function import globals as gl

# file = '3. конец линии.MP4'  # Имя видеофайла
# frame_to_cut = 5  # Колиичество пропускаемых кадров перед сохранением изображения

# frame_cut(file, frame_to_cut)


def main(page: ft.Page):

    def on_save_path_result(e: ft.FilePickerResultEvent):
        if e.path == None:
            return 0
        gl.save_path = e.path
        check_icon.name = ft.icons.CHECK
        check_icon.color = ft.colors.GREEN
        page.update()

    def open_error_diag():
        page.dialog = error_dialog
        error_dialog.open = True
        page.update()

    def frame_cutting(file: str, frame_to_cut: int, save_dir: str):
        if gl.path != '' and gl.save_path != '' and gl.filename != 'Файл не выбран' and gl.save_path != None:
            btn_run.disabled = True
            done_txt.visible = False
            prb.visible = True
            page.update()
            done_txt.value = 'Файл успешно обработан'
            try:
                frame_cut(gl.filename, int(txt_number.value), gl.save_path)
            except Exception as exp:
                done_txt.value = f'Произошла непредвиденная ошибка {exp}'
                prb.visible = False
                btn_run.disabled = False
                done_txt.visible = True
                page.update()

            done_icon.name = ft.icons.CHECK
            done_icon.color = ft.colors.GREEN
            prb.visible = False

            btn_run.disabled = False

            done_txt.visible = True
            page.update()
        else:
            open_error_diag()

    page.title = "Video cut"
    page.window_width = 500
    page.window_height = 300
    page.vertical_alignment = ft.MainAxisAlignment.NONE
    txt_number = ft.TextField(value="5", text_align=ft.TextAlign.CENTER, width=100, bgcolor=ft.colors.WHITE, color=ft.colors.BLACK)
    page.bgcolor = ft.colors.GREY_50
    btn_run = ft.ElevatedButton("Обработать файл",
                               on_click=lambda _: frame_cutting(gl.filename,
                                                                int(txt_number.value),
                                                                gl.save_path))
    filename_txt = ft.Text(str(f'Ваш файл: {gl.filename}'), color=ft.colors.BLACK)
    done_txt = ft.Text('', color=ft.colors.BLACK)
    done_txt.visible = False
    save_path = ft.FilePicker(on_result=on_save_path_result)
    page.overlay.append(save_path)
    check_icon = ft.Icon(name=ft.icons.CLOSE, color=ft.colors.RED)
    done_icon = ft.Icon(name=ft.icons.CLOSE, color=ft.colors.RED)
    error_dialog = ft.AlertDialog(
                title=ft.Text("Ошибка", color=ft.colors.RED),
                content=ft.Text("Заполните все данные")
            )

    def on_dialog_result(e: ft.FilePickerResultEvent):
        try:
            gl.filename = e.files[0].name
            gl.path = e.files[0].path
        except:
            pass
        filename_txt.value = str(f'Ваш файл: {gl.filename}')
        page.update()


    pick_file = ft.FilePicker(on_result=on_dialog_result)
    page.overlay.append(pick_file)
    prb = ft.ProgressBar(width=400, color=ft.colors.ORANGE, visible=False)
    page.update()
    page.add(
        ft.Row(
            [
            txt_number,
            ft.Text('Вырезать каждый n кадр', color=ft.colors.BLACK)
            ],
            alignment=ft.MainAxisAlignment.NONE
        ),
        ft.Row([
            ft.ElevatedButton("Выберите файл",
                              on_click=lambda _: pick_file.pick_files(allow_multiple=True)),
            filename_txt,
        ],
        alignment=ft.MainAxisAlignment.NONE
            ),
        ft.Row([
            ft.ElevatedButton('Выберите место сохранения',
                              on_click=lambda _: save_path.get_directory_path() ),
            check_icon
        ]),
        ft.Row(
            [btn_run,
             done_icon
             ]),
        ft.Row([
            prb,
            done_txt
        ])
    )

ft.app(target=main)
