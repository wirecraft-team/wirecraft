extends Node


func _on_add_switch_button_pressed() -> void:
	var switch_scene = preload("res://scenes/switch.tscn") 
	var switch_instance = switch_scene.instantiate()
	get_tree().current_scene.add_child(switch_instance)

func _on_add_pc_button_pressed() -> void:
	var pc_scene = preload("res://scenes/pc.tscn") 
	var pc_instance = pc_scene.instantiate()
	get_tree().current_scene.add_child(pc_instance)
