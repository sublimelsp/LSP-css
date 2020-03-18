#!/usr/bin/env bash
# @see https://github.com/mattn/vim-lsp-settings/pull/48

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REPO_DIR="${SCRIPT_DIR}"
SRC_DIR="${REPO_DIR}/vscode-css-languageserver"
DIST_DIR="${REPO_DIR}/out"


# ------------------------- #
# download the source codes #
# ------------------------- #

pushd "${REPO_DIR}" || exit

rm -rf \
    "${SRC_DIR}" "${DIST_DIR}" \
    "package.json" "package-lock.json"

# or get the source via git clone
# git clone --depth=1 https://github.com/vscode-langservers/vscode-css-languageserver "${SRC_DIR}"

curl -L https://github.com/vscode-langservers/vscode-css-languageserver/archive/master.tar.gz | tar -xzv
mv vscode-css-languageserver-master "${SRC_DIR}"

popd || exit


# ------------ #
# prepare deps #
# ------------ #

pushd "${SRC_DIR}" || exit

npm install
npm install -D typescript

popd || exit


# ------- #
# compile #
# ------- #

pushd "${SRC_DIR}" || exit

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
    "files": [
        "src/cssServerMain.ts"
    ]
}
EOF

npx tsc --newLine LF -p .

popd || exit


# -------------------- #
# collect output files #
# -------------------- #

pushd "${REPO_DIR}" || exit

mv "${SRC_DIR}/out" "${DIST_DIR}"
cp "${SRC_DIR}/package.json" .
cp "${SRC_DIR}/package-lock.json" .

popd || exit
