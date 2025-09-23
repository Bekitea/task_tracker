#!/bin/bash

# Имя выходного файла
OUTPUT_FILE="collected_code.txt"

# Очищаем или создаём новый файл
> "$OUTPUT_FILE"

# Рекурсивно находим все .py файлы, исключая директорию .venv
find . -path "./.venv" -prune -o -name "*.py" -type f -print0 | while IFS= read -r -d '' file; do
    # Проверяем, что файл существует и не пустой (на всякий случай)
    if [[ -f "$file" ]]; then
        echo "========================================" >> "$OUTPUT_FILE"
        echo "FILE: $file" >> "$OUTPUT_FILE"
        echo "========================================" >> "$OUTPUT_FILE"
        cat "$file" >> "$OUTPUT_FILE"
        echo -e "\n\n" >> "$OUTPUT_FILE"  # Добавляем пустые строки для разделения
    fi
done

echo "Сборка завершена. Все Python-файлы (кроме .venv) сохранены в $OUTPUT_FILE"