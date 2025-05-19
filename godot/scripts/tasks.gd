extends Node



func _init():
	pass

# Inspired by device_controller
# Called when the node enters the scene tree for the first time.
func _ready():
	$Label.text = "Bouboubou1"
	pass

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass

func update_tasks(tasks: Array):
	print("Tasks updated in the window")
	$Label.text = "Bouboubou2"
	return
