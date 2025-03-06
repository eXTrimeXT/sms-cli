# sms-cli
#### Уставновка зависимостей 
```pip install toml argparse```

#### Mock-сервер
https://github.com/stoplightio/prism/releases

Будем использовать версию для Windows.

#### Запуск Mock-сервера
```.\prism-cli-win.exe mock .\sms-platform.yaml```

После запуска API будет доступно по адресу: http://localhost:4010/send_sms

#### Запуск клиента
```python cli.py --sender "123" --recipient "09321" --message "Hello, World!"```

Если Mock-сервер запущен, то при запуске программы в терминале отобразиться сообщение, которое содержит в себе код статуса = 200 и тело ответа:
> Status Code: 200
Response Body: {"status":"success","message_id":"123456"}
