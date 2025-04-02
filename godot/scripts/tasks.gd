extends Node

func _init():
	#do constructor stuff if needed
	pass


# Inspired by device_controller
# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass 


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass

func update_tasks(tasks: Array):
	# Update tasks based on the data received from the server
	print("tasks are",tasks)
