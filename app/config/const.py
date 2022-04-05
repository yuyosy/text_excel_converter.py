config_string = """# Config
name: default_config

# アプリケーション設定

presets:
    default:
        name: Excel-Text Convert
        description: Excel <--> Text
        options:
            definitions:
                folder: 'definitions'
                file_pattern: '*.json'
                version: '*'
                encoding: 'utf-8'
            templates:
                folder: 'templates'
                file_pattern: '*.xlsx'


# ログ出力設定
logging:
    version: 1
    root:
        level: NOTSET
    loggers:
        app:
            handlers: [stdiohandler,filehandler]
            qualname: app
        file:
            handlers: [filehandler]
            qualname: file
    handlers:
        stdiohandler:
            class: logging.StreamHandler
            level: INFO
            formatter: basic
            stream: ext://sys.stdout
        filehandler:
            class: logging.handlers.RotatingFileHandler
            level: NOTSET
            formatter: detail
            filename: app.log
            encoding: utf-8
            maxBytes: 5242880 # 5*1024*1024=5242880(5MB)
            backupCount: 0
    formatters:
        detail:
            class: logging.Formatter
            format: '%(asctime)s\t%(levelno)s\t%(levelname)s\t%(name)s\t%(pathname)s\t%(module)s:%(lineno)d\t%(message)s'
            datefmt: '%Y/%m/%d %H:%M:%S'
        basic:
            format: '[%(levelname)s] %(message)s'
"""