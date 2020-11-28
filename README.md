# AutoMoneyLover
> Automate Money Lover transaction logging

This package uses Selenium browser to download transactions that are parsed by Mint, then uses a command line interface to automatically log those tranactions into Money Lover.

## Installation

OS X & Linux:

```sh
npm i -g moneylover-cli
pip install mintapi
wget https://chromedriver.storage.googleapis.com/83.0.4103.39/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
rm chromedriver_linux64.zip
mv ./chromedriver ~/bin/chromedriver
cd AutoMoneyLover
pip -e install .
```

## Usage example

```sh
automoneylover:log kuangweiturbo "SAMPLE WALLET" --start_date 2020-01-01 --end_date 2020-01-15
```
* `SAMPLE WALLET` needs to be substituted to your own wallet name
* `--start_date` and `--end_date` are optional
    * Though they are highly recommended in order to avoid adding too many errorneous/miscategorized transations over a long period of time, which can be very cumbersome to correct in Money Lover

## Release History
* 0.1.0
    * The first proper release
* 0.0.1
    * Work in progress

## Meta

Kuang Wei – kuangwei0824@gmail.com

## Contributing

1. Fork it (<https://github.com/kuang-wei/AutoMoneyLover/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

<!-- Markdown link & img dfn's -->
[npm-image]: https://img.shields.io/npm/v/datadog-metrics.svg?style=flat-square
[npm-url]: https://npmjs.org/package/datadog-metrics
[npm-downloads]: https://img.shields.io/npm/dm/datadog-metrics.svg?style=flat-square
[travis-image]: https://img.shields.io/travis/dbader/node-datadog-metrics/master.svg?style=flat-square
[travis-url]: https://travis-ci.org/dbader/node-datadog-metrics
[wiki]: https://github.com/yourname/yourproject/wiki