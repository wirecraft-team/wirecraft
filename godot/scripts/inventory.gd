extends Node


func _on_add_switch_button_pressed() -> void:
	get_node("../../ws").add_device("new_switch", "switch")

func _on_add_pc_button_pressed() -> void:
	get_node("../../ws").add_device("new_pc", "pc")

func _on_add_router_button_pressed() -> void:
	get_node("../../ws").add_device("new_router", "router")
