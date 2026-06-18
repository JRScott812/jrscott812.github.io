@echo off
cd /d "%~dp0"
bundle exec jekyll serve --livereload --config _config.yml,_config_dev.yml --host 127.0.0.1 --port 4000
