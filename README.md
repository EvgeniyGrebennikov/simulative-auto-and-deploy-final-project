## Автоматизация обработки данных магазина ##
### <b><i> Задание </i></b> ###
Предварительно необходимо написать скрипт, который генерирует N (кол-во магазинов) выгрузок в формате csv в папку data/. Формат выгрузки будет указан ниже. 

Автоматизируйте этот скрипт так, чтобы он работал каждый день, кроме воскресенья. Вы можете это сделать с помощью того инструмента, который вам удобен - cron или планировщик Windows (зависит от вашей операционной системы).

Создайте базу данных для хранения этих данных.

Напишите скрипт, который будет забирать данные из этой папки и заносить их в базу данных. Учтите, что в папке могут находиться и лишние файлы - игнорируйте их.

Автоматизируйте этот скрипт, чтобы он работал каждый день.

Файлы с выгрузками должны называться {{shop_num}}_{{cash_num}}.csv. Здесь {{shop_num}} - номер магазина, а {{cash_num}} - номер кассы. В одном магазине может быть много касс - у каждой своя выгрузка. Пример названия: 11_2.csv - 11 магазин, 2 касса.

Формат выгрузки:
- doc_id - численно-буквенный идентификатор чекаж
- item - название товараж
- category - категория товара (бытовая химия, текстиль, посуда и т.д.)ж
- amount - кол-во товара в чекеж
- price - цена одной позиции без учета скидкиж
- discount - сумма скидки на эту позицию (может быть 0).

Итоговая база данных

     <img width="302" alt="scheme_shops_db" src="https://github.com/user-attachments/assets/c04fc89c-c77f-498b-8fd7-9f689a1d0671" />

### <b><i> Запуск проекта </i></b> ###

