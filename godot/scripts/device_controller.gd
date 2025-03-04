extends Node2D


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
