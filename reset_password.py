#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import odoo
from odoo import api, SUPERUSER_ID

# Load Odoo configuration
odoo.tools.config.parse_config(['--config=/home/trinhhao/odoo-fitdnu/odoo.conf'])

# Connect to database
db_name = 'TrinhHao_Odoo'
registry = odoo.registry(db_name)

with registry.cursor() as cr:
    env = api.Environment(cr, SUPERUSER_ID, {})
    
    # Find admin user
    admin_user = env['res.users'].search([('id', '=', 2)])
    
    if admin_user:
        # Update password and login
        admin_user.write({
            'login': 'haotrinh142@gmail.com',
            'password': 'trinhhao142'
        })
        cr.commit()
        print(f"Password reset successfully for user: {admin_user.login}")
    else:
        print("Admin user not found!")
