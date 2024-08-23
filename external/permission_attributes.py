owner_permissions = {
    "resturant": {
        "create_restaurant",
        "update_restaurant",
        "list_restaurant",
        "retrieve_restaurant",
        "delete_restaurant",
    },
    "menu": {"create_menu", "update_menu", "list_menu", "retrieve_menu", "delete_menu"},
    "menu_item": {
        "create_menu_item",
        "update_menu_item",
        "list_menu_item",
        "retrieve_menu_item",
        "delete_menu_item",
    },
}

user_permissions = {
    "resturant": {"list_restaurant"},
    "order": {"create_order", "list_order", "retrieve_order", "delete_order"},
}

employee_permissions = {
    "resturant": {"list_restaurant"},
    "order": {"update_order", "list_order", "delete_order"},
    "payment": {
        "process_payment",
    },
}
