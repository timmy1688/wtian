# Headers and timeouts shared by every proxied location.
# proxy_pass stays in nginx.conf so the /api rewrite can run first.
proxy_http_version 1.1;
proxy_set_header Connection "";
proxy_set_header Host $http_host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;

# Streaming interpretations can run for a few minutes; the API sends X-Accel-Buffering: no
proxy_read_timeout 300s;
proxy_send_timeout 300s;
