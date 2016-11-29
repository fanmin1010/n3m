# Testing

## Back-end Testing
For testing the back-end of the n3m application we use pytest. The benefits of our pytest setup are two-fold. First, the tests are easy to write, they use their own in memory sqlite database, and the results are returned quickly. Secondly, the tests output an html report that can be emailed out, displayed in a continuous integration environment, or more, This report contains both total test coverage, as well as individual test results.

### Running Back-end Tests
```
n3m@linux-n3m ~/git/n3m (master) $ python test.py --cov-report=term --cov-report=html --cov=application/ tests/
========================================================================================== test session starts ===========================================================================================
platform linux2 -- Python 2.7.12, pytest-3.0.1, py-1.4.31, pluggy-0.3.1
rootdir: /home/n3m/git/n3m, inifile: 
plugins: cov-2.3.1, flask-0.10.0
collected 5 items 

tests/test_api.py ....
tests/test_models.py .

---------- coverage: platform linux2, python 2.7.12-final-0 ----------
Name                            Stmts   Miss  Cover
---------------------------------------------------
application/__init__.py             0      0   100%
application/app.py                 34      1    97%
application/models.py              16      0   100%
application/utils/__init__.py       0      0   100%
application/utils/auth.py          28      0   100%
---------------------------------------------------
TOTAL                              78      1    99%
Coverage HTML written to dir htmlcov


======================================================================================== 5 passed in 5.22 seconds ========================================================================================

```
### Back-End Linting
From repo root execute:
```
./run_pylint
```

## Front-end Testing
For front-end testing we use the karma test runner with the mocha test runner and phantomjs as a web-driver. Karma was selected because it integrates well with multiple IDEs, CI environments, and testing frameworks. Also, it is really nice to have the option to switch from phantomjs to another real browser as the web-driver (like chrome). Mocha was selected because it is easy to use and there is a lot of documentation o support developer ramp-up time. 

Additionally, we use ESLint for static analysis of the front end javascript code. ESLint is a great tool because it is open source, pluggable, and offers a great set of defaults for both code smells and best-practice enforcement. 

### Running Front-end Tests
```
n3m@linux-n3m ~/git/n3m/static (master) $ npm run-script test                                                                                                                                             

> n3m@1.0.0 test /home/n3m/git/n3m/static
> karma start

Hash: f4683f5fa2953dc3a97c
Version: webpack 1.13.2
Time: 9ms
webpack: bundle is now VALID.
webpack: bundle is now INVALID.
Hash: 8f7bdb590b6a706a2572
Version: webpack 1.13.2
Time: 6906ms
                       Asset     Size  Chunks             Chunk Names
test/example/example.spec.js  41.2 kB       0  [emitted]  test/example/example.spec.js
chunk    {0} test/example/example.spec.js (test/example/example.spec.js) 38.1 kB [rendered]
webpack: bundle is now VALID.
04 10 2016 18:53:51.360:INFO [karma]: Karma v1.3.0 server started at http://localhost:9876/
04 10 2016 18:53:51.362:INFO [launcher]: Launching browser PhantomJS with unlimited concurrency
04 10 2016 18:53:51.412:INFO [launcher]: Starting browser PhantomJS
04 10 2016 18:53:51.963:INFO [PhantomJS 2.1.1 (Linux 0.0.0)]: Connected on socket /#FLjqy1YPmILy0J7hAAAA with id 96130731
.
PhantomJS 2.1.1 (Linux 0.0.0): Executed 1 of 1 SUCCESS (0.041 secs / 0 secs)
```

### Static analysis
```
> n3m@1.0.0 lint /home/n3m/git/n3m/static
> eslint src --fix

The react/require-extension rule is deprecated. Please use the import/extensions rule from eslint-plugin-import instead.

/home/n3m/git/n3m/static/src/actions/auth.js
   66:10  warning  Missing function expression name  func-names
   75:17  warning  Unexpected alert                  no-alert
  119:10  warning  Missing function expression name  func-names

✖ 3 problems (0 errors, 3 warnings)
