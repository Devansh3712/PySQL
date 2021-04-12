# Contributing to PySQL

PySQL is a tool used for making MySQL queries easier for all. It is based on Python and its MySQL-connector library. PR and Issues are welcome.

## How to contribute

### Creating Issues

Suggestions/reviews for improving PySQL can be made by creating Issues for development/enhancement, which should include the specific `function` or `class` and what changes can be made in it.

### Bugs/Testing

If any bugs are found during testing of PySQL tool/library or during unit testing, an issue should be made regarding it, which includes:
  - module name
  - error message
  - any suggestion for debugging
  
### Creating PRs

Pull Requests can be made for PySQL, which can include changes in source code, documentation or creating `Travis CI` test files. If the PR contains all the things mentioned in `pull_request_template`, passes all the checks and is needed in the PySQL library, it will be merged into the `main` branch.

### Code Formatting

The source code is mostly formatted in `PEP8` style, and on every `push` the code in the repository is checked by `DeepSource` for telling possible issues and fixes. The following should be noted while making changes to the source code:

```python
# start a module by writing what it is for
"""
module for testing auth package
of PySQL
"""

# import in-built/pip libraries first, followed by external libraries
import unittest
import os
import sys
import pysql.packages.auth as auth

# create docstrings for every class and module (except __init__)
class TestAuth(unittest.TestCase):
	"""
	class for testing all functions present in
	auth module
	"""
	
	def test_authenticate(self):
		"""
		Test `authenticate` function
		"""
		
		result = auth.Database("root", "root").authenticate()
		self.assertEqual(result, True)
		

# give 2 spaces after every class ends

# create a comment string including creators name & year
"""
PySQL
{name}, {year}
"""
```
