extends Node2D

var pc_scene = preload("res://scenes/pc.tscn")
var switch_scene = preload("res://scenes/switch.tscn")

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass

func get_device_port_position(device_id: int, port_number: int) -> Vector2:
	var devices = self.get_children()
	for device in devices:
		if device.device_id == device_id:
			return device.call("get_port_global_position", port_number)
	return Vector2.ZERO


func update_devices(devices: Array):
	#removes all cables
	for devivce in get_children():
		devivce.queue_free()
	#devices is like [{ "id": 1, "name": "PC-1", "type": "pc", "x": 100, "y": 100, "ports": 1}, ...]
	# Update devices based on the data received from the server
	print("devices are",devices)
	for device in devices:
		var new_device = null
		match device.type:
			"pc":
				new_device = pc_scene.instantiate()
			"switch":
				new_device = switch_scene.instantiate()
		if new_device == null:
			continue
		new_device.device_id = device.id
		new_device.name = device.name
		new_device.position = Vector2(device.x, device.y)
		add_child(new_device)
		new_device.z_index = 0
		# Update the device's ports
		#new_device.call("update_ports", device.ports)
