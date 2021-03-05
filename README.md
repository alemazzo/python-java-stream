# Python-Java-Stream
Java Stream For Python
----
https://pypi.org/project/java-stream/
----

## Install
```bash
pip install java-stream
```
## Usage
```py
from stream import Stream

# Generate a list of 100 random numbers
Stream.randint(1, 100).limit(100).toList()

# Generate a list of the numbers from 1 to 100
Stream.iterate(1, lambda i: i + 1).limit(100).toList()

# Generate a list of squares of the number from 1 to 100
Stream.iterate(1, lambda i: i + 1).map(lambda x: x**2).limit(100).toList()

# Generate a list of 0 with a lenght of 100
Stream.generate(lambda: 0).limit(100).toList()
```
