# openitnow
Search for shit on the web from your terminal

## How to get up and running

    $ git clone https://github.com/jakefb/openitnow
    $ cd openitnow
    $ pip install virtualenv
    $ virtualenv venv
    $ . venv/bin/activate
    $ pip install --editable .
    $ deactivate

## Usage

    Add a website
    $ venv/bin/python openitnow.py add github github.com

    Search a website
    $ venv/bin/python openitnow.py search github openitnow

    List all websites
    $ venv/bin/python openitnow.py list

    Search all websites
    $ venv/bin/python openitnow.py searchall 'cat videos'

    Remove a website
    $ venv/bin/python openitnow.py remove youtube

    Add a website manually if it does not support opensearch
    $ venv/bin/python openitnow.py add_manual bbc http://www.bbc.co.uk/search?q={searchTerms}
