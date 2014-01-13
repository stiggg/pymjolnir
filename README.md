pymjolnir
=========

Website load tester written in python.

# Usage

Simple example:
```
python src/app.py <url>
```

Output is CSV formatted data, with structure like this:
```
<concurrent requests>,<mean response time in ms>,<standard deviation>
```

Output is written to stdout by default. You can set output file with -o:
```
python src/app.py <url> -o /tmp/punish.csv
```

By default, pymjolnir runs requests with 8, 16, 32, 64, 128 and 256 concurrent users.
Request amounts are 10 * concurrency. Concurrencies can be overridden with -c parameter:
```
python src/app.py <url> -c 10 100 200 500
```

Launching with just --help shows usage help:
```
python src/app.py --help
```

# Installation

```
git clone git@github.com:stiggg/pymjolnir.git
cd pymjolnir
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

# Licence

[MIT](LICENCE)