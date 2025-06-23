extends Node

onready var ws = get_node("../../ws")

func _on_add_switch_button_pressed() -> void:
	ws.add_device("test-switch", "switch")

func _on_add_pc_button_pressed() -> void:
	ws.add_device("test-pc", "pc")
