from .agent import Toolkit, create_tool_handlers, create_tool_repository

Todos = dict[str, bool]
todos: Todos = {}

def get_to_do_list_remaining_items() -> list[str]:
    """
    Gets the user's to do list items that still haven't been completed
    NOTE: This function only runs if the user explicitely asks for the remaining to do list items

    Returns:
        list[str]: The list of items that still haven't been completed by the user
    """

    items: list[str] = []
    for todo in todos.keys():
        if not todos[todo]:
            items.append(todo)
    return items

def get_to_do_done_items() -> list[str]:
    """
    Gets the user's to do list items that have been completed
    NOTE: This function only runs if the user explicitely asks for the done to do list items

    Returns:
        list[str]: The list of items that have been completed by the user
    """

    items: list[str] = []
    for todo in todos.keys():
        if todos[todo]:
            items.append(todo)
    return items

def add_item_to_to_do_list(item: str):
    """
    Adds an item to the to do list
    NOTE: This function only runs if the user explicitely asks for the a to do item to be added

    Args:
        item: The item to add to the to do list
    """

    found_item = todos.get(item, None)
    if found_item is not None:
        todos[item] = False

def remove_items_from_to_do_list(item: str):
    """
    Removes an item from the to do list if it exists
    NOTE: This function only runs if the user explicitely asks for the a to do item to be removed

    Args:
        item: The item to remove from the to do list
    """
    found_item = todos.get(item, None)
    if found_item is not None:
        del todos[item]

def mark_to_do_item(item: str, completed: bool):
    """
    Marks a to do item as completed or not completed
    NOTE: This function only runs if the user explicitely asks for the a to do item to be marked

    Args:
        item: The item in the to do list to mark
        completed: The item to remove from the to do list
    """
    found_item = todos.get(item, None)
    if found_item is not None:
        todos[item] = completed

_repository = create_tool_repository(
    add_item_to_to_do_list,
    remove_items_from_to_do_list,
    get_to_do_done_items,
    get_to_do_list_remaining_items,
    mark_to_do_item
)
_handlers = create_tool_handlers(lambda tool_call: {
    add_item_to_to_do_list: [tool_call.function.arguments.get('item')],
    remove_items_from_to_do_list: [tool_call.function.arguments.get('item')],
    get_to_do_done_items: [],
    get_to_do_list_remaining_items: [],
    mark_to_do_item: [
        tool_call.function.arguments.get("item"),
        tool_call.function.arguments.get('completed')
    ]
})

to_do_toolkit = Toolkit(repository=_repository, handlers=_handlers)
