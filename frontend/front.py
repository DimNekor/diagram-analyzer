import os
import requests
import gradio as gr
from PIL import Image
from io import BytesIO

API_URL = os.getenv("API_URL", "http://localhost:8000")

def call_backend(pil_img: Image.Image, language: str, diagram_type_hint: str):

    if pil_img is None:
        return "Загрузите изображение", {}

    buf = BytesIO()
    pil_img.save(buf, format="PNG")
    buf.seek(0)

    files = {
        "image": ("diagram.png", buf, "image/png")
    }
    data = {
        "language": language,
        "diagram_type_hint": diagram_type_hint
    }

    r = requests.post(f"{API_URL}/v1/process", files=files, data=data, timeout=60)
    r.raise_for_status()
    result = r.json()

    steps_text = "\n".join([f"{s['step']}. {s['action']}" for s in result.get("steps", [])])
    return steps_text, result

# Создаем интерфейс с Gradio Blocks для большей гибкости
with gr.Blocks(title="Загрузка файлов", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 📤 Загрузка и обработка файлов
    
    Загрузите диаграмму, и приложение выведет алгоритм, который описывает диаграмма, по шагам.
    """)
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### Выберите файл")
            file_input = gr.Image(
                label="Загрузить файл",
                type="pil"
            )
            language = gr.Dropdown(["ru", "en"], value="ru", label="Язык")
            hint = gr.Dropdown(["auto", "bpmn", "uml", "c4", 'png', 'jpg'], value="auto", label="Тип графика")

    with gr.Row():
        with gr.Column():
            gr.Markdown("### Результат обработки")
            output_text = gr.Textbox(
                label="Алгоритм в текстовом виде",
                lines=10,
                interactive=False,
                placeholder="Загрузите файл, чтобы увидеть результат обработки..."
            )

        with gr.Column():
            gr.Markdown("### JSON")
            output_json = gr.Textbox(
                label="Полный ответ",
                lines=10,
                interactive=False,
                placeholder="Загрузите файл, чтобы увидеть полный json-ответ..."
            )
    
    # Обработчик события загрузки файла
    file_input.change(
        fn=call_backend,
        inputs=[file_input, language, hint],
        outputs=[output_text, output_json]
    )
    
    # Кнопка очистки
    with gr.Row():
        clear_btn = gr.ClearButton(
            [file_input, output_text],
            value="Очистить"
        )

demo.launch(
    server_name="127.0.0.1",
    server_port=7860,
    share=False,
    show_error=True
)