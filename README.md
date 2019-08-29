# note_monitor
something remark for monitor project

# ffmpeg
push stream for rtmp

```
ffmpeg -i 'rtsp://admin:admin@192.168.0.1:8554/stream1' -vcodec lib264 -acodec aac -f flv 'rtmp://127.0.0.1/live/com1'
ffmpeg -re -i '/root/live.mp4' -vcodec copy -acodec copy -f flv 'rtmp://127.0.0.1/live/com1'
```

# livego
stream server for rtmp

简单高效的直播服务器 https://github.com/mh88/livego

# FLV.js
video player plugin for website display

An HTML5 Flash Video (FLV) Player written in pure JavaScript without Flash. LONG LIVE FLV!

https://github.com/bilibili/flv.js

# InsightFace
a demo of insignface network using mxnet

https://github.com/mh88/insightface_for_face_recognition

office website

https://github.com/deepinsight/insightface

# Frp
A fast reverse proxy to help you expose a local server behind a NAT or firewall to the internet.

https://github.com/fatedier/frp

# Demo
![](./attachments/monitor_1.png)
