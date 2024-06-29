# 并行工作进程数，设置为 CPU 核心数
workers = 4
# 指定每个工作者的线程数
threads = 2
# 监听内网端口8000
bind = '0.0.0.0:8080'
# 设置守护进程,将进程交给supervisor管理
daemon = 'false'
# 工作模式协程
worker_class = 'uvicorn.workers.UvicornWorker'
# 设置最大并发量
worker_connections = 2000
# 设置进程文件目录
pidfile = '/var/run/gunicorn.pid'
# 设置访问日志和错误信息日志路径，修正拼写错误
accesslog = '/var/log/gunicorn_access.log'
errorlog = '/var/log/gunicorn_error.log'
# 设置日志记录水平
loglevel = 'info'
