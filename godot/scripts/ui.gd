extends CanvasLayer

var inventory_window
# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	inventory_window = get_node("./Window")
	inventory_window.visible = false


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass


func _on_window_close_requested() -> void:
	inventory_window.visible = false


func _on_button_pressed() -> void:
	inventory_window.visible = not inventory_window.visible
	get_node("./Button").release_focus()
