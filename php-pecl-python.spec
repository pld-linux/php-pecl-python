%define		_modname		python
%define		_status			alpha
Summary:	Embedded Python
Summary(pl):	Python wbudowany w PHP
Name:		php-pecl-%{_modname}
Version:	0.7.0
Release:	1
License:	PHP 2.02
Group:		Development/Languages/PHP
Source0:	http://pear.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	61554c04374a5fab83084e299284f255
URL:		http://pear.php.net/package/%{_pearname}/
BuildRequires:	automake
BuildRequires:	php-devel
BuildRequires:	python-devel
Requires:	php-common
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/php
%define		extensionsdir	%{_libdir}/php

%description
This extension allows the Python interpreter to be embedded inside of
PHP, allowing for the instantiate and manipulation of Python objects
from within PHP.

This extension has in PEAR status: %{_status}.

%description -l pl
To rozszerzenie pozwala na wbudowanie interpretera Pythona do PHP, co
pozwala na wykorzystanie i manipulowanie obiektami Pythona z wewn±trz
PHP.

To rozszerzenie ma w PEAR status: %{_status}.

%prep
%setup -q -c

%build
cd %{_modname}-%{version}
phpize
%{__aclocal}
%configure \
	--with-%{_modname}

%{__make} CPPFLAGS="-DHAVE_CONFIG_H -I%{_prefix}/X11R6/include/X11/"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{extensionsdir}

install %{_modname}-%{version}/modules/%{_modname}.so $RPM_BUILD_ROOT%{extensionsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/usr/sbin/php-module-install install %{_modname} %{_sysconfdir}/php.ini

%preun
if [ "$1" = "0" ]; then
	/usr/sbin/php-module-install remove %{_modname} %{_sysconfdir}/php.ini
fi

%files
%defattr(644,root,root,755)
%doc %{_modname}-%{version}/{CREDITS,EXPERIMENTAL}
%attr(755,root,root) %{extensionsdir}/%{_modname}.so
