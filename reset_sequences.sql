==================================================
DJANGO SETTINGS ARE LOADED
DEBUG setting is: True
ALLOWED_HOSTS setting is: ['127.0.0.1', 'localhost']
==================================================
BEGIN;
SELECT setval(pg_get_serial_sequence('"app_item"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "app_item";
SELECT setval(pg_get_serial_sequence('"app_orderitem"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "app_orderitem";
SELECT setval(pg_get_serial_sequence('"app_order_items"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "app_order_items";
SELECT setval(pg_get_serial_sequence('"app_order"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "app_order";
SELECT setval(pg_get_serial_sequence('"app_payment"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "app_payment";
SELECT setval(pg_get_serial_sequence('"accounts_customuser_groups"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "accounts_customuser_groups";
SELECT setval(pg_get_serial_sequence('"accounts_customuser_user_permissions"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "accounts_customuser_user_permissions";
SELECT setval(pg_get_serial_sequence('"accounts_customuser"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "accounts_customuser";
COMMIT;
