# TODO: PLDify init script
Summary:	SNMP agent for modeling SAForum Hardware Platform Interface
Summary(pl):	Agent SNMP do modelowania interfejsu HPI SAForum
Name:		openhpi-subagent
Version:	1.0.0
Release:	0.1
License:	BSD
Group:		Applications
Source0:	http://dl.sourceforge.net/openhpi/%{name}-%{version}.tar.gz
# Source0-md5:	de299177ac6b1ea6664e6639aed91c06
URL:		http://openhpi.sourceforge.net/
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake
BuildRequires:	docbook-dtd41-sgml
BuildRequires:	docbook-utils
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	libtool
BuildRequires:	net-snmp-devel >= 5.1.1
BuildRequires:	openhpi-devel >= 0.5.0
BuildRequires:	pkgconfig
Requires:	net-snmp >= 5.1.1
Requires:	openhpi >= 0.5.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains an SNMP subagent for the Service Availability
Forum's HPI specification. It is built against OpenHPI, but should be
rebuildable against any HPI 1.0 implementation. Through this subagent
one can includes support for multiple different types of hardware
including: IPMI, IBM Blade Center (via SNMP), Linux Watchdog devices,
and Sysfs based systems.

%description -l pl
Ten pakiet zawiera podagenta SNMP dla specyfikacji HPI z Service
Availability Forum. Jest budowany z bibliotekami OpenHPI, ale powinien
da� si� zbudowa� z dowoln� implementacj� HPI 1.0. Dzi�ki temu
podagentowi mo�na doda� obs�ug� wielu r�nych rodzaj�w sprz�tu, w tym:
IPMI, IBM Blade Center (poprzez SNMP), linuksowe urz�dzenia Watchdog,
systemy oparte na Sysfs.

%prep
%setup -q

%{__perl} -pi -e 's/glib`/glib-2.0`/' configure.ac

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure

%{__make}
%{__make} -C docs pdf-am
%{__make} -C docs subagent-manual/book1.html

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -D openhpi-subagent.rc $RPM_BUILD_ROOT/etc/rc.d/init.d/openhpi-subagent

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING ChangeLog README TODO mib/*.mib docs/*pdf docs/subagent-manual
%config(noreplace) %verify(not size mtime md5) /etc/snmp/hpiSubagent.conf
%attr(754,root,root) /etc/rc.d/init.d/openhpi-subagent
%attr(755,root,root) %{_bindir}/hpi*