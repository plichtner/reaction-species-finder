# About

Online at https://reactions.gentleplants.com/

**Reaction Species Finder** is a web tool for searching a database (e.g. [hanford.dat](hanford.dat)) to find secondary species, gases and minerals given a set of primary species.

Built by Benny and Peter Lichtner with Python 3.13.3 using **[Hyperdiv](https://hyperdiv.io)**.

# Development

Install dependencies:

```
pip install -r
```

Then start the hyperdiv server:

```
python3 server.py
```

And point your web browser to http://localhost:8888

Bam!

# How to use a different database

[`hanford.dat`](hanford.dat) is the default reaction database. In a preprocessing step, we use [split_hanford_file.py](split_hanford_file.py) to split `hanford.dat` into `aq_spec.dat`, `gases.dat`, and `minerals.dat`.

You can use a different database file, but it needs to be structured in the same way, with aqueous reactions listed first, followed by gas reactions, and finally mineral reactions, each block ending in a line that starts with the characters `'null'`. See [split_hanford_file.py](split_hanford_file.py) for details.
