# Co Use It

Common needs sharing platform through 3 kind of activities:

- Co Buy It: buy commons in groups
- Co Share It: use commons in groups
- Co Stock It: stock commons in groups

And

- is open-source and open-data for improving innovation and letting users own their information
- handles multi-currency nest egg for easing grouped buyings ($, €, £, bitcoin, monnaie libre, etc.)
- is connected to same other services (such as leboncoin, pap, zilok, tipimi, my troc, kiloutou, etc.)
- eases grouped buyings with little merchants

## Development

According to platform/app development, the project contains folders:

- django: django project
- ionic2: ionic2 project
- reactnative: reactnative project

### Django

#### Requirements

- python2.7+
- virtualenv

#### Bash

```bash
$ git clone https://github.com/b3j0f/couseit
$ cd couseit/django
$ virtualenv venv
$ source venv/bin/activate
```

#### Development

```bash
$ PLATFORM=dev make install_deps all superuser run
```

#### Production

```bash
$ PLATFORM=prod BIND=0.0.0.0:80 make install_deps all superuser run
```

#### Content

- account: account application
- common: common application
- couseit: server application
- media: media folder
- node_modules: node modules folder
- requirements: dependencies
- static: static files
- templates: template files
- www: generated web site

### Ionic2

TODO

### Reactnative

TODO

## Perspectives

- add service support