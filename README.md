<!--
*** Thanks for checking out this README Template. If you have a suggestion that would
*** make this better, please fork the repo and create a pull request or simply open
*** an issue with the tag "enhancement".
*** Thanks again! Now go create something AMAZING! :D
-->





<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">


  <h1 align="center">Python Stream</h1>

  <p align="center">
    The power of Java stream now available in Python
    <br />
    <a href="https://github.com/alemazzo/python-java-stream"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/alemazzo/python-java-stream">View Demo</a>
    ·
    <a href="https://github.com/alemazzo/python-java-stream/issues">Report Bug</a>
    ·
    <a href="https://github.com/alemazzo/python-java-stream/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

- [Table of Contents](#table-of-contents)
- [About The Project](#about-the-project)
  - [Built With](#built-with)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)



<!-- ABOUT THE PROJECT -->
## About The Project

**What is Stream?**

Stream represents a sequence of objects from a source, which supports aggregate operations. 

Following are the characteristics of a Stream:

* **Sequence of elements** − A stream provides a set of elements of specific type in a sequential manner. A stream gets/computes elements on demand. It never stores the elements.

* **Source** − Stream takes Collections, Arrays, or I/O resources as input source.

* **Aggregate operations** − Stream supports aggregate operations like filter, map, limit, reduce, find, and so on.

* **Pipelining** − Most of the stream operations return stream itself so that their result can be pipelined. These operations are called intermediate operations and their function is to take input, process them, and return output to the target. toList() and toSet() methods are terminals operation which is normally present at the end of the pipelining operation to mark the end of the stream.

* **Automatic iterations** − Stream operations do the iterations internally over the source elements provided, in contrast to Collections where explicit iteration is required.

### Built With

* [Python](https://python.org)



<!-- GETTING STARTED -->
## Getting Started

Follow this steps for install this tool in the right way.

### Prerequisites

That's all you need to use Streams:

* python3
```sh
sudo apt install python3
```

* pip
```sh
sudo apt install python3-pip
```

### Installation

1. Install the module with **pip**
  
```sh
pip install java-stream
```
2. Import the module in your project
  
```py
from stream import Stream
```



<!-- USAGE EXAMPLES -->
## Usage

Here some example of how to use Streams:

* Generate a list of 100 random numbers
```py
Stream.randint(1, 100).limit(100).toList()
```

* Print the numbers from 1 to 100
```py
Stream.iterate(1, lambda i: i + 1).limit(100).forEach(print)
```

* Generate a list of squares of the number from 1 to 100
```py
Stream.iterate(1, lambda i: i + 1).map(lambda x: x**2).limit(100).toList()
```

* Generate a list of 0 with a lenght of 100
```py
Stream.generate(lambda: 0).limit(100).toList()
```

* Generate a set of the first 100 odds number
```py
Stream.odds().limit(100).toSet()
```

* Generate a list of all the primes number smaller than 100
```py
Stream.primes().filter(lambda x: x < 100).toList()
```



<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/alemazzo/python-java-stream/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the GNU License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Alessandro Mazzoli - [@alessandro.py](https://instagram.com/alessandro.py) - developer.alessandro.mazzoli@gmail.com

Project Link: [https://github.com/alemazzo/python-java-stream](https://github.com/alemazzo/python-java-stream)




<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/alemazzo/python-java-stream.svg?style=flat-square
[contributors-url]: https://github.com/alemazzo/python-java-stream/graphs/contributors

[forks-shield]: https://img.shields.io/github/forks/alemazzo/python-java-stream.svg?style=flat-square
[forks-url]: https://github.com/alemazzo/python-java-stream/network/members

[stars-shield]: https://img.shields.io/github/stars/alemazzo/python-java-stream.svg?style=flat-square
[stars-url]: https://github.com/alemazzo/python-java-stream/stargazers

[issues-shield]: https://img.shields.io/github/issues/alemazzo/python-java-stream.svg?style=flat-square
[issues-url]: https://github.com/alemazzo/python-java-stream/issues


[license-shield]: https://img.shields.io/github/license/alemazzo/python-java-stream.svg?style=flat-square
[license-url]: https://github.com/alemazzo/python-java-stream/blob/master/LICENSE

[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/alessandro-mazzoli-009868140

[product-screenshot]: images/screenshot.png
