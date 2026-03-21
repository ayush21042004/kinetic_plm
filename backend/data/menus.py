from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from backend.core.menu_manager import MenuManager, MenuItem

def initialize_menus(menu_manager: 'MenuManager'):
    from backend.core.menu_manager import MenuItem

    # ── ECO ───────────────────────────────────────────────────────────────────
    eco_group = "ECO"
    menu_manager.add_item(eco_group, MenuItem(
        "eco_list", "Engineering Change Orders", "/models/plm.eco",
        "ClipboardList", sequence=10,
        groups=["admin", "engineering", "approver", "operations"]
    ))

    # Master Data (parent label only — children are the real links)
    menu_manager.add_item(eco_group, MenuItem(
        "master_data", "Master Data", None,
        "Database", sequence=20,
        groups=["admin", "engineering", "approver", "operations"],
        children=[
            MenuItem(
                "product_versions", "Products",
                "/models/product.version",
                "Layers", sequence=10,
                groups=["admin", "engineering", "approver", "operations"]
            ),
            MenuItem(
                "bom_list", "Bill of Materials",
                "/models/mrp.bom",
                "List", sequence=20,
                groups=["admin", "engineering", "approver", "operations"]
            ),
            MenuItem(
                "work_centers", "Work Centers",
                "/models/work.center",
                "Factory", sequence=30,
                groups=["admin", "engineering", "approver", "operations"]
            ),
        ]
    ))

    menu_manager.add_item(eco_group, MenuItem(
        "reporting", "Reporting", "/reporting",
        "BarChart3", sequence=30,
        groups=["admin", "engineering", "approver", "operations"]
    ))

    # Settings (dropdown under ECO group)
    menu_manager.add_item(eco_group, MenuItem(
        "settings", "Settings", None,
        "Settings", sequence=40,
        groups=["admin"],
        children=[
            MenuItem(
                "eco_stages", "ECO Stages", "/models/plm.eco.stage",
                "Milestone", sequence=20, groups=["admin"]
            ),
            MenuItem(
                "users", "Users", "/models/user",
                "Users", sequence=10, groups=["admin"]
            ),
            MenuItem(
                "sequences", "Sequences", "/models/sequence",
                "LayoutGrid", sequence=30, groups=["admin"]
            ),
            MenuItem(
                "crons", "Cron Jobs", "/models/cron",
                "Clock", sequence=40, groups=["admin"]
            ),
        ]
    ))
