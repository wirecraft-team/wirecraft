extends Window
# This script is used to manage the tasks in the task window.
# It is attached to the TaskWindow node in the scene tree.
@onready var tasks_container = get_node("TaskContainer")
@onready var wrong_snd : AudioStreamPlayer = get_node("Wrong")

func _init():
	pass

# Inspired by device_controller
# Called when the node enters the scene tree for the first time.
func _ready():
	pass

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass

func update_tasks(tasks: Array):
	if tasks_container == null:
		print("Error: tasks_container not found!")
		return

	# Nettoie les anciennes tâches
	for child in tasks_container.get_children():
		child.queue_free()

	# Ajoute chaque tâche comme un Label
	for task in tasks:
		var task_box = VBoxContainer.new()

		var name_label = Label.new()
		name_label.text = str(task.name)
		name_label.add_theme_font_size_override("font_size", 20)
		if task.completed:
			name_label.add_theme_color_override("font_color", Color(0, 1, 0))
			task_box.add_child(name_label)
		elif (task.completed == null):
			name_label.add_theme_color_override("font_color", Color(1, 1, 0))
			task_box.add_child(name_label)
		else:
			name_label.add_theme_color_override("font_color", Color(1, 0, 0))
			var error_label = Label.new()
			error_label.text = str(task.error_message)
			error_label.add_theme_color_override("font_color", Color(0.5, 0, 0))
			task_box.add_child(name_label)
			task_box.add_child(error_label)
			print(wrong_snd)
			if wrong_snd == null:
				print("Erreur : le nœud Wrong n'est pas trouvé !")
			else:
				wrong_snd.play()
			

		var desc_label = Label.new()
		desc_label.text = str(task.description)
		desc_label.add_theme_color_override("font_color", Color(0.5, 0.5, 0.5))
		task_box.add_child(desc_label)

		tasks_container.add_child(task_box)

	print("Tasks updated in the window")
