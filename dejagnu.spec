Name:		dejagnu
Version:	1.4.4
Release:	%mkrel 11
Epoch:		20010912
Summary:	A front end for testing other programs
License:	GPLv2+
URL:		http://www.gnu.org/software/dejagnu/
Source0:	%{name}-%{version}.tar.bz2 
Patch0:		dejagnu-1.4.4-smp-1.patch
Patch1:		dejagnu-1.4.4-testsuite.patch
Patch2:		dejagnu-1.4.4-runtest.patch
Group:		Development/Other
Requires:	common-licenses, tcl >= 8.0, expect >= 5.21
Requires(post):	info-install
Requires(postun):	info-install
BuildRequires:	docbook-utils
BuildRequires:	docbook-dtd31-sgml
BuildRequires:	expect
BuildRequires:	screen texinfo
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-build

%description
DejaGnu is an Expect/Tcl based framework for testing other programs.
DejaGnu has several purposes: to make it easy to write tests for any
program; to allow you to write tests which will be portable to any
host or target where a program must be tested; and to standardize the
output format of all tests (making it easier to integrate the testing
into software development).

%prep
%setup -q
%patch0 -p1 -b .smp~
%patch1 -p1 -b .testsuite~
%patch2 -p1 -b .runtest~

%build
%configure2_5x
%make

(cd doc
  make overview.html
  make overview.ps && bzip2 -9v overview.ps)

(cd contrib/bluegnu2.0.3/doc
  ./configure --prefix=%_prefix
  %make)

%install
rm -fr %buildroot
%makeinstall_std

cd contrib/bluegnu2.0.3/doc
%makeinstall

# Nuke unpackaged files
rm -f $RPM_BUILD_ROOT%{_libdir}/config.guess
rm -f $RPM_BUILD_ROOT%{_includedir}/dejagnu.h

%check
echo ============TESTING===============
# Dejagnu test suite also has to test reporting to user.  It needs a
# terminal for that.  That doesn't compute in mock.  Work around it by
# running the test under screen and communicating back to test runner
# via temporary file.  If you have better idea, we accept patches.
TMP=`mktemp`
screen -D -m sh -c '(make check RUNTESTFLAGS="RUNTEST=`pwd`/runtest"; echo $?) >> '$TMP
RESULT=`tail -n 1 $TMP`
cat $TMP
rm -f $TMP
echo ============END TESTING===========
exit $RESULT

%clean
rm -rf $RPM_BUILD_ROOT

%post
%_install_info %{name}.info

%preun
%_remove_install_info %{name}.info

%files
%defattr(-,root,root)
%doc AUTHORS NEWS README TODO
%doc doc/overview doc/overview.ps.bz2
%dir %{_datadir}/dejagnu
%{_datadir}/dejagnu/*
%{_bindir}/runtest
%{_mandir}/man1/dejagnu.1*
%{_mandir}/man1/runtest.1*
%{_infodir}/dejagnu.info*
