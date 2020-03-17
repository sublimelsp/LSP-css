import json
import os
import shutil
import sublime
import subprocess
import threading

from sublime_lib import ResourcePath


def run_command(on_exit, on_error, popen_args):
    """
    Runs the given args in a subprocess.Popen, and then calls the function
    on_exit when the subprocess completes.
    on_exit is a callable object, and popen_args is a list/tuple of args that
    on_error when the subprocess throws an error
    would give to subprocess.Popen.
    """
    def run_in_thread(on_exit, on_error, popen_args):
        try:
            subprocess.check_call(popen_args, shell=sublime.platform() == 'windows')
            on_exit()
        except subprocess.CalledProcessError as error:
            on_error(error)

    thread = threading.Thread(target=run_in_thread, args=(on_exit, on_error, popen_args))
    thread.start()
    # returns immediately after the thread starts
    return thread


def log_and_show_message(msg, additional_logs=None):
    print(msg, '\n', additional_logs) if additional_logs else print(msg)
    sublime.active_window().status_message(msg)


class ServerNpmResource(object):
    """Global object providing paths to server resources.
    Also handles the installing and updating of the server in cache.

    setup() needs to be called during (or after) plugin_loaded() for paths to be valid.
    """

    def __init__(self, package_name, server_directory, server_binary_path):
        self._initialized = False
        self._package_name = package_name
        self._server_directory = server_directory
        self._binary_path = server_binary_path
        self._package_cache_path = None

    @property
    def binary_path(self):
        return os.path.join(self._package_cache_path, self._binary_path)

    def setup(self):
        if self._initialized:
            return

        self._initialized = True
        self._package_cache_path = os.path.join(sublime.cache_path(), self._package_name)

        self._copy_to_cache()

    def cleanup(self):
        if os.path.isdir(self._package_cache_path):
            shutil.rmtree(self._package_cache_path)

    def _copy_to_cache(self):
        src_path = 'Packages/{}/{}/'.format(self._package_name, self._server_directory)
        dst_path = 'Cache/{}/{}/'.format(self._package_name, self._server_directory)
        cache_server_path = os.path.join(self._package_cache_path, self._server_directory)

        if os.path.isdir(cache_server_path):
            # Server already in cache. Check if version has changed and if so, delete existing copy in cache.
            try:
                src_package_json = json.loads(ResourcePath(src_path, 'package.json').read_text())
                dst_package_json = json.loads(ResourcePath(dst_path, 'package.json').read_text())

                if src_package_json['version'] != dst_package_json['version']:
                    shutil.rmtree(cache_server_path)
            except FileNotFoundError:
                shutil.rmtree(cache_server_path)

        if not os.path.isdir(cache_server_path):
            # create cache folder
            ResourcePath(src_path).copytree(cache_server_path, exist_ok=True)

        self._install_dependencies(cache_server_path)

    def _install_dependencies(self, cache_server_path):
        dependencies_installed = os.path.isdir(os.path.join(cache_server_path, 'node_modules'))
        print('{}: Server {} installed.'.format(self._package_name, 'is' if dependencies_installed else 'is not'))

        if not dependencies_installed:
            # this will be called only when the plugin gets:
            # - installed for the first time,
            # - or when updated on package control
            log_and_show_message('{}: Installing server.'.format(self._package_name))

            run_command(
                lambda: log_and_show_message(
                    '{}: Server installed.'.format(self._package_name)),
                lambda error: log_and_show_message(
                    '{}: Error while installing the server.'.format(self._package_name), error),
                ["npm", "install", "--verbose", "--production", "--prefix", cache_server_path, cache_server_path]
            )
