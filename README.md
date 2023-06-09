# Проект "Помощник системного администратора"
Вы устроились работать системным администратором в небольшой офис. В ваши обязанности входит мониторинг работоспособности нескольких сайтов. Вы успешно настроили оповещение по почте статуса сервера от хостинга, однако оказалось, что этого недостаточно. И Вы решаете разработать небольшое приложение на Python для того, чтобы оно отправляло Вам сообщения в случае, если какой-либо из сайтов по какой-либо причине станет недоступен.
## Проектирование

<h4 style="text-align: center;">Диаграмма классов</h4>
<p align="center">
  <img src="class_diagram.png" />
</p>

## Запуск
### Запуск со своей машины
Желательно иметь Python версии 3.10 или выше.  
1) Установить зависимости
> pip install -r requirements.txt
2) Настроить список проверяемых адресов input.csv  
Заполняется форматом:
```
Host;Ports
Какой-тоIP;Порт1,Порт2
Какой-тоIP;
Какой-тоIP;Порт1
```
3) Запустить программу через файл app.py
> py app.py
4) Наслаждайтесь


### Запуск с виртуальной машины на Docker 
1) Собрать и запустить сборку используя конфигурацию Dockerfile