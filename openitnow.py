import webbrowser, click, requests, json, os.path
from bs4 import BeautifulSoup
from lxml import etree

chrome = 'open -a /Applications/Google\ Chrome.app %s'

if os.path.isfile('sites.txt'):
    sites = json.load(open('sites.txt'))
else:
    sites = {
        'google': 'https://www.google.co.nz/#q=',
        'dovedale': 'http://dovedale.nz/search/?q={searchTerms}',
        'soundcloud': 'https://soundcloud.com/search?q={searchTerms}',
        'youtube': 'https://www.youtube.com/results?search_query={searchTerms}&page={startPage?}&utm_source=opensearch',
        'tumblr': 'https://www.tumblr.com/search/{searchTerms}',
        'amazon': 'https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords={searchTerms}'

    }
    json.dump(sites, open('sites.txt', 'w'))

json.dump(sites, open('sites.txt', 'w'))

def browse(site, query):
    url = sites[site]
    if '{startPage?}' in url:
        url = webbrowser.get(chrome).open(url.replace('{searchTerms}', query).replace('{startPage?}', '1'))
    else:
        url = webbrowser.get(chrome).open(url.replace('{searchTerms}', query))
    print(url)

@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    click.echo('Debug mode is %s' % ('on' if debug else 'off'))

@cli.command()
@click.argument('site')
@click.argument('query')
def search(site, query):
    click.echo('Searching %s!' % site)
    browse(site, query)

@cli.command()
@click.argument('query')
def searchall(query):
    for site in sites:
        click.echo('Searching %s!' % site)
        browse(site, query)

@cli.command()
@click.argument('name')
@click.argument('url')
def add(name, url):
    click.echo('Adding %s!' % name)

    r = requests.get('http://' + url)
    data = r.text

    soup = BeautifulSoup(data, 'html.parser')
    opensearch = str(soup.find('link', { 'type': 'application/opensearchdescription+xml', 'rel': 'search' }).get('href'))

    # Check if opensearch includes site url
    # Eg https://www.youtube.com/opensearch?locale=en_US
    if url not in opensearch:
        opensearch_request = requests.get('http://' + url + opensearch)
    else:
        opensearch_request = requests.get(opensearch)

    data = etree.fromstring(opensearch_request.content)
    template = data.xpath('//x:Url[1]/@template', namespaces={'x': 'http://a9.com/-/spec/opensearch/1.1/'})

    sites[name] = ''.join(template)

    json.dump(sites, open('sites.txt', 'w'))

@cli.command()
@click.argument('name')
@click.argument('url')
def add_manual(name, url):
    click.echo('Manually adding %s!' % name)

    sites[name] = url
    json.dump(sites, open('sites.txt', 'w'))

@cli.command()
@click.argument('name')
def remove(name):
    click.echo('Removing %s!' % name)

    del sites[name]
    json.dump(sites, open('sites.txt', 'w'))

@cli.command()
def list():
    click.echo('Listing all sites!')

    for site in sites:
        click.echo(site)

if __name__ == '__main__':
    cli()
