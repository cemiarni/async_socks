# A mininal proxy for National Weed Day

## Example usage:

Start proxy:
```
$ python weeday_proxy.py
Serving on ('127.0.0.1', 1080)
Happy Weed Day!
Received b'\x05\x02\x00\x01' from ('127.0.0.1', 53274)
Sent b'\x05\x02\x00\x01' to ('127.0.0.1', 53274)
Received b'\x05\x01\x00\x01\xac\xd9\x13n\x01\xa4' from ('127.0.0.1', 53274)
Stream 172.217.19.110:420 for ('127.0.0.1', 53274)
Close the connection for ('127.0.0.1', 53274)
```

Perform a request through port 420:
```
$ https_proxy=socks5://127.0.0.1:1080 curl -I https://www.youtube.com:420/watch?v=-MI3CKL4NMI
HTTP/2 200
content-type: text/html; charset=utf-8
x-content-type-options: nosniff
cache-control: no-cache, no-store, max-age=0, must-revalidate
pragma: no-cache
expires: Mon, 01 Jan 1990 00:00:00 GMT
date: Sat, 20 Apr 2024 12:19:15 GMT
content-length: 958695
strict-transport-security: max-age=31536000
x-frame-options: SAMEORIGIN
cross-origin-opener-policy: same-origin-allow-popups; report-to="youtube_main"
permissions-policy: ch-ua-arch=*, ch-ua-bitness=*, ch-ua-full-version=*, ch-ua-full-version-list=*, ch-ua-model=*, ch-ua-wow64=*, ch-ua-form-factor=*, ch-ua-platform=*, ch-ua-platform-version=*
report-to: {"group":"youtube_main","max_age":2592000,"endpoints":[{"url":"https://csp.withgoogle.com/csp/report-to/youtube_main"}]}
origin-trial: AmhMBR6zCLzDDxpW+HfpP67BqwIknWnyMOXOQGfzYswFmJe+fgaI6XZgAzcxOrzNtP7hEDsOo1jdjFnVr2IdxQ4AAAB4eyJvcmlnaW4iOiJodHRwczovL3lvdXR1YmUuY29tOjQ0MyIsImZlYXR1cmUiOiJXZWJWaWV3WFJlcXVlc3RlZFdpdGhEZXByZWNhdGlvbiIsImV4cGlyeSI6MTc1ODA2NzE5OSwiaXNTdWJkb21haW4iOnRydWV9
p3p: CP="This is not a P3P policy! See http://support.google.com/accounts/answer/151657 for more info."
server: ESF
x-xss-protection: 0
set-cookie: YSC=B-oDDZDy6Fk; Domain=.youtube.com; Path=/; Secure; HttpOnly; SameSite=none
set-cookie: __Secure-YEC=CgtscElyMl9LbGY2byjD5Y6xBjIOCgJIVRIIEgQSAgsMIFo%3D; Domain=.youtube.com; Expires=Tue, 20-May-2025 12:19:14 GMT; Path=/; Secure; HttpOnly; SameSite=lax
set-cookie: VISITOR_PRIVACY_METADATA=CgJIVRIIEgQSAgsMIFo%3D; Domain=.youtube.com; Expires=Tue, 20-May-2025 12:19:15 GMT; Path=/; Secure; HttpOnly; SameSite=none
set-cookie: VISITOR_INFO1_LIVE=; Domain=.youtube.com; Expires=Sun, 25-Jul-2021 12:19:15 GMT; Path=/; Secure; HttpOnly; SameSite=none
alt-svc: h3=":443"; ma=2592000,h3-29=":443"; ma=2592000
```
