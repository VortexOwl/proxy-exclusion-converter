# Proxy exclusion converter

Использование прокси-сервера в наше время крайне полезно и часто необходимо. Прокси может требоваться для подключения к корпоративной сети или быть полезным для анонимного серфинга в интернете.

Однако при работе с прокси может возникнуть необходимость в составлении списка исключений. Например, некоторые сайты могут блокироваться при подключении через прокси. Кроме того, вы сами можете не хотеть, чтобы информация о посещении определенных ресурсов сохранялась на прокси-сервере.

Проблема в том, что чаще всего списки исключений в настройках прокси представляют собой обычное текстовое поле, которое крайне сложно структурировать. Без четкой структуры легко забыть, какие именно домены были внесены в список и к каким сервисам они относятся.

Гораздо удобнее хранить такую информацию в структурированном виде — например, в Markdown-файле. Моя программа позволяет преобразовать Markdown-файл с определенной структурой в простой текстовый файл, где домены будут перечислены через запятую. Такой формат легко читается и может быть напрямую вставлен в поле исключений прокси.

## Как использовать программу

1. Скачайте и распакуйте загруженный ZIP-архив в отдельную папку.
2. Запустите файл `proxy-exclusion-combinator.exe`.
   После запуска откроется окно терминала, а в браузере автоматически запустится веб-интерфейс по адресу `localhost:8000`.
3. Работайте через браузер. Программа будет активна до тех пор, пока вы не закроете окно терминала или не остановите её командой `Ctrl + C`.
4. В поле "Proxy exception" выберите ваш Markdown-файл.
5. Нажмите кнопку  "Execute" .
6. Программа обработает файл и покажет кнопку  "Download file" , с помощью которой вы сможете скачать готовый список исключений для прокси.

## Пример Markdown-файла

```md
# Базовые
* 127.0.0.1, js-agent.newrelic.com, .hcaptcha.com, fast.fonts.net, .akamaihd.net, .osano.com,
---

# Браузеры
## FireFox
* accounts.firefox.com, mozilla.com, mozilla.org,

## Vivaldi
* themes.vivaldi.net,
---

# Поисковые системы
## Google
* .google.com, .gstatic.com, .googletagmanager, .googleapis.com, lh3.googleusercontent.com,

## Yandex
* .yastatic.net, .yclients.com, .yandex.com, .yandex.net, .naydex.net, storage.yandexcloud.net,

# Duckduckgo
* duckduckgo.com, duck.ai,
---

# AI
## Qwen
* .qwen.ai,

## Deepseek
* .deepseek.com
---
```

## Пример списка исключений для прокси

```
 127.0.0.1, js-agent.newrelic.com, .hcaptcha.com, fast.fonts.net, .akamaihd.net, .osano.com, accounts.firefox.com, mozilla.com, mozilla.org, themes.vivaldi.net, .google.com, .gstatic.com, .googletagmanager, .googleapis.com, lh3.googleusercontent.com, .yastatic.net, .yclients.com, .yandex.com, .yandex.net, .naydex.net, storage.yandexcloud.net, duckduckgo.com, duck.ai, .qwen.ai, .deepseek.com
```
