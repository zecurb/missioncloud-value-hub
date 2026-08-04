{
  description = "MissionCloud Value Hub development environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-26.05";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
      in {
        devShells.default = pkgs.mkShell {
          packages = with pkgs; [
            nodejs_24
            python313
            uv
            ruff
            git
            gh
            gnumake
            docker
            postgresql_17
            postgresql_17.dev
            postgresql_17.pg_config
            pkg-config
            gcc
            jq
          ];

          shellHook = ''
            export UV_PYTHON=${pkgs.python313}/bin/python
            echo "MissionCloud Value Hub development shell"
            echo "Run: make api-install && make web-install"
          '';
        };
      });
}
