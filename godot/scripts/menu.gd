extends Control
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


func _on_line_edit_text_changed(new_text: String) -> void:
	if new_text not in ['0', '1', '2',]:	
		Global.level_id = 0
	else:
		Global.level_id = int(new_text)
