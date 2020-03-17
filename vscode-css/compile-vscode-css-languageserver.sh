#!/usr/bin/env bash
# @see https://github.com/mattn/vim-lsp-settings/pull/48

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REPO_DIR="${SCRIPT_DIR}"
SRC_DIR="${REPO_DIR}/vscode-css-languageserver"
DIST_DIR="${REPO_DIR}/out"


# ------------------------- #
# download the source codes #
# ------------------------- #

pushd "${SCRIPT_DIR}" || exit

rm -rf "${SRC_DIR}" "${DIST_DIR}"

# or get the source via git clone
# git clone --depth=1 https://github.com/vscode-langservers/vscode-css-languageserver "${SRC_DIR}"

wget https://github.com/vscode-langservers/vscode-css-languageserver/archive/master.zip -O src.zip
unzip src.zip
rm -f src.zip
mv vscode-css-languageserver-master "${SRC_DIR}"

popd || exit


# ------------ #
# prepare deps #
# ------------ #

pushd "${SRC_DIR}" || exit

npm install
npm install --save typescript
cat << EOF > tsconfig.json
{
	"compilerOptions": {
		"target": "es2018",
		"module": "commonjs",
		"strict": true,
		"alwaysStrict": true,
		"noImplicitAny": true,
		"noImplicitReturns": true,
		"noUnusedLocals": true,
		"noUnusedParameters": true,
		"outDir": "./out"
	},
	"include": [
		"src/**/*"
	]
}
EOF

popd || exit


# ------- #
# compile #
# ------- #

pushd "${SRC_DIR}" || exit

./node_modules/typescript/bin/tsc -p .

cp package.json "${REPO_DIR}"
mv out "${DIST_DIR}"

popd || exit
