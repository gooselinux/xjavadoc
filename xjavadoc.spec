# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define section		free

Name:		xjavadoc
Version:	1.1
Release:	7.7%{?dist}
Epoch:		0
Summary:	The XJavaDoc engine
License:	BSD
URL:		http://xdoclet.sourceforge.net/xjavadoc/
Group:		Development/Testing
Source0:	xjavadoc-src-1.1-RHCLEAN.tar.bz2
# cvs -d:pserver:anonymous@cvs.sourceforge.net:/cvsroot/xdoclet login
# cvs -z3 -d:pserver:anonymous@cvs.sourceforge.net:/cvsroot/xdoclet export -r XJAVADOC_1_1 xjavadoc
Patch0:		%{name}-build_xml.patch
BuildRequires:	java
BuildRequires:	java-devel >= 0:1.4.2
BuildRequires:	jpackage-utils
BuildRequires:	junit
BuildRequires:	ant >= 0:1.6
BuildRequires:	ant-nodeps >= 0:1.6
BuildRequires:	ant-junit >= 0:1.6
BuildRequires:	jakarta-commons-logging
BuildRequires:	jakarta-commons-collections
BuildRequires:	xml-commons-apis
BuildRequires:	log4j
BuildRequires:	javacc
BuildRequires:	xalan-j2
BuildRequires:	jrefactory
Requires:	java
Requires:	jakarta-commons-logging
Requires:	jakarta-commons-collections
Requires:	xml-commons-apis
Requires:	log4j
Requires:	xalan-j2
Requires:	jrefactory
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The XJavaDoc engine is a complete rewrite of Sun's 
JavaDoc engine that is faster and more suited for 
XDoclet (although it is completely standalone). It 
scans java source code and makes information about 
a class available via special java beans that are 
part of the XJavaDoc core. These beans provide the 
same information about a class as Sun's JavaDoc API, 
and some nice extra features. 

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Development/Documentation
# for /bin/rm and /bin/ln
Requires(post):   coreutils
Requires(postun): coreutils

%description    javadoc
%{summary}.

%prep
%setup -q -n %{name}
find . -name "*.zip" -exec rm {} \;
find . -name "*.jar" -exec rm {} \;

%patch0 -b .sav

%build
build-jar-repository -s -p lib \
xalan-j2 \
junit \
javacc \
log4j \
commons-logging \
commons-collections \
xml-commons-apis \
jrefactory \
ant \


#Fix these binary deps
#BINCLASSPATH=$PWD/lib/ConfigLog4j.jar

ant -Djavacchome=/usr/share/java javadoc

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_javadir}
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}
mkdir -p $RPM_BUILD_ROOT%{_docdir}
install -m 644 target/%{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}

# version less symlinks
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

install -d -m 755 $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
install -m 644 LICENSE.txt $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
install -m 644 docs/architecture.txt $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

#javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr dist/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ "$1" = "0" ]; then
    rm -f %{_javadocdir}/%{name}
fi

%files
%defattr(0644,root,root,0755)
%{_javadir}/*
%{_docdir}/%{name}-%{version}

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{name}-%{version}
%ghost %doc %{_javadocdir}/%{name}

%changelog
* Thu Jan 7 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.1-7.7
- Drop gcj_support.

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 0:1.1-7.6
- Rebuilt for RHEL 6

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1-7.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1-6.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jul 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.1-5.5
- drop repotag

* Thu May 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.1-5jpp.4
- fix license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:1.1-5jpp.3
- Autorebuild for GCC 4.3

* Thu Sep 20 2007 Deepak Bhole <dbhole@redhat.com> 1.1-4jpp.3
- Rebuild for ppc32 execmem issue and new build-id
- Add %%{?dist} as per policy

* Mon Mar 26 2007 Deepak Bhole <dbhole@redhat.com> 1.1-4jpp.2
- Fixed incorrect entry in the files section

* Thu Aug 10 2006 Deepak Bhole <dbhole@redhat.com> 1.1-4jpp.1
- Added missing postun section for javadoc.
- Added missing requirements.

* Mon Jul 24 2006 Deepak Bhole <dbhole@redhat.com> 1.1-3jpp_1fc
- Added conditional native compilation.
- BR fixes.

* Thu Apr 06 2005 Ralph Apel <r.apel at r-apel.de> 1.1-2jpp
- First JPP-1.7 release

* Tue Feb 15 2005 Ralph Apel <r.apel at r-apel.de> 1.1-1jpp
- upgrade to 1.1
- replace requirement of xml-commons by xml-commons-apis

* Thu Aug 26 2004 Ralph Apel <r.apel at r-apel.de> 1.0.3-2jpp
- Build with ant-1.6.2

* Fri Jul 02 2004 Ralph Apel <r.apel at r-apel.de> 1.0.3-1jpp
- upgrade to 1.0.3
- just eliminate __GENERATED__ tests because no sources for old xdoclet 
- add xjavadoc javadoc subpackage

* Tue Dec 16 2003 Paul Nasrat <pauln at truemesh.com> 1.0-2jpp
- fix non-versioned symlink typo

* Mon Dec 15 2003 Paul Nasrat <pauln at truemesh.com> 1.0-1jpp
- Initial Release
