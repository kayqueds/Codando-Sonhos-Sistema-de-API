extends CharacterBody2D




enum State { IDLE, ATTACK, JUMP_ATTACK, RECOVER }

var state = State.IDLE
var state_timer = 0.0
var jump_dir = -1

const SPEED = 100.0
const JUMP_FORCE = -300.0
var gravity = 980
var player: Node2D = null
var player2: Node2D = null
var vida_aranha = 1000
var is_alive = true
@onready var cutscene_music = $CutsceneMusic
@onready var wall_detector = $WallDetector
@onready var floor_detector = $FloorDetector
@onready var jump_timer = $Timer
@onready var anim: AnimatedSprite2D = $AnimatedSprite2D
@onready var attack_hitbox = get_node_or_null("AttackHitbox")

@export var item_cura_scene: PackedScene
@export_range(0, 100) var chance_drop: float = 40.0

@onready var som_explosao: AudioStreamPlayer2D = $SomExplosao


func _ready() -> void:
	player = get_tree().current_scene.find_child("Player", true, false)
	player2 = get_tree().current_scene.find_child("Player2", true, false)
	cutscene_music.play()
	jump_timer.stop()
	state_timer = randf_range(1.0, 2.5)
	anim.play("idle")
	attack_hitbox.monitoring = false
	attack_hitbox.body_entered.connect(_on_attack_hitbox_body_entered)
	if attack_hitbox != null:
		attack_hitbox.monitoring = false
	else:
		print("ERRO: AttackHitbox não encontrado na cena")
	print("AttackHitbox:", attack_hitbox)

func _physics_process(delta):

	if not is_alive:
		return

	velocity.y += gravity * delta
	state_timer -= delta

	match state:

		State.IDLE:
			velocity.x = 0

			if state_timer <= 0:
				state = pick_attack()
				state_timer = 0.2

		State.ATTACK:
		

			if state_timer <= 0:
				await do_attack()

				state = State.RECOVER
				state_timer = randf_range(2.0, 4.0)

		State.JUMP_ATTACK:

			if state_timer <= 0:

				var alvo = get_target()

				if alvo != null:

					if alvo.global_position.x > global_position.x:
						jump_dir = 1
						scale.x = 1
					else:
						jump_dir = -1
						scale.x = -1

				velocity.x = SPEED * 3 * jump_dir
				velocity.y = JUMP_FORCE

				anim.play("walk")

				state = State.RECOVER
				state_timer = randf_range(1.0, 2.5)

		State.RECOVER:

			if is_on_floor():
				velocity.x = 0

			if state_timer <= 0:
				state = State.IDLE
				state_timer = randf_range(1.0, 2.0)

	move_and_slide()

func get_target():
	if player == null and player2 == null:
		return null

	if player != null and player2 == null:
		return player

	if player2 != null and player == null:
		return player2

	var dist_p1 = global_position.distance_to(player.global_position)
	var dist_p2 = global_position.distance_to(player2.global_position)

	if dist_p1 < dist_p2:
		return player

	return player2
# ---------------- ATTACK ----------------

func do_attack():
	anim.play("attack")

	attack_hitbox.monitoring = true

	await anim.animation_finished

	attack_hitbox.monitoring = false

	await get_tree().create_timer(2.0).timeout

func update_life_bar():
	var life_bar = get_tree().current_scene.find_child("BossLifeBar", true, false)
	if life_bar == null:
		return

	var ratio = float(vida_aranha) / float(500) # ou max_life
	ratio = clamp(ratio, 0.0, 1.0)

	var frame = int((1.0 - ratio) * 28)

	life_bar.frame = frame
func pick_attack():
	return State.ATTACK if randi() % 2 == 0 else State.JUMP_ATTACK


# ---------------- DAMAGE ----------------

func _on_attack_hitbox_body_entered(body):
	if body.has_method("receber_dano"):
		body.receber_dano(20)


func receber_dano(quantidade: int) -> void:
	if not is_alive:
		return

	vida_aranha -= quantidade
	modulate = Color.RED
	await get_tree().create_timer(0.1).timeout
	modulate = Color.WHITE
	update_life_bar() # <- ESSENCIAL AQUI
	if vida_aranha <= 0:
		die()


# ---------------- DEATH ----------------
func die():
	is_alive = false
	jump_timer.stop()

	$CollisionShape2D.set_deferred("disabled", true)

	som_explosao.play()
	anim.play("death")

	await anim.animation_finished

	calcular_drop()

	await get_tree().create_timer(2.0).timeout

	get_tree().change_scene_to_file("res://scene/start.tscn")


func calcular_drop():
	if item_cura_scene == null:
		return

	if randf() * 100.0 <= chance_drop:
		var item = item_cura_scene.instantiate()
		get_parent().call_deferred("add_child", item)
		item.global_position = global_position
