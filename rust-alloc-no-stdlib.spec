%bcond_without check
%global debug_package %{nil}

# The binary is useless
%global __cargo_is_bin() false

%global crate alloc-no-stdlib

Name:           rust-%{crate}
Version:        2.0.1
Release:        5
Summary:        Dynamic allocator that may be used with or without the stdlib

# Upstream license specification: BSD-3-Clause
License:        BSD
URL:            https://crates.io/crates/alloc-no-stdlib
Source:         %{crates_source}

ExclusiveArch:  %{rust_arches}
%if %{__cargo_skip_build}
BuildArch:      noarch
%endif

BuildRequires:  rust-packaging

%global _description %{expand:
Dynamic allocator that may be used with or without the stdlib. This allows a
package with nostd to allocate memory dynamically and be used either with a
custom allocator, items on the stack, or by a package that wishes to simply use
Box<>. It also provides options to use calloc or a mutable global variable for
pre-zeroed memory.}

%description %{_description}

%package        devel
Summary:        %{summary}
BuildArch:      noarch

%description    devel %{_description}

This package contains library source intended for building other packages
which use "%{crate}" crate.

%files          devel
%license LICENSE
%doc README.md
%{cargo_registry}/%{crate}-%{version_no_tilde}/

%package     -n %{name}+default-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+default-devel %{_description}

This package contains library source intended for building other packages
which use "default" feature of "%{crate}" crate.

%files       -n %{name}+default-devel
%ghost %{cargo_registry}/%{crate}-%{version_no_tilde}/Cargo.toml

%package     -n %{name}+unsafe-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+unsafe-devel %{_description}

This package contains library source intended for building other packages
which use "unsafe" feature of "%{crate}" crate.

%files       -n %{name}+unsafe-devel
%ghost %{cargo_registry}/%{crate}-%{version_no_tilde}/Cargo.toml

%prep
%autosetup -n %{crate}-%{version_no_tilde} -p1
# https://github.com/dropbox/rust-alloc-no-stdlib/pull/8
find -type f -name '*.rs' -executable -exec chmod -x '{}' +
%cargo_prep

%generate_buildrequires
%cargo_generate_buildrequires

%build
%cargo_build

%install
%cargo_install

%if %{with check}
%check
%cargo_test
%endif
