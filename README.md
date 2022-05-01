# Dpscanner
应对各种无法找到目标真实IP，通过域名加端口的方式来获取其它web资产
基于域名的多线程web端口扫描器、title扫描、多线程、进度展示、端口批量扫描
![example](https://user-images.githubusercontent.com/58037546/166131144-cfc16e4f-2842-432c-9027-dffa2b82b743.png)

-u   指定一个域名
-p   指定端口，支持方式 20,80,443  或 20-500
-d   指定每次请求的延迟   默认为 1
-t   指定扫描的线程   默认为 10
