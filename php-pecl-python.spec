%define		php_name	php%{?php_suffix}
%define		modname		python
%define		status			alpha
Summary:	%{modname} - embedded Python
Summary(pl.UTF-8):	%{modname} - Python wbudowany w PHP
Name:		%{php_name}-pecl-%{modname}
Version:	0.8.0
Release:	1
License:	MIT License
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	bfe4236be15dc5095d1dfc6722f14c35
URL:		http://pecl.php.net/package/python/
BuildRequires:	%{php_name}-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.650
BuildRequires:	python-devel < 1:2.6.0
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This extension allows the Python interpreter to be embedded inside of
PHP, allowing for the instantiate and manipulation of Python objects
from within PHP.

In PECL status of this package is: %{status}.

%description -l pl.UTF-8
To rozszerzenie pozwala na wbudowanie interpretera Pythona do PHP, co
pozwala na wykorzystanie i manipulowanie obiektami Pythona z wewnątrz
PHP.

To rozszerzenie ma w PECL status: %{status}.

%prep
%setup -qc
mv %{modname}-%{version}/* .

%build
phpize
%configure \
	--with-%{modname}

%{__make} \
	CPPFLAGS="-DHAVE_CONFIG_H"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir}}
install -p modules/%{modname}.so $RPM_BUILD_ROOT%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
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
%doc CREDITS EXPERIMENTAL
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
