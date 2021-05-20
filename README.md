[![PyPI version](https://badge.fury.io/py/phpypam.svg)](https://badge.fury.io/py/phpypam)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/ed3511c33a254bfe942777c9ef3251e3)](https://www.codacy.com/gh/codeaffen/phpypam/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=codeaffen/phpypam&amp;utm_campaign=Badge_Grade)
[![Documentation Status](https://readthedocs.org/projects/phpypam/badge/?version=latest)](https://phpypam.readthedocs.io/en/latest/?badge=latest)

As we started to develop phpipam-ansible-modules we used an existing python library for phpIPAM API. As we needed a good error handling and we don't expect a quick fix of existing project we started to develop our own library.

## installation

This library is hosted on [pypi.org](https://pypi.org/project/phpypam/), so you can simply use `pip` to install it.

~~~bash
pip install phpypam
~~~

Alternatively you can install it from source. You need to do the following:

~~~bash
$ git clone https://github.com/codeaffen/phpypam.git
Cloning into 'phpypam'...
remote: Enumerating objects: 1, done.
remote: Counting objects: 100% (1/1), done.
remote: Total 366 (delta 0), reused 0 (delta 0), pack-reused 365
Receiving objects: 100% (366/366), 88.57 KiB | 521.00 KiB/s, done.
Resolving deltas: 100% (187/187), done.
$ cd phpypam/
$ python setup.py install
~~~

## quick start

To start using `phpypam` you simply have to write some lines of code.

~~~python
import phpypam

pi = phpypam.api(
  url='https://ipam.example.com',
  app_id='ansible',
  username='apiuser',
  password='apiP455wd',
  ssl_verify=True
)
pi.get_entity(controller='sections')
~~~

## making api connection

To connect to phpIPAM API you need some parameter to authenticate against the phpIPAM instance.

Parameter | Description | Default |
:-------- | :---------- | :------ |
url | The URL to a phpIPAM instance. It includes the protocol (http or https). | |
app_id | The app_id which is used for the API operations. |
username | The `username` which is used to connect to API. | None |
password | The `password` to authenticate `username` against API. | None |
ssl_verify | Should certificate of endpoint verified or not. Useful if you use a self signed certificate. | True |

*Example* connect to api and request current token:

~~~python
connection_params = dict(
url='https://ipam.example.com',
  app_id='ansible',
  username='apiuser',
  password='apiP455wd',
  ssl_verify=True
)

pi = phpypam.api(**connection_params)

token = pi.get_token()
~~~

First of all you create a dictionary with the connection data. This dictionary will unpacked for creating a `phpypam.api` object.

If all went well you can use the `get_token` to get the currently valid token from API.

## get available controllers

To work with the phpIPAM api it is useful if you know all available controllers. To achieve this you can either read the api documentation or you can use the `controllers` method.

~~~python
controllers = pi.controllers()
~~~

The method returns a set with all supported controllers.

## get an entity

To get an entity the `get_entity` method has to be used.

~~~python
get_entity(controller, controller_path=None, params=None)
~~~

*Example* get a `section` by name:

~~~python
entity = pi.get_entity(controller='sections', controller_path='foobar')
~~~

This call returns a dictionary for the entity with the name `foobar`.

## create an entity

To create an entity the `create_entity` method has to be used.

~~~python
create_entity(controller, controller_path=None, data=None, params=None)
~~~

*Example* create a `section` if it does not exists:

~~~python
my_section = dict(
    name='foobar',
    description='new section',
    permissions='{"3":"1","2":"2"}'
)

try:
    entity = pi.get_entity(controller='sections', controller_path=my_section['name'])
except PHPyPAMEntityNotFoundException:
    print('create entity')
    entity = pi.create_entity(controller='sections', data=my_section)

~~~

In this example first we check if the section we work on already exists. If the PHPyPAMEntityNotFoundException is raised we create the entity.

## update an entity

To update an entity you have to use the `update_entity` method.

~~~python
update_entity(controller, controller_path=None, data=None, params=None)
~~~

*Example* update a `section` if it exists:

~~~python
my_section['description'] = 'new description'

entity = pi.get_entity(controller='sections', controller_path=my_section['name'])
pi.update_entity(controller='sections', controller_path=entity['id'], data=my_section)
~~~

To change data you have to modify the value of the desired key to the value you want. You can see the data is changed in the dict from the former example.
Then you get the entity to obtain its id to work on.

**Note:** All modifying operations need the id of an entity not the name.

In the last step you call `update_entity` and put the entity id in parameter `controller_path` with the `data` parameter you provide the fully entity description dictionary.

## delete an entity

To delete an entity you have to use the `delete_entity` method.

~~~python
delete_entity(controller, controller_path, params=None)
~~~

*Example* delete a existing section:

~~~python
entity = pi.get_entity(controller='sections', controller_path=my_section['name'])
pi.delete_entity(controller='sections', controller_path=entity['id'])
~~~

In this example you request the entity you had created/updated in the above examples.
After that you call `delete_entity` with the entity id from the request before.

## possible exceptions

* ***PHPyPAMInvalidCredentials*** - will be raised if something goes wrong with the authentication
* ***PHPyPAMEntityNotFoundException*** - will be raised if an entity does not exists
* ***PHPyPAMInvalidSyntax*** - will be raised for requests which will be answered with status code 400 from API
* ***PHPyPAMException*** - for any errors which we catch but no specific exception exists this exception wil be raised
