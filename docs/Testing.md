# Testing

## Back-end Testing
For testing the back-end of the n3m application we use pytest. The benefits of our pytest setup are two-fold. First, the tests are easy to write, they use their own in memory sqlite database, and the results are returned quickly. Secondly, the tests output an html report that can be emailed out, displayed in a continuous integration environment, or more, This report contains both total test coverage, as well as individual test results.

### Running Back-end Tests
```
python test.py --cov-report=term --cov-report=html --cov=application/ tests/
```


## Front-end Testing
For front-end testing we use the karma test runner with the mocha test runner and phantomjs as a web-driver. Karma was selected because it integrates well with multiple IDEs, CI environments, and testing frameworks. Also, it is really nice to have the option to switch from phantomjs to another real browser as the web-driver (like chrome). Mocha was selected because it is easy to use and there is a lot of documentation o support developer ramp-up time. 

Additionally, we use ESLint for static analysis of the front end javascript code. ESLint is a great tool because it is open source, pluggable, and offers a great set of defaults for both code smells and best-practice enforcement. 

### Running Front-end Tests
```
npm run-script test
```

### Static analysis
```
npm run-script lint
```
