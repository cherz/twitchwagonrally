import os
import random
import asyncio
import pygame
from twitchio.ext import commands

# Game Settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
FINISH_LINE = SCREEN_WIDTH - 50
EVENTS_TOTAL = 50

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Twitch Chat Game")
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Players dictionary
players = {}

# Player Class
class Player:
    def __init__(self, username, emote="🚀"):
        self.username = username
        self.emote = emote
        self.health = 100
        self.speed = 5
        self.position = 0
        self.events_remaining = EVENTS_TOTAL
        self.y_pos = random.randint(50, SCREEN_HEIGHT - 50)

    def move(self):
        if self.health > 0:
            self.position += self.speed

    def apply_event(self):
        if self.events_remaining > 0:
            self.events_remaining -= 1
            event_type = random.choice(["health", "speed"])
            if event_type == "health":
                change = random.randint(1, 10) * random.choice([-1, 1])
                self.health = max(0, min(100, self.health + change))
                return f"{self.username}'s health {'increased' if change > 0 else 'decreased'} by {abs(change)}."
            elif event_type == "speed":
                change = random.randint(1, 3) * random.choice([-1, 1])
                self.speed = max(1, min(10, self.speed + change))
                return f"{self.username}'s speed {'increased' if change > 0 else 'decreased'} by {abs(change)}."

    def draw(self):
        # Display emote
        emote_surface = font.render(self.emote, True, WHITE)
        screen.blit(emote_surface, (self.position, self.y_pos))
        # Display health bar
        health_bar_width = 100
        health_ratio = self.health / 100
        pygame.draw.rect(screen, RED, (self.position, self.y_pos - 10, health_bar_width, 5))
        pygame.draw.rect(screen, GREEN, (self.position, self.y_pos - 10, health_bar_width * health_ratio, 5))


# Twitch Bot Class
class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            token=os.environ['TWITCH_SECRET'],  # Replace with your bot's OAuth token
            client_id=os.environ['TWITCH_CLIENT_ID'],      # Replace with your Twitch Client ID
            nick=os.environ['TWITCH_BOT_NICK'],            # Replace with your bot's username
            prefix='!',                      # Define the command prefix
            initial_channels=os.environ['TWITCH_CHANNEL']  # Replace with the channel you want the bot to join
        )

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')

    async def event_message(self, message):
        if message.echo:
            return

        await self.handle_commands(message)


    @commands.command(name="cw")
    async def add_player(self, ctx):
        username = ctx.author.name
        if username not in players:
            players[username] = Player(username)
            print(f"Player {username} joined the game!")
        else:
            print(f"Player {username} is already in the game!")


# Main Game Loop
async def main_game_loop():
    running = True
    bot = Bot()
    asyncio.create_task(bot.start())

    while running:
        screen.fill(BLACK)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Game logic
        for username, player in list(players.items()):
            player.move()

            # Trigger random events
            if player.events_remaining > 0:
                event_message = player.apply_event()
                if event_message:
                    print(event_message)

            # Check win/lose conditions
            if player.health <= 0:
                print(f"{username} has died!")
                del players[username]
            elif player.position >= FINISH_LINE:
                print(f"{username} has reached the finish line and wins!")
                del players[username]

            # Draw the player
            player.draw()

        # Draw finish line
        pygame.draw.line(screen, WHITE, (FINISH_LINE, 0), (FINISH_LINE, SCREEN_HEIGHT), 5)

        # Update display
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    await bot.close()


# Run the Game
if __name__ == "__main__":
    asyncio.run(main_game_loop())
