extends Control


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(_delta: float) -> void:
	if Input.is_action_just_pressed("ui_cancel"):
		get_tree().quit()

func _on_button_pressed() -> void:
	get_tree().change_scene_to_file("res://scenes/Game.tscn")


func _on_button_2_pressed() -> void:
	get_tree().change_scene_to_file("res://scenes/Settings.tscn")


func _on_button_3_pressed() -> void:
	get_tree().quit()
