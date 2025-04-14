extends Node

@onready var tasks_container = get_node("/root/Control/CanvasLayer/TaskWindow/TaskContainer")

func _init():
	#do constructor stuff if needed
	pass


# Inspired by device_controller
# Called when the node enters the scene tree for the first time.
func _ready():
	call_deferred("_initialize_tasks_container")

func _initialize_tasks_container():
	tasks_container = get_node("/root/Control/CanvasLayer/TaskWindow/TaskContainer")
	if tasks_container == null:
		print("Error: tasks_container not found!")
	else:
		print("tasks_container found successfully!")


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass

func clear():
	for child in tasks_container.get_children():
		tasks_container.remove_child(child)
		child.queue_free()


func update_tasks(tasks: Array):
	if tasks_container == null:
		print("Error: tasks_container not found!++")
		return
	for task in tasks:
		var task_label = Label.new()
		task_label.text = str(task)
		tasks_container.add_child(task_label)

	print("Tasks updated in the window")
