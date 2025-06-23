extends Node

# The URL we will connect to.
@export var websocket_url = "ws://localhost:8765"

# Our WebSocketClient instance.
var socket = WebSocketPeer.new()
var CableControler = preload("res://scripts/cable_controller.gd")

func _ready():
	# Initiate connection to the given URL.
	var err = socket.connect_to_url(websocket_url)
	if err != OK:
		print("Unable to connect")
		set_process(false)
	else:
		# Wait for the socket to connect.
		await get_tree().create_timer(0.25).timeout
		# Send data.
		socket.send_text('{"t": "GET_LEVEL_DEVICES", "d": {"level_id": 1}}')
		socket.send_text('{"t": "GET_LEVEL_CABLES", "d": {"level_id": 1}}')
		socket.send_text('{"t": "GET_LEVEL_TASKS", "d": {"level_id": 1}}')


func _process(_delta):
	# Call this in _process or _physthisics_process. Data transfer and state updates
	# will only happen when calling  function.
	socket.poll()

	# get_ready_state() tells you what state the socket is in.
	var state = socket.get_ready_state()

	# WebSocketPeer.STATE_OPEN means the socket is connected and ready
	# to send and receive data.
	if state == WebSocketPeer.STATE_OPEN:
		get_node("../CanvasLayer/ServerText").visible = false
		while socket.get_available_packet_count():
			var packet_data = socket.get_packet().get_string_from_utf8()
			# parse data and see if type is "GET_LEVEL_CABLES"
			var json = JSON.new()
			var error = json.parse(packet_data)
			if error == OK:
				var data_received = json.data
				if data_received.t == "GET_LEVEL_CABLES_RESPONSE":
					#call update_cable function in CableControler
					get_node("../CableController").update_cables(data_received.d)
				if data_received.t == "GET_LEVEL_DEVICES_RESPONSE":
					#call update_devices function in CableControler
					get_node("../DeviceController").update_devices(data_received.d)
					get_node("../CableController").update_device_signal()
				if data_received.t == "GET_LEVEL_TASKS_RESPONSE":
					print("tasks are :" , data_received.d)
					get_node("/root/Control/CanvasLayer/TaskWindow").update_tasks(data_received.d)
			else:
				print("Error ", error)

	# WebSocketPeer.STATE_CLOSING means the socket is closing.
	# It is important to keep polling for a clean close.
	elif state == WebSocketPeer.STATE_CLOSING:
		pass

	# WebSocketPeer.STATE_CLOSED means the connection has fully closed.
	# It is now safe to stop polling.
	elif state == WebSocketPeer.STATE_CLOSED:
		# The code will be -1 if the disconnection was not properly notified by the remote peer.
		var code = socket.get_close_code()
		print("WebSocket closed with code: %d. Clean: %s" % [code, code != -1])
		set_process(false) # Stop processing.

func send_cable(start_id:int, start_port:int, end_id:int, end_port:int):
	# Send cable information to the server
	#TODO: Don't hardcode level_id
	socket.send_text('{"t": "ADD_CABLE", "d": {"device_id_1": %d, "port_1": %d, "device_id_2": %d, "port_2": %d, "level_id": 1}}' % [start_id, start_port, end_id, end_port])

func add_device(device_name, device_type):
	socket.send_text('{"t":"ADD_DEVICE", "d":{"name":"%s", "type":"%s", "x":0, "y":0, "level_id":1}}' % [device_name, device_type])
	socket.send_text('{"t": "GET_LEVEL_DEVICES", "d": {"level_id": 1}}')
	socket.send_text('{"t": "GET_LEVEL_CABLES", "d": {"level_id": 1}}')

func update_device_position(device_id:int, x:float, y:float):
	socket.send_text('{"t": "UPDATE_DEVICE_POSITION", "d": {"device_id": %d, "x": %d, "y": %d}}' % [device_id, int(x), int(y)])
	socket.send_text('{"t": "GET_LEVEL_CABLES", "d": {"level_id": 1}}')

func update_tasks():
	socket.send_text('{"t": "GET_LEVEL_TASKS", "d": {"level_id": 1}}')


func _on_line_edit_text_submitted(new_text: String) -> void:
	var ip_editing_device = get_node("../CanvasLayer/LineEdit").device_id
	if ip_editing_device == -1:
		return
	var data = {"t":"UPDATE_IP","d":{"device":ip_editing_device, "ip":new_text}}
	socket.send_text(JSON.stringify(data))
	get_node("../CanvasLayer/LineEdit").visible = false
	get_node("../CanvasLayer/LineEdit").text = ""
	
	
func _on_launch_button_pressed() -> void:
		socket.send_text('{"t": "LAUNCH_SIMULATION", "d": {"level_id": 1}}')
