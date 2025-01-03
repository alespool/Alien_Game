import pygame

class SoundManager:
    """A class to manage all game sounds and music."""
    
    def __init__(self):
        """Initialize the SoundManager."""
        pygame.mixer.quit()  # Restart the mixer with optimized settings
        pygame.mixer.init(buffer=4096)  # Increase buffer size for smoother playback
        pygame.mixer.set_num_channels(16)  # Allow up to 16 simultaneous sounds
        self.music_channel = pygame.mixer.Channel(0)  # Dedicated channel for music
        self.volume_music = 0.5
        self.volume_effects = 1.0
        print(f"Active channels: {pygame.mixer.get_busy()}")
            
    def play_music(self, music_file, loops=-1):
        """Play background music."""
        if not self.music_channel.get_busy():  # Avoid interrupting already playing music
            music = pygame.mixer.Sound(music_file)
            self.music_channel.set_volume(self.volume_music)
            self.music_channel.play(music, loops=loops)
    
    def stop_music(self):
        """Stop the background music."""
        self.music_channel.stop()

    def play_sound_effect(self, selection):
        """Play a sound effect."""
        sound = pygame.mixer.Sound(f"sounds/{selection}.wav")
        available_channel = pygame.mixer.find_channel()
        if available_channel:
            available_channel.set_volume(self.volume_effects)
            available_channel.play(sound)

    def set_music_volume(self, volume):
        """Set the volume for background music."""
        self.volume_music = max(0.0, min(volume, 1.0))  # Clamp volume between 0.0 and 1.0
        self.music_channel.set_volume(self.volume_music)
    
    def set_effects_volume(self, volume):
        """Set the volume for sound effects."""
        self.volume_effects = max(0.0, min(volume, 1.0))  # Clamp volume between 0.0 and 1.0
