#
# TODO: process {bin,doc,indep-utils/model-gen} directories
#
Summary:	NS-2 network simulator
Summary(pl):	Symulator sieci NS-2
Name:		ns
Version:	2.27
Release:	3
License:	various
Group:		Applications/Networking
Source0:	http://www.isi.edu/nsnam/dist/%{name}-src-%{version}.tar.gz
# Source0-md5:	db3a16e450f66a5e4dd881349ccc5dd7
Source1:	http://www.isi.edu/nsnam/ns/doc/ns_doc.pdf
# Source1-md5:	66e82f100292ebe0bda8bcb98fa26bba
URL:		http://www.isi.edu/nsnam/
Patch0:		%{name}-install.patch
Patch1:		tcl-lib.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	otcl-devel
BuildRequires:	tclcl-static
BuildRequires:	tcl-devel >= 8.4
BuildRequires:	tk-devel >= 8.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Ns is a discrete event simulator targeted at networking research. Ns
provides substantial support for simulation of TCP, routing, and
multicast protocols over wired and wireless (local and satellite)
networks.

%description -l pl
Ns jest symulatorem dyskretnych zdarzeñ kierowanym w stronê badañ
sieci. Dobrze wspiera symulacjê protoko³ów TCP, routingu oraz
multicastowych w przewodowych i bezprzewodowych (lokalnych i
satelitarnych) sieciach.

%package cmu-scen
Summary:	CBR connections generator for NS
Summary(pl):	Generator po³±czeñ CBR dla NS
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description cmu-scen
CBR connections generator for NS.

%description cmu-scen -l pl
Generator po³±czeñ CBR dla NS.

%package empweb
Summary:	Empirical FTP/Web traffic model for NS
Summary(pl):	Empiryczny model ruchowy FTP/Web dla NS
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description empweb
Empirical FTP/Web traffic model that simulates FTP/Web traffic based
on a set of CDF (Cumulative Distribution Function) data derived from
live tcpdump trace.

%description empweb -l pl
Empiryczny model ruchowy FTP/Web, który symuluje ruch FTP/Web na
podstawie danych CDF (dystrybuanty) wyci±gniêtych z prawdziwego
¶ledzenia tcpdump.

%package emulate
Summary:	TCP emulation for NS
Summary(pl):	Emulacja TCP dla NS
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description emulate
TCP emulation for NS.

%description emulate -l pl
Emulacja TCP dla NS.

%package tcl
Summary:	Tcl files for NS
Summary(pl):	Pliki Tcl dla NS
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description tcl
Tcl files for NS.

%description tcl -l pl
Pliki Tcl dla NS.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
cp -f /usr/share/automake/config.sub .
%{__autoconf}
%configure \
	--with-tcl-ver=8.4 \
	--with-tk-ver=8.4
%{__make} \
	CCOPT="%{rpmcflags}" \
	CXXFLAGS="%{rpmcflags}"
perl -pe 's|/usr/local/bin/|/usr/bin/|' -i tcl/ex/tcp-fs/{process.awk,run.tcl}
perl -pe 's|/usr/sww/bin/|/usr/bin/|' -i tcl/ex/tcp-fs/run-fs-asym.tcl

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1,%{_datadir}/ns/{,emulate,cmu-scen-gen}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	MANDEST=%{_mandir}

cp -f empweb/scripts/* $RPM_BUILD_ROOT%{_bindir}
cp -f emulate/*.tcl $RPM_BUILD_ROOT%{_datadir}/ns/emulate
cp -f indep-utils/cmu-scen-gen/*.tcl $RPM_BUILD_ROOT%{_datadir}/ns/cmu-scen-gen
cp -fr tcl $RPM_BUILD_ROOT%{_datadir}/ns

install %{SOURCE1} .
cp -f diffusion3/CHANGES CHANGES-diffusion3
cp -f diffusion3/COPYRIGHT COPYRIGHT-diffusion3
cp -f diffusion3/README README-diffusion3
cp -f diffusion3/README.NS README.NS-diffusion3
cp -f indep-utils/webtrace-conv/README README-webtrace-conv
cp -f mpls/README README-mpls
cp -f src_rtg/README.txt README-src_rtg
rm -f ns-tutorial/Makefile

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES* TODO.html COPYRIGHT* README* ns-tutorial ns_doc.pdf
%exclude %{_bindir}/*.awk
%exclude %{_bindir}/*.tcl
%attr(755,root,root) %{_bindir}/*
%dir %{_datadir}/ns
%{_mandir}/man1/*

%files cmu-scen
%defattr(644,root,root,755)
%doc indep-utils/cmu-scen-gen/README
%{_datadir}/ns/cmu-scen-gen

%files empweb
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*.awk
%attr(755,root,root) %{_bindir}/*.tcl

%files emulate
%defattr(644,root,root,755)
%doc emulate/README.notes
%{_datadir}/ns/emulate

%files tcl
%defattr(644,root,root,755)
%{_datadir}/ns/tcl
