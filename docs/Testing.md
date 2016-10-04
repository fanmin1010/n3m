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
n3m@linux-n3m ~/git/n3m/static (master) $ npm run-script lint

> n3m@1.0.0 lint /home/n3m/git/n3m/static
> eslint src

The react/require-extension rule is deprecated. Please use the import/extensions rule from eslint-plugin-import instead.

/home/n3m/git/n3m/static/src/actions/auth.js
   66:12  warning  Missing function expression name  func-names
   75:21  warning  Unexpected alert                  no-alert
  119:12  warning  Missing function expression name  func-names

/home/n3m/git/n3m/static/src/components/About.js
  24:9   error  Expected indentation of 16 space characters but found 0  react/jsx-indent
  25:1   error  Line 25 exceeds the maximum line length of 100           max-len
  25:9   error  Expected indentation of 16 space characters but found 0  react/jsx-indent
  26:1   error  Line 26 exceeds the maximum line length of 100           max-len
  26:9   error  Expected indentation of 16 space characters but found 0  react/jsx-indent
  27:1   error  Line 27 exceeds the maximum line length of 100           max-len
  27:9   error  Expected indentation of 16 space characters but found 0  react/jsx-indent
  28:10  error  Expected indentation of 16 space characters but found 0  react/jsx-indent
  29:1   error  Line 29 exceeds the maximum line length of 100           max-len
  29:10  error  Expected indentation of 16 space characters but found 0  react/jsx-indent
  30:1   error  Line 30 exceeds the maximum line length of 100           max-len
  30:10  error  Expected indentation of 16 space characters but found 0  react/jsx-indent
  31:1   error  Line 31 exceeds the maximum line length of 100           max-len
  31:10  error  Expected indentation of 16 space characters but found 0  react/jsx-indent
  32:1   error  Line 32 exceeds the maximum line length of 100           max-len
  32:10  error  Expected indentation of 16 space characters but found 0  react/jsx-indent
  33:10  error  Expected indentation of 16 space characters but found 0  react/jsx-indent
  34:1   error  Line 34 exceeds the maximum line length of 100           max-len
  34:10  error  Expected indentation of 16 space characters but found 0  react/jsx-indent
  35:1   error  Line 35 exceeds the maximum line length of 100           max-len
  35:10  error  Expected indentation of 16 space characters but found 0  react/jsx-indent

/home/n3m/git/n3m/static/src/components/ProfileView.js
   6:25  error  Absolute imports should come before relative imports      import/imports-first
   7:8   error  'Avatar' is defined but never used                        no-unused-vars
   7:20  error  Absolute imports should come before relative imports      import/imports-first
   8:19  error  Absolute imports should come before relative imports      import/imports-first
  15:42  error  Missing trailing comma                                    comma-dangle
  33:16  error  Component should be written as a pure function            react/prefer-stateless-function
  41:21  error  Expected indentation of 24 space characters but found 20  react/jsx-indent
  41:34  error  'loaded' is missing in props validation                   react/prop-types
  44:27  error  Expected indentation of 24 space characters but found 26  react/jsx-indent
  45:29  error  Expected indentation of 30 space characters but found 28  react/jsx-indent
  46:29  error  Expected indentation of 30 space characters but found 28  react/jsx-indent
  46:44  error  'userName' is missing in props validation                 react/prop-types
  47:29  error  Expected indentation of 30 space characters but found 28  react/jsx-indent
  47:44  error  'data' is missing in props validation                     react/prop-types
  47:49  error  'data.data' is missing in props validation                react/prop-types
  47:54  error  'data.data.email' is missing in props validation          react/prop-types

/home/n3m/git/n3m/static/src/containers/App/styles/index.js
  1:1  error  Expected empty line after import statement not followed by another import  import/newline-after-import

/home/n3m/git/n3m/static/src/test/example/example.spec.js
  1:1   error    Unexpected var, use let or const instead                                     no-var
  1:1   error    Expected empty line after require statement not followed by another require  import/newline-after-import
  2:19  error    Unexpected function expression                                               prefer-arrow-callback
  2:19  warning  Missing function expression name                                             func-names
  2:27  error    Missing space before function parentheses                                    space-before-function-paren
  3:3   error    Expected indentation of 4 spaces but found 2                                 indent
  3:26  error    Unexpected function expression                                               prefer-arrow-callback
  3:26  warning  Missing function expression name                                             func-names
  3:34  error    Missing space before function parentheses                                    space-before-function-paren
  4:5   error    Expected indentation of 6 spaces but found 4                                 indent
  4:58  warning  Missing function expression name                                             func-names
  4:58  error    Unexpected function expression                                               prefer-arrow-callback
  4:66  error    Missing space before function parentheses                                    space-before-function-paren
  5:7   error    Expected indentation of 8 spaces but found 6                                 indent
  5:26  error    A space is required after ','                                                comma-spacing
  5:28  error    A space is required after ','                                                comma-spacing

✖ 57 problems (51 errors, 6 warnings)
```
