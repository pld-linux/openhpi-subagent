Summary:	SNMP agent for modeling SAForum Hardware Platform Interface
Summary(pl):	Agent SNMP do modelowania interfejsu HPI SAForum
Name:		openhpi-subagent
Version:	2.2.0
Release:	1
License:	BSD
Group:		Applications
Source0:	http://dl.sourceforge.net/openhpi/%{name}-%{version}.tar.gz
# Source0-md5:	c3620ae45169e398c09052dabecd9922
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://openhpi.sourceforge.net/
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake
BuildRequires:	docbook-dtd41-sgml
BuildRequires:	docbook-utils
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	libtool
BuildRequires:	net-snmp-devel >= 5.1.1
BuildRequires:	openhpi-devel >= 2.2.0
BuildRequires:	sed >= 4.0
BuildRequires:	pkgconfig
Requires:	net-snmp >= 5.1.1
Requires:	openhpi >= 2.2.0
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
daæ siê zbudowaæ z dowoln± implementacj± HPI 1.0. Dziêki temu
podagentowi mo¿na dodaæ obs³ugê wielu ró¿nych rodzajów sprzêtu, w tym:
IPMI, IBM Blade Center (poprzez SNMP), linuksowe urz±dzenia Watchdog,
systemy oparte na Sysfs.

%prep
%setup -q

# avoid error on some variable used only in debug builds
sed -i -e 's/-Werror/-Werror -Wno-unused/' configure.ac

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

rm -f $RPM_BUILD_ROOT/etc/init.d/openhpi-subagent
install -D %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/openhpi-subagent
install -D %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/openhpi-subagent

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING ChangeLog README TODO mib/*.mib docs/*pdf docs/subagent-manual
%attr(755,root,root) %{_bindir}/hpi*
%config(noreplace) %verify(not md5 mtime size) /etc/snmp/hpiSubagent.conf
%attr(754,root,root) /etc/rc.d/init.d/openhpi-subagent
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/openhpi-subagent
