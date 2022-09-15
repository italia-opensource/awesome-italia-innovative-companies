import json
import os
import sys

import click
import fastjsonschema
from snakemd import Document
from snakemd.generator import InlineText

ALLOWED_TYPE = [
    'B2B',
    'B2C',
    'C2C',
    'D2C',
    'Other',
]

ALLOWED_MARKET = [
    'Fintech',
    'Energy',
    'AI',
    'Biotech',
    'Ecommerce',
    'Software',
    'Hardware',
    'Other',
    # TODO: in progress (crete issues if missing your market)
]

JSONSCHEME_COMPILE = fastjsonschema.compile(
    definition={
        '$schema': 'https://json-schema.org/draft/2019-09/schema',
        'type': 'object',
        'properties': {
            'name': {'type': 'string'},
            'repository_organization_url': {'type': 'string', 'format': 'uri'},
            'site_url': {'type': 'string', 'format': 'uri'},
            'description': {'type': 'string', 'minLength': 5, 'maxLength': 254},
            'type': {'type': 'string', 'enum': ALLOWED_TYPE},
            'market': {'type': 'string', 'enum': ALLOWED_MARKET},
            'foundation_year': {'type': 'string', 'format': 'date'},
            'tags': {
                'type': 'array',
                'minItems': 1,
                'maxItems': 20,
                'uniqueItems': True,
                'items': {
                    'type': 'string',
                    'maxLength': 24
                }
            }
        },
        'required': [
            'name',
            'site_url',
            'type',
            'market'
            'tags',
        ],
        'additionalProperties': False
    }
)


def abspath(*args, os_path=True, separator='/'):
    path = separator.join(args)
    if os_path is True:
        from pathlib import Path

        return str(Path(path))
    return path


def json_validate(filename: str):
    if not os.path.exists(filename):
        raise FileNotFoundError(filename=filename)

    with open(filename) as fh:
        content = json.load(fh)

    return JSONSCHEME_COMPILE(content)


def check(loaded: list):
    values = []
    for name, filename in loaded:
        print(f'Check: {name}')
        values.append(json_validate(filename))

    return values


def build(data):
    def _header(doc, data):
        doc.add_header('Italia Opensource')
        doc.add_paragraph(f"""
            <img src='https://img.shields.io/badge/startups-{len(data)}-green'>
            <img src='https://img.shields.io/github/last-commit/italia-opensource/awesome-italia-startups/main'>
        """)

        doc.add_paragraph(
            'Awesome Italia Startups is a list of italian startups.')
        doc.add_paragraph(
            'The repository intends to give visibility to startups and stimulate the community to contribute to growing the ecosystem.')
        doc.add_paragraph(
            'Please read the contribution guidelines before opening a pull request or contributing to this repository') \
            .insert_link('contribution guidelines', 'https://github.com/italia-opensource/awesome-italia-startups/blob/main/CONTRIBUTING.md')

        doc.add_header('Mantained by', level=3)
        doc.add_paragraph("""- **[Fabrizio Cafolla](https://github.com/FabrizioCafolla)**
        <a href="https://www.buymeacoffee.com/fabriziocafolla" target="_blank"><img  align="right" src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 30px !important; width: 150px !important" ></a>""")

    def _projects(doc, data):
        def _repository(repository_platform, repositories_url, license):
            license = f'<img align="right" src="https://img.shields.io/static/v1?label=license&message={license}&color=orange" alt="License">'
            if repository_platform == 'github':
                repositories_url = '/'.join(repository_url.replace(
                    'https://github.com/', '').split('/')[0:2])
                stars = f'<img align="right" src="https://img.shields.io/github/stars/{repositories_url}?label=%E2%AD%90%EF%B8%8F&logo=github" alt="Stars">'
                issues = f'<img align="right" src="https://img.shields.io/github/issues-raw/{repositories_url}" alt="Issues">'
                return f'{stars}<br>{issues}<br>{license}'

            if repository_platform == 'bitbucket':
                repositories_url = '/'.join(repository_url.replace(
                    'https://bitbucket.org/', '').split('/')[0:2])
                issues = f'<img align="right" src="https://img.shields.io/bitbucket/issues-raw/{repositories_url}" alt="Issues">'
                return f'{issues}<br>{license}'

            if repository_platform == 'gitlab':
                repositories_url = '/'.join(repository_url.replace(
                    'https://gitlab.com', '').split('/')[0:2])
                stars = f'<img align="right" src="https://img.shields.io/gitlab/stars/{repositories_url}?label=%E2%AD%90%EF%B8%8F&logo=gitlab" alt="Stars">'
                issues = f'<img align="right" src="https://img.shields.io/gitlab/issues/open-raw/{repositories_url}" alt="Issues">'
                return f'{stars}<br>{issues}<br>{license}'

        doc.add_header('Startups', level=3)

        doc.add_header('Website view', level=4)
        doc.add_paragraph(
            'italia-opensource.github.io').insert_link('italia-opensource.github.io', 'https://italia-opensource.github.io/awesome-italia-startups/')

        doc.add_header('List', level=4)
        table_content_project = []

        repositories_url = []

        for item in data:
            repository_url = item['repository_url']

            if item.get('repository_url') in repositories_url:
                raise Exception(
                    f"Project {item['name']} ({repository_url}) already exist")

            name = item['name'].title()
            repository = _repository(
                item['repository_platform'], item['repository_url'], item['license'])
            tags = ', '.join(item['tags'])
            description = item.get('description', '')
            if len(description) > 59:
                description = description[0:60] + ' [..]'

            table_content_project.append([
                InlineText(name, url=item.get('site_url')),
                InlineText(repository, url=repository_url),
                tags,
                description
            ])
            repositories_url.append(repository_url)

        doc.add_table(
            ['Name', 'Repository', 'Stack', 'Description'],
            table_content_project
        )

    def _contributors(doc):
        doc.add_header('Contributors', level=3)
        doc.add_paragraph("""
            <a href="https://github.com/italia-opensource/awesome-italia-startups/graphs/contributors">
                <img src="https://contrib.rocks/image?repo=italia-opensource/awesome-italia-startups" />
            </a>
        """)

        doc.add_header('License', level=3)
        doc.add_paragraph(
            'The project is made available under the GPL-3.0 license. See the `LICENSE` file for more information.')

    doc = Document('README')

    _header(doc, data)
    _projects(doc, data)
    _contributors(doc)

    doc.output_page()


@click.command()
@click.option('--render', default=False, help='Make data render', is_flag=True)
@click.option('--output', default=False, help='Make data output', is_flag=True)
def main(render, output):
    data = os.listdir(abspath(os.path.dirname(
        os.path.abspath(__file__)), 'data'))

    loaded = []
    for project in data:
        if not project.endswith('.json'):
            raise Exception(f'File {project} is not json')
        item = (project.replace('.json', ''), abspath(
            os.path.dirname(os.path.abspath(__file__)), 'data', project))
        loaded.append(item)

    loaded = sorted(loaded, key=lambda tup: tup[0])
    parsed = check(loaded)

    if render:
        build(parsed)

    if output:
        with open('website/src/data/outputs.json', 'w+') as file_output:
            file_output.write(json.dumps({'data': parsed}))


if __name__ == '__main__':
    sys.exit(main())
