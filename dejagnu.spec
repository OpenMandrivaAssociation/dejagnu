%define _disable_lto	1
%define _disable_rebuild_configure 1

Summary:	A front end for testing other programs
Name:		dejagnu
Version:	1.6.3
Release:	3
Group:		Development/Other
License:	GPLv2+
Url:		https://www.gnu.org/software/dejagnu/
Source0:	ftp://ftp.gnu.org/gnu/dejagnu/%{name}-%{version}.tar.gz
Source100:	%{name}.rpmlintrc
Patch1:		dejagnu-1.5-runtest.patch
BuildArch:	noarch

BuildRequires:	docbook-utils
BuildRequires:	docbook-utils-pdf
BuildRequires:	docbook-dtd31-sgml
BuildRequires:	expect
BuildRequires:	screen
BuildRequires:	texinfo
Requires:	common-licenses
Requires:	expect >= 5.21
Requires:	tcl >= 8.0

%description
DejaGnu is an Expect/Tcl based framework for testing other programs.
DejaGnu has several purposes: to make it easy to write tests for any
program; to allow you to write tests which will be portable to any
host or target where a program must be tested; and to standardize the
output format of all tests (making it easier to integrate the testing
into software development).

%prep
%setup -q
%autopatch -p1

%build
%configure

%install
%makeinstall_std

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

%files
%doc AUTHORS NEWS README TODO ChangeLog doc/dejagnu.texi
%dir %{_datadir}/dejagnu
%{_bindir}/dejagnu
%{_bindir}/runtest
%{_datadir}/dejagnu/*
%{_mandir}/man1/runtest.1*
%{_mandir}/man1/dejagnu.1*
%{_mandir}/man1/dejagnu-help.1*
%{_mandir}/man1/dejagnu-report-card.1*
%{_infodir}/dejagnu.info*
%{_includedir}/dejagnu.h
