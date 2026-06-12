MODEL_REGISTRY = {
    'accounts.userprofile': {
        'name': 'User Profiles', 'icon': 'bi-person-badge',
        'fields': ('user', 'role', 'phone'),
    },
    'accounts.address': {
        'name': 'Addresses', 'icon': 'bi-geo-alt',
        'fields': ('user', 'city', 'country', 'is_default'),
    },
    'accounts.employeeprofile': {
        'name': 'Employee Profiles', 'icon': 'bi-person-workspace',
        'fields': ('user', 'employee_id', 'department', 'position', 'is_active'),
    },
    'products.category': {
        'name': 'Categories', 'icon': 'bi-folder',
        'fields': ('name', 'slug'),
    },
    'products.brand': {
        'name': 'Brands', 'icon': 'bi-tag',
        'fields': ('name', 'slug', 'description'),
    },
    'products.product': {
        'name': 'Products', 'icon': 'bi-box',
        'fields': ('name', 'category', 'brand', 'price', 'stock', 'available'),
    },
    'products.productimage': {
        'name': 'Product Images', 'icon': 'bi-image',
        'fields': ('product', 'is_primary'),
    },
    'products.productvariation': {
        'name': 'Product Variations', 'icon': 'bi-layers',
        'fields': ('product', 'name', 'value', 'price_adjustment', 'stock'),
    },
    'products.productreview': {
        'name': 'Product Reviews', 'icon': 'bi-star',
        'fields': ('product', 'user', 'rating', 'is_approved'),
    },
    'orders.order': {
        'name': 'Orders', 'icon': 'bi-truck',
        'fields': ('id', 'user', 'first_name', 'status', 'paid', 'created'),
    },
    'orders.orderitem': {
        'name': 'Order Items', 'icon': 'bi-cart',
        'fields': ('order', 'product', 'price', 'quantity'),
    },
    'orders.refund': {
        'name': 'Refunds', 'icon': 'bi-arrow-return-left',
        'fields': ('order', 'amount', 'reason', 'status'),
    },
    'orders.return': {
        'name': 'Returns', 'icon': 'bi-arrow-return-right',
        'fields': ('order', 'reason', 'status'),
    },
    'cart.wishlist': {
        'name': 'Wishlists', 'icon': 'bi-heart',
        'fields': ('user', 'product', 'created'),
    },
    'coupons.coupon': {
        'name': 'Coupons', 'icon': 'bi-ticket-perforated',
        'fields': ('code', 'discount_type', 'discount_value', 'is_active', 'valid_from', 'valid_to'),
    },
    'payment.transaction': {
        'name': 'Transactions', 'icon': 'bi-credit-card',
        'fields': ('order', 'user', 'amount', 'payment_method', 'status'),
    },
    'shipping.shippingzone': {
        'name': 'Shipping Zones', 'icon': 'bi-globe',
        'fields': ('name', 'is_active'),
    },
    'shipping.shippingrate': {
        'name': 'Shipping Rates', 'icon': 'bi-truck',
        'fields': ('zone', 'name', 'price', 'estimated_days', 'is_active'),
    },
    'shipping.shipment': {
        'name': 'Shipments', 'icon': 'bi-box-seam',
        'fields': ('order', 'tracking_number', 'carrier', 'status'),
    },
    'notifications.notification': {
        'name': 'Notifications', 'icon': 'bi-bell',
        'fields': ('user', 'notification_type', 'title', 'is_read', 'created'),
    },
    'cms.sitesettings': {
        'name': 'Site Settings', 'icon': 'bi-gear',
        'fields': ('site_name', 'contact_email', 'contact_phone', 'currency'),
    },
    'cms.banner': {
        'name': 'Banners', 'icon': 'bi-images',
        'fields': ('title', 'is_active', 'order'),
    },
    'cms.faq': {
        'name': 'FAQ', 'icon': 'bi-question-circle',
        'fields': ('question', 'is_active', 'order'),
    },
    'cms.cmspage': {
        'name': 'CMS Pages', 'icon': 'bi-file-text',
        'fields': ('title', 'slug', 'is_active'),
    },
    'support.supportticket': {
        'name': 'Support Tickets', 'icon': 'bi-ticket',
        'fields': ('user', 'subject', 'status', 'priority', 'created'),
    },
    'support.ticketreply': {
        'name': 'Ticket Replies', 'icon': 'bi-chat',
        'fields': ('ticket', 'user', 'created'),
    },
    'support.contactmessage': {
        'name': 'Contact Messages', 'icon': 'bi-envelope-paper',
        'fields': ('full_name', 'email', 'category', 'subject', 'status', 'created'),
    },
    'support.contactreply': {
        'name': 'Contact Replies', 'icon': 'bi-reply',
        'fields': ('contact', 'user', 'created'),
    },
    'activity.activitylog': {
        'name': 'Activity Log', 'icon': 'bi-activity',
        'fields': ('user', 'action', 'model_name', 'created'),
    },
    'loyalty.loyaltypoints': {
        'name': 'Loyalty Points', 'icon': 'bi-star',
        'fields': ('user', 'points', 'reason', 'created'),
    },
    'payroll.payroll': {
        'name': 'Payroll', 'icon': 'bi-wallet2',
        'fields': ('employee', 'month', 'year', 'net_pay', 'is_paid'),
    },
    'payroll.attendance': {
        'name': 'Attendance', 'icon': 'bi-calendar-check',
        'fields': ('employee', 'date', 'is_present', 'notes'),
    },
    'payroll.salaryslip': {
        'name': 'Salary Slips', 'icon': 'bi-file-earmark-text',
        'fields': ('employee', 'gross_salary', 'net_salary', 'is_generated'),
    },
    'vendor.vendor': {
        'name': 'Vendors', 'icon': 'bi-shop',
        'fields': ('business_name', 'business_email', 'is_approved', 'is_active', 'total_earnings'),
    },
    'vendor.vendorpayout': {
        'name': 'Vendor Payouts', 'icon': 'bi-cash',
        'fields': ('vendor', 'amount', 'status', 'created'),
    },
    'vendor.withdrawal': {
        'name': 'Withdrawals', 'icon': 'bi-bank',
        'fields': ('vendor', 'amount', 'status', 'created'),
    },
}


APP_ICONS = {
    'accounts': 'bi-people',
    'products': 'bi-box-seam',
    'orders': 'bi-truck',
    'cart': 'bi-cart',
    'coupons': 'bi-ticket-perforated',
    'payment': 'bi-credit-card',
    'shipping': 'bi-globe',
    'notifications': 'bi-bell',
    'cms': 'bi-layout-text-window',
    'support': 'bi-headset',
    'activity': 'bi-activity',
    'loyalty': 'bi-star',
    'payroll': 'bi-wallet2',
    'vendor': 'bi-shop',
}
