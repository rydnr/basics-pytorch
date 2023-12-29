# nix/flake.nix
#
# This file packages basics-pytorch as a Nix flake.
#
# Copyright (C) 2023-today rydnr's rydnr/basics-pytorch
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
{
  description = "A repository to follow PyTorch basic tutorials";
  inputs = rec {
    flake-utils.url = "github:numtide/flake-utils/v1.0.0";
    nixos.url = "github:NixOS/nixpkgs/23.05";
    pythoneda-shared-pythoneda-application = {
      inputs.flake-utils.follows = "flake-utils";
      inputs.nixos.follows = "nixos";
      inputs.pythoneda-shared-pythoneda-banner.follows =
        "pythoneda-shared-pythoneda-banner";
      inputs.pythoneda-shared-pythoneda-domain.follows =
        "pythoneda-shared-pythoneda-domain";
      url = "github:pythoneda-shared-pythoneda-def/application/0.0.30";
    };
    pythoneda-shared-pythoneda-banner = {
      inputs.flake-utils.follows = "flake-utils";
      inputs.nixos.follows = "nixos";
      url = "github:pythoneda-shared-pythoneda-def/banner/0.0.40";
    };
    pythoneda-shared-pythoneda-domain = {
      inputs.flake-utils.follows = "flake-utils";
      inputs.nixos.follows = "nixos";
      inputs.pythoneda-shared-pythoneda-banner.follows =
        "pythoneda-shared-pythoneda-banner";
      url = "github:pythoneda-shared-pythoneda-def/domain/0.0.19";
    };
  };
  outputs = inputs:
    with inputs;
    let
      defaultSystems = flake-utils.lib.defaultSystems;
      supportedSystems = if builtins.elem "armv6l-linux" defaultSystems then
        defaultSystems
      else
        defaultSystems ++ [ "armv6l-linux" ];
    in flake-utils.lib.eachSystem supportedSystems (system:
      let
        org = "rydnr";
        repo = "basics-pytorch";
        version = "0.0.2";
        pname = "${org}-${repo}";
        pythonpackage = "rydnr.basics.pytorch";
        package = builtins.replaceStrings [ "." ] [ "/" ] pythonpackage;
        entrypoint = "basics_pytorch";
        description = "A repository to follow PyTorch basic tutorials";
        license = pkgs.lib.licenses.gpl3;
        homepage = "https://github.com/rydnr/basics-pytorch";
        maintainers = [ "rydnr <github@acm-sl.org>" ];
        archRole = "B";
        space = "D";
        layer = "D";
        nixosVersion = builtins.readFile "${nixos}/.version";
        nixpkgsRelease =
          builtins.replaceStrings [ "\n" ] [ "" ] "nixos-${nixosVersion}";
        pythonCudaOverlay = final: prev: {
          python = prev.python.override {
            packageOverrides = pySelf: pySuper: {
              torchaudio = pySuper.torchaudio.overridePythonAttrs
                (oldAttrs: { cudaSupport = true; });
              torchvision = pySuper.torchvision.overridePythonAttrs
                (oldAttrs: { cudaSupport = true; });
            };
          };
        };
        pkgs = import nixos { inherit system; };
        pkgsCuda = import nixos {
          config = {
            allowUnfree = true;
            allowUnfreePredicate = pkg:
              builtins.elem (pkgs.lib.getName pkg) [ "cudatoolkit" ];
          };
          overlays = [ pythonCudaOverlay ];
          inherit system;
        };
        shared = import "${pythoneda-shared-pythoneda-banner}/nix/shared.nix";
        rydnr-basics-pytorch-for = { cuda-support, pkgs, python
          , pythoneda-shared-pythoneda-application
          , pythoneda-shared-pythoneda-banner, pythoneda-shared-pythoneda-domain
          }:
          let
            pnameWithUnderscores =
              builtins.replaceStrings [ "-" ] [ "_" ] pname;
            pythonVersionParts = builtins.splitVersion python.version;
            pythonMajorVersion = builtins.head pythonVersionParts;
            pythonMajorMinorVersion =
              "${pythonMajorVersion}.${builtins.elemAt pythonVersionParts 1}";
            wheelName =
              "${pnameWithUnderscores}-${version}-py${pythonMajorVersion}-none-any.whl";
            banner_file = "${package}/basics_pytorch.py";
            banner_class = "BasicsPytorchBanner";
            torchPkg = if cuda-support then
              python.pkgs.torchWithCuda
            else
              python.pkgs.torchWithoutCuda;
          in python.pkgs.buildPythonPackage rec {
            inherit pname version;
            projectDir = ./.;
            pyprojectTemplateFile = ./pyprojecttoml.template;
            pyprojectTemplate = pkgs.substituteAll {
              authors = builtins.concatStringsSep ","
                (map (item: ''"${item}"'') maintainers);
              desc = description;
              inherit homepage package pname pythonMajorMinorVersion
                pythonpackage version;
              torch = torchPkg.version;
              torchaudio = python.pkgs.torchaudio.version;
              torchvision = python.pkgs.torchvision.version;
              pythonedaSharedPythonedaApplication =
                pythoneda-shared-pythoneda-application.version;
              pythonedaSharedPythonedaBanner =
                pythoneda-shared-pythoneda-banner.version;
              pythonedaSharedPythonedaDomain =
                pythoneda-shared-pythoneda-domain.version;
              src = pyprojectTemplateFile;
            };
            bannerTemplateFile = ../templates/banner.py.template;
            bannerTemplate = pkgs.substituteAll {
              project_name = pname;
              file_path = banner_file;
              inherit banner_class org repo;
              tag = version;
              pescio_space = space;
              arch_role = archRole;
              hexagonal_layer = layer;
              python_version = pythonMajorMinorVersion;
              nixpkgs_release = nixpkgsRelease;
              src = bannerTemplateFile;
            };

            entrypointTemplateFile =
              "${pythoneda-shared-pythoneda-banner}/templates/entrypoint.sh.template";
            entrypointTemplate = pkgs.substituteAll {
              arch_role = archRole;
              hexagonal_layer = layer;
              nixpkgs_release = nixpkgsRelease;
              inherit homepage maintainers org python repo version;
              pescio_space = space;
              python_version = pythonMajorMinorVersion;
              pythoneda_shared_pythoneda_banner =
                pythoneda-shared-pythoneda-banner;
              pythoneda_shared_pythoneda_domain =
                pythoneda-shared-pythoneda-domain;
              src = entrypointTemplateFile;
            };
            src = ../.;

            format = "pyproject";

            nativeBuildInputs = with python.pkgs; [ pip poetry-core ];
            propagatedBuildInputs = with python.pkgs; [
              pythoneda-shared-pythoneda-application
              pythoneda-shared-pythoneda-banner
              pythoneda-shared-pythoneda-domain
              torchaudio
              torchPkg
              torchvision
            ];

            # pythonImportsCheck = [ pythonpackage ];

            unpackPhase = ''
              cp -r ${src} .
              sourceRoot=$(ls | grep -v env-vars)
              chmod +w $sourceRoot
              find $sourceRoot -type d -exec chmod 777 {} \;
              cp ${pyprojectTemplate} $sourceRoot/pyproject.toml
              cp ${bannerTemplate} $sourceRoot/${banner_file}
              cp ${entrypointTemplate} $sourceRoot/entrypoint.sh
            '';

            postPatch = ''
              substituteInPlace /build/$sourceRoot/entrypoint.sh \
                --replace "@SOURCE@" "$out/bin/${entrypoint}.sh" \
                --replace "@PYTHONEDA_EXTRA_NAMESPACES@" "rydnr" \
                --replace "@PYTHONPATH@" "$PYTHONPATH" \
                --replace "@CUSTOM_CONTENT@" "" \
                --replace "@ENTRYPOINT@" "$out/lib/python${pythonMajorMinorVersion}/site-packages/${package}/application/${entrypoint}.py" \
                --replace "@BANNER@" "$out/bin/banner.sh"
            '';

            postInstall = ''
              pushd /build/$sourceRoot
              for f in $(find . -name '__init__.py'); do
                if [[ ! -e $out/lib/python${pythonMajorMinorVersion}/site-packages/$f ]]; then
                  cp $f $out/lib/python${pythonMajorMinorVersion}/site-packages/$f;
                fi
              done
              popd
              mkdir $out/dist $out/bin
              cp dist/${wheelName} $out/dist
              cp /build/$sourceRoot/entrypoint.sh $out/bin/${entrypoint}.sh
              chmod +x $out/bin/${entrypoint}.sh
              cp -r /build/$sourceRoot/templates $out/lib/python${pythonMajorMinorVersion}/site-packages
              echo '#!/usr/bin/env sh' > $out/bin/banner.sh
              echo "export PYTHONPATH=$PYTHONPATH" >> $out/bin/banner.sh
              echo "echo 'Running $out/bin/banner'" >> $out/bin/banner.sh
              echo "${python}/bin/python $out/lib/python${pythonMajorMinorVersion}/site-packages/${banner_file} \$@" >> $out/bin/banner.sh
              chmod +x $out/bin/banner.sh
            '';

            meta = with pkgs.lib; {
              inherit description homepage license maintainers;
            };
          };
      in rec {
        apps = rec {
          default = rydnr-basics-pytorch-default;
          rydnr-basics-pytorch-default = rydnr-basics-pytorch-python310-cuda;
          rydnr-basics-pytorch-python38 = shared.app-for {
            package = self.packages.${system}.rydnr-basics-pytorch-python38;
            inherit entrypoint;
          };
          rydnr-basics-pytorch-python38-cuda = shared.app-for {
            package =
              self.packages.${system}.rydnr-basics-pytorch-python38-cuda;
            inherit entrypoint;
          };
          rydnr-basics-pytorch-python39 = shared.app-for {
            package = self.packages.${system}.rydnr-basics-pytorch-python39;
            inherit entrypoint;
          };
          rydnr-basics-pytorch-python39-cuda = shared.app-for {
            package =
              self.packages.${system}.rydnr-basics-pytorch-python39-cuda;
            inherit entrypoint;
          };
          rydnr-basics-pytorch-python310 = shared.app-for {
            package = self.packages.${system}.rydnr-basics-pytorch-python310;
            inherit entrypoint;
          };
          rydnr-basics-pytorch-python310-cuda = shared.app-for {
            package =
              self.packages.${system}.rydnr-basics-pytorch-python310-cuda;
            inherit entrypoint;
          };
          rydnr-basics-pytorch-python311 = shared.app-for {
            package = self.packages.${system}.rydnr-basics-pytorch-python311;
            inherit entrypoint;
          };
          rydnr-basics-pytorch-python311-cuda = shared.app-for {
            package =
              self.packages.${system}.rydnr-basics-pytorch-python311-cuda;
            inherit entrypoint;
          };
        };
        defaultApp = apps.default;
        defaultPackage = packages.default;
        devShells = rec {
          default = rydnr-basics-pytorch-default;
          rydnr-basics-pytorch-default = rydnr-basics-pytorch-python310-cuda;
          rydnr-basics-pytorch-python38 = shared.devShell-for {
            banner = "${packages.rydnr-basics-pytorch-python38}/bin/banner.sh";
            extra-namespaces = "rydnr";
            nixpkgs-release = nixpkgsRelease;
            package = packages.rydnr-basics-pytorch-python38;
            pythoneda-shared-pythoneda-banner =
              pythoneda-shared-pythoneda-banner.packages.${system}.pythoneda-shared-pythoneda-banner-python38;
            pythoneda-shared-pythoneda-domain =
              pythoneda-shared-pythoneda-domain.packages.${system}.pythoneda-shared-pythoneda-domain-python38;
            python = pkgs.python38;
            inherit archRole layer org pkgs repo space;
          };
          rydnr-basics-pytorch-python38-cuda = shared.devShell-for {
            banner =
              "${packages.rydnr-basics-pytorch-python38-cuda}/bin/banner.sh";
            extra-namespaces = "rydnr";
            nixpkgs-release = nixpkgsRelease;
            package = packages.rydnr-basics-pytorch-python38-cuda;
            pkgs = pkgsCuda;
            pythoneda-shared-pythoneda-banner =
              pythoneda-shared-pythoneda-banner.packages.${system}.pythoneda-shared-pythoneda-banner-python38;
            pythoneda-shared-pythoneda-domain =
              pythoneda-shared-pythoneda-domain.packages.${system}.pythoneda-shared-pythoneda-domain-python38;
            python = pkgsCuda.python38;
            inherit archRole layer org repo space;
          };
          rydnr-basics-pytorch-python39 = shared.devShell-for {
            banner = "${packages.rydnr-basics-pytorch-python39}/bin/banner.sh";
            extra-namespaces = "rydnr";
            nixpkgs-release = nixpkgsRelease;
            package = packages.rydnr-basics-pytorch-python39;
            pythoneda-shared-pythoneda-banner =
              pythoneda-shared-pythoneda-banner.packages.${system}.pythoneda-shared-pythoneda-banner-python39;
            pythoneda-shared-pythoneda-domain =
              pythoneda-shared-pythoneda-domain.packages.${system}.pythoneda-shared-pythoneda-domain-python39;
            python = pkgs.python39;
            inherit archRole layer org pkgs repo space;
          };
          rydnr-basics-pytorch-python39-cuda = shared.devShell-for {
            banner =
              "${packages.rydnr-basics-pytorch-python39-cuda}/bin/banner.sh";
            extra-namespaces = "rydnr";
            nixpkgs-release = nixpkgsRelease;
            package = packages.rydnr-basics-pytorch-python39-cuda;
            pkgs = pkgsCuda;
            pythoneda-shared-pythoneda-banner =
              pythoneda-shared-pythoneda-banner.packages.${system}.pythoneda-shared-pythoneda-banner-python39;
            pythoneda-shared-pythoneda-domain =
              pythoneda-shared-pythoneda-domain.packages.${system}.pythoneda-shared-pythoneda-domain-python39;
            python = pkgsCuda.python39;
            inherit archRole layer org repo space;
          };
          rydnr-basics-pytorch-python310 = shared.devShell-for {
            banner = "${packages.rydnr-basics-pytorch-python310}/bin/banner.sh";
            extra-namespaces = "rydnr";
            nixpkgs-release = nixpkgsRelease;
            package = packages.rydnr-basics-pytorch-python310;
            pythoneda-shared-pythoneda-banner =
              pythoneda-shared-pythoneda-banner.packages.${system}.pythoneda-shared-pythoneda-banner-python310;
            pythoneda-shared-pythoneda-domain =
              pythoneda-shared-pythoneda-domain.packages.${system}.pythoneda-shared-pythoneda-domain-python310;
            python = pkgs.python310;
            inherit archRole layer org pkgs repo space;
          };
          rydnr-basics-pytorch-python310-cuda = shared.devShell-for {
            banner =
              "${packages.rydnr-basics-pytorch-python310-cuda}/bin/banner.sh";
            extra-namespaces = "rydnr";
            nixpkgs-release = nixpkgsRelease;
            package = packages.rydnr-basics-pytorch-python310-cuda;
            pkgs = pkgsCuda;
            pythoneda-shared-pythoneda-banner =
              pythoneda-shared-pythoneda-banner.packages.${system}.pythoneda-shared-pythoneda-banner-python310;
            pythoneda-shared-pythoneda-domain =
              pythoneda-shared-pythoneda-domain.packages.${system}.pythoneda-shared-pythoneda-domain-python310;
            python = pkgsCuda.python310;
            inherit archRole layer org repo space;
          };
          rydnr-basics-pytorch-python311 = shared.devShell-for {
            banner = "${packages.rydnr-basics-pytorch-python311}/bin/banner.sh";
            extra-namespaces = "rydnr";
            nixpkgs-release = nixpkgsRelease;
            package = packages.rydnr-basics-pytorch-python311;
            pythoneda-shared-pythoneda-banner =
              pythoneda-shared-pythoneda-banner.packages.${system}.pythoneda-shared-pythoneda-banner-python311;
            pythoneda-shared-pythoneda-domain =
              pythoneda-shared-pythoneda-domain.packages.${system}.pythoneda-shared-pythoneda-domain-python311;
            python = pkgs.python311;
            inherit archRole layer org pkgs repo space;
          };
          rydnr-basics-pytorch-python311-cuda = shared.devShell-for {
            banner =
              "${packages.rydnr-basics-pytorch-python311-cuda}/bin/banner.sh";
            extra-namespaces = "rydnr";
            nixpkgs-release = nixpkgsRelease;
            package = packages.rydnr-basics-pytorch-python311-cuda;
            pkgs = pkgsCuda;
            pythoneda-shared-pythoneda-banner =
              pythoneda-shared-pythoneda-banner.packages.${system}.pythoneda-shared-pythoneda-banner-python311;
            pythoneda-shared-pythoneda-domain =
              pythoneda-shared-pythoneda-domain.packages.${system}.pythoneda-shared-pythoneda-domain-python311;
            python = pkgsCuda.python311;
            inherit archRole layer org repo space;
          };
        };
        packages = rec {
          default = rydnr-basics-pytorch-default;
          rydnr-basics-pytorch-default = rydnr-basics-pytorch-python310-cuda;
          rydnr-basics-pytorch-python38 = rydnr-basics-pytorch-for {
            cuda-support = false;
            inherit pkgs;
            python = pkgs.python38;
            pythoneda-shared-pythoneda-application =
              pythoneda-shared-pythoneda-application.packages.${system}.pythoneda-shared-pythoneda-application-python38;
            pythoneda-shared-pythoneda-banner =
              pythoneda-shared-pythoneda-banner.packages.${system}.pythoneda-shared-pythoneda-banner-python38;
            pythoneda-shared-pythoneda-domain =
              pythoneda-shared-pythoneda-domain.packages.${system}.pythoneda-shared-pythoneda-domain-python38;
          };
          rydnr-basics-pytorch-python38-cuda = rydnr-basics-pytorch-for {
            cuda-support = true;
            pkgs = pkgsCuda;
            python = pkgsCuda.python38;
            pythoneda-shared-pythoneda-application =
              pythoneda-shared-pythoneda-application.packages.${system}.pythoneda-shared-pythoneda-application-python38;
            pythoneda-shared-pythoneda-banner =
              pythoneda-shared-pythoneda-banner.packages.${system}.pythoneda-shared-pythoneda-banner-python38;
            pythoneda-shared-pythoneda-domain =
              pythoneda-shared-pythoneda-domain.packages.${system}.pythoneda-shared-pythoneda-domain-python38;
          };
          rydnr-basics-pytorch-python39 = rydnr-basics-pytorch-for {
            cuda-support = false;
            inherit pkgs;
            python = pkgs.python39;
            pythoneda-shared-pythoneda-application =
              pythoneda-shared-pythoneda-application.packages.${system}.pythoneda-shared-pythoneda-application-python39;
            pythoneda-shared-pythoneda-banner =
              pythoneda-shared-pythoneda-banner.packages.${system}.pythoneda-shared-pythoneda-banner-python39;
            pythoneda-shared-pythoneda-domain =
              pythoneda-shared-pythoneda-domain.packages.${system}.pythoneda-shared-pythoneda-domain-python39;
          };
          rydnr-basics-pytorch-python39-cuda = rydnr-basics-pytorch-for {
            cuda-support = true;
            pkgs = pkgsCuda;
            python = pkgsCuda.python39;
            pythoneda-shared-pythoneda-application =
              pythoneda-shared-pythoneda-application.packages.${system}.pythoneda-shared-pythoneda-application-python39;
            pythoneda-shared-pythoneda-banner =
              pythoneda-shared-pythoneda-banner.packages.${system}.pythoneda-shared-pythoneda-banner-python39;
            pythoneda-shared-pythoneda-domain =
              pythoneda-shared-pythoneda-domain.packages.${system}.pythoneda-shared-pythoneda-domain-python39;
          };
          rydnr-basics-pytorch-python310 = rydnr-basics-pytorch-for {
            cuda-support = false;
            inherit pkgs;
            python = pkgs.python310;
            pythoneda-shared-pythoneda-application =
              pythoneda-shared-pythoneda-application.packages.${system}.pythoneda-shared-pythoneda-application-python310;
            pythoneda-shared-pythoneda-banner =
              pythoneda-shared-pythoneda-banner.packages.${system}.pythoneda-shared-pythoneda-banner-python310;
            pythoneda-shared-pythoneda-domain =
              pythoneda-shared-pythoneda-domain.packages.${system}.pythoneda-shared-pythoneda-domain-python310;
          };
          rydnr-basics-pytorch-python310-cuda = rydnr-basics-pytorch-for {
            cuda-support = true;
            pkgs = pkgsCuda;
            python = pkgsCuda.python310;
            pythoneda-shared-pythoneda-application =
              pythoneda-shared-pythoneda-application.packages.${system}.pythoneda-shared-pythoneda-application-python310;
            pythoneda-shared-pythoneda-banner =
              pythoneda-shared-pythoneda-banner.packages.${system}.pythoneda-shared-pythoneda-banner-python310;
            pythoneda-shared-pythoneda-domain =
              pythoneda-shared-pythoneda-domain.packages.${system}.pythoneda-shared-pythoneda-domain-python310;
          };
          rydnr-basics-pytorch-python311 = rydnr-basics-pytorch-for {
            cuda-support = false;
            inherit pkgs;
            python = pkgs.python311;
            pythoneda-shared-pythoneda-application =
              pythoneda-shared-pythoneda-application.packages.${system}.pythoneda-shared-pythoneda-application-python311;
            pythoneda-shared-pythoneda-banner =
              pythoneda-shared-pythoneda-banner.packages.${system}.pythoneda-shared-pythoneda-banner-python311;
            pythoneda-shared-pythoneda-domain =
              pythoneda-shared-pythoneda-domain.packages.${system}.pythoneda-shared-pythoneda-domain-python311;
          };
          rydnr-basics-pytorch-python311-cuda = rydnr-basics-pytorch-for {
            cuda-support = true;
            pkgs = pkgsCuda;
            python = pkgsCuda.python311;
            pythoneda-shared-pythoneda-application =
              pythoneda-shared-pythoneda-application.packages.${system}.pythoneda-shared-pythoneda-application-python311;
            pythoneda-shared-pythoneda-banner =
              pythoneda-shared-pythoneda-banner.packages.${system}.pythoneda-shared-pythoneda-banner-python311;
            pythoneda-shared-pythoneda-domain =
              pythoneda-shared-pythoneda-domain.packages.${system}.pythoneda-shared-pythoneda-domain-python311;
          };
        };
      });
}
