%global base_name       csv
%global short_name      commons-%{base_name}

Name:             apache-%{short_name}
Version:          1.0
Release:          0.2.svn1071189
Summary:          Utilities to assist with handling of CSV files
License:          ASL 2.0
Group:            Development/Java
URL:              http://commons.apache.org/sandbox/%{base_name}
# svn export -r 1071189 http://svn.apache.org/repos/asf/commons/sandbox/csv/trunk/ apache-commons-csv-1.0
# tar caf apache-commons-csv-1.0.tar.xz apache-commons-csv-1.0
Source0:          %{name}-%{version}.tar.xz
BuildArch:        noarch

BuildRequires:    java-devel >= 0:1.6.0
BuildRequires:    jpackage-utils
BuildRequires:    junit4
BuildRequires:    maven
BuildRequires:    maven-surefire-provider-junit4
BuildRequires:    apache-commons-parent

Requires:         java >= 0:1.6.0
Requires:         jpackage-utils
Requires(post):   jpackage-utils
Requires(postun): jpackage-utils

%description
Commons CSV was started to unify a common and simple interface for
reading and writing CSV files under an ASL license.

%package javadoc
Summary:          API documentation for %{name}
Group:            Development/Java
Requires:         jpackage-utils


%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q
sed -i 's/\r//' *.txt
sed -i 's:commons-sandbox-parent:commons-parent:' pom.xml

%build
mvn-rpmbuild install javadoc:javadoc

%install
# jars
install -d -m 755 %{buildroot}%{_javadir}
install -p -m 644 target/%{short_name}-%{version}-SNAPSHOT.jar %{buildroot}%{_javadir}/%{name}.jar
ln -sf %{name}.jar %{buildroot}%{_javadir}/%{short_name}.jar

# pom
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{short_name}.pom
%add_to_maven_depmap org.apache.commons %{short_name} %{version} JPP %{short_name}

# following line is only for backwards compatibility. New packages
# should use proper groupid org.apache.commons
%add_to_maven_depmap %{short_name} %{short_name} %{version} JPP %{short_name}

# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%defattr(-,root,root,-)
%doc LICENSE.txt NOTICE.txt
%{_javadir}/*.jar
%{_mavenpomdir}/JPP-%{short_name}.pom
%{_mavendepmapfragdir}/*

%files javadoc
%defattr(-,root,root,-)
%doc LICENSE.txt NOTICE.txt
%doc %{_javadocdir}/%{name}

