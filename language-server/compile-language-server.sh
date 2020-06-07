#!/usr/bin/env bash
# @see https://github.com/mattn/vim-lsp-settings/pull/48

GITHUB_REPO_URL="https://github.com/vscode-langservers/vscode-css-languageserver"
GITHUB_REPO_NAME=$(echo "${GITHUB_REPO_URL}" | command grep -oE '[^/]*$')

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REPO_DIR="${SCRIPT_DIR}"
SRC_DIR="${REPO_DIR}/${GITHUB_REPO_NAME}"
DIST_DIR="${REPO_DIR}/out"


# ------------------------- #
# download the source codes #
# ------------------------- #

pushd "${REPO_DIR}" || exit

rm -rf \
    "${SRC_DIR}" "${DIST_DIR}" \
    "package.json" "package-lock.json"

# or get the source via git clone
# git clone --depth=1 "${GITHUB_REPO_URL}.git" "${SRC_DIR}"

curl -L "${GITHUB_REPO_URL}/archive/master.tar.gz" | tar -xzv
mv "${GITHUB_REPO_NAME}-master" "${SRC_DIR}"

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
        "src/node/cssServerMain.ts"
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
