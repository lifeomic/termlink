# termlink

Provide an ontology via _Terminology Service's_ API link.

_Termlink_ is a command line client and library for uploading ontologies to LifeOmic's _Precision Health Cloud_. It's goal is to make uploading standardized ontologies easier and to provide utilities for uploading custom ontologies. It provides a simple command line interface for uploading standard ontologies via the [Precision Health Cloud API](https://docs.us.lifeomic.com/) and a Python SDK for building integrations with custom ontologies.

## Quickstart

Download the following tools:

- [Docker](https://docs.docker.com/install/)

Pull the latest version of _Termlink_ from [Docker Hub](https://hub.docker.com/r/lifeomic/termlink):

```sh
$ docker pull lifeomic/termlink
```

Create an environment variables file containing your LifeOmic account, user and API key.

```sh
$ cat lifeomic.env
LO_ACCOUNT=<your account>
LO_USER=<your username>
LO_ACCESS_KEY=<your access key>
```

Note: The best way to manage API keys is using the [LifeOmic CLI](https://github.com/lifeomic/cli). You can also create an API key using the [Precision Health Cloud](https://docs.us.lifeomic.com/user-guides/api-keys/).

Run it.

```sh
$ docker run --env-file lifeomic.env -e LO_PROJECT=<your project> lifeomic/termlink python -m termlink --help
```

Note: You can obtain your project identifier using the [LifeOmic CLI](https://github.com/lifeomic/cli).

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

The following tools are required to run _Termlink_:

- [Docker](https://docs.docker.com/install/)
- [Git](https://git-scm.com/)
- [Python 3](https://www.python.org/download/releases/3.0/)
- [Yarn](https://yarnpkg.com/en/)

### Installing

The following steps will guide you through installing the project locally.

Clone the `git` repository onto your local machine.

```sh
$ git clone git@github.com:lifeomic/termlink.git && cd ./termlink
```

Using Python 3, create a `virtualenv` and then activate it.

```sh
$ python3 -m venv venv && source venv/bin/activate
```

_Note: Your Python binary may be under a different name._

Check that your local version of Python is at least version 3.7 by running `python --version`.

Once you have verified your version of Python is correct, run the following to download all dependencies.

```
$ pip install -r requirements.txt requirements-dev.txt
```

You now have everything you need to start developing on _Termlink_. 

## Testing

This project uses the Python [`nose`](https://nose.readthedocs.io/en/latest/index.html) framework.

### Unit Testing

The simple way to run unit tests is using `yarn`:

```sh
$ yarn test
```

To speed up development, you can run the tests against your local Python build using the `Makefile`.

```sh
$ make test
```

## Deployment

This project is packaged using Docker and published as a public image on [Docker Hub](https://hub.docker.com/r/lifeomic/termlink). Publish a new version using the following command.

```sh
yarn push
```

You will be promoted to enter a new version, triggered by the `yarn version` command. Please use [SemVer](https://semver.org/) versioning for incrementing versions. To learn more about why SemVer is used, see the section on [_Versioning_](##Versioning) below.

## Built With

- [Docker](https://www.docker.com/): "Build, Ship, and Run Any App, Anywhere."
- [Python 3](https://www.python.org/): "Python is a programming language that lets you work quickly and integrate systems more effectively."
- [Requests](http://docs.python-requests.org/en/master/): "Requests is an elegant and simple HTTP library for Python, built for human beings."

## Contributing

[TODO]

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

The following guidelines are provided on the [SemVer]((http://semver.org/)) website:

> Given a version number MAJOR.MINOR.PATCH, increment the:
> 
> - MAJOR version when you make incompatible API changes,
> - MINOR version when you add functionality in a backwards-compatible manner, and
> - PATCH version when you make backwards-compatible bug fixes.
> 
> Additional labels for pre-release and build metadata are available as extensions to the MAJOR.MINOR.PATCH format.

## Authors

* **Taylor Steinberg** - *Initial work* - [tdstein](https://github.com/tdstein)

See also the list of [contributors](https://github.com/lifeomic/termlink/contributors) who participated in this project.

## License

This project is licensed under the MIT - see the [LICENSE](LICENSE.txt) file for details.

## Acknowledgments

[TODO]
