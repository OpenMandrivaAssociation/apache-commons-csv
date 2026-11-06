Name:		apache-commons-csv
Version:	1.14.1
Release:	1
Summary:	Reads and writes CSV files
Group:		Development/Java
License:	ASL 2.0
URL:		https://commons.apache.org/proper/commons-csv/
Source0:	https://github.com/apache/commons-csv/archive/refs/tags/rel/commons-csv-%{version}.tar.gz#/commons-csv-%{version}.tar.gz

BuildArch:	noarch
Obsoletes:	%{name}-javadoc < %{version}
BuildRequires:	mvn(org.apache.commons:commons-parent:pom::)
BuildRequires:	mvn(org.apache:apache:pom::)
BuildRequires:	mvn(commons-io:commons-io)
BuildRequires:	mvn(commons-codec:commons-codec)
# Literal, so the first rpmbuild -bs records them before sysjar is installed.
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildSystem:	maven
BuildOption(install):	--file-name commons-csv --link %{name}

%description
Apache Commons CSV reads and writes CSV files. 1.14.1 replaces the
sandbox 1.0 snapshot. CSVPrinter.printRecord no longer hangs on a
parallel stream, and printRecords(ResultSet) writes one record at a
time under a lock. Tests are skipped.

%prep
%autosetup -n commons-csv-rel-commons-csv-%{version}
# spotbugs-annotations is optional and not packaged. Maven still
# resolves it, and CSVPrinter imports the suppression annotation.
python - <<'PY'
import re
from pathlib import Path

pom = Path("pom.xml")
text = pom.read_text()
text, n = re.subn(
    r"\s*<dependency>\s*<groupId>com\.github\.spotbugs</groupId>\s*<artifactId>spotbugs-annotations</artifactId>.*?</dependency>",
    "",
    text,
    count=1,
    flags=re.S,
)
if n != 1:
    raise SystemExit(f"spotbugs dep {n}")
pom.write_text(text)

src = Path("src/main/java/org/apache/commons/csv/CSVPrinter.java")
body = src.read_text()
old_import = "import edu.umd.cs.findbugs.annotations.SuppressFBWarnings;\n"
old_ann = '    @SuppressFBWarnings(value = "AT_NONATOMIC_OPERATIONS_ON_SHARED_VARIABLE", justification = "https://github.com/spotbugs/spotbugs/issues/3428")\n'
if old_import not in body or old_ann not in body:
    raise SystemExit("spotbugs annotation not found")
src.write_text(body.replace(old_import, "", 1).replace(old_ann, "", 1))
PY

%files -f .mfiles
%doc LICENSE.txt NOTICE.txt RELEASE-NOTES.txt README.md
