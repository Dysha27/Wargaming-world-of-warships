Тестовое задание Wargaming.
В проекте два файла generate_data.py и test_wg.py. 
В generate_data реализовано следующие:
1)Генерация данных
2)Если база отутствует то он ее сам создает и наполняет (во время тестирования эта функция сокращала время на чистку базы)
В test_wg.py реализовано следующие:
1)Подготовительный этап (Suite Setup) в котором происходит сохранение дампа таблицы в формате json и рандомизация параметров исходной базы
2)Сами тесты я вынес отдельно. Отдельно тестирую соответствие характеристик у двигателя, корпуса, оружия и отдельно различие параметров у коробля (корпус, двигатель, оружие.)



