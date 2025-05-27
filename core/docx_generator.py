from io import BytesIO
from docxtpl import DocxTemplate
from docx import Document

def generate_document(template_path, context, employees_data):
    """
    Генерирует документ DOCX на основе шаблона и данных.

    :param template_path: Путь к файлу шаблона DOCX.
    :param context: Словарь с данными для основного шаблона (без списка сотрудников).
    :param employees_data: Список словарей с данными сотрудников.
    :return: BytesIO объект с финальным документом.
    """
    doc = DocxTemplate(template_path)
    
    # Рендеринг базового шаблона с основным контекстом
    doc.render(context)
    
    intermediate_output = BytesIO()
    doc.save(intermediate_output)
    intermediate_output.seek(0)
    
    # Загрузка через python-docx
    document = Document(intermediate_output)
    
    # Предполагаем, что таблица сотрудников - это первая таблица в документе
    # или имеет определенное количество столбцов, например, 5
    # Это нужно будет адаптировать под конкретный шаблон
    target_table = None
    for table in document.tables:
        # Пример: ищем таблицу с 5 столбцами. 
        # Условие может быть другим (например, по тексту в первой ячейке заголовка)
        if len(table.columns) == 5: # Замените 5 на актуальное количество столбцов
            target_table = table
            break
            
    if target_table:
        # Очистка строк-плейсхолдеров (кроме заголовка)
        # Предполагаем, что плейсхолдеры находятся в строках, начиная со второй (индекс 1)
        # и содержат специфичные Jinja-теги, например, '{{'
        rows_to_delete = []
        for i, row in enumerate(target_table.rows):
            if i == 0: # Пропускаем заголовок
                continue
            # Проверяем, есть ли Jinja-теги в ячейках строки
            contains_jinja_tag = False
            for cell in row.cells:
                if "{{" in cell.text and "}}" in cell.text:
                    contains_jinja_tag = True
                    break
            if contains_jinja_tag:
                rows_to_delete.append(row)

        for row_to_delete in rows_to_delete:
            # Удаление строки (в python-docx нет прямого метода delete_row, используем такой обход)
            tbl = row_to_delete._element.getparent()
            tbl.remove(row_to_delete._element)

        # Добавление строк вручную
        for emp_data in employees_data:
            row_cells = target_table.add_row().cells
            # Заполняем ячейки. Порядок и ключи должны соответствовать вашим данным
            # Пример для 5 столбцов:
            row_cells[0].text = str(emp_data.get('id', ''))
            row_cells[1].text = str(emp_data.get('full_name', ''))
            row_cells[2].text = str(emp_data.get('position', ''))
            row_cells[3].text = str(emp_data.get('department', ''))
            row_cells[4].text = str(emp_data.get('status', ''))
            # Добавьте больше row_cells[N].text = ... если у вас больше столбцов
    else:
        # Обработка случая, если таблица не найдена (опционально)
        print("Warning: Employee table not found in the document.")

    final_output = BytesIO()
    document.save(final_output)
    final_output.seek(0)
    
    return final_output

# Пример использования (для тестирования, потом убрать или закомментировать):
if __name__ == '__main__':
    # Создайте фиктивный шаблон 'template.docx' с Jinja-тегами:
    # {{ company_name }}
    # {{ report_date }}
    # И таблицей с заголовком и одной строкой-плейсхолдером:
    # | ID | ФИО            | Должность      | Отдел         | Статус        |
    # |----|----------------|----------------|---------------|---------------|
    # | {{ e.id }} | {{ e.full_name }} | {{ e.position }} | {{ e.department }} | {{ e.status }} |

    # doc_tpl = DocxTemplate() # Нужен реальный шаблон для создания
    # # ... код для создания простого шаблона template.docx ...
    # # doc_tpl.save("template.docx") # Раскомментируйте, если создаете шаблон программно

    example_context = {
        'company_name': 'Моя Компания',
        'report_date': '2024-07-25',
        # НЕ ВКЛЮЧАЕМ 'employees' здесь
    }
    
    example_employees = [
        {'id': 1, 'full_name': 'Иванов Иван', 'position': 'Инженер', 'department': 'IT', 'status': 'Работает'},
        {'id': 2, 'full_name': 'Петров Петр', 'position': 'Менеджер', 'department': 'Продажи', 'status': 'В отпуске'},
    ]

    try:
        # Убедитесь, что файл 'template.docx' существует в той же директории,
        # или укажите правильный путь к нему.
        # Для теста, создайте простой docx файл с именем template.docx
        # содержащий {{ company_name }} и таблицу с одной строкой и 5 колонками
        # с плейсхолдерами типа {{ e.id }} в ячейках.
        # final_doc_buffer = generate_document("template.docx", example_context, example_employees)
        # with open("generated_document.docx", "wb") as f:
        #     f.write(final_doc_buffer.getvalue())
        # print("Документ 'generated_document.docx' успешно создан.")
        print("Пример использования закомментирован. Для теста создайте шаблон 'template.docx'.")
    except Exception as e:
        print(f"Ошибка при генерации документа: {e}") 