#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	openmp		# parallelization using OpenMP
%bcond_with	tbb		# parallelization using TBB (disables OpenMP)
%bcond_with	xsimd		# SIMD acceleration
#
%if %{with tbb}
%undefine	with_openmp
%endif
Summary:	Multi-dimensional arrays with broadcasting and lazy computing
Summary(pl.UTF-8):	Wielowymiarowe tablice z rozpraszaniem i leniwym obliczaniem
Name:		xtensor
Version:	0.24.6
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/xtensor-stack/xtensor/tags
Source0:	https://github.com/xtensor-stack/xtensor/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	368a1172b78ebc81ee91366dd9f525b5
URL:		https://xtensor.readthedocs.io/
BuildRequires:	cmake >= 3.1
%{?with_openmp:BuildRequires:	libgomp-devel}
BuildRequires:	libstdc++-devel >= 6:5
BuildRequires:	nlohmann-json-devel >= 3.1.1
BuildRequires:	rpmbuild(macros) >= 1.605
%{?with_tbb:BuildRequires:	tbb-devel}
%{?with_xsimd:BuildRequires:	xsimd-devel = 10.0.0}
BuildRequires:	xtl-devel >= 0.7.5
%if %{with apidocs}
BuildRequires:	doxygen
BuildRequires:	python3-breathe
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	sphinx-pdg-3
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
xtensor is a C++ library meant for numerical analysis with
multi-dimensional array expressions. It provides:
- an extensible expression system enabling lazy broadcasting.
- an API following the idioms of the C++ standard library.
- tools to manipulate array expressions and build upon xtensor.

%description -l pl.UTF-8
xtensor to biblioteka C++ służąca do analizy numerycznej z
wielowymiarowymi wyrażeniami tablicowymi. Zapewnia:
- rozszerzalny system wyrażeń pozwalający na leniwe rozpraszanie,
- API naśladujące idiomy biblioteki standardowej C++,
- narzędzia do operacji na wyrażeniach tablicowych, zbudowane w
  oparciu o xtensor.

%package devel
Summary:	Multi-dimensional arrays with broadcasting and lazy computing
Summary(pl.UTF-8):	Wielowymiarowe tablice z rozpraszaniem i leniwym obliczaniem
Group:		Development/Libraries
%{?with_openmp:Requires:	libgomp-devel}
Requires:	libstdc++-devel >= 6:5
Requires:	xtl-devel >= 0.7.5

%description devel
xtensor is a C++ library meant for numerical analysis with
multi-dimensional array expressions. It provides:
- an extensible expression system enabling lazy broadcasting.
- an API following the idioms of the C++ standard library.
- tools to manipulate array expressions and build upon xtensor.

%description devel -l pl.UTF-8
xtensor to biblioteka C++ służąca do analizy numerycznej z
wielowymiarowymi wyrażeniami tablicowymi. Zapewnia:
- rozszerzalny system wyrażeń pozwalający na leniwe rozpraszanie,
- API naśladujące idiomy biblioteki standardowej C++,
- narzędzia do operacji na wyrażeniach tablicowych, zbudowane w
  oparciu o xtensor.

%package apidocs
Summary:	API documentation for xtensor library
Summary(pl.UTF-8):	Dokumentacja API biblioteki xtensor
Group:		Documentation

%description apidocs
API documentation for xtensor library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki xtensor.

%prep
%setup -q

%build
install -d build
cd build
# fake LIBDIR so we can create noarch package
%cmake .. \
	-DCMAKE_INSTALL_LIBDIR=%{_datadir} \
	-DDOWNLOAD_BENCHMARK=OFF \
	%{?with_openmp:-DXTENSOR_USE_OPENMP=ON} \
	%{?with_tbb:-DXTENSOR_USE_TBB=ON} \
	%{?with_xsimd:-DXTENSOR_USE_XSIMD=ON}

%{__make}
cd ..

%if %{with apidocs}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files devel
%defattr(644,root,root,755)
%doc LICENSE README.md
%{_includedir}/xtensor.hpp
%{_includedir}/xtensor
%{_npkgconfigdir}/xtensor.pc
%{_datadir}/cmake/xtensor

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_images,_static,*.html,*.js}
%endif
