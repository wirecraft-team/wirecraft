extends Node


func _on_add_switch_button_pressed() -> void:
	get_node("../../ws").add_device("test-switch", "switch")

func _on_add_pc_button_pressed() -> void:
	get_node("../../ws").add_device("test-pc", "pc")
