# Contributing to Awesome Italia Startups

## Code of Conduct

Please read [the full text](https://github.com/italia-opensource/awesome-italia-startups/blob/main/CODE_OF_CONDUCT.md) so that you can understand what actions will and will not be tolerated.

### Join our Community

We have
- [Discord](https://discord.gg/CsPwpqTGDK)
- [Twitter]() coming soon.
- [Blog]() coming soon.

## Issues

We have two type of issue:

1. Bug report
2. Feature reqeust

**Please don't use the GitHub issue tracker for questions.** If you have any questions please contact us via Discord channel.

## Development

### Online one-click setup for contributing

Reuirements:

- Python >= 3.6
- utils: make, pip3

Setup env:

- clone the awesome-italia-startups repostory.
- run `make setup`
- run `source .activate`


## Pull Requests

*Pull requests can be used to add/edit/delete companies from the list.*

### How To Contribute with PRs

The new project must be added to the `/data` folder using a dedicated file in `kebab-case.json` format.
Subsequently, the `README.md` file is automatically generated, so you don't have to edit it manually.

1. Open `./data` directory
2. Add a new JSON file for the new project (file name should be a slugified version of the project name)
3. File content should respect the following format:

```JSON
{
  "name": "Test",
  "repository_organization_url": "https://www.github.com/test/name-of-repo", // no required
  "site_url": "https://www.test.com",
  "type": "B2B",
  "market": "Fintech",
  "description": "lorem ipsum",
  "tags": [
    "python", "aws"
  ],
  "foundation_year": "YYYY" // required data >= 2010
}
```

#### Allowed Type of startups

- B2B
- B2C
- C2C
- D2C
- Consulting
- Other

#### Allowed Market of startups

- Food
- Health
- Automotive
- Fintech
- Energy
- AI
- Biotech
- Ecommerce
- Software
- Hardware
- Service
- Insurance
- Other

#### Tags

The maximum number of tags is 20. This rule is necessary to avoid format problems with the MarkDown file.
