Name:		dejagnu
Version:	1.5
Release:	2
Epoch:		20010912
Summary:	A front end for testing other programs
License:	GPLv2+
URL:		http://www.gnu.org/software/dejagnu/
Source0:	ftp://ftp.gnu.org/gnu/dejagnu/%{name}-%{version}.tar.gz
Patch0:		dejagnu-1.5-smp-1.patch
Patch1:		dejagnu-1.5-runtest.patch
Group:		Development/Other
Requires:	common-licenses tcl >= 8.0 expect >= 5.21
BuildRequires:	docbook-utils docbook-utils-pdf
BuildRequires:	docbook-dtd31-sgml
# in contrib, but likely not needed anyways even if configure checks for it..
#BuildRequires:	docbook2x
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

%files
%doc AUTHORS NEWS README TODO ChangeLog doc/dejagnu.texi
%dir %{_datadir}/dejagnu
%{_datadir}/dejagnu/*
%{_bindir}/runtest
%{_mandir}/man1/runtest.1*
%{_infodir}/dejagnu.info*
%{_includedir}/dejagnu.h


%changelog
* Thu May 05 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 20010912:1.5-1
+ Revision: 669311
- add download url
- add missing buildrequires
- new version
- clean out legacy rpm stuff

* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 20010912:1.4.4-13
+ Revision: 663761
- mass rebuild

* Thu Dec 02 2010 Oden Eriksson <oeriksson@mandriva.com> 20010912:1.4.4-12mdv2011.0
+ Revision: 604782
- rebuild

* Tue Mar 16 2010 Oden Eriksson <oeriksson@mandriva.com> 20010912:1.4.4-11mdv2010.1
+ Revision: 522427
- rebuilt for 2010.1

  + Sandro Cazzaniga <kharec@mandriva.org>
    - fix licence

* Mon Oct 05 2009 Funda Wang <fwang@mandriva.org> 20010912:1.4.4-10mdv2010.0
+ Revision: 453833
- fix build and test

  + Christophe Fergeau <cfergeau@mandriva.com>
    - rebuild

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuild

* Wed Dec 24 2008 Per Øyvind Karlsen <peroyvind@mandriva.org> 20010912:1.4.4-8mdv2009.1
+ Revision: 318146
- merge in fedora patches

* Mon Jun 16 2008 Thierry Vignaud <tv@mandriva.org> 20010912:1.4.4-7mdv2009.0
+ Revision: 220578
- rebuild

* Fri Jan 11 2008 Thierry Vignaud <tv@mandriva.org> 20010912:1.4.4-6mdv2008.1
+ Revision: 149167
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Guillaume Rousse <guillomovitch@mandriva.org>
    - rebuild

* Fri Aug 24 2007 David Walluck <walluck@mandriva.org> 20010912:1.4.4-4mdv2008.0
+ Revision: 70758
- fix install-info Requires

* Thu Aug 23 2007 Thierry Vignaud <tv@mandriva.org> 20010912:1.4.4-3mdv2008.0
+ Revision: 70183
- convert prereq


* Thu Jan 25 2007 Lenny Cartier <lenny@mandriva.com> 1.4.4-2mdv2007.0
+ Revision: 113318
- Rebuild
- Import dejagnu

* Thu Jan 06 2005 Lenny Cartier <lenny@mandrakesoft.com> 1.4.4-1mdk
- 1.4.4
- keep 2.0.3 bluegnu files

