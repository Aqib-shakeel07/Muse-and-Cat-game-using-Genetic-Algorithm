def main():
    pygame.mixer.music.load(game_music)
    pygame.mixer.music.play(-1)
    mousetraps_player = []
    n = 5
    mice = [Mouse(use_image=True) for _ in range(n)]  # Player's mice
    mice_ai = [Mouse(offset=SCREEN_WIDTH // 2, use_image=True) for _ in range(n)]  # AI's mice

    ga = GeneticAlgorithm(population_size=n, mutation_rate=0.1)
    ga.initialize_population()
    mousetraps_ai = ga.population[0]

    player_kills = 0
    ai_kills = 0
    generation = 0
    # Your existing setup here...
    global log_data
    log_data = pd.DataFrame(columns=['Generation', 'AI_Kills', 'Player_Kills', 'Average_AI_Health'])

    # Periodically log the data after each generation
    generation = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # visualize_performance()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if mouse_x < SCREEN_WIDTH // 2:
                    grid_x = (mouse_x // GRID_SIZE) * GRID_SIZE + GRID_SIZE // 2
                    grid_y = (mouse_y // GRID_SIZE) * GRID_SIZE + GRID_SIZE // 2
                    mousetraps_player.append(Mousetrap(grid_x, grid_y))

        for mouse in mice[:]:
            mouse.move()
            if mouse.health <= 0:
                mice.remove(mouse)
                player_kills += 1
                if player_kills == n:
                    win("Player", n)

        for mouse in mice_ai[:]:
            mouse.move()
            if mouse.health <= 0:
                mice_ai.remove(mouse)
                ai_kills += 1
                if ai_kills == n:
                    win("AI", n)

        avg_health = sum(mouse.health for mouse in mice_ai) / len(mice_ai) if mice_ai else 0
        
        log_data = append_log_data(log_data, {
            'Generation': [generation],
            'AI_Kills': [ai_kills],
            'Player_Kills': [player_kills],
            'Average_AI_Health': [avg_health]
        })

        generation += 1

        screen.fill(BLACK)
        draw_wall()

        for mousetrap in mousetraps_player:
            mousetrap.draw()
            mousetrap.attack(mice)

        for mousetrap_pos in mousetraps_ai:
            mousetrap = Mousetrap(mousetrap_pos[0], mousetrap_pos[1])
            mousetrap.draw(offset=SCREEN_WIDTH // 2)
            mousetrap.attack(mice_ai)

        for enemy in mice:
            enemy.draw()
        for enemy in mice_ai:
            enemy.draw()

        player_score_text = small_font.render(f"Player's Score: {player_kills}", True, WHITE)
        ai_score_text = small_font.render(f"AI's Score: {ai_kills}", True, WHITE)
        screen.blit(player_score_text, (10, 10))
        screen.blit(ai_score_text, (SCREEN_WIDTH // 2 + 10, 10))

        pygame.display.flip()
        clock.tick(FPS)

main_menu()