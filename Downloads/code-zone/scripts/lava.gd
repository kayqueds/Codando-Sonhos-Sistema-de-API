extends TileMapLayer

func _physics_process(_delta):
	var players = get_tree().get_nodes_in_group("player")
	for p in players:
		# Pega a posição em pixels e converte
		var map_pos = local_to_map(p.global_position)
		
		# Tenta pegar os dados
		var data = get_cell_tile_data(map_pos)
		
		if data != null:
			var lethal = data.get_custom_data("is_lethal")
			if lethal:
				p.die()
		else:
			# Isso vai te mostrar se o jogador está "fora" da área do mapa de lava
			print("Nenhum dado encontrado na posição: ", map_pos)
