extends Node
# The URL we will connect to.
@export var websocket_url = "ws://localhost:8765"
# Our WebSocketClient instance.
var socket = WebSocketPeer.new()
var CableControler = preload("res://scripts/cable_controller.gd")


func connect_to_server():
	socket = WebSocketPeer.new()
	var err = socket.connect_to_url(websocket_url)
	if err != OK:
		print("Unable to connect")
		print(err)
		set_process(false)
	else:
		set_process(true)

func _ready():
	connect_to_server()
		# Wait for the socket to connect.
	await get_tree().create_timer(0.25).timeout
		# Send data.
	socket.send_text('{"t": "GET_LEVEL_DEVICES", "d": {"level_id":'+ str(Global.level_id)+'}}')
	socket.send_text('{"t": "GET_LEVEL_CABLES", "d": {"level_id":'+ str(Global.level_id)+'}}')
	socket.send_text('{"t": "GET_LEVEL_TASKS", "d": {"level_id":'+ str(Global.level_id)+'}}')


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
					Global.dragging = false
					get_node("../DeviceController").update_devices(data_received.d)
					get_node("../CableController").update_device_signal()
				if data_received.t == "GET_LEVEL_TASKS_RESPONSE":
					get_node("/root/Control/CanvasLayer/TaskWindow").update_tasks(data_received.d)
					check_completion(data_received.d)
				if data_received.t == "GET_DEVICE_RESPONSE":
					if data_received.d.ip:
						get_node("../CanvasLayer/InputGroup/IpAdressInput").text = data_received.d.ip
					get_node("../CanvasLayer/InputGroup/NameInput").text = data_received.d.name					
				# if data_received.t == "GET_NAME_RESPONSE":
				if data_received.t == "ADD_CABLE_RESPONSE":
					update_cables()
				if data_received.t == "ADD_DEVICE_RESPONSE":
					update_devices()
				if data_received.t == "UPDATE_DEVICE_POSITION_RESPONSE":
					update_devices()
					update_cables()
				
				if data_received.t == "UPDATE_LEVEL_ID_RESPONSE":
					Global.level_id = data_received.d.level_id
					update_game()
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
	#TODO: Don't hardcode Global.level_id
	socket.send_text('{"t": "ADD_CABLE", "d": {"device_id_1": %d, "port_1": %d, "device_id_2": %d, "port_2": %d, "level_id": %d}}' % [start_id, start_port, end_id, end_port, Global.level_id])

func add_device(device_name, device_type):
	socket.send_text('{"t":"ADD_DEVICE", "d":{"name":"%s", "type":"%s", "x":0, "y":0, "level_id":%d}}' % [device_name, device_type, Global.level_id])
	socket.send_text('{"t": "GET_LEVEL_DEVICES", "d": {"level_id":'+ str(Global.level_id)+'}}')
	socket.send_text('{"t": "GET_LEVEL_CABLES", "d": {"level_id":'+ str(Global.level_id)+'}}')

func update_device_position(device_id:int, x:float, y:float):
	socket.send_text('{"t": "UPDATE_DEVICE_POSITION", "d": {"device_id": %d, "x": %d, "y": %d}}' % [device_id, int(x), int(y)])
	socket.send_text('{"t": "GET_LEVEL_CABLES", "d": {"level_id":'+ str(Global.level_id)+'}}')

func update_tasks():
	socket.send_text('{"t": "GET_LEVEL_TASKS", "d": {"level_id":'+ str(Global.level_id)+'}}')

func update_devices():
	socket.send_text('{"t": "GET_LEVEL_DEVICES", "d": {"level_id":'+ str(Global.level_id)+'}}')
	
func update_cables():
	socket.send_text('{"t": "GET_LEVEL_CABLES", "d": {"level_id":'+ str(Global.level_id)+'}}')
	
func update_game():
	# to be called when we want the whole thing refreshed (level sucess)
	update_tasks()
	update_devices()
	update_cables()

	
func get_device(device_id:int):
	socket.send_text('{"t": "GET_DEVICE", "d": {"device_id":' +str(device_id)+'}}')
	
	
func _on_launch_button_pressed() -> void:
		socket.send_text('{"t": "LAUNCH_SIMULATION", "d": {"level_id":'+ str(Global.level_id)+'}}')
		socket.send_text('{"t": "GET_LEVEL_TASKS", "d": {"level_id":'+ str(Global.level_id)+'}}')


func _on_button_pressed() -> void:
	var ip_input = get_node("../CanvasLayer/InputGroup/IpAdressInput")
	var name_input = get_node("../CanvasLayer/InputGroup/NameInput")
	if ip_input.device_id == -1:
		return
	var data = {"t":"UPDATE_DEVICE","d":{"device_id": ip_input.device_id}}
	if ip_input.text:
		data['d']["ip"] = ip_input.text
	if name_input.text:
		data['d']["name"] = name_input.text
	socket.send_text(JSON.stringify(data))

	get_node("../CanvasLayer/InputGroup").visible = false
	ip_input.text = ""
	name_input.text = ""

func check_completion(data):
	for task in data:
		if task.completed != true:
			return
	show_level_succes_modal()
	
func show_level_succes_modal():
	get_node("../CanvasLayer/Sucess").visible = true
	
func _on_next_level_button_pressed() -> void:
	Global.level_id+=1
	update_game()
	socket.send_text('{"t": "UPDATE_LEVEL_ID", "d": {"level_id":'+ str(Global.level_id)+'}}')
	get_node("../CanvasLayer/Sucess").visible = false



func _on_server_url_text_submitted(new_text: String) -> void:
	websocket_url = new_text
	connect_to_server()
	await get_tree().create_timer(0.25).timeout
	update_game()
