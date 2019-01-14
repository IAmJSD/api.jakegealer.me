from pluginbase import PluginBase
from flask import Flask
from flask_cors import CORS
# Imports go here.

server = Flask(__name__)
# Defines the web server.

CORS(server)
# Handles CORS on the server.

plugin_base = PluginBase(package="__main__.plugins")
plugin_source = plugin_base.make_plugin_source(
    searchpath=["./plugins"]
)
for plugin in plugin_source.list_plugins():
    loaded = plugin_source.load_plugin(plugin)
    loaded.setup(server)
# Loads the plugins.

if __name__ == "__main__":
    server.run(port=7575)
# Starts the server.
