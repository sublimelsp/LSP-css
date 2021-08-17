#!/usr/bin/env bash

GITHUB_REPO_URL="https://github.com/microsoft/vscode"
GITHUB_REPO_NAME=$(echo "${GITHUB_REPO_URL}" | command grep -oE '[^/]*$')

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REPO_DIR="${SCRIPT_DIR}"
SRC_DIR="${REPO_DIR}/${GITHUB_REPO_NAME}/extensions/css-language-features/server"
DIST_DIR="${REPO_DIR}/css-language-features/server"


# -------- #
# clean up #
# -------- #

pushd "${REPO_DIR}" || exit

rm -rf \
    "css-language-features/" \
    "package.json" "package-lock.json"

popd || exit


# ------------------------- #
# download the source codes #
# ------------------------- #

pushd "${REPO_DIR}" || exit

echo 'Enter commit SHA, branch or tag (for example 2.1.0) to build'
read -rp 'SHA, branch or tag (default: main): ' ref

# use the "main" branch by default
if [ "${ref}" = "" ]; then
    ref="main"
fi

temp_zip="src-${ref}.zip"
curl -L "${GITHUB_REPO_URL}/archive/${ref}.zip" -o "${temp_zip}"
unzip -z "${temp_zip}" | tr -d '\r' > update-info.log
unzip "${temp_zip}" && rm -f "${temp_zip}"
mv "${GITHUB_REPO_NAME}-"* "${GITHUB_REPO_NAME}"

popd || exit


# ------------ #
# prepare deps #
# ------------ #

pushd "${SRC_DIR}" || exit

npm install

# @see https://github.com/microsoft/vscode/blob/main/extensions/package.json
npm install -D typescript@^4.4.1-rc

popd || exit


# ------- #
# compile #
# ------- #

pushd "${SRC_DIR}" || exit

# @see https://github.com/microsoft/vscode/blob/main/extensions/tsconfig.base.json
cat << EOF > tsconfig.json
{
    "compilerOptions": {
        "target": "es2020",
        "lib": [
            "ES2016",
            "ES2017.Object",
            "ES2017.String",
            "ES2017.Intl",
            "ES2017.TypedArrays",
            "ES2018.AsyncIterable",
            "ES2018.AsyncGenerator",
            "ES2018.Promise",
            "ES2018.Regexp",
            "ES2018.Intl",
            "ES2019.Array",
            "ES2019.Object",
            "ES2019.String",
            "ES2019.Symbol",
            "ES2020.BigInt",
            "ES2020.Promise",
            "ES2020.String",
            "ES2020.Symbol.WellKnown",
            "ES2020.Intl"
        ],
        "module": "commonjs",
        "strict": true,
        "exactOptionalPropertyTypes": false,
        "useUnknownInCatchVariables": false,
        "alwaysStrict": true,
        "noImplicitAny": true,
        "noImplicitReturns": true,
        "noImplicitOverride": true,
        "noUnusedLocals": true,
        "noUnusedParameters": true,
        "forceConsistentCasingInFileNames": true,
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

mkdir -p "${DIST_DIR}"

cp -rf "${SRC_DIR}/out" "${DIST_DIR}"
cp "${SRC_DIR}/package.json" .
cp "${SRC_DIR}/package-lock.json" .

popd || exit


# -------- #
# clean up #
# -------- #

pushd "${REPO_DIR}" || exit

rm -rf "${GITHUB_REPO_NAME}"

popd || exit
