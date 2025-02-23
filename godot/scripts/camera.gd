extends Camera2D

@export var drag_sensitivity: float = 1.0
@export var zoom_sensitivity: float = 0.1
@export var min_zoom: float = 0.1
@export var max_zoom: float = 1
@export var zoom_speed: float = 0.3

var is_placing_cable: bool = false


var dragging: bool = false

func _input(event: InputEvent):
	if event is InputEventMouseButton:
		if event.button_index == MOUSE_BUTTON_LEFT:
			dragging = event.pressed
			
	elif event is InputEventMouseMotion and dragging:
		position -= (event.relative * drag_sensitivity) / zoom
	
	if event is InputEventMouseButton and event.pressed:
		var zoom_direction: float = 0.0
		if event.button_index == MOUSE_BUTTON_WHEEL_DOWN:
			zoom_direction = -1.0
		elif event.button_index == MOUSE_BUTTON_WHEEL_UP:
			zoom_direction = 1.0
		
		if zoom_direction != 0.0:
			var old_zoom = zoom
			var new_zoom = old_zoom * (1.0 + zoom_direction * zoom_sensitivity)
			# Clamp zoom values
			new_zoom = new_zoom.clamp(
				Vector2(min_zoom, min_zoom), 
				Vector2(max_zoom, max_zoom)
			)
			zoom = lerp(old_zoom, new_zoom, zoom_speed)

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and not is_placing_cable:
		if Input.is_action_just_released("ui_cancel"):
			get_tree().change_scene_to_file("res://scenes/Menu.tscn")

func _process(delta: float) -> void:
	# get is_placing_cable from cable_controller.gd
	is_placing_cable = get_node("../CableController").is_placing_cable
