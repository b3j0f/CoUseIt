Co Use It
---------

Common needs sharing platform through 3 kind of activities:

- Co Buy It: buy commons in groups
- Co Share It: use commons in groups
- Co Stock It: stock commons in groups

# Development

- django: django project
- ionic2: ionic2 project
- reactnative: reactnative project

## Django

### Requirements

- python2.7+
- virtualenv

$ git clone https://github.com/b3j0f/couseit
$ cd couseit/django
$ virtualenv venv
$ source venv/bin/activate

### Development

PLATFORM=dev make install_deps all superuser run

### Production

PLATFORM=prod BIND=0.0.0.0:80 make install_deps all superuser run

### Content

- account: account application
- common: common application
- couseit: server application
- media: media folder
- node_modules: node modules folder
- requirements: dependencies
- static: static files
- templates: template files
- www: generated static web site
