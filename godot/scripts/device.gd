extends Sprite2D
@export var device_id :int
@export var dragging :bool
# Define all port signals
signal port_pressed(port_number: int, device_id: int, port_pos: Vector2)

func _ready():
	# Connect all port input events automatically
	for child in get_children():
		if child is Area2D:
			var port_number = _get_port_number_from_child(child)
			if port_number != null:
				child.connect("input_event", Callable(self, "_handle_port_input").bind(port_number))

func _on_area_2d_input_event(viewport: Node, event: InputEvent, shape_idx: int) -> void:
	if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT and event.pressed:
		if dragging:
			dragging = false
		elif not get_node("../../CableController").is_placing_cable:
			dragging = true

func _handle_port_input(_viewport: Node, event: InputEvent, _shape_idx: int, port_number: int):
	if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT and event.pressed and port_number >0:
		port_pressed.emit(port_number, device_id, get_node("Port" + str(port_number)).global_position)

func _get_port_number_from_child(child: Node) -> int:
	if child.name.begins_with("Port"):
		return child.name.trim_prefix("Port").to_int()
	return -1


func get_port_global_position(port_number: int) -> Vector2:
	# Return global position of the specified port
	var port_node = get_node("Port" + str(port_number))
	return Vector2(port_node.global_position)

func _process(delta: float) -> void:
	if dragging:
		var mouse_pos = get_global_mouse_position()
		set_global_position(mouse_pos)
		get_node("../../ws").update_device_position(device_id, mouse_pos.x, mouse_pos.y)
