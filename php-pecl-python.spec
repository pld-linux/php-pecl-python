# TODO
# - doesn't build (can't find python)
%define		_modname		python
%define		_status			alpha
Summary:	Embedded Python
Summary(pl.UTF-8):   Python wbudowany w PHP
Name:		php-pecl-%{_modname}
Version:	0.7.0
Release:	1.1
License:	PHP 2.02
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	61554c04374a5fab83084e299284f255
URL:		http://pecl.php.net/package/python/
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.344
BuildRequires:	python-devel
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This extension allows the Python interpreter to be embedded inside of
PHP, allowing for the instantiate and manipulation of Python objects
from within PHP.

In PECL status of this package is: %{_status}.

%description -l pl.UTF-8
To rozszerzenie pozwala na wbudowanie interpretera Pythona do PHP, co
pozwala na wykorzystanie i manipulowanie obiektami Pythona z wewnątrz
PHP.

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c

%build
cd %{_modname}-%{version}
phpize
%configure \
	--with-%{_modname}

%{__make} CPPFLAGS="-DHAVE_CONFIG_H -I%{_prefix}/X11R6/include/X11/"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir}}

install %{_modname}-%{version}/modules/%{_modname}.so $RPM_BUILD_ROOT%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc %{_modname}-%{version}/{CREDITS,EXPERIMENTAL}
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{_modname}.so
