# phpypam: Python API client library for phpIPAM installation

phpypam is intended to be a complete library for speaking with phpIPAM API.

Using `phpypam` is as easy as using the UI.

```python
import phpypam

pi = phpypam.api(
  url='https://ipam.example.com',
  app_id='ansible',
  username='apiuser',
  password='apiP455wd',
  ssl_verify=True
)
pi.get_entity(controller='sections')
```
