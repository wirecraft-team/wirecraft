extends OptionButton
var res = {
	"640x480": Vector2(640, 480),
	"1920x1080": Vector2(1920, 1080),
	"1920x1200": Vector2(1920, 1200),
	"3024x1964": Vector2(3024, 1964),
	"3440x1440": Vector2(3440, 1440),
}

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	for r in res.keys():
		add_item(r)


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(_delta: float) -> void:
	pass


func _on_item_selected(index: int) -> void:
	get_viewport().size = res[get_item_text(index)]

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey:
		if Input.is_action_just_released("ui_cancel"):
			get_tree().change_scene_to_file("res://scenes/Menu.tscn")
