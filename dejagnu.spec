Name:		dejagnu
Version:	1.5
Release:	1
Epoch:		20010912
Summary:	A front end for testing other programs
License:	GPLv2+
URL:		http://www.gnu.org/software/dejagnu/
Source0:	%{name}-%{version}.tar.gz
Patch0:		dejagnu-1.5-smp-1.patch
Patch1:		dejagnu-1.5-runtest.patch
Group:		Development/Other
Requires:	common-licenses tcl >= 8.0 expect >= 5.21
Requires(post):	info-install
Requires(postun):	info-install
BuildRequires:	docbook-utils
BuildRequires:	docbook-dtd31-sgml
BuildRequires:	expect
BuildRequires:	screen texinfo
BuildArch:	noarch

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
%patch1 -p1 -b .runtest~

%build
%configure2_5x -v

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

%post
%_install_info %{name}.info

%preun
%_remove_install_info %{name}.info

%files
%doc AUTHORS NEWS README TODO ChangeLog doc/dejagnu.texi
%dir %{_datadir}/dejagnu
%{_datadir}/dejagnu/*
%{_bindir}/runtest
%{_mandir}/man1/runtest.1*
%{_infodir}/dejagnu.info*
%{_includedir}/dejagnu.h
