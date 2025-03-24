extends Node2D

static var is_placing_cable: bool = false
static var port_occupied: bool = false
var current_cable: Line2D = null
var start_switch: int = -1
var start_port: int = -1
var cable_scene = preload("res://scenes/cable.tscn")

func _ready():
	update_device_signal()

func update_device_signal():
	for device in get_node("../DeviceController").get_children():
		device.connect("port_pressed", Callable(self, "_on_port_pressed"))

func _on_port_pressed(port_number: int, device_id: int, port_pos: Vector2):
	if is_placing_cable:
		finish_cable(port_number, device_id, port_pos)
	else:
		start_placing_cable(port_number, device_id, port_pos)

func start_placing_cable(port_number: int, device_id: int, port_pos: Vector2):
	port_occupied = get_port_satus(device_id, port_number)
	if port_occupied:
		return
	# Start placing a cable
	is_placing_cable = true
	# Create a new cable
	current_cable = cable_scene.instantiate()
	current_cable.add_point(port_pos)
	current_cable.add_point(get_global_mouse_position())
	add_child(current_cable)
	current_cable.z_index = 1
	# change exported properties
	current_cable.start_switch = device_id
	current_cable.start_port = port_number
	current_cable.end_switch = -1
	current_cable.end_port = -1

func finish_cable(port_number: int, device_id: int, port_pos:Vector2):
	port_occupied = get_port_satus(device_id, port_number)
	if port_occupied or device_id == current_cable.start_switch:
		return
	# Finish placing a cable
	is_placing_cable = false	
	# Connect the cable to the switches
	var definitive_cable = current_cable
	definitive_cable.set_point_position(1, port_pos)
	definitive_cable.end_switch = device_id
	definitive_cable.end_port = port_number
	# Send cable information to the server
	get_node("../ws").send_cable(definitive_cable.start_switch, definitive_cable.start_port, definitive_cable.end_switch, definitive_cable.end_port)

func _process(_delta):
	if is_placing_cable and Input.is_action_just_released("ui_cancel"):
		is_placing_cable = false
		current_cable.queue_free()
	if is_placing_cable and current_cable:
		# Update temporary end point to follow mouse
		var mouse_pos = get_global_mouse_position()
		current_cable.set_point_position(1, mouse_pos)

func get_port_satus(device_id: int, port_number: int) -> bool:
	# Check if the port is already occupied. Will check with server later
	for cable in get_children():
		if cable.start_switch == device_id and cable.start_port == port_number:
			return true
		if cable.end_switch == device_id and cable.end_port == port_number:
			return true
	return false


func update_cables(cables: Array):
	#removes all cables
	for cable in get_children():
		cable.queue_free()
	#cables is like [{ "device_id_1": 1, "id": 1, "port_2": 1, "port_1": 1, "device_id_2": 2, "level_id": 1 }]
	print("cables are",cables)
	# Update cables based on the data received from the server
	for cable in cables:
		var new_cable = cable_scene.instantiate()
		new_cable.start_switch = cable.device_id_1
		new_cable.start_port = cable.port_1
		new_cable.end_switch = cable.device_id_2
		new_cable.end_port = cable.port_2
		new_cable.z_index = 1
		new_cable.add_point(get_node("../DeviceController").get_device_port_position(cable.device_id_1, cable.port_1))
		new_cable.add_point(get_node("../DeviceController").get_device_port_position(cable.device_id_2, cable.port_2))
		add_child(new_cable)
