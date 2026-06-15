# Copyright 2026 Wong Hoi Sing Edison <hswong3i@pantarei-design.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

%global debug_package %{nil}

%global source_date_epoch_from_changelog 0

Name: helm-diff
Epoch: 100
Version: 3.15.9
Release: 1%{?dist}
Summary: Helm Diff Plugin
License: Apache-2.0
URL: https://github.com/databus23/helm-diff/tags
Source0: %{name}_%{version}.orig.tar.gz
BuildRequires: golang-1.26
BuildRequires: glibc-static
Requires: helm

%description
A helm plugin that shows a diff explaining what a helm upgrade would
change.

%prep
%autosetup -T -c -n %{name}_%{version}-%{release}
tar -zx -f %{S:0} --strip-components=1 -C .

%build
mkdir -p bin
set -ex && \
    export CGO_ENABLED=0 && \
    go build \
        -mod vendor -buildmode pie -v \
        -ldflags "-s -w -extldflags '-static -lm' \
            -X github.com/databus23/helm-diff/v3/cmd.Version=3.15.9 \
        " \
        -o ./bin/diff .

%install
install -Dpm755 -d %{buildroot}%{_datadir}/helm/plugins/helm-diff/bin
install -Dpm755 -t %{buildroot}%{_datadir}/helm/plugins/helm-diff/bin bin/diff
install -Dpm644 -t %{buildroot}%{_datadir}/helm/plugins/helm-diff plugin.yaml

%files
%license LICENSE
%dir %{_datadir}/helm
%dir %{_datadir}/helm/plugins
%dir %{_datadir}/helm/plugins/helm-diff
%{_datadir}/helm/plugins/helm-diff/*

%changelog
