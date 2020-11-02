# phpypam: Python API client library for phpIPAM installation

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/6b89ed13b6694197944cddea94c953ed)](https://app.codacy.com/gh/codeaffen/phpypam?utm_source=github.com&utm_medium=referral&utm_content=codeaffen/phpypam&utm_campaign=Badge_Grade_Settings)

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
