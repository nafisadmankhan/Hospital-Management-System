#!/bin/sh
# Ensure dependencies are installed
composer install

# Start the Laravel server
php artisan serve --host=0.0.0.0 --port=8000