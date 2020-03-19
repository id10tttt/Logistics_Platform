#!/usr/bin/env bash

# default log path ~/sentinel.log
export ODOO_SENTINEL_CODE=hard1
./__init__.py -c ~/.odoorpcrc $1 $2
