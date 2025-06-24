extends CanvasLayer

var inventory_window
var task_window
# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	inventory_window = get_node("./InventoryWindow")
	inventory_window.visible = false
	task_window = get_node("./TaskWindow")
	task_window.visible = false

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass

func _input(event):
	if event.is_action_pressed("inventory"):
		_on_inventory_button_pressed()

	if event.is_action_pressed("tasks"):
		_on_task_button_pressed()

	if event.is_action_pressed("launch_simulation"):
		get_node("res://scripts/ws.gd")._on_launch_button_pressed()
	
# Close action on window
func _on_inventory_window_close_requested() -> void:
	inventory_window.visible = false

func _on_task_window_close_requested() -> void:
	task_window.visible = false


# Button actions to open / close windows
func _on_inventory_button_pressed() -> void:
	inventory_window.visible = not inventory_window.visible
	get_node("./InventoryButton").release_focus()

func _on_task_button_pressed() -> void:
	task_window.visible = not task_window.visible
	get_node("./TaskButton").release_focus()
