from ...tools.tools import define_toolkit, description

Todos = dict[str, bool]
todos: Todos = {}

tool, resource, register_toolkit = define_toolkit()


@resource.create(
    description=description(
        """
        Gets the user's to do list items that still haven't been completed
        NOTE: This function only runs if the user explicitely asks for the remaining to do list items
        """,
        returns=[
            (
                "list[str]",
                "The list of items that still haven't been completed by the user",
            )
        ],
    ),
)
def get_to_do_list_remaining_items() -> list[str]:
    items: list[str] = []
    for todo in todos.keys():
        if not todos[todo]:
            items.append(todo)
    return items


@resource.create(
    description=description(
        """
        Gets the user's to do list items that have been completed
        NOTE: This function only runs if the user explicitely asks for the done to do list items
        """,
        returns=[
            ("list[str]", "The list of items that have been completed by the user")
        ],
    ),
)
def get_to_do_done_items() -> list[str]:
    items: list[str] = []
    for todo in todos.keys():
        if todos[todo]:
            items.append(todo)
    return items


@tool.create(
    description=description(
        """
        Adds an item to the to do list
        NOTE: This function only runs if the user explicitely asks for the a to do item to be added
        """,
        args=[("item", "The item to add to the to do list")],
    ),
)
def add_item_to_to_do_list(item: str):
    found_item = todos.get(item, None)
    if found_item is not None:
        todos[item] = False


@tool.create(
    description=description(
        """
        Removes an item from the to do list if it exists
        NOTE: This function only runs if the user explicitely asks for the a to do item to be removed
        """,
        args=[("item", "The item to remove from the to do list")],
    ),
)
def remove_items_from_to_do_list(item: str):
    found_item = todos.get(item, None)
    if found_item is not None:
        del todos[item]


@tool.create(
    description=description(
        """
        Marks a to do item as completed or not completed
        NOTE: This function only runs if the user explicitely asks for the a to do item to be marked
        """,
        args=[
            ("item", "The item in the to do list to mark"),
            ("completed", "The item to remove from the to do list"),
        ],
    ),
)
def mark_to_do_item(item: str, completed: bool):
    found_item = todos.get(item, None)
    if found_item is not None:
        todos[item] = completed
