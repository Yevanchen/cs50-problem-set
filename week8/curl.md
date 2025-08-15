curl -I https://www.harvard.edu/
注意这个命令的输出返回了服务器响应的所有HTTP头信息。

server: nginx
date: Fri, 15 Aug 2025 08:56:17 GMT
content-type: text/html; charset=UTF-8
vary: Accept-Encoding
host-header: a9130478a60e5f9135f765b23f26593b
link: <https://www.harvard.edu/wp-json/>; rel="https://api.w.org/"
link: <https://www.harvard.edu/wp-json/wp/v2/pages/6392>; rel="alternate"; title
="JSON"; type="application/j
son"
                            link: <https://www.harvard.edu/>; rel=shortlink
x-rq: hkg1 0 30 9980
cache-control: max-age=300, must-revalidate
x-cache: HIT
accept-ranges: bytes



curl -I https://harvard.edu
🐍 base  chenxiefan@chenxiefandeMacBook-Pro  /Applications/Development/cs50/cs50-problem-set   main  c
url -I https://harvard.edu                                                                                 c
url -I https://harvard.edu
HTTP/2 301 
server: nginx
date: Fri, 15 Aug 2025 08:57:13 GMT
content-type: text/html; charset=utf-8
location: https://www.harvard.edu/
x-rq: hkg1 0 30 9980
x-cache: HIT

这是一个301永久重定向响应。服务器告诉浏览器："这个页面已经永久移动到新位置了。"

关键信息：
- 状态码：301 Moved Permanently
- Location头：https://www.harvard.edu/ 

有www和没有www的区别：
1. harvard.edu（无www）→ 重定向到 → www.harvard.edu（有www）
2. 这是一个常见的SEO和品牌策略
3. 统一所有流量到一个规范的域名（www版本）
4. 避免重复内容问题，搜索引擎会认为它们是同一个网站






curl -I http://www.harvard.edu/
🐍 base  chenxiefan@chenxiefandeMacBook-Pro  /Applications/Development/cs50/cs50-problem-set   main  c
url -I http://www.harvard.edu/                                                                             c
url -I http://www.harvard.edu/
HTTP/1.1 301 Moved Permanently
Server: nginx
Date: Fri, 15 Aug 2025 08:58:06 GMT
Content-Type: text/html
Content-Length: 162
Connection: keep-alive
Location: https://www.harvard.edu/

这是HTTP到HTTPS的重定向：

关键区别：
- 请求协议：HTTP (不安全) → 重定向到 → HTTPS (安全)
- 状态码：301 Moved Permanently
- Location头：https://www.harvard.edu/ (注意协议变成了https)
- HTTP版本：HTTP/1.1 (而不是HTTP/2)

安全策略：
1. 强制HTTPS：现代网站都会将所有HTTP流量重定向到HTTPS
2. 保护数据传输：HTTPS加密所有通信内容
3. SEO友好：搜索引擎优先索引HTTPS版本
4. 浏览器安全警告：现代浏览器会标记HTTP网站为"不安全"

总结三个重定向链：
1. harvard.edu → www.harvard.edu (域名规范化)
2. http://www.harvard.edu → https://www.harvard.edu (协议升级)
3. 最终目标：https://www.harvard.edu (安全的规范域名)