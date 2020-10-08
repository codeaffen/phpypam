# pyhpipam: phpIPAM API bindings for python

pyhpipam is intended to be a complete library for speaking with phpIPAM API.

Using `pyhpipam` is as easy as using the UI.

```
pi = pyhpipam.api(
  url='https://ipam.example.com',
  app_id='ansible',
  username='apiuser',
  password='apiP455wd',
  ssl_verify=True
)
pi.search_entity(controller='sections')
```
