// postgresql 
su - postgres
psql
\l              //list database
\c cam_config   //change database
\q              //exit
\d              //view tables relations
\d config       //view table config relations

//
netstat -tunlp | grep 'listen'


//Linux 定时任务 删除指定时间前的文件操作
|- 新建一个可执行文件
|-- touch /usr/local/bin/clear_log 
|-- chmod 777 clear_log
|
|- 编辑 clear_log 文件，在其中添加类似下面的代码
|-- #!/bin/sh
| find /mnt/www/Application/Runtime/Logs  -mtimes +10 -name *.* -exec rm -rf {} \;
| find /tmp  -type f -mmin 120 -name *.log -exec rm -rf {} \;
|---
| 解析：
|  find 后面紧跟的是要查找的目录，. 表示当前目录
|  -type f：	指定查找对象为文件
|  -name *.log：	指定查找对象名称以.log结尾
|  -mtime +10:	 查找10天以前的老文件
|  -mmin +120:	 查找120分钟（两小时）以前的老文件
|  -exec rm -rf {} ;  :执行删除命令，这句注意，后面有个 {} ; 是必须的
|---
|
|- 将 clear_log 文件加入到系统计划任务
|-- # crontab -e
|-- # 每分钟执行一次
| */1 * * * * /usr/local/bin/clear_log
|-- # 每天凌晨0点10分执行auto-del-7-days-ago-log.sh文件进行数据清理任务
| 10 0 * * * /opt/soft/log/auto-del-7-days-ago-log.sh
|-- # 每五分钟执行 */5 * * * *
|-- # 每五小时执行 0 */5 * * *
|-- # 每天执行 0 0 * * *
|-- # 每周执行 0 0 * * 0
|-- # 每月执行 0 0 1 * *
|-- # 每年执行 0 0 1 1 *
|-- # 每个月的每隔10天 0 0 */10 * *
|-- # 下午6点到早上6点，每隔15分钟执行一次 0,15,30,45 18-06 * * *
|-- # 每两小时 重启 * */2 * * * /etc/init.d/service restart
|
|
|- 保存代码后 ,再执行下面的命令，以保证计划任务的生效
|-- # /etc/rc.d/init.d/crond restart  
|
|- crontab文件格式
|-- [!attachment]
|
|- 可通过 df -h 查看磁盘使用情况
|- 通过 du -h --max-depth=1 查看对应目录下文件的资源占用情况

CentOS 7 - 配置服务实现开机自启动
cd /etc/systemd/system
sudo vim myapp.service

添加以下配置
[Unit]
# 这里添加你的服务描述
Description=myapp
After=syslog.target

[Service]
# 这里更改为你的用户名
User=myapp
# 这里路径为你的spring boot工程的jar包路径
ExecStart=这里是需要执行的命令
SuccessExitStatus=143

[Install]
WantedBy=multi-user.target

设置为系统服务，开机自启动
systemctl enable myapp.service


Ubuntu 创建自定义服务 并设置开机自启
# cd /etc/rc.d
# touch myService

编辑创建的服务脚本，填入以下模板
#!/bin/bash

## Fill in name of program here.
PROG="myService"
PROG_PATH="/usr/local/myServer" ## Not need, but sometimes helpful (if $PROG resides in /opt for example).
PROG_ARGS="" 
PID_PATH="/var/run/"

start() {
    if [ -e "$PID_PATH/$PROG.pid" ]; then
        ## Program is running, exit with error.
        echo "Error! $PROG is currently running!" 1>&2
        exit 1
    else
        ## Change from /dev/null to something like /var/log/$PROG if you want to save output.
        $PROG_PATH/$PROG $PROG_ARGS 2>&1 >/var/log/$PROG &
    $pid=`ps ax | grep -i 'myService' | sed 's/^\([0-9]\{1,\}\).*/\1/g' | head -n 1`

        echo "$PROG started"
        echo $pid > "$PID_PATH/$PROG.pid"
    fi
}

stop() {
    echo "begin stop"
    if [ -e "$PID_PATH/$PROG.pid" ]; then
        ## Program is running, so stop it
    pid=`ps ax | grep -i 'myService' | sed 's/^\([0-9]\{1,\}\).*/\1/g' | head -n 1`
    kill $pid

        rm -f  "$PID_PATH/$PROG.pid"
        echo "$PROG stopped"
    else
        ## Program is not running, exit with error.
        echo "Error! $PROG not started!" 1>&2
        exit 1
    fi
}

## Check to see if we are running as root first.
## Found at http://www.cyberciti.biz/tips/shell-root-user-check-script.html
if [ "$(id -u)" != "0" ]; then
    echo "This script must be run as root" 1>&2
    exit 1
fi

case "$1" in
    start)
        start
        exit 0
    ;;
    stop)
        stop
        exit 0
    ;;
    reload|restart|force-reload)
        stop
        start
        exit 0
    ;;
    **)
        echo "Usage: $0 {start|stop|reload}" 1>&2
        exit 1
    ;;
esac
