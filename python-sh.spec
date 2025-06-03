%define module sh
%bcond_without tests

Name:		python-sh
Version:	2.2.2
Release:	1
License:	MIT
Summary:	Subprocess replacement for python
Group:		Development/Python
URL:		https://pypi.org/project/sh/
Source0:	https://github.com/amoffat/sh/archive/%{version}/%{module}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	pkgconfig(python)
BuildRequires:	python%{pyver}dist(pip)
BuildRequires:	python%{pyver}dist(poetry-core)
BuildRequires:	python%{pyver}dist(setuptools)
BuildRequires:	python%{pyver}dist(wheel)
%if %{with tests}
BuildRequires:	python%{pyver}dist(pytest)
%endif

%description
sh is a full-fledged subprocess replacement for Python 2.6 - 3.6, PyPy and PyPy3
that allows you to call any program as if it were a function:

.. code:: python

from sh import ifconfig
print ifconfig("eth0")

sh is *not* a collection of system commands implemented in Python.

%prep
%autosetup -n %{module}-%{version} -p1

# Remove git badge remote images from README
sed -i '1,3d;7,22d;' README.rst

%build
%py_build

%install
%py_install

%if %{with tests}
export CI=true
export PYTHONPATH="%{buildroot}%{python_sitelib}:%{buildroot}%{python_sitelib}:${PWD}"

# For the following env globals usage see:
# https://github.com/amoffat/sh/blob/ea434f0bafd285bbe5b93d218e62227f2b77f310/sh.py#L88-L95
export SH_TESTS_RUNNING=1
# Run tests with both poll and select.
SH_TESTS_USE_SELECT=0 %{__python} -m pytest -v
SH_TESTS_USE_SELECT=1 %{__python} -m pytest -v
%endif

%files
%{python_sitelib}/sh.py
%{python_sitelib}/__pycache__/sh.*pyc
%{python_sitelib}/%{module}-%{version}.dist-info
%doc README.rst
%license LICENSE.txt