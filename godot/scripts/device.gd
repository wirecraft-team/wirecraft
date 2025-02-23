extends Sprite2D
@export var device_id :int
# Define all port signals
signal port_pressed(port_number: int, device_id: int, port_pos: Vector2)

func _ready():
	# Connect all port input events automatically
	for child in get_children():
		if child is Area2D:
			var port_number = _get_port_number_from_child(child)
			if port_number != null:
				child.connect("input_event", Callable(self, "_handle_port_input").bind(port_number))

func _handle_port_input(_viewport: Node, event: InputEvent, _shape_idx: int, port_number: int):
	if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT and event.pressed:
		port_pressed.emit(port_number, device_id, get_node("Port" + str(port_number)).global_position)

func _get_port_number_from_child(child: Node) -> int:
	if child.name.begins_with("Port"):
		return child.name.trim_prefix("Port").to_int()
	return -1


func get_port_global_position(port_number: int) -> Vector2:
	# Return global position of the specified port
	var port_node = get_node("Port" + str(port_number))
	return Vector2(port_node.global_position)
