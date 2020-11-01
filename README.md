# phpypam: Python API client library for phpIPAM installation

[![PyPI version](https://badge.fury.io/py/phpypam.svg)](https://badge.fury.io/py/phpypam)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/ed3511c33a254bfe942777c9ef3251e3)](https://www.codacy.com/gh/codeaffen/phpypam/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=codeaffen/phpypam&amp;utm_campaign=Badge_Grade)
[![Documentation Status](https://readthedocs.org/projects/phpypam/badge/?version=latest)](https://phpypam.readthedocs.io/en/latest/?badge=latest)

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
